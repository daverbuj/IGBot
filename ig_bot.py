from selenium import webdriver
import time, random #, sys, os
import json

class IGBot:
	def __init__(self):
		self.driver = webdriver.Chrome('chromedriver')
		self.base_url = 'https://www.instagram.com/'
		self.json_file = 'ig_bot.json'

		self.meta = self.read_json()
		self.username = self.meta['username']
		self.password = self.meta['password']
		self.login()

		self.exclusion = self.meta['exclusion']
		self.influencers = self.meta['influencers']
		self.following = self.meta['following']
		self.followers = self.meta['followers']
		self.followed = self.meta['followed']
		self.follow_rate = self.meta['follow rate']

	def login(self):
		self.driver.get('https://www.instagram.com/accounts/login/')
		time.sleep(1)
		username_box = self.driver.find_element_by_name("username")
		password_box = self.driver.find_element_by_name("password")
		login_button = self.driver.find_element_by_xpath("//div[contains(text(), 'Log In')]")
		username_box.send_keys(self.username)
		password_box.send_keys(self.password)
		time.sleep(1)
		login_button.click()
		time.sleep(3)
		self.go_home()
		time.sleep(2)
		try:
			notification_button = self.find_buttons('Not Now')[0]
			notification_button.click()
		except:
			self.go_home()
		time.sleep(1)

	def go_home(self):
		self.driver.get(self.base_url)

	def nav_user(self, user):
		user_url = "{}{}".format(self.base_url, user)
		self.driver.get(user_url)
		time.sleep(1)
		try:
			self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/article/div[1]/div/h2")
			public = False
		except:
			public = True
		return public

	def update_json(self):
		out_file_handle = open(self.json_file,'w')
		json.dump(self.meta, out_file_handle)
		out_file_handle.close()

	def add_influencer(self):
		influencer = input('Which influencer would you like to add?: ')
		if influencer in self.influencers:
			print('{} is already in your influencers list.'.format(influencer))
		else:
			self.influencers.append(influencer)
			self.update_json()
			print('{} has been added'.format(influencer))
		return

	def remove_influencer(self):
		influencer = input('Which influencer would you like to remove?: ')
		if influencer in self.influencers:
			self.influencers.remove(influencer)
			self.update_json()
			print('{} has been removed'.format(influencer))
			
		else:
			print('{} is not in your influencers list.'.format(influencer))
		return

	def add_exclude(self):
		excluder = input('Which excluder would you like to add?: ')
		if excluder in self.exclusion:
			print('{} is already in your exclusion list.'.format(excluder))
		else:
			self.exclusion.append(excluder)
			self.update_json()
			print('{} has been added'.format(excluder))
		return

	def remove_exclude(self):
		excluder = input('Which excluder would you like to remove?: ')
		if excluder in self.exclusion:
			self.exclusion.remove(excluder)
			self.update_json()
			print('{} has been removed'.format(excluder))
		else:
			print('{} is not in your exclusion list.'.format(excluder))
		return

	def read_json(self):
		# load metadata object from a json file
		with open(self.json_file) as json_fh:
			data = json.load(json_fh)
		return data

	def follow_user(self, user):
		follow_buttons = self.find_buttons('Follow')
		for btn in follow_buttons:
			btn.click()

	def unfollow_user(self, user):
		try:
			self.nav_user(user)
			unfollow_btn = self.find_buttons('Following')
			unfollow_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button/div')
			unfollow_btn.click()
			time.sleep(random.randint(1,4))
			unfollow2 = self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[1]')
			unfollow2.click()
			time.sleep(random.randint(1,4))
		except:
			print('Failed to unfollow. If you are not currently following this user, update the following list. Continuing...')
			return

	def like_posts(self, user, n_posts):
		imgs = []
		imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))
		for img in imgs[:n_posts]:
			img.click()
			time.sleep(1)
			like_buttons = self.driver.find_elements_by_class_name("_8-yf5 ")
			for button in like_buttons:
				try:
					button.click()
					time.sleep(3)
					break
				except:
					continue
			#x = self.find_buttons('Close')[0]
			#x = self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/button/svg')
			x = self.driver.find_elements_by_css_selector("[aria-label='Close']")[0]
			x.click()
			timer = random.randint(1,2)
			time.sleep(timer)

	def likers_list(self, influencer, num_follows):
		likers = set()
		# go to influencers page
		self.nav_user(influencer)
		# click on latest image on influencers page
		first_img = self.driver.find_elements_by_class_name('_9AhH0')[0]
		first_img.click()
		#print('clicked on first image')
		time.sleep(random.randint(2,5))
		# click on the "likes" button to open list of the people who liked the post
		try:
			try:
				likes_button = self.driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/article/div/div[2]/div/div[2]/section[2]/div/div[2]/a')
				#print('found likes button')
			except:
				print('Unable to find likes button')
			likes_button.click()
			time.sleep(random.randint(2,5))
			# scroll down adding likers to a list
			while len(likers) < num_follows+20:
				elements = self.driver.find_elements_by_xpath('//*[@id]/div/span/a') # elements are all of the users' web elements that fit in scroll box
				for user in elements:
					likers.add(user.get_attribute('title')) # get each users' web element name/tag/title
				# scroll down
				self.driver.execute_script("return arguments[0].scrollIntoView();", elements[-1])
				time.sleep(random.randint(1,3))
				#print(len(likers))
			self.go_home()
			#print('final', len(likers))
			return likers
		except:
			#print('error in likers_list()')
			return likers

	def interrogate_user(self, user):
		timer = random.randint(1,2)
		time.sleep(timer)
		if self.nav_user(user):
			time.sleep(random.randint(4,8))
			#print('found user')
			if self.find_buttons('Follow'):
				#print('found Follow button (not private)')
				info = self.driver.find_elements_by_class_name('g47SY')
				try:
					posts = int(info[0].text.replace(',',''))
					followers = int(info[1].get_attribute('title').replace(',',''))
					following = int(info[2].text.replace(',',''))
					#print(posts, followers, following)
					if (posts > random.randint(5,9)) and (followers < random.randint(2800,3000)) and (following < random.randint(1800,2000)) and (following > random.randint(30,60)):
						return True
					else:
						#print('bad user')
						return False
				except Exception as e:
					print(e)
					return False
		return False

	def follow_spree(self, n_follows):
		n_followed = 0
		while n_followed < n_follows:
			try:
				# pick an influencer at random
				random.shuffle(self.influencers)
				#print(self.influencers[0])
				# get list of users that have liked influencers picture
				targets = self.likers_list(self.influencers[0],n_follow)
				for user in targets:
					#print('next user')
					if n_followed < n_follows:
						if user in self.followed:
							#print('already following', user)
							continue # skip if already interrogated / followed
						self.followed.append(user)
						# determine if user is good to follow
						if self.interrogate_user(user):
							#print('user good')
							self.follow_user(user)
							print('Followed {}'.format(user))
							self.following.append(user)
							n_followed += 1
					else:
						print('Finished following {} users.'.format(n_follows))
						self.update_json()
						return
			except Exception as e:
				#sys.exc_info()
				print(e)
				# update followed list to json
				#print('updating json - bad')
				self.update_json()
				return

	def find_buttons(self, button_text):
		buttons = self.driver.find_elements_by_xpath("//*[text()='{}']".format(button_text))
		return buttons

	def update_following_list(self):
		self.nav_user(self.username)
		following_button = self.find_buttons(' following')[0]
		following_button.click()
		time.sleep(4)

		scrollbox = self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div[3]')
		last_height, curr_height= 0, 1
		while last_height!= curr_height:
			last_height = curr_height
			time.sleep(1)
			curr_height= self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight);
			return arguments[0].scrollHeight;
			""", scrollbox
			)
			time.sleep(1)

		following_links= scrollbox.find_elements_by_tag_name('a')
		following_names= [name.text for name in following_links]
		following_names= [x for x in following_names if x!='']
		
		self.following = following_names
		self.update_json()
		print('Finished updating list of users you are following. Total {} following.'.format(len(following_names)))

	def get_followers(self):
		self.nav_user(self.username)
		follower_button = self.find_buttons(' followers')[0]
		follower_button.click()
		time.sleep(4)

		scrollbox= self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]')
		last_height, curr_height= 0, 1
		while last_height!= curr_height:
			last_height= curr_height
			time.sleep(1)
			curr_height= self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight);
			return arguments[0].scrollHeight;
			""", scrollbox
			)
			time.sleep(1)

		follower_links= scrollbox.find_elements_by_tag_name('a')
		followers_names= [name.text for name in follower_links]
		followers_names= [x for x in followers_names if x!='']
		#print(followers_names)
		#print(len(followers_names))

		self.followers = followers_names
		self.update_json()

	def unfollow_spree(self, n_unfollow):
		n_unfollowed = 0
		before = len(self.followers)
		self.get_followers()
		after = len(self.followers) 
		print('Followers changed by {} since last time.'.format(after-before))
		print('after', len(self.followers))
		for following in self.following:
			if n_unfollowed < n_unfollow:
				if (following not in self.followers) and (following not in self.exclusion) and (following not in self.influencers):
					self.unfollow_user(following)
					print("Unfollowed {}".format(following))
					self.following.remove(following)
					n_unfollowed += 1
			else:
				self.update_json()
				print('Finished unfollowing {} users.'.format(n_unfollow))
				return

###############################################
# MAIN SCRIPT     MAIN SCRIPT     MAIN SCRIPT #   
###############################################

if __name__ == '__main__':
	try:
		Bot = IGBot()
		while True:
			choice = input("""
#######################################################################################
###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###
#######################################################################################

What would you like to do?

1. Navigate to Your Profile
2. Follow users
3. Unfollow users
4. Show influencer list (Add/Remove)
5. Show exclusion list (Add/Remove)
6. Update following list
7. Update username
8. Update password
0. Exit

Select number from menu above: """
				)


			if choice == '1':
				Bot.nav_user(Bot.username)

			if choice == '2':
				n_follow = int(input("How many people would you like to follow? (safe rate = 27): "))
				Bot.follow_spree(n_follow)

			if choice == '3':
				n_unfollow = int(input("How many people would you like to unfollow? (safe rate = 27): "))
				Bot.unfollow_spree(n_unfollow)

			if choice == '4':
				print("\n{}".format(Bot.influencers))
				next_choice = input('\nWould you like to (A)dd or (R)emove influencers? Or (N)either?: ')
				if next_choice.lower() == 'a':
					cont = 'y'
					while cont.lower() == 'y':
						Bot.add_influencer()
						cont = input('Would you like to add another? (y/n): ')
				if next_choice.lower() == 'r':
					cont = 'y'
					while cont.lower() == 'y':
						Bot.remove_influencer()
						cont = input('Would you like to remove another? (y/n): ')
				if next_choice.lower() == 'n':
					continue

			if choice == '5':
				print("\n{}".format(Bot.exclusion))
				next_choice = input('\nWould you like to (A)dd or (R)emove user from exclusion list? Or (N)o?: ')
				if next_choice.lower() == 'a':
					cont = 'y'
					while cont.lower() == 'y':
						Bot.add_exclude()
						cont = input('Would you like to add another? (y/n): ')
				if next_choice.lower() == 'r':
					cont = 'y'
					while cont.lower() == 'y':
						Bot.remove_exclude()
						cont = input('Would you like to remove another? (y/n): ')
				if next_choice.lower() == 'n':
					continue


			if choice == '6':
				Bot.update_following_list()

			if choice == '7':
				new_username = input('Enter new username: ')
				Bot.meta['username'] = new_username
				Bot.update_json()
				print('{} selected as new username.'.format(new_username))

			if choice == '8':
				new_pwd = input('Enter new password')
				Bot.meta['password'] = new_pwd
				Bot.update_json()
				print('Password has been updated.')

			if choice == '0':
				print("Exiting Now")
				try:
					obj.close_browser()
				except Exception:
					break
				break

			if choice == 'x':
				Bot.unfollow_user(input('user:'))

	except KeyboardInterrupt:
		Bot.update_json()
		print('\n\n**************** Process Interrupted by User ******************\n')
