import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}


def get_response(url: str) -> requests.models.Response:
    return requests.get(url, headers=HEADERS)


def get_best_buy_price(item: str) -> dict:
    str_item = quote_plus(item)
    url = f'https://www.bestbuy.com/site/searchpage.jsp?st={str_item}&intl=nosplash'  # nopep8
    response = get_response(url)
    # Check if response is valid
    if response.status_code == 200:
        # Get items
        best_buy_search_page_soup = BeautifulSoup(
            response.content, "html.parser")
        items = best_buy_search_page_soup.find_all('li', class_='sku-item')

        # Check if there are items
        if not items:
            raise Exception("No items found in Best Buy search page")

        # If we reach here - there is at least one item
        item = items[0]

        # Get item name
        item_name = item.find('h4', class_='sku-title').text

        # Get item page link: inside the h4 tag there is a <a> tag with the link
        item_page_link = item.find('h4', class_='sku-title').a['href']
        full_item_page_link = f'https://www.bestbuy.com{item_page_link}&intl=nosplash'  # nopep8

        # Get item page response
        item_page_response = get_response(full_item_page_link)
        # Check if response is valid
        if item_page_response.status_code == 200:
            # Get item price: class "priceView-hero-price priceView-customer-price"
            item_page_soup = BeautifulSoup(item_page_response.content, "html.parser")  # nopep8
            item_price = item_page_soup.find('div', class_='priceView-hero-price priceView-customer-price').span.text  # nopep8
            if not item_price:
                raise Exception("Item price not found in item page")

            # If we reach here - we have the item price
            # extract the price as a number from the string
            item_price = float(item_price.replace('$', '').replace(',', '').strip())  # nopep8
            return {"Site": "Best Buy", "Item title name": item_name, "Price(USD)": item_price, "Link": full_item_page_link}  # nopep8
        else:
            raise Exception("Invalid item page response")
    else:
        raise Exception("Invalid Best Buy search page response")


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
    get_walmart_price(
        'Sony XR85X93L 85" 4K Mini LED Smart Google TV with PS5 Features (2023)')
