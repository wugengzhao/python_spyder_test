from bs4 import BeautifulSoup
import requests
import time
import random
from pymongo import MongoClient

base_url = 'http://www.allitebooks.com/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
all_it = requests.get(base_url, headers = headers)
# print(all_it.text)
soup = BeautifulSoup(all_it.text, 'lxml')
all_pages_str = soup.find('span', class_='pages').text
all_pages_int = int(all_pages_str.split('/')[1].split(' ')[1])
current_page = 1;

# database

client = MongoClient('localhost', 27017)
db = client['test']
collection = db['all_it_books']

total = collection.find().count()
current_page = int(total / 10) + 1;

# articles = soup.find_all('article')
# print(len(articles))

# print(all_pages_int)


def get_all_pages(current):
    for i in range(current, all_pages_int + 1):
        current_page = i
        print('current page=' + str(i))
        url = base_url + 'page/'+ str(i)
        try:
            html_content = requests.get(url, headers = headers).text
            soup = BeautifulSoup(html_content, 'lxml')
            articles = soup.find_all('article')
            for article in articles:
                book_titile = article.find(class_='entry-title').find('a')
                book_authors = article.find(class_='entry-author').find_all('a')
                save_book_info(book_titile, book_authors)
        except BaseException as ex:
            print("Exception occur")
            get_all_pages(current_page)
    time.sleep(random.randint(1, 3)) 

            

def save_book_info(book_titile, book_authors):
    book = {}
    i = 0
    book['title'] = book_titile.text
    
    #print(book_titile.text)
    for author in book_authors:
        i += 1
        book['author_' + str(i)] = author.text
    #   print(author.text)
    #print('----------------------------------------------------')
    collection.insert_one(book)


if __name__ == '__main__':
    get_all_pages(current_page)