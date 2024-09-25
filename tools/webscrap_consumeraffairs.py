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
        divs_reviews = soup.find_all("div", class_="rvw__dtls")

        # Extract review details
        for div_review in divs_reviews:
            review_date = div_review.find("p", class_="rvw__rvd-dt")
            review_date = review_date.text.strip() if review_date else ""

            text_review = div_review.find("div", class_="rvw__top-text")
            text_review = text_review.text.strip() if text_review else ""

            # Combine date and review text
            combined_review = f"{review_date}\n{text_review}"
            if combined_review:
                reviews.append({"manufacturer": "tesla", "url": url, "review": combined_review})

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
        "tesla": [
            "https://www.consumeraffairs.com/automotive/tesla_motors.html?page=1#scroll_to_reviews=true",
            "https://www.consumeraffairs.com/automotive/tesla_motors.html?page=2#scroll_to_reviews=true",
            "https://www.consumeraffairs.com/automotive/tesla_motors.html?page=3#scroll_to_reviews=true",
            "https://www.consumeraffairs.com/automotive/tesla_motors.html?page=4#scroll_to_reviews=true",
            "https://www.consumeraffairs.com/automotive/tesla_motors.html?page=5#scroll_to_reviews=true",
        ]
    }
    
    save_as = "consumeraffairs_tesla_reviews.csv"

    # Initialize Chrome driver
    driver = initialize_driver()

    # Scrape reviews
    all_reviews = scrape_reviews(driver, sources["tesla"])

    # Clean up
    driver.quit()

    # Save reviews to CSV
    save_reviews_to_csv(all_reviews, save_as)
