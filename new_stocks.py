import tornado.web
import datetime
import json
import tushare as ts

from tornado import gen
from base_handler import BaseHandler

class NewStockHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        _new_stocks = self._get_new_stocks()
        _new_stocks.sort(key=lambda x:x['issue_date'], reverse = True)
        self.write(json.dumps(_new_stocks))
        self.finish()

    def _get_new_stocks(self):
        df = ts.new_stocks()
        _from_time = datetime.datetime.now() - datetime.timedelta(days=30)
        df.dropna(inplace = True)
        _new_stocks = [{"code":row['code'], "name":row['name'], "price":row['price'], "issue_date":row['issue_date']} for index, row in df.iterrows() if (datetime.datetime.strptime(row['issue_date'], '%Y-%m-%d')) > _from_time]
        return _new_stocks


if __name__ == "__main__":
    print(NewStockHandler()._get_new_stocks())
