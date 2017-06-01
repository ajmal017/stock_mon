import tornado.web
import datetime
import json
import tushare as ts

from tornado import gen
from base_handler import BaseHandler

class NewHighHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        indays = self.get_argument("indays", 30)
        info = ts.get_stock_basics()
        new_high_stocks = [{'code':code, 'name':info.ix[code]['name']} for code in info.index if self._is_new_high(code, indays)]
        self.write(json.dumps(new_high_stocks))
        self.finish()

    def _is_new_high(self, code, indays):
        #count into the weekend
        indays = indays * 7 / 5
        today = datetime.date.today()
        start_day = today - datetime.timedelta(indays)
        #df=ts.get_h_data(code, start_day.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))
        df=ts.get_k_data(code, ktype='60', start=start_day.strftime("%Y-%m-%d"), end=today.strftime("%Y-%m-%d"))
        print(df.dtypes)
        print(df)
        period_high = df['high'].max()
        today_high = df.iloc[0]['high']
        if today_high == period_high :
            return True
        else:
            return False


if __name__ == "__main__":
    info = ts.get_stock_basics()
    new_high_stocks = []
    for code in info.index :
        if _is_new_high(code, 30) :
            new_high_stock = {'code':code, 'name':info.ix[code]['name']}
            print(new_high_stock)
            new_high_stocks.append(new_high_stock)

