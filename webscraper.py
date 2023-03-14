# https://realpython.com/beautiful-soup-web-scraper-python/
import requests
from bs4 import BeautifulSoup

# adresa webu odkud chceme získávat data
URL = 'https://svetserialu.to/zoznam-serialov'

# Odeslání požadavku metodou get na určenou URL adresu - HTTP server vrací zpět obsah stránky
page = requests.get(URL, headers={'User-agent': 'Mozilla/5.0'})
# Vytvoření objektu parseru stránky
soup = BeautifulSoup(page.content, 'html.parser')

# získání jména seriálu
show_name = soup.select('.original')
# získání jednoho žánru ze seriálu
show_genre = soup.select('.genres> span:first-child')
# získání roku seriálu
show_years = soup.select('div.years>span')
# získání hodnocení seriálu
show_ratings = soup.select('.ratings>.imdb>div')
# získání stanice seriálu
show_station = soup.select('.default>span')

titles = [tag.text for tag in show_name]
years = [int(tag.text[:4]) for tag in show_years]
ratings = [float(tag['data-progress']) for tag in show_ratings]
station = [tag.text.replace('- ', '') for tag in show_station]
genre = [tag.text for tag in show_genre]

# zapsání získaných dat do souboru series.json
with open("series.json", "w", encoding='utf-8') as file:
    file.write('[')
    for i in range(0, 35):
        row = f'"title": "{titles[i]}", "year": {years[i]}, "rating": {ratings[i]}, "station": "{station[i]}", "genre' \
              f'": "{genre[i]}" '
        row = '{' + row + '} ' if i == 34 else '{' + row + '}, \n'
        print(row)
        file.write(row)
    file.write(']')
