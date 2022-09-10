import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class KdpBrowser:
	"""docstring for KdpBrowser"""
	def __init__(self, login, pw, headless=False):
		self.login = login
		self.password = pw
		self.headless = headless

	def __enter__(self):
		self.connect()

	def __exit__(self, ex_type, ex_val, ex_tb):
		self.close()

	def connect(self):
		chrome_options = Options()
		if self.headless:
			chrome_options.add_argument("--headless")
			#chrome_options.add_argument("--disable-extensions")
			# chrome_options.add_argument("--disable-gpu")
			#chrome_options.add_argument("--no-sandbox") # linux only
		
		self.driver = webdriver.Chrome(options=chrome_options)
		self.driver.get("https://kdp.amazon.com/fr_FR/bookshelf")
		login_field = WebDriverWait(self.driver, 10).until(
        	EC.presence_of_element_located((By.ID, "ap_email"))
    	)
		print(login_field)
		login_field.clear()
		login_field.send_keys(self.login)

		pw_field = self.driver.find_element(By.ID, "ap_password")
		pw_field.clear()
		pw_field.send_keys(self.password)
		pw_field.send_keys(Keys.RETURN)
		sleep(10)


	def close(self):
		self.driver.close()

# assert "Python" in driver.title
# assert "No results found." not in driver.page_source

if __name__ == '__main__':
	with KdpBrowser("gabibathie@gmail.com", sys.argv[1], False) as kb:
		pass