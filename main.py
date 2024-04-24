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
        first_product = soup.find_all(
            'a', class_='absolute w-100 h-100 z-1 hide-sibling-opacity')

        # Check if the element was found
        if first_product:
            # Extract the URL from the href attribute
            product_url = first_product[0]['href']
            # takes the string from the characters '/ip' including until the end of the string
            product_url = product_url[product_url.index('/ip'):]
        else:
            print("Couldn't find the URL of the first product.")

        name_url = 'https://www.walmart.com' + product_url
        print(name_url)
        response = get_response(name_url)

        # check if response is valid
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # # Find the element containing the price of the product
            # product_price = soup.find(
            #     'span', class_='inline-flex flex-column')

            # # Check if the element was found
            # if product_price:
            #     # Extract the name of the product
            #     price = product_price.text
            #     price_numbers = price.split('$')
            #     price = price_numbers[1]
            #     return price
            # else:
            #     print("Couldn't find the price of the product.")
            # Find the element containing the price of the product
            product_price = soup.find('span', itemprop='price')

            # Check if the element was found
            if product_price:
                print(product_price)
                # Extract the price of the product
                price = product_price.text.strip()
                return price
            else:
                print("Couldn't find the price of the product.")
    else:
        return {'error': 'Invalid response'}


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
    print(get_walmart_price('macbook'))
