import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# headers to mimic a request from a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# create a csv file to store the data
with open("amazon_products.csv", mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        ["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"]
    )

    # loop through the pages to scrape
    for i in range(1, 21):
        page_url = f"{url}&page={i}"
        response = requests.get(page_url, headers=headers)

        # parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # find all the product listings on the page
        products = soup.find_all("div", {"data-component-type": "s-search-result"})

        # extract the required information from each product listing and write it to the csv file
        for product in products:
            product_url = product.find("a", {"class": "a-link-normal s-no-outline"})[
                "href"
            ]
            product_name = product.find(
                "span", {"class": "a-size-medium a-color-base a-text-normal"}
            ).text.strip()
            product_price = product.find(
                "span", {"class": "a-price-whole"}
            ).text.strip()
            rating = (
                product.find("span", {"class": "a-icon-alt"}).text.strip().split()[0]
            )
            num_reviews = (
                product.find("span", {"class": "a-size-base"}).text.strip().split()[0]
            )

            writer.writerow(
                [product_url, product_name, product_price, rating, num_reviews]
            )
