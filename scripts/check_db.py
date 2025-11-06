import os
import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import STRCNX
print('STRCNX=', STRCNX)
from config.cnx import engine
from sqlalchemy import text

with engine.connect() as conn:
    res = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    print('tables:', [r[0] for r in res.fetchall()])
    try:
        res = conn.execute(text('SELECT count(*) FROM products'))
        print('products count:', res.fetchone()[0])
    except Exception as e:
        print('cannot count products:', e)
