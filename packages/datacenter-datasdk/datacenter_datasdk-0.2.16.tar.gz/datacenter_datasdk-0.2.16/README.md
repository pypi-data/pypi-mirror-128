# datacenter_datasdk

### INSTALL

step.1 
```
pip install datacenter-datasdk
```

step.2 add auth(token, password) (ask for admin) before query data


### USAGE

```
from datacenter_datasdk import auth, get_price, get_trade_days, get_security_info
from datacenter_datasdk import CN_JQ_SUMMARY, query
from datacenter_datasdk import query_by_sql

auth(token, password)

data = get_price('600033.XSHG', 'cn', 'm1', start_date='2010-01-01', end_date='2021-01-01')

trade_days = get_trade_days('cn', start_date='2021-01-01', count=10)

info = get_security_info('cn', '600033.XSHG')

d = query(CN_JQ_SUMMARY).filter(
    CN_JQ_SUMMARY.code=='000001.XSHE').order_by(
    CN_JQ_SUMMARY.date.desc()).all() 

df = query_by_sql('cn_jq_summary', 
                  condition='code = \'000004.XSHE\' and date= \'2021-01-11\'', 
                  columns=['date', 'code', 'industry_name']
                 )

```

### API
---
#### *get_price()*
get kline data, include daily, minute and tick

**params**

code(required): str or list, single code or multi code as list

region(required): str, 'cn' or 'us'

frequency(required): str, represent frequency of kline, 'd1', 'm1', 'm5', 'm15', 'm30', 'm60' and 'tick'(only in cn), 'd1_post'(only in cn), 'd1_raw'(only in cn)

start_date(optional), datetime.datetime or datetime.date or str, start time of data, default '2005-01-01'

end_date(optional), datetime.datetime or datetime.date or str, end time of data, default 0 o'clock of today

**return**

dataframe

---

#### *get_trade_days()*
get trade days

**params**

region(required): str, 'cn' or 'us'

start_date(optional), datetime.datetime or datetime.date or str, start time of data, default None

end_date(optional), datetime.datetime or datetime.date or str, end time of data, default None

count(optional), int, default None

**return**

list of date

---

#### *get_security_info()*
get security info

**params**

region(required): str, 'cn' or 'us'

types(optional): list, values in ('etf', 'stock', 'index'), default ['etf', 'stock', 'index']

code(optional): str, default None (get all code info), default None

date(optional), datetime.datetime or datetime.date or str, not exit market until this date, default None

**return**

dataframe

---

#### *query()*
is also query object in sqlalchemy

**params**

table(required): object, import from given list of table object, the given table list ask for admin


**return**

list of table object or table object

---

#### *query_by_sql()*
get data by defining 'where' condition in sql, max rows of one return is 100w

**params**

table_name(required): str, table name

condition(optional): str, 'where' condition str in sql, to filter data, default None

columns(optional): list, the return columns, default None and return all columns

**return**

dataframe

---
