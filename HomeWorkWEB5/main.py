import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

class ExchangeRateService:
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close()

    async def fetch_exchange_rate(self, date):
        url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
        async with self.session.get(url) as response:
            return await response.json()

    async def get_exchange_rates(self, days):
        tasks = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
            tasks.append(self.fetch_exchange_rate(date))
        return await asyncio.gather(*tasks)

def parse_arguments():
    if len(sys.argv) != 2:
        print("Приклад: python main.py <кількість днів>")
        sys.exit(1)
    try:
        days = int(sys.argv[1])
        if days > 10:
            print("Error: Number of days should not exceed 10.")
            sys.exit(1)
        return days
    except ValueError:
        print("Error: Invalid input. Please enter a valid number of days.")
        sys.exit(1)

def format_exchange_rates(exchange_rates):
    formatted_rates = []
    for i, rate in enumerate(exchange_rates):
        date = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
        formatted_rate = {
            date: {'EUR': {'sale': rate['exchangeRate'][0]['saleRateNB'],'purchase': rate['exchangeRate'][0]['purchaseRateNB']},
                'USD': {'sale': rate['exchangeRate'][1]['saleRateNB'],'purchase': rate['exchangeRate'][1]['purchaseRateNB']}}}
        formatted_rates.append(formatted_rate)
    return formatted_rates

async def main():
    days = parse_arguments()
    async with ExchangeRateService() as exchange_rate_service:
        try:
            exchange_rates = await exchange_rate_service.get_exchange_rates(days)
            formatted_rates = format_exchange_rates(exchange_rates)
            print(formatted_rates)
        except Exception as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    asyncio.run(main())