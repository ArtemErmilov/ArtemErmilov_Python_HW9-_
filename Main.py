from random import randint
#import Controller as con
from os import system

import Loger as log
import Check as cek
import Game as gm

import logging

from config import TOKEN

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot 
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    Handler
)

system ('cls')



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


                     


(START_GAME, MAN_PARTNER_NAME, BOT_TOTAL_CANDIES, SMART_BOT_TOTAL_CANDIES, 
MAN_PARTNER_NAME_TOTAL_CANDIES, MAX_CANDIES_ONE_STEP, GAME_STEP1,
GAME_STEP2,GAME_STEP3) = range(9)







def start(update, _):
    user = update.message.from_user
    logger.info("Старт игры в конфеты. Пользователь %s %s", user.first_name, user.last_name)
    log.log_data(f"Старт игры в конфеты. Пользователь {user.first_name} {user.last_name} ")

    reply_keyboard = [['С партнёром', 'C Ботом', 'C умным ботом']]
    
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    
    update.message.reply_text(
        f'Приветствую тебя {user.first_name} {user.last_name}\n'
        'Я Бот.\n'
        'Предлагаю поиграть в игру "Конфеты."\n'
        'Выбери, с кем ты будешь играть:\n'
        'Для выход из игры введите /cancel  ',
        reply_markup=markup_key,)
    return START_GAME
    

def start_game(update, _):
    
    global gamer
    
    user = update.message.from_user
    
    logger.info("%s выбрал %s", user.first_name, update.message.text)
    log.log_data(f"{user.first_name} выбрал {update.message.text}")
                                            
    text =  update.message.text
    if text == 'С партнёром':
        gamer = 'mane'
        update.message.reply_text(
            f'{user.first_name}, ты выбрал игру с партнёром.\n'
            'Введи его имя:\n'
            'Для завершения введите /cancel',

            reply_markup=ReplyKeyboardRemove(), # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
        )
        return MAN_PARTNER_NAME
    elif text == 'C Ботом':
        gamer = 'bot'
        update.message.reply_text(
            f'{user.first_name}, ты выбрал игру с ботом. \n'
            'Введи, какое количество конфет будут участвовать в игре\n'
		    'Минимальное количество конфет 21 шт.'
            'Для завершения введите /cancel',
            reply_markup=ReplyKeyboardRemove(),
        )
        return MAN_PARTNER_NAME_TOTAL_CANDIES
    else:
        gamer = 'smart_bot'
        update.message.reply_text(
            f'{user.first_name}, ты выбрал игру с УМНЫМ ботом. \n'
            'Введи, какое количество конфет будут участвовать в игре\n'
		    'Минимальное количество конфет 21 шт.'
            'Для завершения введите /cancel',

            reply_markup=ReplyKeyboardRemove(),
        )
        return MAN_PARTNER_NAME_TOTAL_CANDIES


def man_partner_name(update, _):
    user = update.message.from_user
    
    global partner_name

    partner_name = update.message.text
    
    logger.info("%s ввёл: %s", user.first_name, update.message.text)
    log.log_data(f"{user.first_name} ввёл: {update.message.text}")
    
    bool_error, text_name= cek.imput_name(partner_name)
    partner_name=text_name
    

    if bool_error == False:
        if user.first_name==partner_name:
            partner_name=partner_name+' 2'
        logger.info("Имя 2-го игрока %s ", partner_name)
        log.log_data(f"Имя 2-го игрока {partner_name}")

        update.message.reply_text(
            f'Имя партнёра:{partner_name}\n'
            f'{user.first_name} введи, какое количество конфет будут участвовать в игре\n'
		    'Минимальное количество конфет 21 шт.\n'
            'Для завершения введите /cancel',
            )
        return MAN_PARTNER_NAME_TOTAL_CANDIES
        
    else:
        logger.info("Ошибка: %s ", partner_name)
        log.log_data(f"Ошибка: {partner_name} ")
        update.message.reply_text(
        f'{partner_name}\n' 
        '\nВведите имя заново'
        )
        return MAN_PARTNER_NAME
    


def man_partner_name_total_candies(update, _): # Определение максимального количества конфет за один ход в игре
    global total_candies
    user = update.message.from_user
    total_candies = update.message.text

    logger.info("Пользователь %s ввёл количество конфет:  %s", user.first_name, total_candies)
    log.log_data(f"{user.first_name} ввёл количество конфет:  {update.message.text}")

    text_breac = 'Вы ввели число не корректно, введите его заново:'
    text_min ='Вы ввели число меньше 21, повторите ввод заново:'
    bool_error,  text_error, total_candies= cek.check_number_min(total_candies,21,text_breac,text_min)
    
    if bool_error == False:
        max_candies = total_candies//3
        update.message.reply_text(
            'Введите максимальное количество конфет, '
            'которые будут забираться за один шаг.'
            f'От 3 до {max_candies}'
            )
        return MAX_CANDIES_ONE_STEP
    else:
        update.message.reply_text(text_error)
        logger.info("Ошибка: %s ввёл количество конфет не верно: %s\n%s", user.first_name, total_candies,text_error)
        log.log_data(f"Ошибка:{user.first_name} ввёл количество конфет не верно: {update.message.text}\n{text_error}")
        return MAN_PARTNER_NAME_TOTAL_CANDIES
    

def max_candies_one_step (update, _):
    global candies_one_step
    user = update.message.from_user
    candies_one_step = update.message.text

    logger.info("Пользователь %s ввёл количество конфет за один шаг в игре:  %s", user.first_name, total_candies)
    log.log_data(f"{user.first_name} ввёл количество конфет за один шаг в игре:  {update.message.text}")

    text_breac = 'Вы ввели число не корректно, введите его заново:'
    text_min ='Вы ввели число меньше 3, введите его заново:'
    text_max =f'Вы ввели число больше {total_candies//3}, введите его заново: '
    bool_error,text_error,candies_one_step = cek.check_number_min_max(candies_one_step,3,total_candies//3,text_breac,text_min,text_max)

    if bool_error == True:
        update.message.reply_text(text_error)
        logger.info("Ошибка: %s ввёл количество конфет за один шаг в игре не верно: %s\n%s", user.first_name, update.message.text,text_error)
        log.log_data(f"Ошибка:{user.first_name} ввёл количество конфет за один шаг в игре не верно: {update.message.text}\n{text_error}")
        return MAX_CANDIES_ONE_STEP
    else:
        reply_keyboard = [['Начать', 'Выход']]
    
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    
        update.message.reply_text(
        'Начинаем игру',
        reply_markup=markup_key,)
        return GAME_STEP1


def game_step1 (update, _): # Старт игры
    user = update.message.from_user
    global us0
    global us1
    global us
    global candies_one_step
    global gamer
    global candies
    global total_candies
    if update.message.text=='Выход':
        cancel(update, _)
        return ConversationHandler.END
    
    else:
        us0 =  user.first_name
        if gamer == 'mane':
            us1 =  partner_name
        elif gamer == 'bot':
            us1 = 'Бот'
        else: 
            us1 = 'Умный бот'

        us_random = randint(0,1)
        if us_random==0:
            us=us0
        else:
            us=us1
        
        logger.info("Игру начинает %s", us)
        log.log_data(f"Игру начинает {us}")

        if gamer == 'mane' or us == us0:
            update.message.reply_text(
                    f'Игру начинает {us}\n\n'
                    f'Всего {total_candies} конфет'
                    f'{us} введи сколько конфет хочешь взять (от 1 до {candies_one_step}):',
                    reply_markup=ReplyKeyboardRemove() # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
                )
        elif gamer == 'bot' or gamer == 'smart_bot':
            if gamer == 'bot':
                candies = gm.bot_game_candies(1,candies_one_step)
            else:
                candies = gm.smart_bot_game_candies(total_candies,candies_one_step)

            total_candies, candies_one_step, us, game_run = gm.candy_game(candies,total_candies,
                                                        candies_one_step,us,us0,us1)
            update.message.reply_text(
                    f'Игру начал  {us1}\n\n'
                    f'{us1} взял {candies} конфет. Осталось {total_candies}конфет.\n'
                    f'{us0} введи сколько конфет хочешь взять (от 1 до {candies_one_step}):',
                    reply_markup=ReplyKeyboardRemove() # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
                )            
            logger.info("%s взял %s конфет, осталось %s конфет. Ход переходит к %s", us,candies,total_candies,us0)
            log.log_data(f"{us} взял {candies} конфет, осталось {total_candies} конфет. Ход переходит к {us0}")
        return GAME_STEP2


def game_step2 (update, context):

    global candies
    global candies_one_step
    global total_candies
    global us


    user = update.message.from_user
    candies = update.message.text

    logger.info("%s ввёл %s", user.first_name, candies)
    log.log_data(f"{user.first_name} ввёл {candies}")

    
     
    text_breac = 'Вы ввели число не корректно, введите его заново:'
    text_min ='Вы ввели число меньше 1, введите его заново:'
    text_max =f'Вы ввели число больше {candies_one_step}, введите его заново:'
    bool_error,text_error,candies = cek.check_number_min_max(candies,1,candies_one_step,
                                                                text_breac,text_min,text_max)
    if bool_error == True:
        update.message.reply_text(text_error)
        logger.info("Ошибка: %s ввёл не корректно число.\n %s", us,text_error)
        log.log_data(f"Ошибка: {us} ввёл не корректно число.\n %s {text_error}")
        return GAME_STEP2
    else:
        total_candies, candies_one_step, us, game_run = gm.candy_game(candies,total_candies,
                                                    candies_one_step,us,us0,us1)
        if gamer == 'bot' or gamer == 'smart_bot':
            context.bot.send_message(update.effective_chat.id, f"{us0} взял {candies}, осталось {total_candies} конфет")
        
        if game_run == True:
            if gamer == 'bot' or gamer == 'smart_bot':
                
                if gamer == 'bot':
                    candies = gm.bot_game_candies(1,candies_one_step)
                else:
                    candies = gm.smart_bot_game_candies(total_candies,candies_one_step)

                total_candies, candies_one_step, us, game_run = gm.candy_game(candies,total_candies,
                                                        candies_one_step,us,us0,us1)
            
            if gamer == 'mane':
                    update.message.reply_text(
                    f'Осталось {total_candies} конфет\n'
                    f'{us} введи, сколько конфет хочешь взять (от 1 до {candies_one_step}):'
                    )
                    logger.info("Осталось %s конфет, ход переходит к %s", total_candies,us)
                    log.log_data(f"Осталось {total_candies} конфет, ход переходит к {us}")
            else:
                    context.bot.send_message(update.effective_chat.id, f'{us1} взял {candies} конфет. Осталось {total_candies} конфет.\n')
                    if game_run == True:    
                        update.message.reply_text(
                            f'{us0} введи сколько конфет хочешь взять (от 1 до {candies_one_step}):',
                            reply_markup=ReplyKeyboardRemove() # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
                            )            
                    logger.info("%s взял %s конфет, осталось %s конфет.", us1,candies,total_candies)
                    if game_run == True:  logger.info("Ход переходит к %s", us0)
                    log.log_data(f"{us1} взял {candies} конфет, осталось {total_candies} конфет.")
                    if game_run == True: log.log_data(f"Ход переходит к {us0}")
        if game_run == True:
            return GAME_STEP2
        else:
            logger.info("Выиграл %s", us)
            log.log_data(f"Выиграл {us}")
            repeat_game_menu(update, context)
            return GAME_STEP3
           
            
            
            

def repeat_game_menu (update, _):
    reply_keyboard = [['Выход', 'Продолжить']]
    
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    
    update.message.reply_text(
        f'Поздравляю выиграл {us}.\n'
        f'{us} ты молодец!\n'
        'Продолжить игру?',
        reply_markup=markup_key,)
    return GAME_STEP3


def repeat_game(update, _):
    user = update.message.from_user
    repeat_or_end = update.message.text
    
    if repeat_or_end=='Продолжить':
        logger.info("%s решил продолжить игру", user.first_name)
        log.log_data(f"{user.first_name} решил продолжить игру")
        start(update, _)
        return START_GAME
       
    elif repeat_or_end=='Выход':
        logger.info("%s решил выйти из игры", user.first_name)
        log.log_data(f"{user.first_name} решил выйти из игры")
        cancel(update, _)
        return ConversationHandler.END

def cancel(update, _): # Обрабатываем команду /cancel если пользователь отменил разговор
    
    user = update.message.from_user
   
    logger.info("%s вышел из игры.", user.first_name)
    log.log_data(f"{user.first_name} вышел из игры." )
    
    update.message.reply_text(
        'Вы вышли из игры.\n'
        f'До скорых встреч {user.first_name}! ', 
        reply_markup=ReplyKeyboardRemove()
    )
   
    return ConversationHandler.END


def unknown (update, context):# 
    user = update.message.from_user
    text=update.message.text
    context.bot.send_message(update.effective_chat.id, f"{text} Странная команда, я такой не знаю!")
    logger.info(" %s ввёл %s. Данной команды не существует.",user.first_name,text)
    log.log_data(f"{user.first_name} ввёл {text}. Данной команды не существует.")


def give_word (update, context):
    word = update.message.text
    user = update.message.from_user
    logger.info(" %s ввёл %s.",user.first_name,word)
    log.log_data(f"{user.first_name} ввёл {word}.")
    
    context.bot.send_message(update.effective_chat.id, f"{user.first_name} я тебя не могу понять!")










if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(TOKEN)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Определяем обработчик разговоров `ConversationHandler` 
    conv_handler = ConversationHandler( # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            START_GAME: [MessageHandler(Filters.regex('^(С партнёром|C Ботом|C умным ботом)$'), start_game)],
            MAN_PARTNER_NAME: [CommandHandler('cancel', cancel),MessageHandler(Filters.text, man_partner_name)],
            MAN_PARTNER_NAME_TOTAL_CANDIES: 
                [CommandHandler('cancel', cancel),MessageHandler(Filters.text, man_partner_name_total_candies)],
            MAX_CANDIES_ONE_STEP:
                [CommandHandler('cancel', cancel),MessageHandler(Filters.text, max_candies_one_step)],
            GAME_STEP1:
                [MessageHandler(Filters.regex('^(Начать|Выход)$'), game_step1)],
            GAME_STEP2: 
                [CommandHandler('cancel', cancel),MessageHandler(Filters.text, game_step2)],
           GAME_STEP3: 
                [MessageHandler(Filters.regex('^(Выход|Продолжить)$'), repeat_game)],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )


    message_handler=MessageHandler(Filters.text, give_word)
    unknown_handler = MessageHandler(Filters.command, unknown)


    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(message_handler)

    # Запуск бота
    log.log_data('|'+'-'*10+"Сервер старт"+'-'*10+'|')
    updater.start_polling()
    updater.idle()
    log.log_data('|'+'-'*10+"Сервер стоп"+'-'*10+'|'+'\n\n')