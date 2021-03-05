from selenium.webdriver import Chrome
from bs4 import BeautifulSoup as bs
import pandas as pd
from sqlalchemy import create_engine

base_url = "https://books.toscrape.com/"
web_engine = Chrome()

# Data storage
titles_data = []
prices_data = []


# Title and price scrape
def infos_scrape():
    bs_obj = bs(web_engine.page_source, 'html.parser')
    boxes = bs_obj.find_all('div', {'class': 'image_container'})
    for box in boxes:
        titles_data.append(box.find('img').get('alt'))

    prices = bs_obj.find_all('p', {'class': 'price_color'})
    for price in prices:
        prices_data.append(price.text)


for page in range(1, 51):
    if page == 1:
        web_engine.get(base_url)
        infos_scrape()
    else:
        next_url = f'{base_url}catalogue/page-{page}.html'
        web_engine.get(next_url)
        infos_scrape()

# Creating Pandas DataFrame
teste = {'titles': titles_data, 'prices': prices_data}
df = pd.DataFrame(teste)

# Connection with sqlite database
engine = create_engine('sqlite:///book_scrape.db')
sqlite_connection = engine.connect()
sqlite_table = 'BookScraping'
df.to_sql(sqlite_table, sqlite_connection, if_exists='fail')
sqlite_connection.close()

web_engine.quit()
