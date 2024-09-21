import requests
from bs4 import BeautifulSoup

# Define headers if needed
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

# Send request
response = requests.get("https://www.weather.gov.hk/wxinfo/pastwx/metob202408c.htm", headers=headers)
html = response.text
soup = BeautifulSoup(html, "html.parser")# use the html parser in beautifulsoup

# Find all humidity data
all_humidities = soup.findAll("td", attrs={"headers": "rh d32"})
print("\nhumidity Data:")
for humidity in all_humidities:
    print(humidity.string)

# Find all cloudage data
all_cloudage = soup.findAll("td", attrs={"headers": "ca d32"})
print("\nCloudage Data:")
for cloud in all_cloudage:
    print(cloud.string)