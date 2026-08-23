"""
量子コンピューター ニュース更新スクリプト
GitHub Actions から週次（毎週月曜）／月次（毎月1日）で自動実行される。

RSSフィードで最新ニュースを収集し、以下を更新する:
  - quantum_roadmap.html  : 現在地バッジ / フッター日付 / ニュースセクション
  - quantum_by_type.html  : 現在地タグ   / フッター日付 / ニュースセクション
  - CLAUDE.md             : 最終更新日

使い方:
    python scripts/update_quantum.py                 # 週次モード
    python scripts/update_quantum.py --mode monthly  # 月次モード
    python scripts/update_quantum.py --dry-run       # ファイルを書き換えず結果だけ表示
    python scripts/update_quantum.py --no-translate  # 翻訳せず英語のまま

日本語化:
    収集元は英語のRSSなので、環境変数 ANTHROPIC_API_KEY が設定されていれば
    Claude API で見出し・要約を日本語に翻訳する。キーが無い場合は翻訳を
    スキップして英語のまま出力する（処理は止めない）。

手動で書いた「今月のハイライト」ブロックは
<!-- HIGHLIGHT_START --> 〜 <!-- HIGHLIGHT_END --> で囲んでおけば
自動更新でも消えずに保持される。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

import feedparser

# ============================================================
# 設定
# ============================================================
JST = timezone(timedelta(hours=9))
NOW = datetime.now(JST)

TODAY_JP = NOW.strftime("%Y年%m月%d日")          # 2026年07月31日
TODAY_JP_SHORT = f"{NOW.year}年{NOW.month}月{NOW.day}日"  # 2026年7月31日
TODAY_ISO = NOW.strftime("%Y-%m-%d")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROADMAP_HTML = os.path.join(BASE_DIR, "quantum_roadmap.html")
BY_TYPE_HTML = os.path.join(BASE_DIR, "quantum_by_type.html")
CLAUDE_MD = os.path.join(BASE_DIR, "CLAUDE.md")

HTML_FILES = [
    (ROADMAP_HTML, "quantum_roadmap.html"),
    (BY_TYPE_HTML, "quantum_by_type.html"),
]

# 収集対象のRSSフィード（英語）
RSS_FEEDS_EN = [
    "https://thequantuminsider.com/feed/",
    "https://quantumcomputingreport.com/feed/",
    "https://www.sciencedaily.com/rss/computers_math/quantum_computers.xml",
    "https://developer.nvidia.com/blog/tag/quantum-computing/feed/",
    "https://research.ibm.com/blog/rss.xml",
    "https://quantumzeitgeist.com/feed/",
]

# 収集対象のRSSフィード（日本語）
# Googleニュースの日本語検索RSS。最初から日本語なので翻訳が不要で、
# 国内メディアの記事を取りこぼさずに拾える。
_GNEWS = "https://news.google.com/rss/search?hl=ja&gl=JP&ceid=JP:ja&q="
RSS_FEEDS_JA = [
    _GNEWS + urllib.parse.quote("量子コンピューター"),
    _GNEWS + urllib.parse.quote("量子ビット OR 量子computing"),
    _GNEWS + urllib.parse.quote("量子技術 誤り訂正 OR 量子優位性"),
]

RSS_FEEDS = RSS_FEEDS_EN + RSS_FEEDS_JA

# フィルタリングキーワード
KEYWORDS = [
    "quantum", "qubit", "FTQC", "error correction", "error mitigation",
    "calibration", "logical qubit", "fault tolerant", "quantum advantage",
    "IBM", "Google", "NVIDIA", "Microsoft", "IonQ", "Quantinuum", "Qedma",
    "PsiQuantum", "Atom Computing", "QuEra", "Rigetti", "D-Wave", "Pasqal",
    "IQM", "Xanadu", "Infleqtion", "HRL",
    "富士通", "NTT", "産総研", "理研", "日立", "量子",
    "Majorana", "CUDA-Q", "NVQLink", "Ising", "anyon", "PQC",
]

# モード別パラメーター
MODE_CONFIG = {
    "weekly": {
        "lookback_days": 7,
        "max_items": 10,
        "commit_label": "週次",
    },
    "monthly": {
        "lookback_days": 31,
        "max_items": 16,
        "commit_label": "月次",
    },
}


# ============================================================
# ① ニュース収集
# ============================================================
def fetch_news(lookback_days: int, max_items: int) -> list[dict]:
    """RSSフィードから直近 lookback_days 日間の量子関連ニュースを収集する"""
    items: list[dict] = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)

    # SSL証明書エラー回避（企業ネットワーク等の中間CA対応）
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    for url in RSS_FEEDS:
        try:
            # まず標準パースを試み、失敗またはエントリ0件ならSSL無効でリトライ
            feed = feedparser.parse(url)
            if not feed.entries:
                req = urllib.request.Request(
                    url, headers={"User-Agent": "Mozilla/5.0 feedparser"}
                )
                with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
                    feed = feedparser.parse(resp.read())

            for entry in feed.entries[:30]:
                published = None
                if getattr(entry, "published_parsed", None):
                    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                if published and published < cutoff:
                    continue

                title = getattr(entry, "title", "")
                summary = getattr(entry, "summary", "")
                link = getattr(entry, "link", "")
                text = f"{title} {summary}".lower()

                if any(kw.lower() in text for kw in KEYWORDS):
                    clean_summary = re.sub(r"<[^>]+>", "", summary).strip()[:220]
                    # Googleニュースの要約は媒体名リンクの羅列になりがちなので削る
                    clean_summary = re.sub(r"\s{2,}", " ", clean_summary)
                    items.append({
                        "title": title,
                        "summary": clean_summary,
                        "link": link,
                        "date": published.strftime("%Y-%m-%d") if published else "unknown",
                        "sort_key": published or datetime.min.replace(tzinfo=timezone.utc),
                    })
        except Exception as exc:  # noqa: BLE001 - フィード単位で失敗を握りつぶす
            print(f"⚠️  RSSフェッチ失敗 ({url}): {exc}")

    # 重複除去（タイトル基準／媒体名サフィックスを無視）→ 新しい順
    seen: set[str] = set()
    unique: list[dict] = []
    for item in sorted(items, key=lambda x: x["sort_key"], reverse=True):
        # Googleニュースは「見出し - 媒体名」形式なので媒体名を落として比較する
        key = re.sub(r"\s+-\s+[^-]+$", "", item["title"]).strip().lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)

    ja = sum(1 for i in unique if is_japanese(i["title"]))
    print(f"✅ ニュース収集完了: {len(unique)} 件"
          f"（日本語 {ja} / 英語 {len(unique) - ja}・直近{lookback_days}日）")
    return unique[:max_items]


# ============================================================
# ①-b 日本語への翻訳
#
# バックエンドは2系統。無料で使える GitHub Models を既定とし、
# ANTHROPIC_API_KEY がある場合のみ Claude API を使う。
# どちらも使えなければ英語のまま出力する（処理は止めない）。
# ============================================================
GITHUB_MODELS_URL = "https://models.github.ai/inference/chat/completions"
GITHUB_MODELS_MODEL = "openai/gpt-4o-mini"

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"

JP_CHARS = re.compile(r"[ぁ-んァ-ヶ一-龥]")


def is_japanese(text: str) -> bool:
    """ひらがな・カタカナ・漢字を含むなら日本語記事とみなす"""
    return bool(JP_CHARS.search(text or ""))


TRANSLATE_PROMPT = """あなたは量子コンピューター分野の専門知識を持つ技術翻訳者です。
以下の英語ニュース記事の見出しと要約を、日本語に翻訳してください。

翻訳ルール:
- 企業名・製品名（IBM, IonQ, Quantinuum, Willow, Heron など）は原文表記のまま残す
- 専門用語は日本語の定訳を使う（qubit→量子ビット、error correction→誤り訂正、
  fault tolerant→誤り耐性、logical qubit→論理量子ビット、
  quantum advantage→量子優位性、trapped-ion→イオントラップ型、
  neutral atom→中性原子型、annealing→アニーリング）
- 見出しは簡潔な日本語に。要約は2文程度に収める
- 数値・単位・固有名詞は正確に保持する
- 訳せない場合は原文をそのまま返す

以下のJSON配列を、同じ構造・同じ件数・同じ順序で返してください。
title と summary のみ日本語化し、他のキーは変更しないこと。
JSON以外の説明文は一切出力しないこと。

{payload}"""


def _post_json(url: str, body: dict, headers: dict, timeout: int = 90) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), headers=headers
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _extract_json_array(text: str) -> list:
    """モデル出力から JSON 配列を取り出す（```json 囲みにも対応）"""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(.+?)\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    return json.loads(text)


def _translate_via_github_models(prompt: str, token: str) -> list:
    """GitHub Models（無料枠あり・GITHUB_TOKENで利用可）で翻訳する"""
    data = _post_json(
        GITHUB_MODELS_URL,
        {
            "model": GITHUB_MODELS_MODEL,
            "temperature": 0,
            "messages": [{"role": "user", "content": prompt}],
        },
        {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
    )
    return _extract_json_array(data["choices"][0]["message"]["content"])


def _translate_via_anthropic(prompt: str, api_key: str) -> list:
    """Claude API で翻訳する（ANTHROPIC_API_KEY がある場合のみ）"""
    data = _post_json(
        ANTHROPIC_API_URL,
        {
            "model": ANTHROPIC_MODEL,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        },
        {
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    text = "".join(
        b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"
    )
    return _extract_json_array(text)


def translate_items(items: list[dict], enabled: bool) -> list[dict]:
    """英語のニュースだけを日本語化する

    バックエンドの優先順位:
      1. ANTHROPIC_API_KEY があれば Claude API
      2. なければ GitHub Models（GITHUB_TOKEN、Actions上では自動で入る）
      3. どちらも使えなければ英語のまま（処理は止めない）
    """
    if not items:
        return items
    if not enabled:
        print("ℹ️  翻訳スキップ（--no-translate 指定）")
        return items

    # 日本語ソースから取れた記事は翻訳不要
    targets = [i for i in items if not is_japanese(i["title"])]
    ja_count = len(items) - len(targets)
    if ja_count:
        print(f"ℹ️  日本語記事 {ja_count} 件は翻訳不要")
    if not targets:
        return items

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    gh_token = os.environ.get("GITHUB_TOKEN", "").strip()

    if anthropic_key:
        backend, runner = "Claude API", lambda p: _translate_via_anthropic(p, anthropic_key)
    elif gh_token:
        backend, runner = "GitHub Models", lambda p: _translate_via_github_models(p, gh_token)
    else:
        print("ℹ️  翻訳バックエンドなし（GITHUB_TOKEN / ANTHROPIC_API_KEY 未設定）"
              " — 英語のまま出力")
        return items

    payload = json.dumps(
        [{"title": i["title"], "summary": i["summary"]} for i in targets],
        ensure_ascii=False,
    )
    prompt = TRANSLATE_PROMPT.format(payload=payload)

    try:
        translated = runner(prompt)
        if not isinstance(translated, list) or len(translated) != len(targets):
            got = len(translated) if isinstance(translated, list) else "?"
            print(f"⚠️  翻訳結果の件数が不一致（{got}/{len(targets)}）。英語のまま使用")
            return items

        for original, ja in zip(targets, translated):
            original["title"] = ja.get("title") or original["title"]
            original["summary"] = ja.get("summary") or original["summary"]

        print(f"✅ 日本語に翻訳: {len(targets)} 件（{backend}）")
    except Exception as exc:  # noqa: BLE001 - 翻訳失敗で更新を止めない
        print(f"⚠️  翻訳に失敗（英語のまま続行 / {backend}）: {exc}")

    return items


# ============================================================
# ② 日付表記の更新
# ============================================================
def target_month() -> tuple[int, int, int]:
    """月次まとめの対象月を (年, 月, 末日) で返す

    毎月1日の cron で走った場合は「前月のまとめ」を作るのが自然なので、
    1日実行のときだけ前月を対象にする。月中の手動実行なら当月扱い。
    """
    if NOW.day == 1:
        last = NOW.replace(day=1) - timedelta(days=1)
        return last.year, last.month, last.day
    return NOW.year, NOW.month, NOW.day


def build_footer_label(mode: str) -> str:
    """フッターに表示する最終更新ラベルを組み立てる"""
    if mode == "monthly":
        _, month, _ = target_month()
        return f"最終更新：{TODAY_JP}（{month}月度 月次更新）"
    return f"最終更新：{TODAY_JP}"


def update_dates(filepath: str, label: str, mode: str, dry_run: bool) -> None:
    """現在地バッジとフッター日付を更新する"""
    if not os.path.exists(filepath):
        print(f"⚠️  ファイルが見つかりません（スキップ）: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    content = original

    # 📍 現在地：2026年7月31日
    content = re.sub(
        r"現在地：\d{4}年\d{1,2}月\d{1,2}日",
        f"現在地：{TODAY_JP_SHORT}",
        content,
    )

    # 最終更新：2026年07月31日（7月度 月次更新） ← 括弧付き注記も丸ごと置換
    content = re.sub(
        r"最終更新：\d{4}年\d{1,2}月\d{1,2}日(?:（[^）]*）)?",
        build_footer_label(mode),
        content,
    )

    # 旧フォーマット（作成日：）にも後方互換で対応
    content = re.sub(
        r"作成日：\d{4}年\d{1,2}月\d{1,2}日",
        f"作成日：{TODAY_JP}",
        content,
    )

    if content == original:
        print(f"ℹ️  日付変更なし: {label}")
        return
    if dry_run:
        print(f"🔍 [dry-run] 日付更新対象: {label}")
        return

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 日付更新: {label}")


# ============================================================
# ③ ニュースセクションの生成・差し替え
# ============================================================
NEWS_START = "<!-- NEWS_SECTION_START -->"
NEWS_END = "<!-- NEWS_SECTION_END -->"
HIGHLIGHT_START = "<!-- HIGHLIGHT_START -->"
HIGHLIGHT_END = "<!-- HIGHLIGHT_END -->"


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_heading(mode: str) -> str:
    if mode == "monthly":
        year, month, last_day = target_month()
        return f"📰 {year}年{month}月 まとめ（月次更新・{month}/1〜{month}/{last_day}）"
    return f"📰 今週の量子ニュース（{TODAY_JP}更新）"


def extract_highlight(content: str) -> str:
    """既存のハイライトブロック（手動編集分）を取り出す"""
    match = re.search(
        re.escape(HIGHLIGHT_START) + r".*?" + re.escape(HIGHLIGHT_END),
        content,
        flags=re.DOTALL,
    )
    return match.group(0) if match else ""


def build_news_section(news_items: list[dict], mode: str, highlight: str) -> str:
    """ニュースセクションのHTML文字列を生成する（タグは必ず対で閉じる）"""
    cards = []
    if highlight:
        cards.append(f"      {highlight}")

    for item in news_items:
        cards.append(
            '      <div style="background:#1e293b;border:1px solid #334155;'
            'border-radius:8px;padding:14px;margin-bottom:10px;">\n'
            f'        <div style="font-size:11px;color:#64748b;margin-bottom:6px;">{esc(item["date"])}</div>\n'
            f'        <a href="{esc(item["link"])}" target="_blank" '
            'style="color:#60a5fa;text-decoration:none;font-weight:600;font-size:13px;">'
            f'{esc(item["title"])}</a>\n'
            f'        <p style="color:#94a3b8;font-size:12px;margin:6px 0 0;">{esc(item["summary"])}</p>\n'
            "      </div>"
        )

    cards_html = "\n".join(cards)
    return (
        f"{NEWS_START}\n"
        '    <div id="weekly-news" style="background:#0f172a;border:1px solid #1e3a5f;'
        'border-radius:12px;padding:20px;margin:24px 0;">\n'
        f'      <h3 style="color:#60a5fa;margin:0 0 16px;font-size:16px;">{build_heading(mode)}</h3>\n'
        f"{cards_html}\n"
        "    </div>\n"
        f"    {NEWS_END}"
    )


def update_news_section(filepath: str, label: str, news_items: list[dict],
                        mode: str, dry_run: bool) -> None:
    """指定HTMLファイルのニュースセクションを差し替える"""
    if not os.path.exists(filepath):
        print(f"⚠️  {label} が見つかりません（スキップ）")
        return
    if not news_items:
        print(f"ℹ️  対象期間のニュースなし。{label} のニュースセクションはスキップ。")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    highlight = extract_highlight(content)
    section = build_news_section(news_items, mode, highlight)

    if NEWS_START in content:
        updated = re.sub(
            re.escape(NEWS_START) + r".*?" + re.escape(NEWS_END),
            lambda _: section,
            content,
            flags=re.DOTALL,
        )
    else:
        updated = content.replace("</body>", f"\n    {section}\n</body>", 1)

    if dry_run:
        print(f"🔍 [dry-run] ニュースセクション更新対象: {label}（{len(news_items)}件）")
        return

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated)
    kept = "（ハイライト保持）" if highlight else ""
    print(f"✅ ニュースセクション更新: {label} {len(news_items)}件{kept}")


# ============================================================
# ④ CLAUDE.md の更新
# ============================================================
def update_claude_md(mode: str, dry_run: bool) -> None:
    if not os.path.exists(CLAUDE_MD):
        print("⚠️  CLAUDE.md が見つかりません（スキップ）")
        return

    with open(CLAUDE_MD, "r", encoding="utf-8") as f:
        content = f.read()

    updated = re.sub(
        r"\*\*最終更新：\*\*\s*\d{4}年\d{1,2}月\d{1,2}日(?:（[^）]*）)?",
        f"**最終更新：** {build_footer_label(mode).replace('最終更新：', '')}",
        content,
    )

    if updated == content:
        print("ℹ️  CLAUDE.md 変更なし")
        return
    if dry_run:
        print("🔍 [dry-run] CLAUDE.md 更新対象")
        return

    with open(CLAUDE_MD, "w", encoding="utf-8") as f:
        f.write(updated)
    print("✅ CLAUDE.md 最終更新日を更新")


# ============================================================
# メイン
# ============================================================
def main() -> int:
    parser = argparse.ArgumentParser(description="量子コンピューター ニュース更新")
    parser.add_argument("--mode", choices=["weekly", "monthly"], default="weekly",
                        help="更新モード（既定: weekly）")
    parser.add_argument("--dry-run", action="store_true",
                        help="ファイルを書き換えずに結果のみ表示")
    parser.add_argument("--no-translate", action="store_true",
                        help="翻訳を行わず英語のまま出力する")
    args = parser.parse_args()

    cfg = MODE_CONFIG[args.mode]

    print(f"\n{'=' * 56}")
    print(f"🔄 量子ニュース{cfg['commit_label']}更新 — {TODAY_JP}"
          f"{'  [dry-run]' if args.dry_run else ''}")
    print(f"{'=' * 56}\n")

    news_items = fetch_news(cfg["lookback_days"], cfg["max_items"])
    news_items = translate_items(news_items, enabled=not args.no_translate)

    for path, label in HTML_FILES:
        update_dates(path, label, args.mode, args.dry_run)
    for path, label in HTML_FILES:
        update_news_section(path, label, news_items, args.mode, args.dry_run)

    update_claude_md(args.mode, args.dry_run)

    print(f"\n{'=' * 56}")
    print(f"📋 収集ニュース（{len(news_items)}件）")
    print(f"{'=' * 56}")
    for item in news_items:
        print(f"  [{item['date']}] {item['title'][:64]}")

    print(f"\n✅ 更新完了: {TODAY_JP}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
