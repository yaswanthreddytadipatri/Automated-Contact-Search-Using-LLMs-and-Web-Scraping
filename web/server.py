from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import ollama
from urllib.parse import urljoin

app = Flask(__name__)

# Route for the form page
@app.route('/')
def index():
    return render_template('front.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    
    web_data = []

    def find_contact_pages(base_url):
        # Send a GET request to the base URL
        response = requests.get(base_url)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return []

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # List of possible contact page keywords
        contact_keywords = [
            'contact', 'get in touch', 'support', 'help', 'customer service', 'reach us',
            'contact us', 'support us', 'connect', 'talk to us', 'inquire', 'service',
            'customer care', 'contact center', 'customer support', 'feedback', 'contact form',
            'get support', 'contact information', 'contact page', 'service center'
        ]

        contact_page_urls = []
        for link in soup.find_all('a', href=True):
            link_href = link['href']
            # Convert relative URL to absolute URL
            full_url = urljoin(base_url, link_href)
            
            # Check if the URL contains any contact keyword and is a proper contact page URL
            if any(keyword in full_url.lower() for keyword in contact_keywords):
                if base_url in full_url:
                    contact_page_urls.append(full_url)

        return contact_page_urls

    def scrape_contact_page(url):
        # Send a GET request to the contact page URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve the contact page. Status code: {response.status_code}")
            return

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract and print all text content
        # print("Contact Page Content:")
        # print(soup.get_text(separator='\n', strip=True))
        web_data.append(soup.get_text(separator='\n', strip=True))
        # print("\n" + "="*50 + "\n")

    # Main URL (replace with the website you want to scrape)
    # main_url = 'https://vit.ac.in/'
    # main_url = input("Enter the URL: ")
    main_url = request.form['url']
    # Find and scrape contact pages
    contact_urls = find_contact_pages(main_url)
    if contact_urls:
        for contact_url in contact_urls:
            print(f"Scraping Contact Page: {contact_url}")
            scrape_contact_page(contact_url)
    else:
        print("No contact pages found.")

    # print(web_data)
    # ---------------------------------------------------------------------

    # LLM # ---------------------------------------------------------------------

    model_name = "llama3:8b"

    # problem = input("Enter the problem: ")
    problem = request.form['problem']

    # prompt = f"Give me the contact deatils based on the problem: {problem} by using the data: {website_text}. Make sure you give me only the Name, Designation, Contact number and email. IF any address then include"
    # prompt = f"Based on the problem described as '{problem}', extract the contact details of the person who should be contacted for resolution from the following text:\n\n{website_text}. Note: Make sure you give me only the Name, Designation, Contact number and email. IF any address then include"
    prompt = f"From the following data '{web_data} give me the best contact details that i can contact for the following problme '{problem}. Note: Make sure you give me only the Name, Designation, Contact number and email. IF any address then include.'"
    response = ollama.generate(model= model_name,prompt=prompt)

    # print(response['response'])




    # ---------------------------------------------------------------------
    # user_input = request.form['input']  # Get data from form
    # Process the input (e.g., modify it)
    processed_input = f"Modified: {response['response']}"
    # Render a different HTML template and pass the processed data
    return render_template('result.html', result=processed_input)

if __name__ == '__main__':
    app.run(debug=True)
