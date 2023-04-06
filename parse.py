import requests
from bs4 import BeautifulSoup

# Send a GET request to the webpage and retrieve the HTML response
url = "https://www.example.com/"
response = requests.get(url)
html = response.text

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Find all the HTML elements that have an href attribute or an onclick attribute
clickable_items = soup.find_all(lambda tag: tag.has_attr('href') or tag.has_attr('onclick'))

# Loop over the clickable items and print their attributes
for item in clickable_items:
    print(item.attrs)
