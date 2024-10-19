import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Define headers if needed
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

# Send request
response = requests.get("https://www.weather.gov.hk/wxinfo/pastwx/metob202408c.htm", headers=headers)
html = response.text
soup = BeautifulSoup(html, "html.parser")  # Use the html parser in BeautifulSoup

# Find all humidity data
all_humidities = soup.findAll("td", attrs={"headers": "rh d32"})
humidities = [float(humidity.string.strip()) for humidity in all_humidities if humidity.string is not None]

# Find all cloudage data
all_cloudage = soup.findAll("td", attrs={"headers": "ca d32"})
cloudages = [float(cloud.string.strip()) for cloud in all_cloudage if cloud.string is not None]

# Exclude the last two data points
humidities = humidities[:-2]  # Exclude last two items
cloudages = cloudages[:-2]    # Exclude last two items

# Create a DataFrame to store the data for better visualization
data = pd.DataFrame({
    'Humidity': humidities,
    'Cloudage': cloudages
})

# Plot the data
plt.figure(figsize=(15, 5))

# Plot Humidity
plt.plot(data['Humidity'], label='Humidity', marker='p')

# Plot Cloudage
plt.plot(data['Cloudage'], label='Cloudage', marker='h')

# Adding title and labels
plt.title('Humidity and Cloudage Over the August2024')
plt.xlabel('August date')
plt.ylabel('Percentage')

#set x-axis and y-axis to have finer unit
x_values = np.arange(0, len(data),1)
y_values = np.arange(0, 99, 10)
plt.xticks(x_values)
plt.yticks(y_values)

# Show the legend
plt.legend()

# Display the plot
plt.show()
