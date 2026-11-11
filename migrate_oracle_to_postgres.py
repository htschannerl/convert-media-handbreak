#!/usr/bin/env python3
# One-off copy of the E400CAM table from Oracle to Postgres.
# Uses the Oracle settings (dbuser, dbpassword, dbhost, dbport, dbservice) and DATABASE_URL from .env.
# Safe to run more than once: rows are upserted by srcfile.
import os
import oracledb
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

COLUMNS = ["srcfile", "dstfile", "srcsize", "dstsize", "diff", "cam", "path", "seconds", "len", "backup", "video_date"]

load_dotenv()
oracle = create_engine(f'oracle+oracledb://{os.getenv("dbuser")}:{os.getenv("dbpassword")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/?service_name={os.getenv("dbservice")}')
postgres = create_engine(os.getenv("DATABASE_URL"))

select_sql = f"SELECT {', '.join(COLUMNS)} FROM E400CAM"
upsert_sql = f"""
INSERT INTO e400cam ({', '.join(COLUMNS)})
VALUES ({', '.join(':' + c for c in COLUMNS)})
ON CONFLICT (srcfile) DO UPDATE SET {', '.join(f'{c} = EXCLUDED.{c}' for c in COLUMNS[1:])}
"""

with oracle.connect() as src:
    rows = [dict(r._mapping) for r in src.execute(text(select_sql))]
print(f"Read {len(rows)} rows from Oracle")

with postgres.begin() as dst:
    for i in range(0, len(rows), 1000):
        dst.execute(text(upsert_sql), rows[i:i + 1000])
    total = dst.execute(text("SELECT count(*) FROM e400cam")).scalar()
print(f"Postgres e400cam now has {total} rows")
