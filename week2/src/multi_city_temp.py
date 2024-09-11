import dotenv
import os
from scraping_utils import get_url, parse
dotenv.load_dotenv()

url = os.getenv('URL');

for i in range(1, 10):
    city_url = url.format(city_id=i)
    print(city_url)
    page = get_url(city_url, f'city-{i}.json')
    tree = parse(page, 'json')    
    city = tree['city']['cityName']
    print(city)

    


