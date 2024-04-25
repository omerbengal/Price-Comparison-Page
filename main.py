import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}


def get_response(url: str) -> requests.models.Response:
    return requests.get(url, headers=HEADERS)


def get_best_buy_price(item: str) -> dict:
    url = ''
    response = get_response(url)
    # check if response is valid
    if response.status_code == 200:
        return {}
    else:
        return {'error': 'Invalid response'}


def get_walmart_price(item: str) -> dict:
    url = 'https://www.walmart.com/search?q=' + quote_plus(item)
    response = get_response(url)

    # check if response is valid
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the element containing the URL of the first product
        products = soup.find_all(
            'a', class_='absolute w-100 h-100 z-1 hide-sibling-opacity')

        # Check if the element was found
        if not products:
            raise Exception("No items found in Walmart search page")

        first_product = products[0]
        # Extract the URL from the href attribute
        product_url = first_product['href']
        # takes the string from the characters '/ip' including until the end of the string
        product_url = product_url[product_url.index('/ip'):]

        final_url = 'https://www.walmart.com' + product_url
        # Find the element containing the price of the first product
        prices = soup.find_all(
            'div', class_='mr1 mr2-xl b black lh-copy f5 f4-l')

        if not prices:
            raise Exception("Item price not found in Walmart search page")

        first_price = prices[0]
        # Extract the price from the text
        price = first_price.text
        price = price.replace('$', '').strip()
        # Insert a dot before the last two digits
        price = price[:-2] + '.' + price[-2:]
        price = float(price)
        # format the price to 2 decimal places
        price = "{:.2f}".format(price)
        return {"Site": "Walmart", "Item title name": final_url, "Price(USD)": price}  # nopep8
    else:
        raise Exception("Invalid Walmart search page response")


def get_newegg_price(item: str) -> dict:
    url = ''
    response = get_response(url)
    # check if response is valid
    if response.status_code == 200:
        return {}
    else:
        return {'error': 'Invalid response'}


# Main
if __name__ == "__main__":
    pass
