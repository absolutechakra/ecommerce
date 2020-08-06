import requests
import time
import calendar


# Define attributes
stock_symbol = 'AMD'
api_key = 'BSSLD481RTQSRQYNFD9PXBNUMTMYWQAH'
price_history = 'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format(stock_symbol)
quote_url = 'https://api.tdameritrade.com/v1/marketdata/{}/quotes'.format(stock_symbol)
number_of_days = 5
# current_time = calendar.timegm(time.gmtime())
current_time = '1595905820000'
five_day_time = '1595625820000'

# Stack for storing EMA
class Stack:
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()
    
    def top(self):
        return self.items[self.size() - 1]
    
    def size(self):
        return len(self.items)
    
    def is_empty(self):
        return self.items == []


payload = {
    'apikey': api_key,
    'periodType': 'month',
    'frequencyType': 'daily',
    'endDate': current_time,
    'startDate': five_day_time,
}

content = requests.get(url=price_history, params=payload)
print ('Two day price history :- ', content)
data = content.json().get('candles')

closing_price = []
print ('Stock AMD :-', data)
for i in data:
    closing_price.append(i.get('close'))

# Simple moving average
simple_moving_avg = float(sum(closing_price)/len(closing_price))

# Define an EMA
all_emas = Stack()

# Find Initial EMA
if all_emas.is_empty():
    all_emas.push(simple_moving_avg)

# Calculate Smoothing Constant
weighting_multiplier = 2/(number_of_days + 1)
print ('Smoothing Constant :- ', weighting_multiplier)

# Calculate today's closing price
quote_payload = {
    'apikey': api_key
}

result = requests.get(url=quote_url, params=quote_payload)
data = result.json().get(stock_symbol)
todays_closing_price = data.get('closePrice')

# Top most value in the stack will be the previous day EMA
previous_day_ema = all_emas.top()
print ('Previous Day EMA :-', previous_day_ema)

# Calculate today's EMA
todays_ema = (todays_closing_price - previous_day_ema) * weighting_multiplier + previous_day_ema

# Add all the emas to one place
all_emas.push(todays_ema)

# Print EMA's as a list
print ('ALL EMAs :- ', all_emas.items)



