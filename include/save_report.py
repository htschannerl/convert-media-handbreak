import os
import oracledb
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

class save_report:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv("dbuser")
        self.password = os.getenv("dbpassword")
        self.hostname = os.getenv("dbhost")
        self.port = os.getenv("dbport")
        self.service_name = os.getenv("dbservice")

    def insertReport(self,df):
        engine = create_engine(f'oracle+oracledb://{self.username}:{self.password}@{self.hostname}:{self.port}/?service_name={self.service_name}')

        merge_sql = """
        MERGE INTO E400CAM tgt
        USING (SELECT :srcfile AS srcfile, :dstfile AS dstfile, :srcsize AS srcsize, :dstsize AS dstsize, :diff AS diff,
                      :cam AS cam, :path AS path, :seconds AS seconds, :len AS len, :backup AS backup, :date AS "date" FROM dual) src
        ON (tgt.srcfile = src.srcfile)
        WHEN MATCHED THEN
            UPDATE SET dstfile = src.dstfile, srcsize = src.srcsize, dstsize = src.dstsize, diff = src.diff, cam = src.cam,
                       path = src.path, seconds = src.seconds, len = src.len, backup = src.backup, "date" = src."date"
        WHEN NOT MATCHED THEN
            INSERT (srcfile, dstfile, srcsize, dstsize, diff, cam, path, seconds, len, backup, "date")
            VALUES (src.srcfile, src.dstfile, src.srcsize, src.dstsize, src.diff, src.cam, src.path, src.seconds, src.len, src.backup, src."date")
        """

        try:
            with engine.begin() as conn:
                # When converting the DataFrame row to a dict, ensure the key is 'date' not '"date"'
                for row in df.to_dict(orient='records'):
                    if '"date"' in row:
                        row['date'] = row.pop('"date"')
                    conn.execute(text(merge_sql), row)

            print(f"Report inserted with success")
            return True
        except Exception as e:
            print(f"Error to insert: {e}")
            return False
