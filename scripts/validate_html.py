"""
HTML構造の健全性チェック

週次・月次更新でカード類を手作業／自動で追記した際に、閉じタグの欠落や
余剰が混入していないかを検出する。GitHub Actions では更新処理の直後に
実行し、崩れていればコミットを止める。

検出内容:
  1. <div> / <a> / <p> の開閉バランス（行番号つきで報告）
  2. 必須マーカーの存在（NEWS_SECTION_START / END）
  3. 日付表記のフォーマット妥当性

使い方:
    python scripts/validate_html.py
    python scripts/validate_html.py quantum_roadmap.html
"""

from __future__ import annotations

import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGETS = ["quantum_roadmap.html", "quantum_by_type.html"]

# 開閉が対になるべきタグ
PAIRED_TAGS = ["div", "a", "p", "table", "tbody", "thead", "tr"]

VOID_OR_SELF_CLOSING = re.compile(r"/>\s*$")


def check_tag_balance(path: str, tag: str) -> list[str]:
    """タグの開閉バランスを行番号つきで検査する"""
    errors: list[str] = []
    stack: list[int] = []
    pattern = re.compile(rf"<(/?){tag}\b[^>]*?(/?)>", re.IGNORECASE)

    with open(path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            for m in pattern.finditer(line):
                is_close, is_self = m.group(1), m.group(2)
                if is_close:
                    if stack:
                        stack.pop()
                    else:
                        errors.append(
                            f"  L{lineno}: 余分な </{tag}> があります "
                            f"→ {line.strip()[:60]}"
                        )
                elif not is_self:
                    stack.append(lineno)

    for lineno in stack:
        errors.append(f"  L{lineno}: <{tag}> が閉じられていません")
    return errors


def check_markers(path: str, content: str) -> list[str]:
    errors: list[str] = []
    starts = content.count("<!-- NEWS_SECTION_START -->")
    ends = content.count("<!-- NEWS_SECTION_END -->")
    if starts != 1 or ends != 1:
        errors.append(
            f"  ニュースセクションのマーカー数が不正です "
            f"(START={starts}, END={ends}, 期待値=1)"
        )

    h_start = content.count("<!-- HIGHLIGHT_START -->")
    h_end = content.count("<!-- HIGHLIGHT_END -->")
    if h_start != h_end:
        errors.append(
            f"  ハイライトマーカーが対になっていません "
            f"(START={h_start}, END={h_end})"
        )
    return errors


def check_dates(content: str) -> list[str]:
    errors: list[str] = []
    if not re.search(r"現在地：\d{4}年\d{1,2}月\d{1,2}日", content):
        errors.append("  「現在地：YYYY年M月D日」の表記が見つかりません")
    if not re.search(r"最終更新：\d{4}年\d{1,2}月\d{1,2}日", content):
        errors.append("  「最終更新：YYYY年MM月DD日」の表記が見つかりません")
    return errors


def validate(filename: str) -> bool:
    path = os.path.join(BASE_DIR, filename)
    print(f"\n🔍 {filename}")

    if not os.path.exists(path):
        print("  ⚠️  ファイルが存在しません（スキップ）")
        return True

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    errors: list[str] = []
    for tag in PAIRED_TAGS:
        errors.extend(check_tag_balance(path, tag))
    errors.extend(check_markers(path, content))
    errors.extend(check_dates(content))

    if errors:
        print(f"  ❌ {len(errors)} 件の問題を検出:")
        for err in errors:
            print(err)
        return False

    news_count = len(re.findall(r'font-size:11px;color:#(?:64748b|93c5fd)', content))
    print(f"  ✅ 構造OK（ニュース {news_count} 件 / {len(content):,} 文字）")
    return True


def main() -> int:
    targets = sys.argv[1:] or DEFAULT_TARGETS
    print("=" * 56)
    print("🧪 HTML構造チェック")
    print("=" * 56)

    results = [validate(name) for name in targets]

    print("\n" + "=" * 56)
    if all(results):
        print("✅ すべてのファイルが健全です")
        print("=" * 56)
        return 0

    failed = sum(1 for ok in results if not ok)
    print(f"❌ {failed} ファイルに問題があります — 更新を中止してください")
    print("=" * 56)
    return 1


if __name__ == "__main__":
    sys.exit(main())
