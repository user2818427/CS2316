from pprint import pprint
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def song_search():
    soup = BeautifulSoup(open("SpotifyCharts.html"), "html.parser")
    ul =  soup.find_all("ul")
    country_list = []
    for country in ul[0]:
        if country != "\n":
            country_list.append(str(country))
    code_list = []
    for code in country_list[1:]:
        code_list.append(re.search("\"([a-z]{2})\"", code).group().strip("\""))

    PATH = "/usr/local/chromedriver"
    driver = webdriver.Chrome(PATH)
    country_dict = {}
    for country in code_list:
        try:
            driver.get("https://spotifycharts.com/regional/" + country + "/weekly/2022-01-28--2022-02-04")
            country_tab = driver.find_element_by_xpath("/html/body/div[@id='content']")
            data = country_tab.text.split("\n")
            country_dict[data[7]] = []
            for num in range(14,len(data[14:]) + 14,2):
                song_list = data[num].split(" by ")
                song = song_list[0]
                artist = " ".join(song_list[1].split()[:-1])
                country_dict[data[7]].append((song,artist))
        except:
            continue
    return country_dict

def genre_search():
    clientid = "21563db5e11c49dba4ac41693f516db5"
    secretid = "23efc8c8fed54796a78f316afd4b3496"
    client_credentials_manager = SpotifyClientCredentials(client_id=clientid, client_secret=secretid)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    country_dict = dict(song_search())

    countries = ['Argentina', 'Brazil', 'Colombia', 'Costa Rica','Ecuador', 'El Salvador', 'Guatemala', 'Honduras', 'India', 'Indonesia','Mexico', 'Paraguay', 'Peru','South Africa', 'Thailand', 'Uruguay', 'Viet Nam']
    countries2 = []
    for country in countries:
        countries2.append(country.upper())

    genres_list = []
    for key,value in country_dict.items():
        if key in countries2:
            genre_dict = {}
            genre_list = []
            for song_name,artist_name in value:
                try:
                    print('before search')
                    search = sp.search(artist_name)
                    print('after search')
                    track = search['tracks']['items'][0]
                    artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
                    genres = artist["genres"]
                    for genre in genres:
                        genre_list.append(genre)
                    print('after genre')
                except:
                    continue
            genre_dict[key] = list(set(genre_list))
            genres_list.append(genre_dict)
    return genres_list

pprint(genre_search())