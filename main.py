import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys
import json

class Currency_exchange():

    async def exchange(self, date):
        self.link = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
        async with aiohttp.ClientSession() as session:
            response = await session.get(self.link)
            result = await response.json()
            return result


async def main(value=5):
    if value > 10:
        print("Max value is 10")
        value = 10
    elif value < 1:
        print("Min value is 1")
        value = 1

    cur_exchange = Currency_exchange()

    date_lst = [
        (datetime.now().date() - timedelta(days=number_day)).strftime('%d.%m.%Y')
        for number_day in range(value)
    ]
    result = []

    for date in date_lst:
        data_PB = await (cur_exchange.exchange(date))
        res_dict = {}
        for data in data_PB['exchangeRate']:
            if data['currency'] == 'USD':
                res_dict.update({'USD': {'sale': data['saleRate'], 'purchase': data['purchaseRate']}})
            elif data['currency'] == 'EUR':
                res_dict.update({'EUR': {'sale': data['saleRate'], 'purchase': data['purchaseRate']}})
        result.append({date: res_dict})

    formatted_data = json.dumps(result, indent=4, ensure_ascii=False)
    print(formatted_data)


if __name__ == '__main__':
    try:
        val = sys.argv[1]
        asyncio.run(main(int(val)))

    except ValueError:
        print('Incorrect value')

    except:
        asyncio.run(main())

