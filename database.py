import sqlite3
from datetime import date, timedelta

DB_PATH = "data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_log (
            day TEXT PRIMARY KEY,
            success BOOLEAN NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def mark_day_as_success(day: str = None):
    if day is None:
        day = str(date.today())
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT OR REPLACE INTO daily_log (day, success) VALUES (?, 1)", (day,))
    conn.commit()
    conn.close()

def get_streak():
    """Возвращает текущую цепочку успешных дней до сегодня (включительно)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT day FROM daily_log WHERE success = 1 ORDER BY day DESC")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return 0

    today = date.today()
    streak = 0
    current = today

    # Преобразуем строки в даты и сортируем
    success_days = {date.fromisoformat(row[0]) for row in rows}

    while current in success_days:
        streak += 1
        current -= timedelta(days=1)
        if streak > 3650:  # защита от бесконечного цикла
            break

    return streak

def get_month_data(year: int, month: int):
    """Возвращает словарь: дата (str) -> успех (bool) для заданного месяца."""
    from calendar import monthrange
    _, last_day = monthrange(year, month)
    start = date(year, month, 1)
    end = date(year, month, last_day)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT day, success FROM daily_log
        WHERE day BETWEEN ? AND ?
    """, (str(start), str(end)))
    data = {row[0]: bool(row[1]) for row in cur.fetchall()}
    conn.close()

    # Заполняем все дни месяца
    result = {}
    for i in range(1, last_day + 1):
        d = date(year, month, i)
        result[str(d)] = data.get(str(d), False)
    return result