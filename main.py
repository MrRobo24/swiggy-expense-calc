from scraper import Scraper
from analyser import Analyser

if __name__ == '__main__':
  scraper = Scraper()
  scraper.init_swiggy_scraper_env()
  all_orders = scraper.get_all_swiggy_orders()
  Analyser.anaylise_all_orders(all_orders)