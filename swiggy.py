import requests
import re
import json
from exception import CustomException

class SwiggyScrape:
  _session = None
  _csrf_token = None
  
  def __init__(self) -> None:
    if (SwiggyScrape._session != None):
      raise CustomException("SwiggyScrape is a Singleton class")
    
    SwiggyScrape._session = requests.Session()
    
  def check_session(self):
    if (SwiggyScrape._session == None):
      raise CustomException("SwiggyScrape session not initialised properly")
    
  def check_csrf(self):
    if (SwiggyScrape._csrf_token == None):
      raise CustomException("SwiggyScrape csrf token not set properly")
    
  def set_csrf_from_home(self):
    self.check_session()
    
    url = "https://www.swiggy.com/"
    payload={}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = SwiggyScrape._session.request("GET", url, headers=headers, data=payload)
    SwiggyScrape._csrf_token = re.search('csrf(.*);   window', response.text).group(1).split('"')[1]
    
  def sms_otp(self, mobile_number):
    self.check_session()
    self.check_csrf()
    
    url = "https://www.swiggy.com/dapi/auth/sms-otp"
    payload = json.dumps({
      "mobile": mobile_number,
      "_csrf": SwiggyScrape._csrf_token
    })
    headers = {
      '__fetch_req__': 'true',
      'accept': '*/*',
      'accept-language': 'en-IN,en;q=0.9',
      'content-type': 'application/json',
      'origin': 'https://www.swiggy.com',
      'priority': 'u=1, i',
      'referer': 'https://www.swiggy.com/',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    
    try:
      response = SwiggyScrape._session.request("POST", url, headers=headers, data=payload)
      if (response.status_code != 200):
        print('swiggy sms_otp error:', response.text)
        
      print("sms_otp:", response.text)
    except Exception as e:
      print('swiggy sms_otp exception:', e)
      
  def verify_otp(self, otp):
    self.check_session()
    self.check_csrf()
    
    url = "https://www.swiggy.com/dapi/auth/otp-verify"
    payload = json.dumps({
      "otp": otp,
      "_csrf": SwiggyScrape._csrf_token
    })
    
    headers = {
      '__fetch_req__': 'true',
      'accept': '*/*',
      'accept-language': 'en-IN,en;q=0.9',
      'content-type': 'application/json',
      'origin': 'https://www.swiggy.com',
      'priority': 'u=1, i',
      'referer': 'https://www.swiggy.com/',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    try:
      response = SwiggyScrape._session.request("POST", url, headers=headers, data=payload)
      if (response.status_code != 200):
        print('swiggy verify_otp error:', response.text)
        
      print("verify_otp:", response.json()['statusMessage'])
    except Exception as e:
      print('swiggy verify_otp exception:', e)
      
  def get_swiggy_orders(self, order_id: str = ""):
    url = "https://www.swiggy.com/dapi/order/all?order_id=" + order_id
    headers = {
      '__fetch_req__': 'true',
      'accept': '*/*',
      'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
      'content-type': 'application/json',
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
      response = SwiggyScrape._session.request("GET", url, headers=headers)
      if (response.status_code != 200):
        print('get_swiggy_orders error:', response.text)
      else:
        result = response.json()['data']['orders']
    except Exception as e:
      print('get_swiggy_orders exception:', e)
      print('get_swiggy_orders:', response.text)
    finally:
      return result