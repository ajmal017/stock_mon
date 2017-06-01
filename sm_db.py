import psycopg2
import os
import sm_util

db_database = os.environ.get('SM_DB', 'stock_mon')
db_user = os.environ.get('SM_USER', 'postgres')
db_password = os.environ.get('SM_PASSWORD', 'Reuters1')
db_host = os.environ.get('SM_HOST', 'localhost')
db_port = os.environ.get('SM_PORT', 5432)
enable_hstore = True if os.environ.get('SM_HSTORE', False) == '1' else False
db_dsn = 'dbname=%s user=%s password=%s host=%s port=%s' % (
    db_database, db_user, db_password, db_host, db_port)

hst_data_sqls = {
    'M':{
        "insert_data": "INSERT INTO stocks_m_hst_data VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT pk_smhd DO UPDATE SET open = EXCLUDED.open,close=EXCLUDED.close,high=EXCLUDED.high,low=EXCLUDED.low,volume = EXCLUDED.volume",
        'get_last_updated_date': "SELECT MAX(date) from stocks_m_hst_data"
    },
    'W':{
        "insert_data":  "INSERT INTO stocks_w_hst_data VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT pk_swhd DO UPDATE SET open = EXCLUDED.open,close=EXCLUDED.close,high=EXCLUDED.high,low=EXCLUDED.low,volume = EXCLUDED.volume",
        "get_last_updated_date": "SELECT MAX(date) from stocks_w_hst_data"
    },
    'D':{
        "insert_data": "INSERT INTO stocks_d_hst_data VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT pk_sdhd DO UPDATE SET open = EXCLUDED.open,close=EXCLUDED.close,high=EXCLUDED.high,low=EXCLUDED.low,volume = EXCLUDED.volume",
        "get_last_updated_date": "SELECT MAX(date) from stocks_d_hst_data"
    },
    '60':{
        "insert_data": "INSERT INTO stocks_60m_hst_data VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT pk_s60mhd DO UPDATE SET open = EXCLUDED.open,close=EXCLUDED.close,high=EXCLUDED.high,low=EXCLUDED.low,volume = EXCLUDED.volume",
        "get_last_updated_date": "SELECT MAX(date) from stocks_60m_hst_data"
    },
    '30':{
        "insert_data": "INSERT INTO stocks_30m_hst_data VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT pk_s30mhd DO UPDATE SET open = EXCLUDED.open,close=EXCLUDED.close,high=EXCLUDED.high,low=EXCLUDED.low,volume = EXCLUDED.volume",
        "get_last_updated_date": "SELECT MAX(date) from stocks_30m_hst_data"
    },
    '15':{
        "insert_data": "INSERT INTO stocks_15m_hst_data VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT pk_s15mhd DO UPDATE SET open = EXCLUDED.open,close=EXCLUDED.close,high=EXCLUDED.high,low=EXCLUDED.low,volume = EXCLUDED.volume",
        "get_last_updated_date": "SELECT MAX(date) from stocks_15m_hst_data"
    },
    '5':{
        "insert_data": "INSERT INTO stocks_5m_hst_data VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT pk_s5mhd DO UPDATE SET open = EXCLUDED.open,close=EXCLUDED.close,high=EXCLUDED.high,low=EXCLUDED.low,volume = EXCLUDED.volume",
        "get_last_updated_date": "SELECT MAX(date) from stocks_5m_hst_data"
    }
}

stock_info_sql = "INSERT INTO stocks_info VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT pk_si UPDATE set ( \
name = EXCLUDED.name,\
industry = EXCLUDED.industry,\
area = EXCLUDED.are,\
pe = EXCLUDED.pe,\
outstanding = EXCLUDED.outstanding,\
totals = EXCLUDED.totals,\
totalAssets = EXCLUDED.totalAssets,\
liquidAssets = EXCLUDED.liquidAssets,\
fixedAssets = EXCLUDED.fixedAssets,\
reserved = EXCLUDED.reserved,\
reservedPerShare = EXCLUDED.reservedPerShare,\
esp = EXCLUDED.esp,\
bvps = EXCLUDED.bvps,\
pb = EXCLUDED.pb,\
timeToMarket = EXCLUDED.timeToMarket,\
undp = EXCLUDED.undp,\
perundp = EXCLUDED.perundp,\
rev = EXCLUDED.rev,\
profit = EXCLUDED.profit,\
gpr = EXCLUDED.gpr,\
npr = EXCLUDED.npr,\
holders = EXCLUDED.holders)"

class smdb:
    #call this function before use db
    def sm_db_connect(self):
        try:
            self.conn = psycopg2.connect(dsn=db_dsn)
        except (psycopg2.Warning, psycopg2.Error) as error:
            print("connect to stock_mon db failed with error: %s" % error)
        else:
            return self.conn;

    def save_hst_data_to_db(self, df, ktype):
        cursor = self.conn.cursor()
        for idx, row in df.iterrows():
            date, open, close, high, low, volume, code = row[:]
            print([code, date, open, close, high, low, volume])
            #date format is different for different K type
            if ktype in ('M', 'W', 'D'):
                format  = "%Y-%m-%d"
            else:
                format  = "%Y-%m-%d %H:%M"
                timestamp = sm_util.str2timestamp(date, format)
                cursor.execute(hst_data_sqls[ktype]["insert_data"], [code, timestamp, open, close, high, low, volume])

    def update_stock_info_to_db(self, info):
        cursor = self.conn.cursor()
        for code in info.index:
            print(code)

    def get_db_last_updated_date(self, ktype):
        cursor = self.conn.cursor()
        cursor.execute(hst_data_sqls[ktype]["get_last_updated_date"])
        last_timestamp, = cursor.fetchone()
        return sm_util.timestamp2date(int(last_timestamp)) if last_timestamp is not None else None

    def commit(self):
        self.conn.commit()


