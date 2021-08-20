import glob
import os
from instabot import Bot
# from instaloader import Instaloader, Profile

# loader = Instaloader()
# USER = 'hackaton_test'
# PASSWORD = '456321Zx'
# loader.login(USER, PASSWORD)
# target_profile = 'alisa_belleza'
# profile = Profile.from_username(loader.context, target_profile)
# num_followers = profile.followers
# print(profile, num_followers)
# total_num_likes = 0
# total_num_comments = 0
# total_num_posts = 0
# # print(list(profile.get_tagged_posts()))
# for post in profile.get_posts():
#   print(post)
#   total_num_likes += post.likes
#   total_num_comments += post.comments
#   total_num_posts += 1
#   print(total_num_likes)
#   1/0

# engagement = float(total_num_likes + total_num_comments) / \
#   (num_followers * total_num_posts)
# print(engagement * 100)
# 1/0


cookie_del = glob.glob("config/*cookie.json")
os.remove(cookie_del[0])

bot = Bot(max_likes_to_like=1000000, min_likes_to_like=10)
# bot.login(username='sov89bur',  password='456321Zxcv!')

bot.login(username='hackaton_test',  password='456321Zx')
# username = 'ekaterina_in_'
# user_followers = bot.get_user_followers(username)
# print(len(user_followers))
# user_id = user_followers[1]
# username = bot.get_username_from_user_id(user_id)
# print(username)
# twony_last_medias = bot.get_user_medias(username, filtration = None)
# media_id = twony_last_medias[0]
# media_info = bot.get_media_info(media_id)[0]
# print(media_info)


accounts = {}
# twony_last_medias = bot.get_geotag_medias(214290799)
# print("twony_last_medias", len(twony_last_medias))
# for count, val in enumerate(twony_last_medias):
#   print(val['user']['username'], val['user']
#         ['full_name'], )
#   media_id = val['id']
#   # media_info = bot.get_media_info(media_id)[0]
#   # if media_info['caption']:
#   #   print(media_info['caption']['text'])


hastag = u'самара'
twony_last_medias = bot.get_total_hashtag_medias(hastag)
print("twony_last_medias", len(twony_last_medias))
# check_list = ['самара', 'travel']
# all_key = True
# check_list = ['самара', 'samara']
# all_key = False
# check_geo = ['самара']
# for count, user_id in enumerate(twony_last_medias):
#   print(bot.get_user_reel(user_id))
#   username = bot.get_username_from_user_id(user_id)
#   print(username)


#   media_id = val
#   media_info = bot.get_media_info(media_id)[0]
#   flag = False
#   if media_info['caption']:
#     for check in check_list:
#       if check in media_info['caption']['text']:
#         flag = True
#       else:
#         if all_key:
#           flag = False
#           break
#   if flag:
#     accounts[media_info['user']['username']] = media_info['like_count']
#   # if count > 23:
#   #   break
# # for username in accounts:
# #   user_followers = bot.get_user_followers(username)
# #   print(username, len(user_followers))


# # 214290799/samara-russia/

