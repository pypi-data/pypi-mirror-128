# Official Python repository for TrueData (Market Data APIs)
----
This Python library attempts to make it easy for you to connect to TrueData Market Data Apis, thereby allowing you to concentrate on startegy development, while this library works to get you all the data you need from the TrueData backend both for Real Time & Historical.

Please make sure you follow us on our Telegram channel where we push a lot of information with regards to API updates, implementation ideas, tips & tricks to use this library & raw feed, etc...
* [TrueData Market Data API - Telegram Channel](https://t.me/truedata_ws_api)
* [TrueData Market Data APIs - Website](https://www.truedata.in/api)

We have also built a sandbox environmemt for testing the raw feed. Please feel free to use this environment to check/test/compare your results with the raw data feed (real time & historical).
* [TrueData Market Data API - Sandbox Environment](https://wstest.truedata.in)

We are trying to improve this library continuously and feedback for the same is welcome. 

----
## What have we covered so far ?

**WebSocket APIs**

  *  Live data (Streaming Ticks) - Enabled by Default
  *  Live Data (Streaming 1 min bars) - Needs to be enabled from our backend
  *  Live Data (Streaming 5 min bars) - Needs to be enabled from our backend

**REST APIs**
  *  Historical Data
  
----
# Getting Started 
**Installation**

* Installing the truedata-ws library from PyPi
```shell script
python3 -m pip install truedata_ws
```
or
```shell script
pip3 install truedata_ws
```

**Minimum Requirements**

The minimum required versions are:-
```
- Python >= 3.7
```
**In-built dependencies**

All these dependancies should get installed automatically when you install the truedata_ws library. In case of an issue, make sure you meet the requirements as mentioned below.
```
- websocket-client>=0.57.0
- colorama>=0.4.3
- python-dateutil>=2.8.1
- pandas>=1.0.3
- setuptools>=50.3.2
- requests>=2.25.0
- lz4>=3.1.3
```

**Connecting / Logging in**
* Connecting / Logging in (Both Real time & Historical data feed subscriptions)
```python
from truedata_ws.websocket.TD import TD
td_obj = TD('<enter_your_login_id>', '<enter_your_password>')
# This connects you to the default real time port which is 8082 & the REST History feed. 
# If you have been authourised on another live port please enter another parameter
# Example
# td_obj = TD('<enter_your_login_id>', '<enter_your_password>', live_port=8084)
```
* Connecting / Logging in (For Historical Data Subscription Only)
```python
from truedata_ws.websocket.TD import TD
td_obj = TD('<enter_your_login_id>', '<enter_your_password>', live_port=None)
```
* Connecting / Logging in (For Real time Data Subscription Only)
```python
from truedata_ws.websocket.TD import TD
td_obj = TD('<enter_your_login_id>', '<enter_your_password>', historical_api=False)
```
**Automatic Reconnection of Real Time Streaming Feed**

In case of a Websocket disconnection, the library will check for the internet connection and once the connection is steady, it will try to re-connect the Websocket, automatically.

Once the websocket connection is re-established, the library will automatically re-subscribe the symbols & restart the live data seamlessly.

**Logging**

We have integrated the python stdlib logger. You can provide LOG_LEVEL and LOG_FORMAT if you want.
```python
from truedata_ws.websocket.TD import TD
import logging
td_obj = TD('<enter_your_login_id>', '<enter_your_password>', log_level=logging.WARNING, log_format="(%(asctime)s) %(levelname)s :: %(message)s (PID:%(process)d Thread:%(thread)d)")
```


Additional LOG_LEVEL info can be found at https://docs.python.org/3/library/logging.html#logging-levels. 

Additional LOG_FORMAT info can be found at https://docs.python.org/3/library/logging.html#logrecord-attributes.

If you really know what you are doing, you can simply provide a log handler. 
```python
td_obj = TD('<enter_your_login_id>', '<enter_your_password>', log_handler=log_handler_obj)
```

----
# Real Time Data Streaming (Live)
* Starting Live Data For Multiple symbols
```python
req_ids = td_obj.start_live_data(['<symbol_1>', '<symbol_2>', '<symbol_3>', ...])
# Example:
# req_ids = td_obj.start_live_data(['CRUDEOIL-I', 'BANKNIFTY-I', 'RELIANCE', 'ITC'])
# This returns a list that can be used to reference data later
```

* Accessing Touchline Data 

The touchline data is useful post market hours as this provides the last updates / settlement updates / snap quotes. 

Please note that it is not recommended to use this during market hours as all the fields of the touchline data already form a part of the real time market data feed.

```python
import time
time.sleep(1)
# You need to wait until for 1 sec for all of the touchline data to populate
for req_id in req_ids:
    print(td_obj.touchline_data[req_id])
```
* Accessing live streaming data
  
All updated relevant live data can be found in the object at `td_obj.live_data[req_id]`.

For more details try: `print(f"{type(td_obj.live_data[req_id])} -> {td_obj.live_data[req_id]})`
```python
last_traded_price = td_obj.live_data[req_id].ltp
change_perc = td_obj.live_data[req_id].change_perc
day_high = td_obj.live_data[req_id].day_high
highest_available_bid = td_obj.live_data[req_id].best_bid_price
```
> The code can be used for if you are subscribed to `tick` only or `minute` only streaming. If you are using `tick+min` streaming, then, tick data can be found at `td_obj.live_data[req_id]` and, the minute bar data can be found at `td_obj.min_live_data[req_id]`.

* Stopping live data

```python
td_obj.stop_live_data(['<symbol_1>', '<symbol_2>', '<symbol_3>', ...])
```
* Disconnect from the WebSocket service
```python
td_obj.disconnect()
```

* QUICK START LIVE DATA CODE

If you simply want to print data in the format given, try the code just below that.
> Symbol > LTP > Change
```Python
req_ids = td_obj.start_live_data(symbols)
live_data_objs = {}

time.sleep(1)

for req_id in req_ids:
    live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])

while True:
    for req_id in req_ids:
        if not td_obj.live_data[req_id] == live_data_objs[req_id]:
            print(f'{td_obj.live_data[req_id].symbol} > {td_obj.live_data[req_id].ltp} > {td_obj.live_data[req_id].change:.2f}')
            live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])
```

* CONVERTING REAL TIME STREAM TO DICT

In some cases, some people may need to convert the real time stream to dict. This could be either to push the real time
stream into pandas, a SQL database or work with processing the stream differently at your end.

So, if you need to convert the Real Time Stream to dict, use the **to_dict()** function.

```python
td_obj.live_data[req_id].to_dict()
```
Here is a sample code to push the data into a pandas Dataframe. 
Please adapt to your code as this is just a sample and there could be better ways to do the same thing more efficiently. 

```python
from truedata_ws.websocket.TD import TD
import time
import pandas as pd
from copy import deepcopy

td_obj = TD('<enter_your_login_id>', '<enter_your_password>')

symbols = ['CRUDEOIL-I', 'GOLD-I', 'NIFTY-I']
symbol_ids = td_obj.get_req_id_list(2000, len(symbols))  # symbol_ids = list(range(2000, 2000+len(symbols)))

live_data_objs = {}
td_obj.start_live_data(symbols, req_id=symbol_ids)
time.sleep(1)

for symbol_id in symbol_ids:
	live_data_objs[symbol_id] = deepcopy(td_obj.live_data[symbol_id])

df = pd.DataFrame()
# pd.set_option("display.max_rows", None, "display.max_columns", None)

while True:
	time.sleep(0.05)
	for req_id in symbol_ids:
		if td_obj.live_data[req_id] != live_data_objs[req_id]:
			live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])
			if td_obj.live_data[req_id].tick_type == 1:  # picking up trade packets & discarding only bid ask packets
				op_dict = deepcopy(td_obj.live_data[req_id].to_dict())
				temp_df = pd.DataFrame.from_records([op_dict])
				# temp_df = pd.DataFrame(op_dict, index=[0])  # BOTH WORK
				df = df.append(temp_df, ignore_index=True)
				print(df)  # just printing out the df with each update

```
----
# Option Chain Streaming
>Starting Option chain data for a symbol
```python
from datetime import datetime as dt
from truedata_ws.websocket.TD import TD

td_obj = TD('<enter_your_login_id>', '<enter_your_password>')

nifty_chain = td_obj.start_option_chain( 'NIFTY' , dt(2021 , 8 , 26) )
# this line enabling option chain for NIFTY with corresponding expiry. 
```
* start_option_chain function takes following arguments:
  * symbols for egs: NIFTY , BANKNIFTY , SBIN etc......
  * expiry : date (date object) 
  * chain_length : number of strike need to pull with respect to future prices. default value is 10 (int)
  * bid_ask : enable live quote . default value is false (boolean)
  * market_open_post_hours : extra parameter for updating the chain in extra NSE session like (muhurat session) , default is False

>Pulling option chain
```python
df = nifty_chain.get_option_chain()
#this line returns a dataframe that contain option chain for repective symbol
```
this get_option_chain function can call anywhere  that will return respective option chain

>Stop option chain update when
```python
nifty_chain.stop_option_chain()
#this function call will stop updating the respective option chain. 
```

>example for pulling option chain and live data from
* common mistake people doing is leaving while loop without putting proper time sleep . 
```python
from truedata_ws.websocket.TD import TD
from copy import deepcopy
import time
import logging
from datetime import datetime as dt

td_obj = TD('<your_login>', '<your_password>' , log_level= logging.WARNING )

symbols = ['BANKNIFTY-I' , 'NIFTY 50' , 'NIFTY21072915600CE' , 'SBIN' ]
#starting live data for symbols 
req_ids = td_obj.start_live_data(symbols)
live_data_objs = {}
time.sleep(1)

# initilizing option chain with symbol expiry chain length(optional) , bid ask (optional)
sbi_chain = td_obj.start_option_chain( 'SBIN', dt(2021 , 8 , 26) )
bnf_chain = td_obj.start_option_chain( 'BANKNIFTY', dt(2021 , 8 , 26) , chain_length = 20 )
nifty_chain = td_obj.start_option_chain( 'NIFTY', dt(2021 , 8 , 26), chain_length = 10, bid_ask = True)
time.sleep(2)

for req_id in req_ids:
    live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])
print(sbi_chain.get_option_chain())
print(nifty_chain.get_option_chain())
print(bnf_chain.get_option_chain())

count = 1
while True:
    for req_id in req_ids:
        if not td_obj.live_data[req_id] == live_data_objs[req_id]:
            #this will priint live tick that requested 
            print( f'{td_obj.live_data[req_id].symbol} ==> {td_obj.live_data[req_id].ltp}')
            live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])
            # fetching option chain every 50 ticks
            if count % 50 == 0:
                print(sbi_chain.get_option_chain())
                print(nifty_chain.get_option_chain())
                print(bnf_chain.get_option_chain())
            count += 1
    time.sleep(0.05)  # important otherwise cpu will overthrottle.

```
----
# Historical Data
>Historical Data is provided over REST (from the backend) using Start time, End time or Duration 

* Using no parameters
```python
hist_data_1 = td_obj.get_historic_data('BANKNIFTY-I')
# This returns 1 minute bars from the start of the present day until current time
```

* Using a given duration (For available duration options, please read the limitations section)
```python
hist_data_2 = td_obj.get_historic_data('BANKNIFTY-I', duration='3 D')
```
* Using a specified bar_size (For available bar_size options, please read the limitations section)
```python
hist_data_3 = td_obj.get_historic_data('BANKNIFTY-I', bar_size='30 mins')
```
* Using start time INSTEAD of duration
```python
from dateutil.relativedelta import relativedelta
hist_data_4 = td_obj.get_historic_data('BANKNIFTY-I', start_time=datetime.now()-relativedelta(days=3))
```
* Using a specific ending time
```python
from datetime import datetime
hist_data_5 = td_obj.get_historic_data('BANKNIFTY-I', end_time=datetime(2021, 3, 5, 12, 30))
# Any time can be given here
```
* Using a specific number of bars (Enabled for Tick, 1 min & EOD bars)

You can specify the number of bars (or ticks) which you want to see or use in your code.
This is currently enabled for Ticks , 1 min bars & EOD Bars.
```python
hist_data_6=td_app.get_n_historical_bars(symbol, no_of_bars=30, bar_size=barsize
```


* Enabling / Disabling Bid Ask data with Tick Data History

If you have subscribed for Historical Bid Ask (not activated by default), you can control the visibility of this data depending upon your needs by setting the bidask parameter to True, like, `bidask=True`.  
```python
hist_data_7 = td_obj.get_historic_data(symbol, duration='1 D', bar_size='tick', bidask=True)
```
> Default `bidask=False`

* Storing data for later use

Until v3.x.x, requested data was stored in the `td_obj` at `td_obj.hist_data[req_id]`.

As of v4.0.1, you need to **explicitly** provide a ticker_id to store the data for later use. For example,
```python
td_obj.get_historic_data('BANKNIFTY-I', ticker_id=1000)
# At any later point
print(td_obj.hist_data[1000])
```
**IMPORTANT NOTE:**

Now that we have covered the basic parameters, you can mix and match the parameters as you please. If a parameter is not specified, the defaults are as follows
```python
end_time = datetime.now()
duration = "1 D"
bar_size = "1 min"
```

* Example of mix and match
```python
hist_data_8 = td_obj.get_historic_data('BANKNIFTY-I', duration='3 D', bar_size='15 mins')
```

*On a side note: You can convert historical data to **Pandas DataFrames** with a single line*
```python
import pandas as pd
df = pd.DataFrame(hist_data_1)
```
**Get Bhavcopy**

This function enables you to get the NSE & MCX bhavcopies for the day / date. 
```python
eq_bhav = td_obj.get_bhavcopy('EQ')
fo_bhav = td_obj.get_bhavcopy('FO')
mcx_bhav = td_obj.get_bhavcopy('MCX')
```
The request checks if the latest completed bhavcopy has arrived for that segment and, if arrived, it returns the data. 

In case it has not arrived it provides the date and time of the last bhavcopy available which can also be pulled by providing the bhavcopy date.
```
*No complete bhavcopy found for requested date. Last available for 2021-03-19 16:46:00.*
```
>In this case, if you need the bhavcopy of the date provided, you can get it by giving the date for which the bhavcopy is required as shown below..

```python
specific_bhav = td_obj.get_bhavcopy('EQ', date=datetime.datetime(2021, 3, 19))
```
**Limitations and caveats for historical data**

1) If you provide both duration and start time, duration will be used and start time will be ignored.
2) If you provide neither duration nor start time, duration = "1 D" will be used
3) If you donot provide the bar size bar_size = "1 min" will be used
4) The following BAR_SIZES are available:

    - tick
    - 1 min
    - 2 mins
    - 3 mins
    - 5 mins
    - 10 mins
    - 15 mins
    - 30 mins
    - 60 mins
    - EOD

5) The following annotation can be used for DURATION:-

    - D = Days
    - W = Weeks
    - M = Months
    - Y = Years

**Get Gainers losers information**

This function enables you to get the NSE gainers losers information at present state. 
```python
gainers = td_obj.get_gainers(segment = "NSEEQ" , topn= 10 , df_style= False)
losers = td_obj.get_losers(segment = "NSEEQ" , topn= 10 )
```
The function call return a dataframe or list that contains gainers losers information accoriding to your style preferred 

* gainers , losers function takes following arguments:
  * segment (string) : NSEEQ, NSEFUT, NSEOPT, MCX
  * topn (int) : default 10 , top n number  
  * df_style : default is True , output style customization 

----
# Example Strategies

Here we cover 4 sample strategies, the first 2 use a constant state check mechanism and, the last 2 use a callback.

Strategy 1
   - Tick based
   - State Check
   - BUY when past 50 ticks SMA goes above 100 ticks SMA.
   - SELLS when past 50 ticks SMA goes below 100 ticks SMA.

Strategy 2
   - Tick based
   - Callback
   - BUY when past 50 ticks SMA goes above 100 ticks SMA.
   - SELLS when past 50 ticks SMA goes below 100 ticks SMA.

Strategy 3
   - Minute Bar based
   - Callback
   - BUY when past 50 bars close SMA goes above 100 bars close SMA.
   - SELLS when past 50 bars close SMA goes below 100 bars close SMA.

Strategy 4
   - Minute Bar based
   - State Check
   - BUY when past 50 bars close SMA goes above 100 bars close SMA.
   - SELLS when past 50 bars close SMA goes below 100 bars close SMA.

### Strategy 1
```python
from truedata_ws.websocket.TD import TD
from copy import deepcopy
import time , os
import logging

td_obj = TD( '<enter_your_login_id>', '<enter_your_password>', log_level= logging.WARNING)
symbols = ['CRUDEOIL-I', 'GOLD-I', 'SILVER-I']

# generating symbol_id for distinguishing which symbol it is for comparison etc....
symbol_ids = td_obj.get_req_id_list(2000, len(symbols))

is_market_open = True
data = {}

# fetching historical data for strategy calculation ,
for symbol_id, symbol in zip(symbol_ids, symbols):
    print(f"Requesting historical data for {symbol}")
    symbol_hist_data = td_obj.get_historic_data(symbol, duration='1 D', bar_size='tick')
    data[symbol_id] = list(map(lambda x: x['ltp'], symbol_hist_data))[-100:]

# live data initilizing for required symbols , passing symbol_id that generated
symbol_ids = td_obj.start_live_data(symbols, req_id=symbol_ids)
time.sleep(1)

# bidask_callback callback function , strategy is logic is inside call back function
@td_obj.bidask_callback
def new_bidask(symbol_id, tick_data):
        data[symbol_id] = data[symbol_id][1:] + [td_obj.live_data[symbol_id].ltp]
        if sum(data[symbol_id][-50:]) / 50 > sum(data[symbol_id]) / 100:
            print(f'{td_obj.live_data[symbol_id].symbol} - SEND OMS LONG SIGNAL {sum(data[symbol_id][-50:]) / 50:.2f} > {sum(data[symbol_id]) / 100:.2f}, '
                  f'ltp = {td_obj.live_data[symbol_id].ltp:.2f}')
        else:
            print(f'{td_obj.live_data[symbol_id].symbol} - SEND OMS SHORT SIGNAL {sum(data[symbol_id][-50:]) / 50:.2f} < {sum(data[symbol_id]) / 100:.2f}, '
                  f'ltp = {td_obj.live_data[symbol_id].ltp:.2f}')

# keeping the while loop to keep the program running
while is_market_open:
    time.sleep(10)

# Graceful exit
td_obj.clear_bidask_callback()
td_obj.stop_live_data(symbols)
td_obj.disconnect()

```
### Strategy 2
```python
from truedata_ws.websocket.TD import TD
import time

td_obj = TD('<enter_your_login_id>', '<enter_your_password>')
symbols = ['CRUDEOIL-I', 'GOLD-I', 'SILVER-I']
symbol_ids = td_obj.get_req_id_list(2000, len(symbols))
is_market_open = True

data = {}

for sym_id, symbol in zip(symbol_ids, symbols):
    print(f"Requesting historical data for {symbol}")
    symbol_hist_data = td_obj.get_historic_data(symbol, duration='1 D', bar_size='tick')
    data[sym_id] = list(map(lambda x: x['ltp'], symbol_hist_data))[-100:]

td_obj.start_live_data(symbols, req_id=symbol_ids)


@td_obj.trade_callback
def strategy_callback(symbol_id, tick_data):
    data[symbol_id] = data[symbol_id][1:] + [tick_data.ltp]
    if sum(data[symbol_id][-50:]) / 50 > sum(data[symbol_id]) / 100:
        print(f'{tick_data.symbol} - SEND OMS LONG SIGNAL {sum(data[symbol_id][-50:]) / 50:.2f} > {sum(data[symbol_id]) / 100:.2f}, '
              f'ltp = {tick_data.ltp:.2f}')
    else:
        print(f'{tick_data.symbol} - SEND OMS SHORT SIGNAL {sum(data[symbol_id][-50:]) / 50:.2f} < {sum(data[symbol_id]) / 100:.2f}, '
              f'ltp = {tick_data.ltp:.2f}')


@td_obj.bidask_callback
def new_bidask(symbol_id, tick_data):
    print(f"Got a BIDASK update for {symbol_id} ({tick_data.symbol})")


while is_market_open:  # Remember to keep your main thread alive.
    time.sleep(120)

# Graceful exit
td_obj.clear_trade_callback()
td_obj.clear_bidask_callback()
td_obj.stop_live_data(symbols)
td_obj.disconnect()
```
### Strategy 3
```python
from truedata_ws.websocket.TD import TD
from copy import deepcopy
import time

td_obj = TD('<enter_your_login_id>', '<enter_your_password>')
symbols = ['CRUDEOIL-I', 'GOLD-I', 'SILVER-I']
symbol_ids = td_obj.get_req_id_list(2000, len(symbols))
is_market_open = True

data = {}
live_data_objs = {}

for sym_id, symbol in zip(symbol_ids, symbols):
    print(f"Requesting historical data for {symbol}")
    symbol_hist_data = td_obj.get_historic_data(symbol, duration='1 D', bar_size='1 min')
    data[sym_id] = list(map(lambda x: x['c'], symbol_hist_data))[-100:]

td_obj.start_live_data(symbols, req_id=symbol_ids)

time.sleep(1)
for sym_id in symbol_ids:
    live_data_objs[sym_id] = deepcopy(td_obj.live_data[sym_id])


@td_obj.bar_callback
def strategy_callback(symbol_id, min_data):
    data[symbol_id] = data[symbol_id][1:] + [min_data.close]
    if sum(data[symbol_id][-50:]) / 50 > sum(data[symbol_id]) / 100:
        print(f'{min_data.symbol} - SEND OMS LONG SIGNAL {sum(data[symbol_id][-50:]) / 50:.2f} > {sum(data[symbol_id]) / 100:.2f}, '
              f'ltp = {min_data.ltp:.2f}')
    else:
        print(f'{min_data.symbol} - SEND OMS SHORT SIGNAL {sum(data[symbol_id][-50:]) / 50:.2f} < {sum(data[symbol_id]) / 100:.2f}, '
              f'ltp = {min_data.ltp:.2f}')


while is_market_open:  # Remember to keep your main thread alive.
    time.sleep(120)

# Graceful exit
td_obj.clear_bar_callback()
td_obj.stop_live_data(symbols)
td_obj.disconnect()
```

### Strategy 4
```python
from truedata_ws.websocket.TD import TD
from copy import deepcopy
import time

td_obj = TD('<enter_your_login_id>', '<enter_your_password>')
symbols = ['CRUDEOIL-I', 'GOLD-I', 'SILVER-I']
symbol_ids = td_obj.get_req_id_list(2000, len(symbols))
is_market_open = True

data = {}
live_data_objs = {}

for symbol_id, symbol in zip(symbol_ids, symbols):
    print(f"Requesting historical data for {symbol}")
    symbol_hist_data = td_obj.get_historic_data(symbol, duration='1 D', bar_size='1 min')
    data[symbol_id] = list(map(lambda x: x['c'], symbol_hist_data))[-100:]

td_obj.start_live_data(symbols, req_id=symbol_ids)

time.sleep(1)
for symbol_id in symbol_ids:
    # If you are subscribed ONLY to min data, just USE live_data NOT min_live_data
    live_data_objs[symbol_id] = deepcopy(td_obj.min_live_data[symbol_id])

while is_market_open:
    time.sleep(0.1)  # Adding this reduces CPU overhead, since strategy not sensitive to tick timescale.
    for symbol_id in symbol_ids:
        # If you are subscribed ONLY to min data, just USE live_data NOT min_live_data
        if live_data_objs[symbol_id] != td_obj.min_live_data[symbol_id]:
            live_data_objs[symbol_id] = deepcopy(td_obj.min_live_data[symbol_id])
            # Here is where you can do your manipulation on the min data
            data[symbol_id] = data[symbol_id][1:] + [live_data_objs[symbol_id].close]
            if sum(data[symbol_id][-50:]) / 50 > sum(data[symbol_id]) / 100:
                print(f'{live_data_objs[symbol_id].symbol} - SEND OMS LONG SIGNAL {sum(data[symbol_id][-50:]) / 50:.2f} > {sum(data[symbol_id]) / 100:.2f}, '
                      f'ltp = {live_data_objs[symbol_id].close:.2f}')
            else:
                print(f'{live_data_objs[symbol_id].symbol} - SEND OMS SHORT SIGNAL {sum(data[symbol_id][-50:]) / 50:.2f} < {sum(data[symbol_id]) / 100:.2f}, '
                      f'ltp = {live_data_objs[symbol_id].close:.2f}')

# Graceful exit
td_obj.stop_live_data(symbols)
td_obj.disconnect()
```

## Differences between State Check and Callback strategies
 * In the context of this library, callbacks are meant to be light-weight. Primarily used for quick POCs and other speedy development. 
 * The callback execution happens on the websocket thread and will therefore be harder to divvy up computation across processing cores.

----    
# Complete Test Suite
**Running tests to ensure everything is in order** 
```shell script
python3.7 -m truedata_ws run_all_tests <enter_your_login_id> <enter_your_password>
```

**Test Suite - Historical & Real time data**

1) Please copy this code and paste > run it in your python environment.
2) You need to enter your login id & password to make this code works
3) This code first downloads Historical data in 9 different ways and also shows you the commands used to get that data 
4) The Historical data is then put into a pandas Dataframe also.
5) Please note that if the market is closed on the test day, you will get 'No Data Exists for <symbol>' returns for the current day's data tests.
6) Real time Live Data tests come towards the end and include printing of the touchline data followed by the live real time data stream.

```python
from truedata_ws.websocket.TD import TD
from copy import deepcopy
from time import sleep
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from colorama import Style, Fore

username = '<enter_your_username>'
password = '<enter_your_password>'

symbols = ['NIFTY-I', 'RELIANCE', 'BANKNIFTY-I']

# ------- In this sample, we use the first of the above given symbols for historical data
symbol = symbols[0]
test_time = datetime.today()

#  Creating our object
td_obj = TD(username, password, live_port=8082)

print('Please wait.. Beginning Historical Data Test !')

# ------- Beginning historical data test...
hist_data_1 = td_obj.get_historic_data(f'{symbol}')
hist_data_2 = td_obj.get_historic_data(f'{symbol}', duration='3 D')
hist_data_3 = td_obj.get_historic_data(f'{symbol}', duration='3 D', bar_size='15 mins')
hist_data_4 = td_obj.get_historic_data(f'{symbol}', bar_size='30 mins')
hist_data_5 = td_obj.get_historic_data(f'{symbol}', bar_size='30 mins', start_time=test_time - relativedelta(days=3))
hist_data_6 = td_obj.get_historic_data(f'{symbol}', bar_size='EOD', duration='1 M')

# Testing tick historical data
tick_hist_data_1 = td_obj.get_historic_data(f'{symbol}', bar_size='tick')
tick_hist_data_2 = td_obj.get_historic_data(f'{symbol}', bar_size='tick', duration='3 D')
tick_hist_data_3 = td_obj.get_historic_data(f'{symbol}', bar_size='tick', start_time=test_time - relativedelta(days=3))

# Printing out the results
print(f'{Style.BRIGHT}{Fore.BLUE}------------- HIST BAR DATA TEST RESULTS -------------{Style.RESET_ALL}')
print()
print(f"{Style.BRIGHT}{Fore.BLUE}HISTDATA 1...\n"
      f"\tCommand used -> hist_data_1 = td_obj.get_historic_data('{symbol}')\n"
      f"\tLENGTH OF RESULT = {len(hist_data_1)}{Style.RESET_ALL}")

for hist_point in hist_data_1[-20:]:
    print(hist_point)
print()
print(f"{Style.BRIGHT}{Fore.BLUE}HISTDATA 2...\n"
      f"\tCommand used -> hist_data_2 = td_obj.get_historic_data('{symbol}', duration='3 D')\n"
      f"\tLENGTH OF RESULT = {len(hist_data_2)}{Style.RESET_ALL}")

for hist_point in hist_data_2[-20:]:
    print(hist_point)
print()
print(f"{Style.BRIGHT}{Fore.BLUE}HISTDATA 3...\n"
      f"\tCommand used -> hist_data_3 = td_obj.get_historic_data('{symbol}', duration='3 D', bar_size='15 mins')\n"
      f"\tLENGTH OF RESULT = {len(hist_data_3)}{Style.RESET_ALL}")

for hist_point in hist_data_3[-20:]:
    print(hist_point)
print()
print(f"{Style.BRIGHT}{Fore.BLUE}HISTDATA 4...\n"
      f"\tCommand used -> hist_data_4 = td_obj.get_historic_data('{symbol}', bar_size='30 mins')\n"
      f"\tLENGTH OF RESULT = {len(hist_data_4)}{Style.RESET_ALL}")

for hist_point in hist_data_4[-20:]:
    print(hist_point)
print()
print(f"{Style.BRIGHT}{Fore.BLUE}HISTDATA 5...\n"
      f"\tCommand used -> hist_data_5 = td_obj.get_historic_data('{symbol}', bar_size='30 mins', start_time=datetime({(test_time - relativedelta(days=3)).strftime('%Y, %m, %d, %H, %M, %S').replace(' 0', ' ')}))\n"
      f"\tLENGTH OF RESULT = {len(hist_data_5)}{Style.RESET_ALL}")

for hist_point in hist_data_5[-20:]:
    print(hist_point)
print()
print(f"{Style.BRIGHT}{Fore.BLUE}HISTDATA 6...\n"
      f"\tCommand used -> hist_data_6 = td_obj.get_historic_data(f'{symbol}', bar_size='EOD', duration='1 M'))\n"
      f"\tLENGTH OF RESULT = {len(hist_data_6)}{Style.RESET_ALL}")

for hist_point in hist_data_6[-20:]:
    print(hist_point)
print()
print()
print(f'{Style.BRIGHT}{Fore.BLUE}------------- HIST TICK DATA TEST RESULTS -------------{Style.RESET_ALL}')
print()
print(f"{Style.BRIGHT}{Fore.BLUE}TICKDATA 1...\n"
      f"\tCommand used -> tick_data_1 = td_obj.get_historic_data('{symbol}', bar_size='tick')\n"
      f"\tLENGTH OF RESULT = {len(tick_hist_data_1)}{Style.RESET_ALL}")

for hist_point in tick_hist_data_1[-20:]:
    print(hist_point)
print()
print(f"{Style.BRIGHT}{Fore.BLUE}TICKDATA 2...\n"
      f"\tCommand used -> tick_data_2 = td_obj.get_historic_data('{symbol}', bar_size='tick', duration='3 D')\n"
      f"\tLENGTH OF RESULT = {len(tick_hist_data_2)}{Style.RESET_ALL}")

for hist_point in tick_hist_data_2[-20:]:
    print(hist_point)
print()
print(f"{Style.BRIGHT}{Fore.BLUE}TICKDATA 3...\n"
      f"\tCommand used -> tick_data_3 = td_obj.get_historic_data('{symbol}', bar_size='tick', start_time=datetime({(test_time - relativedelta(days=3)).strftime('%Y, %m, %d, %H, %M, %S').replace(' 0', ' ')}))\n"
      f"\tLENGTH OF RESULT = {len(tick_hist_data_3)}{Style.RESET_ALL}")

for hist_point in tick_hist_data_3[-20:]:
    print(hist_point)

# Testing conversion to pandas dataframe
print(f'{Style.BRIGHT}{Fore.BLUE}Converting HISTDATA 1 to a Pandas DataFrame{Style.RESET_ALL}')
print(f'Command used -> df = pd.DataFrame(hist_data_1)')
df = pd.DataFrame(hist_data_1)
print(df)

print(f'{Style.BRIGHT}{Fore.BLUE}Converting TICKDATA 1 to a Pandas DataFrame{Style.RESET_ALL}')
print(f'Command used -> df = pd.DataFrame(tick_hist_data_1)')
df = pd.DataFrame(tick_hist_data_1)
print(df)

# ------- Beginning live data test...
req_ids = td_obj.start_live_data(symbols)
sleep(3)  # This is here just to give the touchline data some time to populate... (Generally takes less than 1 sec)
print(f"{Style.BRIGHT}{Fore.BLUE}Here's the touchline data...{Style.RESET_ALL}")

for req_id in req_ids:
    print(td_obj.touchline_data[req_id])
print()
print(f"{Style.BRIGHT}{Fore.BLUE}Here's the LIVE stream... Stop code execution to exit...{Style.RESET_ALL}")
sleep(2)  # This is here just to give the user time to read the instructions...
live_data_objs = {}

for req_id in req_ids:    
    live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])
while True:
    try:
        for req_id in req_ids:
            if live_data_objs[req_id] != td_obj.live_data[req_id]:
                print(td_obj.live_data[req_id])
                live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])
    except KeyboardInterrupt:
        td_obj.stop_live_data(symbols)
        td_obj.disconnect()
        exit()

```

----
# Release Notes
Version 4.0.8
* Gainers Losers function included 
* Currency option chains added
* Bugfix: Automatic Reconnection due to Network Issue - Fixed

Version 4.0.7
* Option chains now include Previous OI, OI Change & Volume
* `market_close` parameter changed to `market_open_post_hours`. Default is False. Set to true when markets live post normal trading hours (eg. Mahurat Trading) 
* Bugfix - Python 32 bit - Float error handled.
* Bugfix - Removed the dict in case stoplivedata is called.

Version 4.0.6
* Option chains into pandas enabled > td_obj.start_option_chain(Symbol, Expiry_date, chain length, bid_ask)
* The option chain is enabled for tick and 1 min bar streaming
* The option chain also works post and pre market hours using the touchline data
* History - Call Specific Number of historical Bars (Tick, 1 min & EOD)
* Code cleaned

Version 4.0.1
* Breaking changes made to `td_obj.get_historic_data` -> ONLY if the `ticker_id` parameter is given, data can later be accessed at `td_obj.hist_data[ticker_id]`.
* If you are subscribed to tick+min streaming, you can access the min bar data at `td_obj.min_live_data[req_id]` in additional to your tick feed at `td_obj.live_data[req_id]`.
* Log Handler added + logging convenience parameters added + logging README section
* Examples added to repo.
* Examples + descriptions + differences updated in README.

Version 3.0.2
* Automatic streaming websocket reconnect enabled. 
* Automatic subscription of symbols & restart of live data after reconnect
* Now Avoiding server calls for repeated / duplicate streaming symbols...

Version 3.0.1
* Historical feed via Websocket - Deprecated
* Historical feed via REST - Added 
* More time frames have been added
* `get_bhavcopy` added
* Code cleaned up to improve dependancy handling (eg. for websocket-client)

Version 0.3.11
* Refactored `query_time` to `end_time` in `td_obj.get_historic_data()` function.
* Refactored `truedata_id` to `symbol_id` in `td_obj.touchline_data` objects.
* Filled missing values in `td_obj.live_data` objects upon initialization.
* Added better debugging information for error reporting.
* Cleaned up the code base.

### Stay Updated with the latest on this API
>Please make sure you follow us on our Telegram channel where we push a lot of information with regards to API updates, implementation ideas, tips & tricks to use this library & raw feed, etc...
* [TrueData Market Data API - Telegram Channel](https://t.me/truedata_ws_api)
* [TrueData Market Data APIs - Website](https://www.truedata.in/api)

### Sandbox Environment
>We have also built a sandbox environmemt for testing the raw feed. Please feel free to use this environment to check/test/compare your results with the raw data feed (real time & historical).
* [TrueData Market Data API - Sandbox Environment](https://wstest.truedata.in)

We are trying to improve this library continuously and feedback for the same is welcome.
