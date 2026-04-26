"""
量子コンピューター 週次ニュース更新スクリプト
毎週月曜日にGitHub Actionsから自動実行される。
RSSフィードで最新ニュースを収集し、Claude APIでHTML更新内容を生成する。
"""

import os
import re
import json
from datetime import datetime, timezone, timedelta
import feedparser
import requests
import anthropic

# ============================================================
# 設定
# ============================================================
JST = timezone(timedelta(hours=9))
TODAY = datetime.now(JST).strftime("%Y年%m月%d日")
TODAY_ISO = datetime.now(JST).strftime("%Y-%m-%d")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROADMAP_HTML  = os.path.join(BASE_DIR, "quantum_roadmap.html")
BY_TYPE_HTML  = os.path.join(BASE_DIR, "quantum_by_type.html")
CLAUDE_MD     = os.path.join(BASE_DIR, "CLAUDE.md")

# 収集対象のRSSフィード
RSS_FEEDS = [
    # 量子コンピューター専門メディア
    "https://thequantuminsider.com/feed/",
    "https://quantumcomputingreport.com/feed/",
    # 科学全般（量子キーワードでフィルタ）
    "https://www.sciencedaily.com/rss/computers_math/quantum_computers.xml",
    # NVIDIAブログ
    "https://developer.nvidia.com/blog/tag/quantum-computing/feed/",
    # IBMリサーチ
    "https://research.ibm.com/blog/rss.xml",
]

# フィルタリングキーワード（英語・日本語）
KEYWORDS = [
    "quantum", "qubit", "FTQC", "error correction", "calibration",
    "IBM", "Google", "NVIDIA", "Microsoft", "IonQ", "Quantinuum",
    "PsiQuantum", "Atom Computing", "QuEra", "Rigetti",
    "富士通", "NTT", "産総研", "量子", "Majorana", "CUDA-Q", "NVQLink",
    "Ising", "logical qubit", "fault tolerant",
]

# ============================================================
# ① ニュース収集
# ============================================================
def fetch_news() -> list[dict]:
    """RSSフィードから直近7日間の量子関連ニュースを収集する"""
    items = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                # 日付チェック
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                if published and published < cutoff:
                    continue

                title   = getattr(entry, "title", "")
                summary = getattr(entry, "summary", "")
                link    = getattr(entry, "link", "")
                text    = (title + " " + summary).lower()

                # キーワードフィルタ
                if any(kw.lower() in text for kw in KEYWORDS):
                    items.append({
                        "title":   title,
                        "summary": summary[:300],
                        "link":    link,
                        "date":    published.strftime("%Y-%m-%d") if published else "unknown",
                    })
        except Exception as e:
            print(f"⚠️  RSSフェッチ失敗 ({url}): {e}")

    # 重複除去（タイトルで）
    seen, unique = set(), []
    for item in items:
        if item["title"] not in seen:
            seen.add(item["title"])
            unique.append(item)

    print(f"✅ ニュース収集完了: {len(unique)} 件")
    return unique[:30]   # 最大30件をClaudeへ渡す


# ============================================================
# ② Claude API で更新内容を生成
# ============================================================
def generate_updates(news_items: list[dict]) -> dict:
    """Claude claude-opus-4-6 を使ってHTML更新内容を生成する"""

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    news_text = "\n\n".join(
        f"[{item['date']}] {item['title']}\n{item['summary']}\nURL: {item['link']}"
        for item in news_items
    ) if news_items else "今週は新しいニュースが見つかりませんでした。"

    prompt = f"""あなたは量子コンピューター技術の専門家です。
以下の今週（直近7日間）の量子コンピューター関連ニュースを分析してください。

=== 今週のニュース ===
{news_text}

=== タスク ===
以下の情報を日本語でJSON形式で返してください：

1. "summary": 今週の重要トピックを3〜5点の箇条書き（各50文字以内）
2. "nvidia_update": NVIDIAに関する新情報（なければnull）
3. "company_milestones": 各企業の新マイルストーン（企業名: 内容の辞書形式）
   対象企業: IBM, Google, Microsoft, IonQ, Quantinuum, 富士通, NTT, 産総研, NTTデータ, PsiQuantum
4. "has_updates": 重要なアップデートがあったか（true/false）
5. "update_date": "{TODAY}"

JSONのみを返してください。コードブロックや説明文は不要です。"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    # コードブロックがあれば除去
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    result = json.loads(raw)
    print(f"✅ Claude分析完了: updates={result.get('has_updates')}")
    return result


# ============================================================
# ③ HTML ファイルを更新
# ============================================================
def update_html_date(filepath: str, today: str) -> None:
    """HTML末尾の「作成日：」をToday日付に更新する"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    updated = re.sub(
        r"作成日：\d{4}年\d{1,2}月\d{1,2}日",
        f"作成日：{today}",
        content,
    )
    if updated != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"✅ 日付更新: {os.path.basename(filepath)}")


def update_nvidia_banner(updates: dict) -> None:
    """quantum_roadmap.html の NVIDIAバナーに新情報を追記する"""
    nvidia_info = updates.get("nvidia_update")
    if not nvidia_info:
        return

    with open(ROADMAP_HTML, "r", encoding="utf-8") as f:
        content = f.read()

    # 既存のNVIDIAバナー内の <p> タグに追記
    new_text = f'<br><strong style="color:#fff">📰 {TODAY_ISO}更新：</strong>{nvidia_info}'
    updated = re.sub(
        r'(CUDA-Q・NVQLink と統合。)</p>',
        f'\\1{new_text}</p>',
        content,
        count=1,
    )
    if updated != content:
        with open(ROADMAP_HTML, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"✅ NVIDIAバナー更新")


def update_claude_md(updates: dict) -> None:
    """CLAUDE.md の最終更新日とマイルストーン情報を更新する"""
    with open(CLAUDE_MD, "r", encoding="utf-8") as f:
        content = f.read()

    # 最終更新日を更新
    updated = re.sub(
        r"\*\*最終更新：\*\*\s*\d{4}年\d{1,2}月\d{1,2}日",
        f"**最終更新：** {TODAY}",
        content,
    )
    with open(CLAUDE_MD, "w", encoding="utf-8") as f:
        f.write(updated)
    print(f"✅ CLAUDE.md 更新日を更新")


# ============================================================
# メイン
# ============================================================
def main():
    print(f"\n{'='*50}")
    print(f"🔄 量子ニュース週次更新 — {TODAY}")
    print(f"{'='*50}\n")

    # ① ニュース収集
    news_items = fetch_news()

    # ② Claude で分析
    updates = generate_updates(news_items)

    # ③ HTML・MD を更新
    update_html_date(ROADMAP_HTML, TODAY)
    update_html_date(BY_TYPE_HTML, TODAY)
    update_nvidia_banner(updates)
    update_claude_md(updates)

    # ④ サマリー出力
    print(f"\n{'='*50}")
    print("📋 今週の更新サマリー")
    print(f"{'='*50}")
    for point in updates.get("summary", []):
        print(f"  • {point}")

    milestones = updates.get("company_milestones", {})
    if milestones:
        print("\n🏢 企業別新情報:")
        for company, info in milestones.items():
            print(f"  [{company}] {info}")

    print(f"\n✅ 更新完了: {TODAY}\n")


if __name__ == "__main__":
    main()
