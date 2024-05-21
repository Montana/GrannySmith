import requests
from bs4 import BeautifulSoup

def fetch_prices_whole_foods(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    apple_elements = soup.find_all('div', class_='product-tile')
    prices = []
    for element in apple_elements:
        if 'Granny Smith' in element.text:
            price_text = element.find('span', class_='price').text
            price = float(price_text.replace('$', '').strip())
            prices.append(price)
    
    return prices

def fetch_prices_safeway(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    apple_elements = soup.find_all('div', class_='product')
    prices = []
    for element in apple_elements:
        if 'Granny Smith' in element.text:
            price_text = element.find('span', class_='product-price').text
            price = float(price_text.replace('$', '').strip())
            prices.append(price)
    
    return prices

def find_cheapest_apples():
    grocery_urls = {
        'Whole Foods': 'https://www.wholefoods.com/granny-smith-apples',
        'Safeway': 'https://www.safeway.com/granny-smith-apples'
    }
    
    all_prices = []
    
    for store, url in grocery_urls.items():
        try:
            if store == 'Whole Foods':
                prices = fetch_prices_whole_foods(url)
            elif store == 'Safeway':
                prices = fetch_prices_safeway(url)
            all_prices.extend(prices)
        except requests.RequestException as e:
            print(f"Error fetching prices from {store}: {e}")
    
    if all_prices:
        cheapest_price = min(all_prices)
        print(f"The cheapest Granny Smith apples are ${cheapest_price:.2f} per unit.")
    else:
        print("Couldn't fetch prices from any grocery stores.")

if __name__ == "__main__":
    find_cheapest_apples()
