import requests
from bs4 import BeautifulSoup
import time

URL = 'https://www.dns-shop.kz'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

r = requests.get(URL + '/catalog/', verify=False, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

parent_categories = [
    (
        i.find('a', class_='subcategory__childs-item')['href'],
        i.find('a', class_='subcategory__childs-item')
    ) 
    for i 
    in soup.find_all('ul', class_='subcategory__childs-list')
    ]

def get_nested_category(URL):
    r = requests.get(
        URL, 
        verify=False, 
        headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    subcategories = [
        (i['href'], i.find('span', class_='subcategory__title')) 
        for i in 
        soup.find_all('a', class_='subcategory__item')]

    return subcategories

def get_all_categories(categories, URL, category_names):
    for category_link, category_name in categories:
        subcategories = get_nested_category(URL + category_link)
        category_names.append(category_name.text)
        if subcategories:
            get_all_categories(subcategories, URL, category_names)
        else:
            # open prod_list
            i = 1
            while True:
                r = requests.get(
                    URL + category_link + f'?p={i}', 
                    verify=False, 
                    headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                products = soup.find_all('div', class_='catalog-product')
                if products:
                    for product in products:
                        # selenium here

                        # price = product.find('div', class_='product-buy product-buy_one-line catalog-product__buy')
                        name_tab = product.find('a', class_='catalog-product__name')
                        name = name_tab.text
                        link = name_tab['href']
                        print(name, link)
                        print(category_names)
                    i += 1
                else:
                    break

category_names = []
print(get_all_categories(parent_categories[:1], URL, category_names))
