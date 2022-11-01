from pprint import pprint
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

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
pprint(song_search())