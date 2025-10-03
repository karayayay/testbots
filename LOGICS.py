# основная логика бота

import telebot
import buttons
import database

bot = telebot.TeleBot('8286560411:AAGoWToSj3PQOnBJuWVeLiIjkIgVIeVKX-c')

# Обработчик команды/start

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Проверяем зарегестрироваля ли юзер
    if database.check_user(user_id):
        bot.send_message(user_id, 'Добро пожаловать!')
    else:
        bot.send_message(user_id, 'Здравствуйте! Давайте начнем регистрацию! \n'
                                  'Введите свое имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        #  переход на этап получения имени
        bot.register_next_step_handler(message, get_name)

#  этап получения имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Отлично! Теперь отправьте свой номер!',
                     reply_markup=buttons.num_button())
    # Переход на этап получения номера
    bot.register_next_step_handler(message, get_num, user_name)

# этап получения номера
def get_num(message, user_name):
    user_id = message.from_user.id
    # Проверяем правильность отправки номера
    if message.contact:
        user_num = message.contact.phone_number
        # регистрируем юзера
        database.register(user_id, user_name, user_num)
        bot.send_message(user_id, 'Регистрация прошла успешно!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте номер по кнопке!')
        # Возвращаем на этап получения номера
        bot.register_next_step_handler(message, get_num, user_name)

        # запуск бота
bot.polling(non_stop=True)


# testing git add function with comment function