import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

class report:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv("dbuser")
        self.password = os.getenv("dbpassword")
        self.hostname = os.getenv("dbhost")
        self.port = os.getenv("dbport")
        self.service_name = os.getenv("dbservice")

    def insertReport(self,df):
        connection_string = f"oracle+cx_oracle://{self.username}:{self.password}@{self.hostname}:{self.port}/?service_name={self.service_name}"

        engine = create_engine(connection_string)
        try:
            df.to_sql('E400CAM', con=engine, if_exists='append', index=False)
            return True
        except Exception as e:
            print(f"Error to insert")
            return False
