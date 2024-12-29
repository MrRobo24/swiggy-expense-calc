import time
import os
from swiggy import SwiggyScrape
from exception import CustomException

class Scraper:
  _max_iters = None
  _swiggy = None
  
  def __init__(self) -> None:
    if (Scraper._swiggy != None):
      raise CustomException("Scraper is a Singleton class")
    
    Scraper._swiggy = SwiggyScrape()
    Scraper._max_iters = 100 if os.getenv('ENV', 'sandbox') == 'production' else 1

  def check_swiggy(self):
    if (Scraper._swiggy == None):
      raise CustomException("Scraper not initialised properly")
  
  def init_swiggy_scraper_env(self):
    self.check_swiggy()
    
    Scraper._swiggy.set_csrf_from_home()
    Scraper._swiggy.sms_otp(input('Enter Mobile Number for swiggy: '))
    Scraper._swiggy.verify_otp(input('Enter OTP from swiggy: '))

  def get_all_swiggy_orders(self):
    last_order_id = ''
    all_orders = []
    for i in range(Scraper._max_iters):
      curr_orders = Scraper._swiggy.get_swiggy_orders(last_order_id)
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