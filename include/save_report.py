import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

class save_report:
    def __init__(self):
        load_dotenv()
        self.database_url = os.getenv("DATABASE_URL")

    def insertReport(self,df):
        engine = create_engine(self.database_url)

        upsert_sql = """
        INSERT INTO e400cam (srcfile, dstfile, srcsize, dstsize, diff, cam, path, seconds, len, backup, video_date)
        VALUES (:srcfile, :dstfile, :srcsize, :dstsize, :diff, :cam, :path, :seconds, :len, :backup, :video_date)
        ON CONFLICT (srcfile) DO UPDATE SET
            dstfile = EXCLUDED.dstfile, srcsize = EXCLUDED.srcsize, dstsize = EXCLUDED.dstsize, diff = EXCLUDED.diff,
            cam = EXCLUDED.cam, path = EXCLUDED.path, seconds = EXCLUDED.seconds, len = EXCLUDED.len,
            backup = EXCLUDED.backup, video_date = EXCLUDED.video_date
        """

        try:
            # Postgres stores NaN as a value (and rejects it in text columns), so send empty cells as NULL
            df = df.astype(object).where(df.notna(), None)
            with engine.begin() as conn:
                conn.execute(text(upsert_sql), df.to_dict(orient='records'))

            print(f"Report inserted with success")
            return True
        except Exception as e:
            print(f"Error to insert: {e}")
            return False
