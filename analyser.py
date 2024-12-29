import pandas as pd
from datetime import datetime

class Analyser:
  def __init__():
    pass
  
  def __custom_agg(x):
    d = {}
    d['order_total'] = x['order_total'].sum()
    d['order_avg_val'] = x['order_total'].mean()
    d['order_count'] = x['order_total'].count()
    
    return pd.Series(d, index=['order_total', 'order_avg_val', 'order_count'])

  @classmethod
  def anaylise_all_orders(cls, all_orders):
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

    grouped_by_rest = df.groupby(['restaurant_name']).apply(cls.__custom_agg, include_groups=False).sort_values('order_total', ascending=False)
    # grouped_by_month_year = df.groupby(['order_month', 'order_year']).apply(cls.__custom_agg, include_groups=False).sort_values('order_year')

    grouped_by_rest.to_csv('swiggy-expenses.csv')
    df.to_csv('all_data.csv')
    