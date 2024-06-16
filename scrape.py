import requests
from bs4 import BeautifulSoup
import json

# Base URL of the website
URL = "http://books.toscrape.com/"

# List of categories to scrape
CATEGORIES = ["Travel", "Mystery", "Historical Fiction"]

def extract_books(category_url):
    """
    Extracts book information from a given category URL.
    
    Args:
        category_url (str): The URL of the book category page.
    
    Returns:
        list: A list of dictionaries, each containing details of a book.
    """
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    books = []
    for book in soup.select('ol.row li'):
        title = book.h3.a['title']
        rating = book.p['class'][1]
        price = book.select_one('.price_color').text
        availability = book.select_one('.availability').text.strip()
        
        books.append({
            "title": title,
            "rating": rating,
            "price": price,
            "availability": availability
        })
    return books

def scrape_books():
    """
    Scrapes books from predefined categories on the website.
    
    Returns:
        list: A list of dictionaries, each containing the category type and its corresponding books.
    """
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    categories = []
    for category in soup.select('.side_categories ul li ul li a'):
        category_name = category.text.strip()
        if category_name in CATEGORIES:
            # Construct the category URL properly
            category_url = URL + category['href']
            books = extract_books(category_url)
            categories.append({
                "data": books,
                "type": category_name
            })
    return categories

if __name__ == "__main__":
    # Scrape the book data
    books_data = scrape_books()
    
    # Write the data to a JSON file
    with open('book_api.json', 'w') as json_file:
        json.dump(books_data, json_file, ensure_ascii=False, indent=4)
