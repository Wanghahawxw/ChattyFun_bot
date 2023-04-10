'''
Author: huibing 13728166372@163.com
Date: 2023-03-28 21:09:05
LastEditors: huibing 13728166372@163.com
LastEditTime: 2023-04-10 13:56:36
FilePath: /chatbot10/chatbot.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import configparser
import os
import random
import pyodbc
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, JobQueue

# 从 config.ini 文件中读取配置信息
# config = configparser.ConfigParser()
# config.read('config.ini')

# telegram_api_token = config.get('TELEGRAM', 'ACCESS_TOKEN')
# azure_sql_server = config.get('AZURE_SQL', 'SERVER')
# azure_sql_database = config.get('AZURE_SQL', 'DATABASE')
# azure_sql_user = config.get('AZURE_SQL', 'USER')
# azure_sql_password = config.get('AZURE_SQL', 'PASSWORD')
# azure_sql_driver = config.get('AZURE_SQL', 'DRIVER')
# spotify_client_id = config.get('SPOTIFY', 'CLIENT_ID')
# spotify_client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')

telegram_api_token = os.environ.get('TELEGRAM_ACCESS_TOKEN')
azure_sql_server = os.environ.get('AZURE_SQL_SERVER')
azure_sql_database = os.environ.get('AZURE_SQL_DATABASE')
azure_sql_user = os.environ.get('AZURE_SQL_USER')
azure_sql_password = os.environ.get('AZURE_SQL_PASSWORD')
azure_sql_driver = os.environ.get('AZURE_SQL_DRIVER')
spotify_client_id = os.environ.get('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
news_api_key = os.environ.get('NEWS_API_KEY')

# 创建数据库连接字符串
connection_string = f"DRIVER={azure_sql_driver};SERVER={azure_sql_server};DATABASE={azure_sql_database};UID={azure_sql_user};PWD={azure_sql_password}"

# 设置Spotify API客户端
spotify_credentials = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
spotify = spotipy.Spotify(client_credentials_manager=spotify_credentials)

# 示例笑话和谜语列表
jokes = [
    "Why don't scientists trust atoms? Because they make up everything.",
    "Why did the chicken go to the seance? To get to the other side.",
    "Why don't some couples go to the gym? Because some relationships don't work out.",
    "Why did the coffee file a police report? It got mugged.",
    "What do you call a fake noodle? An impasta.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "How does a penguin build its house? Igloos it together.",
    "Why don't oysters donate to charity? They're shellfish.",
]

riddles = [
    {
        "question": "What has keys but can't open locks?",
        "answer": "A piano."
    },
    {
        "question": "What has a head and a tail but no body?",
        "answer": "A coin."
    },
    {
        "question": "What gets wetter as it dries?",
        "answer": "A towel."
    },
    {
        "question": "What starts with an E, ends with an E, but only contains one letter? ",
        "answer": "An envelope."
    },
    {
        "question": "I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?",
        "answer": "Fire."
    },
    {
        "question": "The more you take, the more you leave behind. What am I?",
        "answer": "Footsteps."
    },
]

# 定义命令处理函数
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! I'm a Chatbot. I can tell jokes, riddles, and recommend songs from Spotify. Use /joke, /riddle, /song or /news to have fun!")

def joke(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(jokes))

def riddle(update: Update, context: CallbackContext):
    selected_riddle = random.choice(riddles)
    update.message.reply_text(selected_riddle["question"])
    update.message.reply_text("Answer: " + selected_riddle["answer"])

def song(update: Update, context: CallbackContext):
    recommendations = spotify.recommendations(seed_genres=['pop'], limit=1)
    track = recommendations['tracks'][0]
    track_name = track['name']
    track_artist = track['artists'][0]['name']
    track_url = track['external_urls']['spotify']
    update.message.reply_text(f"Check out this song: {track_name} by {track_artist}\n{track_url}")

def get_entertainment_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": news_api_key,
        "category": "entertainment",
        "language": "en",
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["articles"]

def news(update: Update, context: CallbackContext):
    articles = get_entertainment_news()
    selected_article = random.choice(articles)
    title = selected_article["title"]
    url = selected_article["url"]
    update.message.reply_text(f"Check out this entertainment news: {title}\n{url}")

def main():
    # 创建 Updater 和用于处理命令的 CommandHandler
    updater = Updater(token=telegram_api_token, use_context=True)
    dispatcher = updater.dispatcher

    # 添加命令处理函数
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("joke", joke))
    dispatcher.add_handler(CommandHandler("riddle", riddle))
    dispatcher.add_handler(CommandHandler("song", song))
    dispatcher.add_handler(CommandHandler("news", news))
    

    # 启动 Chatbot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
