"""
量子コンピューター 週次ニュース更新スクリプト（Claude APIなし版）
毎週月曜日にGitHub Actionsから自動実行される。
RSSフィードで最新ニュースを収集し、HTMLに直接埋め込む。
"""

import os
import re
from datetime import datetime, timezone, timedelta
import feedparser

# ============================================================
# 設定
# ============================================================
JST = timezone(timedelta(hours=9))
TODAY = datetime.now(JST).strftime("%Y年%m月%d日")
TODAY_ISO = datetime.now(JST).strftime("%Y-%m-%d")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROADMAP_HTML = os.path.join(BASE_DIR, "quantum_roadmap.html")
BY_TYPE_HTML = os.path.join(BASE_DIR, "quantum_by_type.html")
CLAUDE_MD    = os.path.join(BASE_DIR, "CLAUDE.md")

# 収集対象のRSSフィード
RSS_FEEDS = [
    "https://thequantuminsider.com/feed/",
    "https://quantumcomputingreport.com/feed/",
    "https://www.sciencedaily.com/rss/computers_math/quantum_computers.xml",
    "https://developer.nvidia.com/blog/tag/quantum-computing/feed/",
    "https://research.ibm.com/blog/rss.xml",
]

# フィルタリングキーワード
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
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                if published and published < cutoff:
                    continue

                title   = getattr(entry, "title", "")
                summary = getattr(entry, "summary", "")
                link    = getattr(entry, "link", "")
                text    = (title + " " + summary).lower()

                if any(kw.lower() in text for kw in KEYWORDS):
                    # HTMLタグを除去してクリーンなテキストにする
                    clean_summary = re.sub(r"<[^>]+>", "", summary)[:200]
                    items.append({
                        "title":   title,
                        "summary": clean_summary,
                        "link":    link,
                        "date":    published.strftime("%Y-%m-%d") if published else "unknown",
                    })
        except Exception as e:
            print(f"⚠️  RSSフェッチ失敗 ({url}): {e}")

    # 重複除去
    seen, unique = set(), []
    for item in items:
        if item["title"] not in seen:
            seen.add(item["title"])
            unique.append(item)

    print(f"✅ ニュース収集完了: {len(unique)} 件")
    return unique[:10]


# ============================================================
# ② HTMLファイルの日付更新
# ============================================================
def update_html_date(filepath: str, today: str) -> None:
    """HTML内の「作成日：」をToday日付に更新する"""
    if not os.path.exists(filepath):
        print(f"⚠️  ファイルが見つかりません（スキップ）: {filepath}")
        return
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
    else:
        print(f"ℹ️  日付変更なし: {os.path.basename(filepath)}")


# ============================================================
# ③ ニュースセクションをHTMLに挿入・更新（共通関数）
# ============================================================
def build_news_section(news_items: list[dict], section_id: str = "weekly-news") -> str:
    """ニュースセクションのHTML文字列を生成する"""
    cards_html = ""
    for item in news_items:
        title   = item["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        summary = item["summary"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        link    = item["link"]
        date    = item["date"]
        cards_html += f"""      <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:14px;margin-bottom:10px;">
        <div style="font-size:11px;color:#64748b;margin-bottom:6px;">{date}</div>
        <a href="{link}" target="_blank" style="color:#60a5fa;text-decoration:none;font-weight:600;font-size:13px;">{title}</a>
        <p style="color:#94a3b8;font-size:12px;margin:6px 0 0;">{summary}</p>
      </div>\n"""

    return f"""<!-- NEWS_SECTION_START -->
    <div id="{section_id}" style="background:#0f172a;border:1px solid #1e3a5f;border-radius:12px;padding:20px;margin:24px 0;">
      <h3 style="color:#60a5fa;margin:0 0 16px;font-size:16px;">📰 今週の量子ニュース（{TODAY}更新）</h3>
{cards_html}    </div>
    <!-- NEWS_SECTION_END -->"""


def update_news_section(filepath: str, news_items: list[dict], label: str) -> None:
    """指定HTMLファイルの週次ニュースセクションを更新する"""
    if not os.path.exists(filepath):
        print(f"⚠️  {os.path.basename(filepath)} が見つかりません（スキップ）")
        return

    if not news_items:
        print("ℹ️  今週のニュースなし。ニュースセクションはスキップ。")
        return

    news_section = build_news_section(news_items)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 既存のニュースセクションを置換、なければ </body> 直前に挿入
    if "<!-- NEWS_SECTION_START -->" in content:
        updated = re.sub(
            r"<!-- NEWS_SECTION_START -->.*?<!-- NEWS_SECTION_END -->",
            news_section,
            content,
            flags=re.DOTALL,
        )
    else:
        updated = content.replace("</body>", f"\n    {news_section}\n</body>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated)
    print(f"✅ ニュースセクション更新 ({label}): {len(news_items)}件")


# ============================================================
# ④ CLAUDE.md の更新日を更新
# ============================================================
def update_claude_md() -> None:
    if not os.path.exists(CLAUDE_MD):
        print(f"⚠️  CLAUDE.md が見つかりません（スキップ）")
        return
    with open(CLAUDE_MD, "r", encoding="utf-8") as f:
        content = f.read()
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

    # ② HTMLの日付更新
    update_html_date(ROADMAP_HTML, TODAY)
    update_html_date(BY_TYPE_HTML, TODAY)

    # ③ ニュースセクション更新（両ファイル）
    update_news_section(ROADMAP_HTML, news_items, "quantum_roadmap.html")
    update_news_section(BY_TYPE_HTML, news_items, "quantum_by_type.html")

    # ④ CLAUDE.md 更新
    update_claude_md()

    # サマリー出力
    print(f"\n{'='*50}")
    print(f"📋 今週のニュース ({len(news_items)}件)")
    print(f"{'='*50}")
    for item in news_items:
        print(f"  [{item['date']}] {item['title'][:60]}")

    print(f"\n✅ 更新完了: {TODAY}\n")


if __name__ == "__main__":
    main()
