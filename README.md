# PureQuant帮助文档

------

## 下单交易

调用时需先导入trade模块并创建交易所对象

```python
from purequant.trade import OkexFutures

exchange = OkexFutures(access_key, secret_key, passphrase)
```

### 买入开多

```python
exchange.buy()
```

### 卖出平多

```python
exchange.sell()
```

### 卖出开空

```python
exchange.sellshort()
```

### 买入平空

```python
exchange.buytocover()
```

### 平多开空

```python
exchange.SELL()
```

### 平空开多

```python
exchange.BUY()
```

如果下单完全成交，则返回成交信息，否则返回“下单失败”的提示

------



## 获取持仓信息

调用时需先导入position模块并创建position对象

```python
from purequant.position import Position	

position = Position(exchange, instrument_id, time_frame)
```

### 当前持仓方向

```python
direction = position.direction()
# 若当前无持仓，返回None
# 若当前持多头，返回"long"
# 若当前持空头，返回"short"
```

### 当前持仓数量

```python
amount = position.amount()
# 返回整型数字
```

### 当前持仓均价

```python
price = position.price()
# 返回浮点数
```

------



## 获取行情信息

调用时需先导入market模块并创建market对象， 返回浮点数

```python
from purequant.market import Market

market = Market(exchange, instrument_id, time_frame)
```

### 最新成交价

```python
last = market.last()
```

### 开盘价

```python
open = market.open()

market.open(-1)  # 获取当根bar上的开盘价
market.open(-2)  # 获取上根bar上的开盘价
market.open(0)  # 获取最远一根bar上的开盘价
```

### 最高价

```python
high = market.high()

market.high(-1)  # 获取当根bar上的最高价
market.high(-2)  # 获取上根bar上的最高价
market.high(0)  # 获取最远一根bar上的最高价
```

### 最低价

```python
low = market.low()

market.low(-1)  # 获取当根bar上的最低价
market.low(-2)  # 获取上根bar上的最低价
market.low(0)  # 获取最远一根bar上的最低价
```

### 收盘价

```python
close = market.close()

market.close(-1)  # 获取当根bar上的收盘价
market.close(-2)  # 获取上根bar上的收盘价
market.close(0)  # 获取最远一根bar上的收盘价
```

### 合约面值

```python
# 获取合约面值，返回结果为计价货币数量，数据类型为整型数字。
# 如一张币本位BTC合约面值为100美元，一张USDT本位BTC合约面值为0.01个BTC
contract_value = market.contract_value
```

------



## 智能渠道推送

调用时需先导入push模块中的函数名称：

```python
from purequant.utils.push import dingtalk, sendmail, twilio
```

还需导入config模块并载入配置文件

```python
from purequant.config import config 

def __init__(self):
    config.loads(filename)# filename包括文件路径及名称，如"./config.json"表示同目录下的名为config.json文件
```

配置文件是一个名为config.json的文件，只需将其中参数修改为自己的即可

```json
{
    "LOG": {
        "level": "critical",
        "handler": "file"
    },
    "EXCHANGE": {
        "access_key": "f31241-266e-4126268cb86cef",
        "secret_key": "07E5C7FA7A7FA2EC5C4949B9D4",
        "passphrase": "123456"
    },
    "DINGTALK": {
        "ding_talk_api": "https://oapi.dingtalk.com/robot/send?access_token=d3a368908a7db882cd3f6afcccca302e51a1c9"
    },
    "TWILIO": {
        "accountSID" : "AC97a11fcc5ede559cd39061ad140f",
        "authToken" : "3616b6ced8e250232ca2fa4aa559",
        "myNumber" : "+8613712345678",
        "twilio_Number" : "+12058946789"
    },
    "SENDMAIL": {
        "from_addr" : "123456789@qq.com",
        "password" : "xqkwtrsfqwcjgjjgh",
        "to_addr" : "abc@icloud.com",
        "smtp_server" : "smtp.qq.com"
    }
}
```

### 读取交易api信息

在编写策略时，导入config模块并载入配置文件后，可直接使用如下代码来获取配置文件中保存的交易api信息

```python
access_key = config.access_key
secret_key = config.secret_key
passphrase = config.passphrase
```

### 推送钉钉提醒

```python
dingtalk("要推送的信息内容")
```

### 发送邮件通知

```python
sendmail("要推送的信息内容")
```

### 发送短信通知

```python
twilio("要推送的信息内容")
```

------



## 交易指标

调用时需先导入indicators模块：

```python
from purequant.indicators import Indicators
```

要传入的参数中都有platform、instrument_id、time_frame，所以需要声明这几个变量，并且初始化indicators

```python
from purequant.trade import OkexFutures
access_key = "2d3c69bd-754c-4f88-8928ba71a44"  # k线是公共数据，传入空的字符串也可
secret_key = "C3B79F99AB78B9F9645A4A5C746E0"
passphrase = "123456"
exchange = OkexFutures(access_key, secret_key, passphrase)
instrument_id = "BTC-USDT-201225"
time_frame = "1d"

indicators = Indicators(exchange, instrument_id, time_frame)
```

### ATR，平均真实波幅

返回一个一维数组

```python
indicators.ATR(14)
```

```python
# 获取最新一根bar上的atr
atr = indicators.ATR(14)[-1]
```

### BarUpdate，判断k线是否更新

如果更新，返回值为True，否则为False

```python
indicators.BarUpdate()
```

```python
# 调用方式
if indicators.BarUpdate():
    print("k线更新")
```

### BOLL，布林线指标

返回一个字典 {"upperband": 上轨数组， "middleband": 中轨数组， "lowerband": 下轨数组}

```python
indicators.BOLL(20)
```

```python
# 获取最新一根bar上的上、中、下轨值
upperband = indicators.BOLL(20)['upperband'][-1]
middleband = indicators.BOLL(20)['middleband'][-1]
lowerband = indicators.BOLL(20)['lowerband'][-1]
```

### CurrentBar，获取bar的长度

返回一个整型数字

```python
indicators.CurrentBar()
```

```python
# 获取交易所返回k线数据的长度
kline_length = indicators.CurrentBar()
```

### HIGHEST，周期最高价

返回一个一维数组

```python
indicators.HIGHEST(30)
```

```python
# 获取最新一根bar上的最高价
highest = indicators.HIGHEST(30)[-1]
```

### MA，移动平均线

返回一个一维数组

```python
indicators.MA(15)
```

```python
# 获取最新一根bar上的ma
ma15 = indicators.MA(15)[-1]
```

### MACD，指数平滑异同平均线

返回一个字典  {'DIF': DIF数组, 'DEA': DEA数组, 'MACD': MACD数组}

```python
indicators.MACD(12, 26, 9)
```

```python
# 获取最新一根bar上的DIF、DEA、MACD
DIF = indicators.MACD(12, 26, 9)['DIF'][-1]
DEA = indicators.MACD(12, 26, 9)['DEA'][-1]
MACD = indicators.MACD(12, 26, 9)['MACD'][-1]
```

### EMA，指数平均数

返回一个一维数组

```python
indicators.EMA(9)
```

```python
# 获取最新一根bar上的ema
ema = indicators.EMA(9)[-1]
```

### KAMA ，适应性移动平均线

返回一个一维数组

```python
indicators.EMA(30)
```

```python
# 获取最新一根bar上的kama
kama = indicators.KAMA(30)[-1]
```

### KDJ，随机指标

返回一个字典，{'k': k值数组， 'd': d值数组}

```python
indicators.KDJ(9 ,3, 3)
```

```python
# 获取最新一根bar上的k和d
k = indicators.KDJ(9 ,3, 3)['k'][-1]
d = indicators.KDJ(9 ,3, 3)['d'][-1]
```

### LOWEST，周期最低价

返回一个一维数组

```python
indicators.LOWEST(30)
```

```python
# 获取最新一根bar上的最低价
indicators.LOWEST(30)[-1]
```

### OBV，能量潮

返回一个一维数组

```python
indicators.OBV()
```

```python
# 获取最新一根bar上的obv
obv = indicators.OBV()[-1]
```

### RSI，强弱指标

返回一个一维数组

```python
indicators.RSI(14)
```

```python
# 获取最新一根bar上的rsi
rsi = indicators.RSI(14)[-1]
```

### ROC，变动率指标

返回一个一维数组

```python
indicators.ROC(12)
```

```python
# 获取最新一根bar上的roc
roc = indicators.ROC(12)[-1]
```

### STOCHRSI，随机相对强弱指数

返回一个字典  {'stochrsi': stochrsi数组, 'fastk': fastk数组}

```python
indicators.STOCHRSI(14, 14, 3)
```

```python
# 获取最新一根bar上的stochrsi、fastk
stochrsi = indicators.STOCHRSI(14, 14, 3)['stochrsi'][-1]
fastk = indicators.STOCHRSI(14, 14, 3)['fastk'][-1]
```

### SAR，抛物线指标

返回一个一维数组

```python
indicators.SAR()
```

```python
# 获取最新一根bar上的sar
sar = indicators.SAR()[-1]
```

### STDDEV， 标准方差

返回一个一维数组

```python
indicators.STDDEV()
```

```python
# 获取最新一根bar上的stddev
stddev = indicators.STDDEV(20)-1
```

### TRIX，三重指数平滑平均线

返回一个一维数组

```python
indicators.TRIX(12)
```

```python
# 获取最新一根bar上的trix
trix = indicators.TRIX(12)[-1]
```

### VOLUME，成交量

返回一个一维数组

```python
indicators.VOLUME()
```

```python
# 获取最新一根bar上的volume
volume = indicators.VOLUME()[-1]
```

------

##  常用的Python内置函数

### abs()	

函数返回数字的绝对值

以下展示了使用 abs() 方法的实例：

```python
print "abs(-45) : ", abs(-45) 
print "abs(100.12) : ", abs(100.12) 
print "abs(119L) : ", abs(119L)
```

以上实例运行后输出结果为：

```python
abs(-45) :  45
abs(100.12) :  100.12
abs(119L) :  119
```

### float()	

函数用于将整数和字符串转换成浮点数。

以下实例展示了 float() 的使用方法：

```python
>>>float(1)
1.0
>>> float(112)
112.0
>>> float(-123.6)
-123.6
>>> float('123')     # 字符串
123.0
```

### int() 

函数用于将一个字符串或数字转换为整型。

以下展示了使用 int() 方法的实例：

```python
>>>int()               # 不传入参数时，得到结果0
0
>>> int(3)
3
>>> int(3.6)
3
>>> int('12',16)        # 如果是带参数base的话，12要以字符串的形式进行输入，12 为 16进制
18
>>> int('0xa',16)  
10  
>>> int('10',8)  
8
```

###  len() 

方法返回对象（字符、列表、元组等）长度或项目个数。

以下实例展示了 len() 的使用方法：

```python
>>>str = "runoob"
>>> len(str)             # 字符串长度
6
>>> l = [1,2,3,4,5]
>>> len(l)               # 列表元素个数
5
```

### max()

 方法返回给定参数的最大值，参数可以为序列。

以下展示了使用 max() 方法的实例：

```python
print "max(80, 100, 1000) : ", max(80, 100, 1000)
print "max(-20, 100, 400) : ", max(-20, 100, 400)
print "max(-80, -20, -10) : ", max(-80, -20, -10)
print "max(0, 100, -400) : ", max(0, 100, -400)
```

以上实例运行后输出结果为：

```python
max(80, 100, 1000) :  1000
max(-20, 100, 400) :  400
max(-80, -20, -10) :  -10
max(0, 100, -400) :  100
```

### min() 

方法返回给定参数的最小值，参数可以为序列。

以下展示了使用 min() 方法的实例：

```python
print "min(80, 100, 1000) : ", min(80, 100, 1000)
print "min(-20, 100, 400) : ", min(-20, 100, 400)
print "min(-80, -20, -10) : ", min(-80, -20, -10)
print "min(0, 100, -400) : ", min(0, 100, -400)
```

以上实例运行后输出结果为：

```python
min(80, 100, 1000) :  80
min(-20, 100, 400) :  -20
min(-80, -20, -10) :  -80
min(0, 100, -400) :  -400
```

### **pow()**

 方法返回 xy（x的y次方） 的值。

以下展示了使用 pow() 方法的实例：

```python
import math   # 导入 math 模块
 
print "math.pow(100, 2) : ", math.pow(100, 2)
# 使用内置，查看输出结果区别
print "pow(100, 2) : ", pow(100, 2)
 
print "math.pow(100, -2) : ", math.pow(100, -2)
print "math.pow(2, 4) : ", math.pow(2, 4)
print "math.pow(3, 0) : ", math.pow(3, 0)
```

以上实例运行后输出结果为：

```python
math.pow(100, 2) :  10000.0
pow(100, 2) :  10000
math.pow(100, -2) :  0.0001
math.pow(2, 4) :  16.0
math.pow(3, 0) :  1.0
```

### range()

 函数可创建一个整数列表，一般用在 for 循环中。

```python
>>>range(10)        # 从 0 开始到 10
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> range(1, 11)     # 从 1 开始到 11
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> range(0, 30, 5)  # 步长为 5
[0, 5, 10, 15, 20, 25]
>>> range(0, 10, 3)  # 步长为 3
[0, 3, 6, 9]
>>> range(0, -10, -1) # 负数
[0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
>>> range(0)
[]
>>> range(1, 0)
[]
```

以下是 range 在 for 中的使用，循环出runoob 的每个字母:

```python
>>>x = 'runoob'
>>> for i in range(len(x)) :
...     print(x[i])
... 
r
u
n
o
o
b
>>>
```

### reverse() 

函数用于反向列表中元素。

该方法没有返回值，但是会对列表的元素进行反向排序。

以下实例展示了 reverse()函数的使用方法：

```python
aList = [123, 'xyz', 'zara', 'abc', 'xyz']

aList.reverse()
print "List : ", aList
```

以上实例输出结果如下：

```python
List :  ['xyz', 'abc', 'zara', 'xyz', 123]
```

### **round()** 

方法返回浮点数x的四舍五入值。

以下展示了使用 round() 方法的实例：

```python
print "round(80.23456, 2) : ", round(80.23456, 2)
print "round(100.000056, 3) : ", round(100.000056, 3)
print "round(-100.000056, 3) : ", round(-100.000056, 3)
```

以上实例运行后输出结果为：

```python
round(80.23456, 2) :  80.23
round(100.000056, 3) :  100.0
round(-100.000056, 3) :  -100.0
```

### str() 

函数将对象转化为字符串格式。

以下展示了使用 str() 方法的实例：

```python
>>>s = 'RUNOOB'
>>> str(s)
'RUNOOB'
>>> dict = {'runoob': 'runoob.com', 'google': 'google.com'};
>>> str(dict)
"{'google': 'google.com', 'runoob': 'runoob.com'}"
>>>
```

### **sum()** 

方法对系列进行求和计算。

以下展示了使用 sum 函数的实例：

```python
>>>sum([0,1,2])  
3  
>>> sum((2, 3, 4), 1)        # 元组计算总和后再加 1
10
>>> sum([0,1,2,3,4], 2)      # 列表计算总和后再加 2
12
```

### type() 

函数如果只有一个参数则返回对象的类型。

以下展示了使用 type 函数的实例：

```python
# 一个参数实例
>>> type(1)
<type 'int'>
>>> type('runoob')
<type 'str'>
>>> type([2])
<type 'list'>
>>> type({0:'zero'})
<type 'dict'>
>>> x = 1          
>>> type( x ) == int    # 判断类型是否相等
True
```

------

## 输出异常日志

调用时需先导入logger模块，并在当前目录下创建名为"logger"的文件夹用以存放日志输出文件

并且需要初始化logger模块，参数为配置文件路径

```python
from purequant.utils.logger import Logger

logger = Logger(config_file)
```

在配置文件中，可以直接修改日志输出的等级来控制日志输出级别：

```json
# 将"level"设置成"critical"，则只输出"CRITICAL"级别的日志
{
    "LOG": {
        "level": "critical"
    }
}
```

```json
# "handler"中可以指明日志的输出方式
# "file"是以文件输出的方式存储日志到当前目录下的"logger"文件夹，按照文件大小1M进行分割，保留最近10个文件
# "time"也是文件输出，但是以按照一天的时间间隔来分割文件，保留最近10个文件
# "stream"或者不填或者填入其他字符，都是输出到控制台，不会存储到文件
{
    "LOG": {
        "level": "critical",
        "handler": "file"
    }
}
```



### debug

一般用来打印一些调试信息，级别最低

```python
logger.debug("要输出的调试信息")
```

### info

一般用来打印一些正常的操作信息

```python
logger.info("要输出的操作信息")
```

### warning

一般用来打印警告信息

```python
logger.info("要输出的警告信息")
```

### error

一般用来打印一些错误信息

```python
logger.info("要输出的错误信息")
```

### critical

一般用来打印一些致命的错误信息，等级最高

```python
logger.critical("要输出的致命的错误信息")
```

------



## 获取时间信息

调用前需先导入time_tools模块中的函数

```python
from purequant.utils.time_tools import *
```

### 获取本地时间

```python
localtime = get_localtime()
```

### 获取当前utc时间

```python
utc_time = get_utc_time()
```

### 获取当前时间戳（秒）

```python
cur_timestamp = get_cur_timestamp()
```

### 获取当前时间戳（毫秒）

```python
cur_timestamp_ms = get_cur_timestamp_ms()
```

------

## 示例策略

### 双均线多空策略

### 海龟交易策略

### **价栺区间突破多空策略** 

**策略交易规则：**

+ **策略说明**：基于通道突破的判断，配合开仓价反向 atr 初始止损和反向通道止损。生命周期

很长、适用性广的经典策略。

+ **系统要素**：1. 计算 50 根 k 线最高价的区间；2. 计算 40 根 k 线最低价的区间。

+ **入场条件**：1. 价格高于 50 根 K 线最高价的区间，或者低于 50 根 k 线最低价的区间时，用突破价格入场。2. 用入场价格计算初始止损价。

+ **出场条件**：1. 当前价格高于/低于 40 根 K 线最低价的区间，用突破反向通道的价格出场；2. 当前价格高于/低于入场价一定 ATR 波动率幅度，用初始止损价出场。

