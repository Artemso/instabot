import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import json
import random

TIMEOUT = 4

class Instabot():
	def __init__(self, email, password):
		self.options = webdriver.ChromeOptions()
		self.options.add_argument('--ignore-ssl-errors=yes')
		self.options.add_argument('--ignore-certificate-errors')
		self.driver = webdriver.Chrome('/Users/solopov/HIVE/python_scripts/python_instabot/chromedriver', options=self.options)
		self.driver.get('https://www.instagram.com/accounts/login/')
		self.email = email
		self.password = password
		time.sleep(TIMEOUT)
	
	def sign_in(self):
		email_input = self.driver.find_element_by_name('username')
		email_input.send_keys(self.email)
		pass_input = self.driver.find_element_by_name('password')
		pass_input.send_keys(self.password)
		pass_input.send_keys(Keys.RETURN)
		time.sleep(TIMEOUT * 2)
		notifications = self.driver.find_element_by_xpath("//button[contains(text(),'Not Now')]")
		notifications.click()
	
	def get_following(self, profile_url):
		self.driver.get(profile_url)
		time.sleep(TIMEOUT)
		dialog = self.driver.find_elements_by_css_selector('ul li a')[1]
		flwrs_str = self.driver.find_elements_by_css_selector('ul li a span')[1].text
		total_flwrs = int(flwrs_str.replace(',', ''))
		dialog.click()
		time.sleep(TIMEOUT)
		dialog = self.driver.find_element_by_css_selector('div[role="dialog"] ul')
		action_chain = webdriver.ActionChains(self.driver)
		curr_flwrs = 0
		while (curr_flwrs < total_flwrs - 10):
			ac = webdriver.ActionChains(self.driver)
			temp = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
			ac.move_to_element_with_offset(temp, 2, 2).click().perform()
			action_chain.key_down(Keys.SPACE).perform()
			curr_flwrs = len(dialog.find_elements_by_css_selector('li'))
			time.sleep(TIMEOUT / 2)
		links = []
		for elem in dialog.find_elements_by_css_selector('li'):
			userlink = elem.find_element_by_css_selector('a').get_attribute('href')
			links.append(userlink)
			if len(links) == total_flwrs:
				break
		usernames = []
		for elem in links:
			split = elem.split('/')[3]
			usernames.append(split)
		user_list = dict(zip(usernames, links))
		return (user_list)

	def get_followers(self, profile_url):
		self.driver.get(profile_url)
		time.sleep(TIMEOUT)
		dialog = self.driver.find_elements_by_css_selector('ul li a')[0]
		flwrs_str = self.driver.find_elements_by_css_selector('ul li a span')[0].text
		total_flwrs = int(flwrs_str)
		dialog.click()
		time.sleep(TIMEOUT)
		ac = webdriver.ActionChains(self.driver)
		curr_flwrs = 0
		while (curr_flwrs < total_flwrs):
			ac = webdriver.ActionChains(self.driver)
			temp = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
			ac.move_to_element_with_offset(temp, 2, 2).click().perform()
			ac.key_down(Keys.SPACE).perform()
			curr_flwrs = len(dialog.find_elements_by_css_selector('li'))
		links = []
		for elem in dialog.find_elements_by_css_selector('li'):
			userlink = elem.find_element_by_css_selector('a').get_attribute('href')
			links.append(userlink)
			if len(links) == total_flwrs:
				break
		usernames = []
		for elem in links:
			split = elem.split('/')[3]
			usernames.append(split)
		user_list = dict(zip(usernames, links))
		return (user_list)
		
	def	like_user(self, user_link, n_likes, chance):
		self.driver.get(user_link)
		time.sleep(TIMEOUT / 3)
		try:
			first_img = self.driver.find_element_by_css_selector('section main article a')
		except selenium.common.exceptions.NoSuchElementException:
			print('First image not found')
			return 0
		first_img.click()
		curr_likes = 0
		time.sleep(TIMEOUT)
		while (curr_likes != n_likes):
			try:
				like = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button')
			except selenium.common.exceptions.NoSuchElementException:
				print('Like button not found')
				break
			try:
				attr =  self.driver.find_element_by_css_selector('body article button svg')
				attribute = attr.get_attribute('aria-label')
				if attribute == 'Like' and self.get_rand(chance) == True:
					like.click()
					curr_likes += 1
			except selenium.common.exceptions.NoSuchElementException:
				print('Like image not found')
				break
			try:
				buttons = self.driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div/a')
				got_next = False
				for btn in buttons:
					if btn.text == 'Next':
						got_next = True
						btn.click()
						time.sleep(TIMEOUT)
				if got_next == False:
					break
			except selenium.common.exceptions.NoSuchElementException:
				print('Next button not found')
				break
		self.driver.get('https://www.instagram.com/')
	
	def	like_all_from_list(self, usr_list, n_likes):
		for key, value in usr_list.items():
			self.like_user(value, n_likes)

	def	open_json_to_list(self, filename):
		fd = open(filename, 'r')
		lst = fd.read()
		user_lst = json.loads(lst)
		return (user_lst)
	
	def	tags_to_list(self, filename):
		fd = open(filename, 'r')
		lst = fd.read()
		tags = lst.split(',')
		tags = [x.strip() for x in tags]
		return (tags)
	
	def get_rand(self, percent):
		x = random.randint(1, 100)
		if percent < 1 and percent > 100:
			percent = random.randint(1, 100)
		if x <= percent:
			return True
		else:
			return False
	
	def	open_profile(self):
		elem = self.driver.find_element_by_css_selector('a[style="width: 50px; height: 50px;"]')
		my_link = elem.get_attribute("href")
		return (my_link)
	
	def	like_tags_from_list(self, tag_list, n_likes, chance):
		for tag in tag_list:
			link = 'https://www.instagram.com/explore/tags/' + tag
			self.like_user(link, n_likes, chance)
	
	def	get_following_from_dict(self, user_dict):
		for name, link in user_dict.items():
			print('getting people of ' + name)
			curr_dict = self.get_following(link)
			print('got dict! len:' + str(len(curr_dict)))
			total_dict = {name: curr_dict}
			try:
				with open('user_dict.json','r+') as f:
					temp = json.load(f)
					temp.update(total_dict)
				with open('user_dict.json', 'w') as f:
					json.dump(temp, f, indent=4)
			except:
				with open('user_dict.json', 'w') as f:
					json.dump(total_dict, f, indent=4)

	def	user_dict_to_json(self, user_dict):
		with open('user_list.json', 'w') as fp:
					json.dump(user_dict, fp, sort_keys=True, indent=4)