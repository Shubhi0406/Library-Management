from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from secrets import *

def fetch_book_webpg(book):
	path = PATH
	global driver
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(path, chrome_options=chrome_options)

	driver.get("https://www.goodreads.com")

	search = driver.find_element(By.ID, "sitesearch_field")
	search.send_keys(book)
	search.send_keys(Keys.RETURN)
	time.sleep(3)

	try:
		close_popup = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[1]/button")
		close_popup.click()
	except:
		pass
	finally:
		time.sleep(2)

	Book_title = driver.find_element(By.CLASS_NAME, "bookTitle")
	Book_title.click()
	time.sleep(3)

def show_summary():
	try:
		summary = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[3]/div")
	except:
		summary = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[1]/div[2]/div[1]/div[2]/div[4]/div/div[1]/div/div")
	a = summary.text.rstrip("...more")
	return a

def rating():
	try:
		rating = driver.find_element(By.CLASS_NAME, "RatingStatistics__rating")
	except:
		rating = driver.find_element(By.CLASS_NAME, "reviewControls--left")
	return str(rating.text)

def page_count():
	pg = driver.find_element(By.CLASS_NAME, "FeaturedDetails")
	pg = pg.text.split()[:2]
	return str(pg[0] + " pages")

def genres():
	g = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[1]/div[2]/div[1]/div[2]/div[5]")
	g = g.text.split()[1:]
	gen = ""
	for i in g:
		gen = gen + ", " + i
	gen = gen.lstrip(", ")
	gen = gen.rstrip(", ...more")
	return gen

def end_session():
	driver.quit()