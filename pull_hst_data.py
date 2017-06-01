import tushare as ts
import sm_util
import datetime

from sm_db import smdb
from decimal import Decimal as D


class hstdata:
    def __init__(self):
        self.db = smdb()
        self.db.sm_db_connect()
        
    def pull_hst_data(self, code, ktype, start_date, end_date):
        df=ts.get_k_data(code, start_date, end_date, ktype=ktype)
        return df

    #this function will update both stocks_info and hst_data tables
    def get_all_stocks_hst_dat(self, start_date = None):
        info = ts.get_stock_basics()
        #update the stock info db
        #update_stock_info_to_db(info, conn)
        #update history data for the whole stocks
        for ktype in ('M', 'W', 'D', '60', '30', '15', '5'):
            for code in info.index :
                d = self.db.get_db_last_updated_date(ktype)
                end_date = datetime.datetime.now().strftime("%Y-%m-%d")
                if start_date is None:
                    start_date = (datetime.datetime(d.year, d.month, (d.day + 1)).strftime("%Y-%m-%d"))
                #pull the history data from next day of last updated date to today
                print("pull " + code + " from " + start_date + " to " + end_date)
                df = self.pull_hst_data(code, ktype, start_date, end_date)
                #save to db
                self.db.save_hst_data_to_db(df, ktype)
            self.db.commit()
            
if __name__ == "__main__":
    #info = ts.get_stock_basics()
    #df = pull_hst_data("600228", "W", "2016-12-01", "2016-12-27")
    hst_data = hstdata()
    #save_hst_data_to_db(df, conn, ktype='W')
    #sql = "select * from stocks_w_hst_data;"
    #cursor = conn.cursor()
    #print(cursor.execute(sql))
    #for record in cursor:
    #    print(record)
    #print(get_db_last_updated_date(conn, ktype ='W'))
    hst_data.get_all_stocks_hst_dat()
