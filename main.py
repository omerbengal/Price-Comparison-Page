import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    'User-Agent': 'Mozilla/5.0 \
                (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 \
                (KHTML, like Gecko) \
                Chrome/123.0.0.0 Safari/537.36'
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
    url = ''
    response = get_response(url)
    # check if response is valid
    if response.status_code == 200:
        return {}
    else:
        return {'error': 'Invalid response'}


def get_newegg_price(item: str) -> dict:
    url = 'https://www.newegg.com/p/pl?d=' + quote_plus(item)
    response = get_response(url)

    # check if response is valid
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the first div with class "item-container"
        first_item_container_div = soup.find('div', class_='item-container')

        # Check if the div was found
        if first_item_container_div:
            # Find the first <a> element inside the div
            first_a_inside_div = first_item_container_div.find('a')

            # Check if the <a> element was found
            if first_a_inside_div:
                # Extract the href attribute
                final_url = first_a_inside_div.get('href')
            else:
                print(
                    "No <a> element found inside the first div with class 'item-container'.")
        else:
            print("No div found with class 'item-container'.")

        response = get_response(final_url)

        # check if response is valid
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find the element containing the price of the first product
            price = soup.find('li', class_='price-current')

            if not price:
                raise Exception("Item price not found in Newegg product page")

            dollar_price = price.find('strong').text
            cents_price = price.find('sup').text

            if not dollar_price or not cents_price:
                raise Exception("Item price not found in Newegg product page")

            price = dollar_price + '' + cents_price
            price = price.replace(',', '')
            price = float(price)
            price = "{:.2f}".format(price)
            print(price)

            return {"Site": "Newegg", "Item title name": final_url, "Price(USD)": price}  # nopep8
        else:
            raise Exception("Invalid Newegg product page response")
    else:
        raise Exception("Invalid Walmart search page response")


# Main
if __name__ == "__main__":
    pass
