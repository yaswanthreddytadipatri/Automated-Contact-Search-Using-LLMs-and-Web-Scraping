import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send a GET request to the website
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
        return None

# Example usage
url = 'https://vit.ac.in/contactus'
soup = scrape_website(url)
if soup:
    # Extract text from the website
    website_text = soup.get_text()
    print(website_text)
    # print(soup)


