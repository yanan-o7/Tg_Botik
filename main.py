import telebot
from telebot import types
import webbrowser
import random

bot = telebot.TeleBot("8297912494:AAHuugBP3yXZKxBmcmvTXBIKYgJnszH2pWc")
USER_DATA = {}
TASKS = ["Ежедневки", "Смола", "Отметиться"]
challenge = ['Убей босса', 'Пройди подземелье', 'Найди 5 сундуков', 'Сыграть в призыв семерых', 'Пойти в бездну', 'Улучшить персонажа', 'Зайти в мультиплеер']

def get_user_data(uid):
    if uid not in USER_DATA:
        USER_DATA[uid] = {
            'level': 0,
            'tasks_completed': 0,
            'state': [False] * len(TASKS)
        }
    return USER_DATA[uid]

def buttons(state):
    button = types.InlineKeyboardMarkup()
    for ind, (done, text) in enumerate(zip(state, TASKS)):
        label = ("✅ " if done else " ") + text
        button.row(types.InlineKeyboardButton(label, callback_data=f"t:{ind}"))
    return button

@bot.message_handler(commands=['start'])
def main(message):
    user_data = get_user_data(message.from_user.id)
    bot.send_message(message.chat.id,f"Прив\\, {message.from_user.first_name}\\!\n*Уровень*: {user_data['level']}\n*Команды*:\n _/site_ \n _/social_ \n _/news_ \n _/list_ \n _/challenge_ \n _/level_ \n _/progress_", parse_mode='MarkdownV2')

@bot.message_handler(commands=['level'])
def show_level(message):
    user_data = get_user_data(message.from_user.id)
    bot.send_message(message.chat.id, user_data['level'])

@bot.message_handler(commands=['progress'])
def show_progress(message):
    user_data = get_user_data(message.from_user.id)
    bot.send_message(message.chat.id, user_data['tasks_completed'])

@bot.message_handler(commands=['challenge'])
def show_challenge(message):
    bot.send_message(message.chat.id, random.choice(challenge))

@bot.message_handler(commands=['site'])
def go_to_site(message):
    webbrowser.open('https://genshin.hoyoverse.com/ru/home')

@bot.message_handler(commands=['social'])
def go_to_social(message):
    webbrowser.open('https://www.hoyolab.com/home')

@bot.message_handler(commands=['news'])
def go_to_news(message):
    webbrowser.open('t.me/genshin_impact_ru_off')

@bot.message_handler(commands=["list"])
def show_list(message):
    user_data = get_user_data(message.from_user.id)
    bot.send_message(message.chat.id, "_Задачи_", reply_markup=buttons(user_data['state']), parse_mode='MarkdownV2')

@bot.callback_query_handler(func=lambda c: True)
def callback(c: telebot.types.CallbackQuery):
    if not c.data or not c.data.startswith("t:"):
        return
    idx = int(c.data.split(":", 1)[1])
    user_data = get_user_data(c.from_user.id)
    user_data['state'][idx] = not user_data['state'][idx]
    all_completed = all(user_data['state'])
    if all_completed:
        user_data['level'] += 0.5
        user_data['tasks_completed'] += 1
        bot.send_message(c.message.chat.id,f"Уровень повышен: {user_data['level']}")
        bot.send_sticker(c.message.chat.id,"CAACAgIAAxkBAAEDHtpo75LNZsXzPjBqYmYvPWXSMEMNnAACWWYAAhzMoEn_L3mN6-QKOzYE")
        if user_data['level'] in range(1,1000,1):
            bot.send_sticker(c.message.chat.id,"CAACAgIAAxkBAAETJwlo8JZdblgtIRilNrXlYYs5oFPQrAACZG4AAv1coEl_3d2cog233zYE")
        user_data['state'] = [False] * len(user_data['state'])
    bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=buttons(user_data['state']))

bot.polling(none_stop=True)
