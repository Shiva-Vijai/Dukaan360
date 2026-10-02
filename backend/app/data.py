"""SQLite-backed repository for local development and single-instance hosting."""
import json, os, sqlite3
from copy import deepcopy
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parents[1] / "dukaan360.db"
DB_PATH = Path(os.getenv("DUKAAN_DB_PATH", str(DEFAULT_DB_PATH))).expanduser()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
INITIAL_PRODUCTS=[
{"id":"rice5","barcode":"890100000001","name":"Rice 5kg","category":"Staples","price":450,"unit":"pack","quantity":17,"daily_demand":.8,"status":"Healthy"},
{"id":"milk","barcode":"890100000002","name":"Milk 1L","category":"Dairy","price":65,"unit":"unit","quantity":5,"daily_demand":2.1,"status":"Low Stock"},
{"id":"oil5","barcode":"890100000003","name":"Cooking Oil 5L","category":"Oils","price":740,"unit":"tin","quantity":30,"daily_demand":.4,"status":"Overstock"},
{"id":"biscuits","barcode":"890100000004","name":"Premium Biscuits","category":"Snacks","price":60,"unit":"pack","quantity":24,"daily_demand":.14,"status":"Slow Moving"},
{"id":"sugar","barcode":"890100000005","name":"Sugar 1kg","category":"Staples","price":52,"unit":"pack","quantity":25,"daily_demand":1.1,"status":"Healthy"},
{"id":"soap","barcode":"890100000006","name":"Bath Soap","category":"Personal Care","price":38,"unit":"unit","quantity":43,"daily_demand":.7,"status":"Healthy"}]
def con():
 c=sqlite3.connect(DB_PATH);c.execute("CREATE TABLE IF NOT EXISTS products (id TEXT PRIMARY KEY,barcode TEXT UNIQUE,payload TEXT)");c.execute("CREATE TABLE IF NOT EXISTS sales (id TEXT PRIMARY KEY,payload TEXT)");c.execute("CREATE TABLE IF NOT EXISTS customers (phone TEXT PRIMARY KEY,payload TEXT)");return c
def load():
 with con() as c:
  rows=c.execute("SELECT payload FROM products").fetchall()
  if not rows:
   c.executemany("INSERT INTO products VALUES (?,?,?)",[(p['id'],p['barcode'],json.dumps(p)) for p in INITIAL_PRODUCTS]);rows=[(json.dumps(p),) for p in INITIAL_PRODUCTS]
  return [json.loads(r[0]) for r in rows],[json.loads(r[0]) for r in c.execute("SELECT payload FROM sales").fetchall()]
products,sales=load()
def persist_products():
 with con() as c:c.execute("DELETE FROM products");c.executemany("INSERT INTO products VALUES (?,?,?)",[(p['id'],p['barcode'],json.dumps(p)) for p in products])
def persist_sales():
 with con() as c:c.execute("DELETE FROM sales");c.executemany("INSERT INTO sales VALUES (?,?)",[(s['id'],json.dumps(s)) for s in sales])
def reset_demo():
 global products,sales
 products,sales=deepcopy(INITIAL_PRODUCTS),[];persist_products();persist_sales()
