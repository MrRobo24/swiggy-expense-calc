import requests
import pandas as pd
from datetime import datetime
import time
import os

def get_swiggy_orders(order_id: str = ""):
  url = "https://www.swiggy.com/dapi/order/all?order_id=" + order_id

  cookiesValue = ""
  with open('cookies', 'r') as cookiesFile:
    cookiesValue = cookiesFile.read()

  if (cookiesValue == ""):
    print('missing some cookies')
    exit(1)
    
  payload={}
  headers = {
    '__fetch_req__': 'true',
    'accept': '*/*',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'cookie': cookiesValue,
    'if-none-match': 'W/"235cb-dIjl6JiUo+ZiNS3Ve213//T/peY"',
    'priority': 'u=1, i',
    'referer': 'https://www.swiggy.com/my-account',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
  }
  result = {}
  try:
    response = requests.request("GET", url, headers=headers, data=payload)
    
    if (response.status_code != 200):
      print('swiggy error:', response.text)
    else:
      result = response.json()['data']['orders']
  except Exception as e:
    print('swiggy exception:', e)
  finally:
    return result

def get_all_swiggy_orders(max_iters = 100):
  last_order_id = ''
  all_orders = []
  for i in range(max_iters):
    curr_orders = get_swiggy_orders(last_order_id)
    last_order_id = ''
    n = len(curr_orders)
    if n > 0:
      all_orders.extend(curr_orders)
      last_order_id = str(curr_orders[-1]['order_id'])
      print('ITERATION :', i , 'LAST_ORDER_ID :', last_order_id)
    if last_order_id == '':
      break
    time.sleep(1)
  
  return all_orders
  
def custom_agg(x):
  d = {}
  d['order_total'] = x['order_total'].sum()
  d['order_avg_val'] = x['order_total'].mean()
  d['order_count'] = x['order_total'].count()
  
  return pd.Series(d, index=['order_total', 'order_avg_val', 'order_count'])

def anaylise_all_orders(all_orders):
  if (len(all_orders) == 0):
    print('no order found')
    return
  
  imp_cols = ['order_id', 'order_total', 'restaurant_id', 'restaurant_name', 'restaurant_city_name', 'payment_method', 'order_delivery_status', 'delivery_time_in_seconds', 'ordered_time_in_seconds', 'order_items']
  df = pd.json_normalize(all_orders)[imp_cols]
  df = df[df['order_delivery_status'] == 'delivered']  
  df['order_time_datetime'] = df.ordered_time_in_seconds.apply(lambda x: datetime.fromtimestamp(x))
  df['order_day'] = df.order_time_datetime.apply(lambda x: x.day)
  df['order_month'] = df.order_time_datetime.apply(lambda x: x.month)
  df['order_year'] = df.order_time_datetime.apply(lambda x: x.year)

  grouped_by_rest = df.groupby(['restaurant_name']).apply(custom_agg, include_groups=False).sort_values('order_total', ascending=False)
  # grouped_by_month_year = df.groupby(['order_month', 'order_year']).apply(custom_agg, include_groups=False).sort_values('order_year')

  grouped_by_rest.to_csv('swiggy-expenses.csv')
  df.to_csv('all_data.csv')

if __name__ == '__main__':
  ENV = os.getenv('ENV', 'sandbox')
  MAX_ITER = 100 if ENV == 'production' else 1
  
  anaylise_all_orders(get_all_swiggy_orders(MAX_ITER))