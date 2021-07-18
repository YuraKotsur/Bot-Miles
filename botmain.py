import telebot 
import config 
import requests 
from bs4 import BeautifulSoup 


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def get_mess(message):
	if message.text == '/weather':
		question = 'Введіть потрібне місце'
		bot.send_message(message.from_user.id, question)
		bot.register_next_step_handler(message, post_weather)


def post_weather(message):
	global place
	place = message.text
	url = 'https://ua.sinoptik.ua/погода-' + str(place)
	bot.send_message(message.from_user.id, 'Погода у місті ' + place + ': ')
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')

	today_time = soup.find_all('p', class_='today-time')
	today_temp = soup.find_all('p', class_='today-temp')
	description = soup.find_all('div', class_='description')

	for _ in today_time:
		bot.send_message(message.chat.id, _.text)
	for _ in today_temp:
		bot.send_message(message.chat.id, _.text)


bot.polling(none_stop=True)
