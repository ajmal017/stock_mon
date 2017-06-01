import tornado.web
import datetime
import json
import tushare as ts

from tornado import gen
from base_handler import BaseHandler

class TickDataHandler(BaseHandler):
    @gen.coroutine
    def get(self):

        _stock_code = self.get_argument("code", None)
        _date = self.get_argument("date", datetime.date.today().strftime('%Y-%m-%d'))
        _num_of_tick = self.get_argument("numofticks", None)
        if _stock_code is not None:
            df = ts.get_tick_data(_stock_code, _date)
            if _num_of_tick is not None:
                s = df.head(int(_num_of_tick)).to_json()
            else:
                s = df.head(10).to_json()
            d = json.loads(s)
            _ticks = [{"time": _time, "price": _price, "volume": _volume, "change":_change, "amount":_amount, "type":_type} for _time, _price, _volume, _change, _amount,_type in zip(d['time'].values(), d['price'].values(), d['volume'].values(), d['change'].values(), d['amount'].values(), d['type'].values())]
            _ticks.sort(key=lambda x : x['time'], reverse = True)
            self.write(json.dumps(_ticks))
        else:
            self.write("Stock code is not provided")

        self.finish()

