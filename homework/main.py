import telebot
from telebot import types
import requests
import random

NASA_API_KEY = 'DEMO_KEY'
ROVER_URL = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
TOKEN = '6773544393:AAGWJSEZqfTXk-Kh_QnxHhRMwmnvKLuYdwk'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def hello(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Получить фото")
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}! Нажав на кнопку, ты получишь случайную фотографию с марсохода NASA Curiosity',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Получить фото':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить фото')
        markup.add(btn1)
        image_url = None
        while not image_url:
            try:
                image_url = get_mars_photo_url()
            except ThereWereNoPicturesOnThisDay:
                image_url = get_mars_photo_url()
        bot.send_photo(message.chat.id, image_url, reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Получить фото')
        markup.add(btn1)
        bot.send_message(message.from_user.id, 'Вы должны ввести "Получить фото" или /start',
                         reply_markup=markup)  # ответ бота


def get_mars_image_urls_from_nasa():
    params = {
        'sol': random.randint(0, 4000),
        'api_key': NASA_API_KEY,
        'camera': 'fhaz'
    }
    response = requests.get(ROVER_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        print("Данные получены")
        photos = data['photos']
        return photos
    else:
        print(f"Ошибка запроса. Код статуса: {response.status_code}")


class ThereWereNoPicturesOnThisDay(Exception):
    def __init__(self, message):
        print("В этот день не было фотографий")
        super().__init__(message)


def get_mars_photo_url():
    photos = get_mars_image_urls_from_nasa()
    print(photos, len(photos))
    if len(photos) == 0:
        raise ThereWereNoPicturesOnThisDay("В этот день не было фотографий")
    image_url = photos[0]['img_src']
    camera_tipe = photos[0]["camera"]["name"]
    return image_url


bot.polling(none_stop=True)
