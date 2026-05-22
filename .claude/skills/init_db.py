import sqlite3, os

db_path = '/Users/bytedance/project/data/news.db'
if os.path.exists(db_path):
    exit(0)  # 已存在，跳过

os.makedirs(os.path.dirname(db_path), exist_ok=True)
db = sqlite3.connect(db_path)

db.executescript('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        summary TEXT,
        url TEXT,
        source TEXT,
        category TEXT,
        importance INTEGER DEFAULT 0,
        published_date TEXT,
        fetched_date TEXT NOT NULL DEFAULT (date('now')),
        content_hash TEXT UNIQUE,
        created_at TEXT DEFAULT (datetime('now'))
    );
    CREATE INDEX IF NOT EXISTS idx_articles_date ON articles(fetched_date);
    CREATE INDEX IF NOT EXISTS idx_articles_cat ON articles(category);
    CREATE INDEX IF NOT EXISTS idx_articles_hash ON articles(content_hash);

    CREATE TABLE IF NOT EXISTS market_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_name TEXT NOT NULL,
        asset_category TEXT,
        value REAL,
        change_percent REAL,
        data_date TEXT NOT NULL,
        source TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    );
    CREATE INDEX IF NOT EXISTS idx_market_date ON market_data(data_date);
    CREATE INDEX IF NOT EXISTS idx_market_asset ON market_data(asset_name);

    CREATE TABLE IF NOT EXISTS daily_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_date TEXT NOT NULL,
        report_type TEXT NOT NULL,
        file_path TEXT,
        article_count INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now'))
    );
    CREATE INDEX IF NOT EXISTS idx_reports_date ON daily_reports(report_date);

    -- 注：暂不启用 FTS5。日后的 Phase 2 再添加。
    -- 当前用 LIKE 搜索足够快。
''')

db.commit()
db.close()
