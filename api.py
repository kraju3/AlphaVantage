import dotenv
import time
from main import log,Database
import os
import asyncio
from alpha_vantage.async_support.timeseries import TimeSeries

dotenv.load_dotenv()

class Time_Series:
    def __init__(self,symbols,db):
        self.symbols = symbols
        self.results = 0
        self.db = db
    async def get_data(self,symbol):
        log.debug("Success on creating TimeSeries")
        ts = TimeSeries(os.environ['API_KEY'])
        log.debug("Querying alpha vantage for data for {}".format(symbol))
        data,meta = await ts.get_daily_adjusted(symbol=symbol,outputsize="compact")
        await ts.close()
        log.debug(meta)

        log.debug("Returned alpha vantage data for {}".format(symbol))
        return (data,meta)

    def wait_for(self):
        log.debug("Started event Loop")
        loop = asyncio.get_event_loop()
        tasks = [self.get_data(symbol) for symbol in self.symbols]
        group = asyncio.gather(*tasks)
        results = loop.run_until_complete(group)
        log.debug("Returned all the results")
        loop.close()
        log.debug("Asyncronous loop finished")
        self.results = results
        info=[]

        for result,meta in self.results:
            i=0
            stockName = meta ["2. Symbol"]
            tempResult = {}
            tempResult["name"] = stockName
            tempResult["date"] = {}
            for data in result:
                tempResult["date"][data] = {}
                for value in result[data]:
                    tempvalue = value.split(".")[1].strip()
                    tempResult["date"][data][tempvalue] = result[data][value]
                i+=1
                if i == 10:
                    info.append(tempResult)
                    break;



        self.db.insert(info,"fp","stocks")




database = Database(os.environ.get("MONGODB_HOST"),int(os.environ.get("MONGODB_PORT")))


ts = Time_Series(['AAPL', 'GOOG', 'TSLA', 'MSFT'],database)
ts.wait_for();

