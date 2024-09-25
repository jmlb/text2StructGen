import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def initialize_driver():
    """
    Initializes the Chrome WebDriver with necessary options.

    Returns:
        WebDriver: An instance of the Chrome WebDriver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver


def scrape_reviews(driver, urls):
    """
    Scrapes reviews from the given URLs.

    Args:
        driver (WebDriver): The initialized WebDriver instance.
        urls (list): A list of URLs to scrape.

    Returns:
        list: A list of dictionaries containing scraped review data.
    """
    reviews = []

    for url in tqdm(urls):
        print(f"Scraping URL: {url}")
        driver.get(url)
        
        # Wait for the page to load
        WebDriverWait(driver, 10)

        # Parse the page source
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Find all review containers
        divs_reviews = soup.find_all("section", class_="styles_reviewContentwrapper__zH_9M")

        # Extract review details
        for div_review in divs_reviews:
            div_rating = div_review.find('div', class_='styles_reviewHeader__iU9Px')
            try:
                rating_value = div_rating['rating']
            except:
                div_rating = ""
            div_review = div_review.find('div', class_='styles_reviewContent__0Q2Tg')
            text_review = div_review.text if div_review else ""

            if len(div_rating) + len(text_review) == 0:
                continue
            
            text = f"Rating: {rating_value}\n{text_review}"
            reviews.append({"manufacturer": manufacturer, "url": url, "review": text})
        # Sleep to prevent overwhelming the server
        time.sleep(10)

    return reviews


def save_reviews_to_csv(reviews, filename):
    """
    Saves the scraped reviews to a CSV file.

    Args:
        reviews (list): A list of dictionaries containing review data.
        filename (str): The filename for the CSV output.
    """
    df = pd.DataFrame(reviews)
    df.to_csv(filename, index=False)
    print(f"Reviews saved to {filename}")


if __name__ == "__main__":
    # Define source URLs
    sources = {
        "tesla": ["https://www.trustpilot.com/review/tesla.com?page=11",
                "https://www.trustpilot.com/review/tesla.com?page=12",
                "https://www.trustpilot.com/review/tesla.com?page=13",
                "https://www.trustpilot.com/review/tesla.com?page=14",
                "https://www.trustpilot.com/review/tesla.com?page=15",
                "https://www.trustpilot.com/review/tesla.com?page=16",
                "https://www.trustpilot.com/review/tesla.com?page=17",
                "https://www.trustpilot.com/review/tesla.com?page=18",
                "https://www.trustpilot.com/review/tesla.com?page=19",
                "https://www.trustpilot.com/review/tesla.com?page=20", 
                "https://www.trustpilot.com/review/tesla.com?page=21"]
            }
    
    save_as = "trustpilot_tesla_reviews.csv"

    # Initialize Chrome driver
    driver = initialize_driver()

    # Scrape reviews
    all_reviews = scrape_reviews(driver, sources["tesla"])

    # Clean up
    driver.quit()

    # Save reviews to CSV
    save_reviews_to_csv(all_reviews, save_as)