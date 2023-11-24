import telebot
from telebot import types
import requests
import random

NASA_API_KEY = 'DEMO_KEY'
CURIOSITY_URL = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
OPPORTUNITY_URL = 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos'
SPIRIT_URL = 'https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos'
TOKEN_TG = '6773544393:AAGWJSEZqfTXk-Kh_QnxHhRMwmnvKLuYdwk'
bot = telebot.TeleBot(TOKEN_TG)


@bot.message_handler(commands=['start'])
def hello(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Curiosity")
    btn2 = types.KeyboardButton("Opportunity")
    btn3 = types.KeyboardButton("Spirit")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}! Выбери один из марсоходов NASA: Curiosity, Opportunity или Spirit и бот отправит тебе фотографию с него.',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Curiosity':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Curiosity')
        btn2 = types.KeyboardButton("Opportunity")
        btn3 = types.KeyboardButton("Spirit")
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        image_url = None
        while not image_url:
            try:
                image_url = get_mars_photo_url(message.text)
                bot.send_photo(message.chat.id, image_url, reply_markup=markup)
            except NoPicturesOnThisDayException:
                print("фото не найдено. попытка найти ещё раз")
    elif message.text == 'Opportunity':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Curiosity')
        btn2 = types.KeyboardButton("Opportunity")
        btn3 = types.KeyboardButton("Spirit")
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        image_url = None
        while not image_url:
            try:
                image_url = get_mars_photo_url(message.text)
                bot.send_photo(message.chat.id, image_url, reply_markup=markup)
            except NoPicturesOnThisDayException:
                print("фото не найдено. попытка найти ещё раз")
    elif message.text == 'Spirit':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Curiosity')
        btn2 = types.KeyboardButton("Opportunity")
        btn3 = types.KeyboardButton("Spirit")
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        image_url = None
        while not image_url:
            try:
                image_url = get_mars_photo_url(message.text)
                bot.send_photo(message.chat.id, image_url, reply_markup=markup)
            except NoPicturesOnThisDayException:
                print("фото не найдено. попытка найти ещё раз")
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Curiosity')
        btn2 = types.KeyboardButton("Opportunity")
        btn3 = types.KeyboardButton("Spirit")
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        bot.send_message(message.from_user.id, 'Я не понимаю такой команды. Выберите марсоход или введите /start',
                         reply_markup=markup)  # ответ бота


def get_curiosity_mars_image_urls_from_nasa():
    params = {
        'sol': random.randint(0, 4125),
        'api_key': NASA_API_KEY,
        'camera': 'fhaz'
    }
    response = requests.get(CURIOSITY_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        print("Данные получены")
        photos = data['photos']
        return photos
    else:
        print(f"Ошибка запроса. Код статуса: {response.status_code}")


def get_opportunity_mars_image_urls_from_nasa():
    params = {
        'sol': random.randint(0, 5111),
        'api_key': NASA_API_KEY,
        'camera': 'fhaz'
    }
    response = requests.get(OPPORTUNITY_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        print("Данные получены")
        photos = data['photos']
        return photos
    else:
        print(f"Ошибка запроса. Код статуса: {response.status_code}")


def get_spirit_mars_image_urls_from_nasa():
    params = {
        'sol': random.randint(0, 1892),
        'api_key': NASA_API_KEY,
        'camera': 'fhaz'
    }
    response = requests.get(SPIRIT_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        print("Данные получены")
        photos = data['photos']
        return photos
    else:
        print(f"Ошибка запроса. Код статуса: {response.status_code}")


class NoPicturesOnThisDayException(Exception):
    def __init__(self, message):
        print("В этот день не было фотографий")
        super().__init__(message)


def get_mars_photo_url(rover):
    photos = None
    if rover == 'Curiosity':
        photos = get_curiosity_mars_image_urls_from_nasa()
    if rover == 'Opportunity':
        photos = get_opportunity_mars_image_urls_from_nasa()
    if rover == 'Spirit':
        photos = get_spirit_mars_image_urls_from_nasa()
    print(photos, len(photos))
    if len(photos) == 0:
        raise NoPicturesOnThisDayException("В этот день не было фотографий")
    image_url = photos[0]['img_src']
    camera_tipe = photos[0]["camera"]["name"]
    return image_url


bot.polling(none_stop=True)
