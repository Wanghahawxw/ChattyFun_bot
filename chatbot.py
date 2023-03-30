'''
Author: huibing 13728166372@163.com
Date: 2023-03-28 21:09:05
LastEditors: huibing 13728166372@163.com
LastEditTime: 2023-03-29 17:06:20
FilePath: /chatbot10/chatbot.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import configparser
import random
import pyodbc
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 从 config.ini 文件中读取配置信息
config = configparser.ConfigParser()
config.read('config.ini')

telegram_api_token = config.get('TELEGRAM', 'ACCESS_TOKEN')
azure_sql_server = config.get('AZURE_SQL', 'SERVER')
azure_sql_database = config.get('AZURE_SQL', 'DATABASE')
azure_sql_user = config.get('AZURE_SQL', 'USER')
azure_sql_password = config.get('AZURE_SQL', 'PASSWORD')
azure_sql_driver = config.get('AZURE_SQL', 'DRIVER')
spotify_client_id = config.get('SPOTIFY', 'CLIENT_ID')
spotify_client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')

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
]

# 定义命令处理函数
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! I'm a Chatbot. I can tell jokes, riddles, and recommend songs from Spotify. Use /joke, /riddle or /song to have fun!")

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

def main():
    # 创建 Updater 和用于处理命令的 CommandHandler
    updater = Updater(token=telegram_api_token, use_context=True)
    dispatcher = updater.dispatcher

    # 添加命令处理函数
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("joke", joke))
    dispatcher.add_handler(CommandHandler("riddle", riddle))
    dispatcher.add_handler(CommandHandler("song", song))

    # 启动 Chatbot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
