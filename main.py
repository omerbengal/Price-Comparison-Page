import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlparse, parse_qs
from fastapi import FastAPI, HTTPException
import re

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

        if not item_page_link:
            raise Exception("Item page link not found in first item")

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

        # put reponse text in html file
        with open('walmart.html', 'w') as file:
            file.write(response.text)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the element containing the URL of the first product
        # select a div which has the attribute "data-testid" and it's value is "item-stack"
        item_stack = soup.select('div[data-testid="item-stack"]')

        # Check if the element was found
        if not item_stack:
            raise Exception("No items found in Walmart search page")

        if len(item_stack) > 1:
            raise Exception("More than one item stacks found in Walmart search page")  # nopep8

        products = item_stack[0].find_all('div', class_='mb0 ph1 ph0-xl pt0-xl pb3-m bb b--near-white w-25')  # nopep8

        if products is None:
            raise Exception("No products found in Walmart search page")

        # go through each product and find the first product that is not a sponsered product
        for product in products:
            role_group_element = product.select_one('div[role="group"]')
            if role_group_element is not None:
                sponser = role_group_element.select_one('div[data-testid="list-view"] div div[class="mt5 mb0"] div')  # nopep8
                if sponser is None:
                    product_url = role_group_element.find('a')
                    if product_url is not None:
                        product_url = product_url.get('href')
                    break

        # parse the redirect URL and extract the direct URL from it
        parsed_url = urlparse(product_url)
        query_params = parse_qs(parsed_url.query)

        final_irl_if_not_redirect = 'https://www.walmart.com' + product_url

        # check if key 'rd' exists in the query params
        final_url = query_params['rd'][0] if query_params.keys() & {'rd'} else final_irl_if_not_redirect  # nopep8

        price_text = role_group_element.select_one('div[data-testid="list-view"] div[data-automation-id="product-price"] div').text  # nopep8
        if not price_text:
            raise Exception("Item price not found in Walmart search page")

        numbers_and_dots = re.findall(r'[0-9.]+', price_text)
        price = ''.join(numbers_and_dots)

        # Insert a dot before the last two digits
        price = price[:-2] + '.' + price[-2:]
        price = float(price)
        # format the price to 2 decimal places
        # price = "{:.2f}".format(price)
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

        items = soup.find_all('div', class_='item-container')  # nopep8

        # Check if the div was not found
        if not items:
            raise Exception("No items found in Newegg search page")

        final_url = ''
        # Find the first item that has a price (and is not an add)
        for item in items:
            item_action_div = item.find('div', class_='item-action')
            if item_action_div is not None:
                prive_div = item_action_div.find('ul', class_='price')
                if prive_div is not None:
                    price_current_li = prive_div.find(
                        'li', class_='price-current')
                    if price_current_li is not None:
                        strong = price_current_li.find('strong')
                        if strong is not None:
                            # Extract the href attribute
                            final_url = item.find(
                                'a', class_='item-img').get('href')
                            break

        if not final_url:
            raise Exception("Item page link not found in first item")

        response = get_response(final_url)

        # check if response is valid
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find the element containing the price of the first product
            row_side_div = soup.find('div', class_='row-side')

            if row_side_div is None:
                raise Exception("Item price not found in Newegg product page")

            price = row_side_div.find('li', class_='price-current')

            if not price:
                raise Exception("Item price not found in Newegg product page")

            dollar_price = price.find('strong').text
            cents_price = price.find('sup').text

            if not dollar_price or not cents_price:
                raise Exception("Item price not found in Newegg product page")

            price = dollar_price + '' + cents_price
            price = price.replace(',', '')
            price = float(price)
            # price = "{:.2f}".format(price)

            return {"Site": "Newegg", "Item title name": final_url, "Price(USD)": price}  # nopep8
        else:
            raise Exception("Invalid Newegg product page response")
    else:
        raise Exception("Invalid Newegg search page response")


# FastAPI
app = FastAPI()


@app.get("/prices")
def get_sites_data(item: str):
    try:
        best_buy_price = get_best_buy_price(item)
        walmart_price = get_walmart_price(item)
        newegg_price = get_newegg_price(item)
        return {"Best Buy": best_buy_price, "Walmart": walmart_price, "Newegg": newegg_price}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Main
if __name__ == "__main__":
    pass
