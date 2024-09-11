import requests
import dotenv
import os
from scraping_utils import get_url, parse_to_xml
dotenv.load_dotenv()

url = os.getenv('URL');

for i in range(0, 10):
    city_url = url.format(city_id=i)
    page = get_url(city_url, f'city-{i}.html')
    tree = parse_to_xml(page)
    city = tree.xpath('div[@class="col-10"]')
    print(city)

    


