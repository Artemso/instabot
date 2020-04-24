# python_instabot

# An elementary Selenium Instagram bot:

Requires Selenium package installed.

Features:
* signs in
* opens profile
* exports followers/following in json format
* can import dict of users and like them with probability
* can import lists of tags and like them with probability

* Usage example:
```
bot = Instabot("email@mail.com", "password")
bot.sign_in()
my_profile_url = bot.open_profile()
my_followers_dict = bot.get_followers(my_profile_url)
n_likes = 20 # number of likes to give to each follower
percent = 20 # a percent chance of putting a like under an image
bot.like_all_from_list(my_followers_dict, n_likes, percent)
```