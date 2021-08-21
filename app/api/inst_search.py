import glob
import os
import time
import json

from instabot import Bot
from instaloader import Instaloader, Profile, Hashtag

from flask import request

from app import app, db
from app.utils import send_datetime_to_client
from app.api import support

class INSTGRMSearch(object):

	DEF_LOC = 1000.0

	def __init__(self, keyword):
		self.users = {}
		self.users_names = []
		self.list_of_request_keys = []
		self.keyword = keyword
		self.users_infos = {}
		self.bot, self.loader = self.__set_login_instagram__()
		self.__set_default_location__()

	def __set_default_location__(self):
		# Для локации установим дефолтные координаты
		for attr in ['s_lat', 'u_lat', 'z_lng', 'v_lng']:
			setattr(self, attr, self.DEF_LOC)
		return

	def __set_login_instagram__(self):
		# очистка данных и авторизация пользователя
		cookie_del = glob.glob("config/*cookie.json")
		if len(cookie_del) > 0:
		  os.remove(cookie_del[0])
		bot = Bot(max_likes_to_like=1000000, min_likes_to_like=10)
		bot.login(username='hackaton_test1', password='456321Zx', is_threaded=True)
		loader = Instaloader()
		USER = 'hackaton_test1'
		PASSWORD = '456321Zx'
		loader.login(USER, PASSWORD)
		return bot, loader

	def generate_list_of_request_keys(self):
		# Генерируем топ запросы
		self.list_of_request_keys = [
			'%sпутешествие' % self.keyword,
			'%s контент' % self.keyword,
			'%s путешествия' % self.keyword,
			'%s красивая' % self.keyword,
			'%s блогер' % self.keyword,
			'блогер %s' % self.keyword,
			'%s блог' % self.keyword,
			'блог %s' % self.keyword,
			'%s путешественник' % self.keyword
		]
		return

	def set_keyword(self, keyword):
		self.keyword = keyword
		return

	def set_location(self, s_lat, u_lat, z_lng, v_lng):
		#координаты, относительно которых будут определяться нужные блогеры
		self.s_lat = float(s_lat)
		self.u_lat = float(u_lat)
		self.z_lng = float(z_lng)
		self.v_lng = float(v_lng)
		return

	def set_users_by_request_key(self, request_key):
		# получаем юзеров по ключу
		_users_ = []
		_structure_ = self.bot.get_topsearch(request_key)
		for user in _structure_['users']:
			_users_.append(user.get('user', {}).get('username'))
		return _users_

	def start_search(self, max_posts, min_followers):
		# TODO старт поиска по хэштегам
		# self.users = self.get_users_of_posts(self.keyword, max_posts)
		# старт по топовым выдачам
		self.generate_list_of_request_keys()
		for request_key in self.list_of_request_keys:
			users = self.set_users_by_request_key(request_key)
			self.request_users_infos(users, min_followers)
		return
		
	def request_users_infos(self, users, min_followers):
		# функция запрашивает сведения о пользователях-блогерах
		time.sleep(15)
		for username in users:
			profile = Profile.from_username(self.loader.context, username)
			time.sleep(1)
			if profile.followers > min_followers:
				self.users_infos[username] = {
					'user_name': username,
					'full_name': profile.full_name,
					'followers': profile.followers,
					'is_business_account': profile.is_business_account,
					'profile_pic_url': profile.profile_pic_url
				}
				with open('data23.txt', 'w') as f:
					json.dump(self.users_infos, f, ensure_ascii=False)
		return

	def get_users_of_posts(self, hastag, max_posts):
		# функция возвращает множество юзеров
		_users_ = set()
		posts_of_hashtag = self.get_posts_of_hashtag(hastag, max_posts)
		for url_post in posts_of_hashtag:
			_request_media_info_ = self.bot.get_media_info(url_post)
			if len(_request_media_info_) > 0:
				media_info = _request_media_info_[0]
				location = media_info.get('location', {})
				lng = float(location.get('lng', self.DEF_LOC))
				lat = float(location.get('lat', self.DEF_LOC))
				_user_name_ = media_info.get('user').get('username')
				if lng == self.DEF_LOC or lat == self.DEF_LOC:
					# исключаем посты без локаций,
					# ответственный тревелблогер локацию ставит всегда
					...
				elif lat > self.u_lat and lat < self.s_lat:
					if lng < self.v_lng and lng > self.z_lng:
						_users_.add(_user_name_)
				else:
					# Пост не входит в локации
					...
		return _users_

	def get_posts_of_hashtag(self, hastag, max_posts):
		return self.bot.get_total_hashtag_medias(hastag, amount=max_posts)

	def get_frequent_hashtags(self, list_of_hashtags):
		hashtags_humbers = {}
		number_hashtags = {}
		for item in list_of_hashtags:
			if item in number_hashtags:
				hashtags_humbers[item] = hashtags_humbers[item] + 1
			else:
				hashtags_humbers[item] = 1
		for hashtag, number in hashtags_humbers.items():
			if number in number_hashtags:
				number_hashtags[number].append(hashtag)
			else:
				number_hashtags[number] = [hashtag]
		_sorted_keys_ = sorted(list(number_hashtags.keys()), reverse=True)
		_popular_ = []
		for number in _sorted_keys_:
			for hashtag in number_hashtags[number]:
				_popular_.append(hashtag)
				if len(_popular_) > 10:
					return _popular_
		return _popular_
							
	def get_bloger_info_by_username(self, username):
		loader = Instaloader()
		profile = Profile.from_username(loader.context, username)
		posts = profile.get_posts()
		likes_count = 0.0
		posts_count = 0.0
		comments_count = 0.0
		list_of_hashtags = []
		for post in posts:
			posts_count += 1.0
			likes_count += post.likes
			comments_count += post.comments
			list_of_hashtags += post.caption_hashtags
		coef = ((likes_count + comments_count) / (posts_count * profile.followers) ) * 100.0
		# _popular_ = self.get_frequent_hashtags(list_of_hashtags)
		return {
			'username': username,
			'posts_count': posts_count,
			'likes_count': likes_count,
			'comments_count': comments_count,
			'coef': coef,
			# '_popular_': _popular_
		}
	
@support
@app.route('/api/v1/bloger', methods=['GET'])
def get_bloger_info():
  _instgrm_ = INSTGRMSearch()
  bloger_info = _instgrm_.get_bloger_info_by_username(username='kristina_azman')

  return json.dumps({
    'success': True,
    'result': bloger_info
  })


if __name__ == '__main__':
	# создание соединения
	_instgrm_ = INSTGRMSearch(keyword='самара')
	# установка координат города
	_instgrm_.set_location(
		s_lat='54.41',
		u_lat='51.470',
		z_lng='47.55',
		v_lng='52.35'
	)
	# # поиск блогеров и создание бд
	_instgrm_.start_search(max_posts=100, min_followers=100)

	_instgrm_.get_bloger_info_by_username(user_name='kristina_azman')