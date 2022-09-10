# Модератор в доработке
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import pymysql
import pymysql.cursors
import sqlite3

API_TOKEN = "5617800181:AAEn56y_Cup_4kEILLAjObncMPYxqGt34sw"

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

print("START")
connection = pymysql.connect(host='khaliloy.beget.tech',
                             user='khaliloy_taxi',
                             password='123q123Q',
                             database='khaliloy_taxi',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def add_service(name, age, phone, date, time, address):  # Добавить инфу в БД
    db = pymysql.connect(host='khaliloy.beget.tech', user='khaliloy_taxi', passwd='123q123Q',
                         db='khaliloy_taxi', charset='utf8')
    cur = db.cursor()
    try:
        if address:
            sql = f"INSERT INTO us (`id`, `name`, `age`, `phone`, `date`, `time`, `address`) " \
              f"VALUES (NULL, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (name, age, phone, date, time, address))
        else:
            sql = f"INSERT INTO tax (`id`, `name`, `age`, `phone`, `date`, `time`) " \
              f"VALUES (NULL, %s, %s, %s, %s, %s)"
            cur.execute(sql, (name, age, phone, date, time))
        db.commit()
    except sqlite3.Error as e:
        print("Ошибка добавления информации в БД: " + str(e))
        return False
    return True


start = KeyboardButton('/start')
choose_start = ReplyKeyboardMarkup(resize_keyboard=True).add(start)

backward = KeyboardButton('Назад')

tax = KeyboardButton('Я таксист')
us = KeyboardButton('Я не таксист')
choose_type = ReplyKeyboardMarkup(resize_keyboard=True).add(tax).add(us)

accept = KeyboardButton('Принять заявку')
keep = KeyboardButton('Оставить заявку')
choose_service = ReplyKeyboardMarkup(resize_keyboard=True).add(accept).add(keep).add(backward)

# change_status_order = KeyboardButton('Изменить статус обращения')
# block = KeyboardButton('Заблокировать пользователя')
# unlock = KeyboardButton('Разблокировать пользователя')
# admin_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(change_status_order).add(block).add(unlock)

only_backward = ReplyKeyboardMarkup(resize_keyboard=True).add(backward)


class author(StatesGroup):
    wait_author = State()


class us(StatesGroup):
    type_service = State()
    keep_service = State()


class tax(StatesGroup):
    type_service = State()
    keep_service = State()


@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Добрый день. Авторизируйтесь', reply_markup=choose_type)
    await author.wait_author.set()


# @dp.message_handler(commands=['admin'], state="*")
# async def admin(message: types.Message, state: FSMContext):
#     await state.finish()
#     result = str(get_user_info(message)).split(", ")[2]
#     if result == "1":
#         await message.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=admin_kb)
#     else:
#         await message.answer('Доступ запрещён', reply_markup=choose_start)
#
#
# @dp.message_handler(text='Изменить категории')
# async def start_change_categories(message: types.Message, state: FSMContext):
#     result = str(get_user_info(message)).split(", ")[2]
#     if result:
#         categories = get_categories()
#         categories = ([x[1] for x in categories])
#         categories = ", ".join(categories)
#         print(categories)
#         await message.answer(f"{categories}")
#         await message.answer('Вы хотите добавить или удалить категорию', reply_markup=change_cat)
#         await Admin.change_category.set()
#     else:
#         await message.answer('Доступ запрещён', reply_markup=choose_start)
#
#
# @dp.message_handler(state=Admin.change_category)
# async def changing_categories(message: types.Message, state: FSMContext):
#     result = str(get_user_info(message)).split(", ")[2]
#     if result:
#         if message.text == "Добавить":
#             await state.update_data(category="Добавить")
#         elif message.text == "Удалить":
#             await state.update_data(category="Удалить")
#         await message.answer('Теперь введите название', reply_markup=only_backward)
#         await Admin.category.set()
#     else:
#         await message.answer('Доступ запрещён', reply_markup=choose_start)
#
#
# @dp.message_handler(state=Admin.category)
# async def change_categories(message: types.Message, state: FSMContext):
#     result = str(get_user_info(message)).split(", ")[2]
#     if result:
#         con = pymysql.connect(host='almetkvant.beget.tech', user='almetkvant_bot', passwd='Parol22',
#                               db='almetkvant_bot', charset='utf8')
#         cur = con.cursor()
#         user_data = await state.get_data()
#         if user_data["category"] == "Добавить":
#             sql = f"INSERT INTO categories (`id`, `category`) " \
#                   f"VALUES (NULL, %s)"
#             cur.execute(sql, message.text)
#         elif user_data["category"] == "Удалить":
#             sql = f"DELETE FROM categories WHERE category = '{message.text}'"
#             cur.execute(sql)
#         con.commit()
#         await message.answer('Выполнено!', reply_markup=admin_kb)
#         await state.finish()
#     else:
#         await message.answer('Доступ запрещён', reply_markup=choose_start)
#
#
# @dp.message_handler(text='Изменить статус обращения')
# async def start_change_status(message: types.Message, state: FSMContext):
#     result = str(get_user_info(message)).split(", ")[2]
#     if result:
#         await message.answer('Введите id обращения, статус которого вы хотите изменить.\nДля отмены нажмите кнопку ниже',
#                              reply_markup=only_backward)
#         await Admin.status.set()
#     else:
#         await message.answer('Доступ запрещён', reply_markup=choose_start)
#
#
# @dp.message_handler(state=Admin.status)
# async def change_status(message: types.Message, state: FSMContext):
#     if message.text.isdigit():
#         con = pymysql.connect(host='almetkvant.beget.tech', user='almetkvant_bot', passwd='Parol22',
#                               db='almetkvant_bot', charset='utf8')
#         cur = con.cursor()
#         cur.execute(f"SELECT * FROM orders WHERE id = {message.text}")
#         result = cur.fetchall()
#         if len(result) == 0:
#             await message.answer('Такое обращение не найдено в базе данных.', reply_markup=only_backward)
#         else:
#             await state.update_data(id=message.text)
#             await message.answer('Теперь выберите статусы', reply_markup=statuses)
#             await Admin.change_status.set()
#
#     else:
#         await message.answer('Ты вводишь буквы...\nВведи ID')
#
#
# @dp.message_handler(state=Admin.change_status)
# async def changing_status(message: types.Message, state: FSMContext):
#     con = pymysql.connect(host='almetkvant.beget.tech', user='almetkvant_bot', passwd='Parol22',
#                           db='almetkvant_bot', charset='utf8')
#     cur = con.cursor()
#     user_data = await state.get_data()
#     cur.execute(f"SELECT chat_id, address FROM orders WHERE id = '{user_data['id']}'")
#     chat_id, address = cur.fetchone()
#     await state.update_data(chat_id=chat_id, address=address)
#     if message.text == "Написать обратившемуся":
#         await message.answer('Хорошо! Введите текст сообшения, которое вы хотите отправить обратившемуся',
#                              reply_markup=only_backward)
#         await Admin.write_message.set()
#     else:
#         text = None
#         if message.text == "В работе":
#             text = "В работе"
#         elif message.text == "Исполнено":
#             text = "Исполнено"
#         elif message.text == "Не исполнено":
#             text = "Не исполнено"
#         elif message.text == "Удалить обращение":
#             text = "Ваше обращение не было зарегистрировано. Причина указана выше."
#         if text:
#             cur.execute(f"UPDATE orders SET made = '{text}' WHERE id = {user_data['id']}")
#             con.commit()
#             await bot.send_message(chat_id=chat_id, text=f"Администраторы изменили статус вашего обращения по адресу:"
#                                                          f"\n'{address}'\nна '{text}'")
#             await message.answer('Статус обращения изменён. Обратившийся осведомлён', reply_markup=admin_kb)
#             await state.finish()
#
#
# @dp.message_handler(state=Admin.write_message)
# async def writing_message(message: types.Message, state: FSMContext):
#     user_data = await state.get_data()
#     await bot.send_message(chat_id=user_data["chat_id"], text=f"Администратор написал вам по поводу вашего обращения по"
#                                                               f" адресу:\n'{user_data['address']}'.\n{message.text}\n")
#     await message.answer('Ваше сообщение было отправлено обратившемуся', reply_markup=admin_kb)
#     await state.finish()
#
#
# @dp.message_handler(text='Заблокировать пользователя')
# async def start_block_user(message: types.Message, state: FSMContext):
#     result = str(get_user_info(message)).split(", ")[2]
#     if result:
#         await message.answer('Введите chat_id обращения, чтобы заблокировать обатившегося.\nДля отмены нажмите кнопку '
#                              'ниже', reply_markup=only_backward)
#         await Admin.block.set()
#     else:
#         await message.answer('Доступ запрещён', reply_markup=choose_start)
#
#
# @dp.message_handler(state=Admin.block)
# async def block_user(message: types.Message, state: FSMContext):
#     if message.text.isdigit():
#         con = pymysql.connect(host='almetkvant.beget.tech', user='almetkvant_bot', passwd='Parol22',
#                               db='almetkvant_bot', charset='utf8')
#         cur = con.cursor()
#         cur.execute(f"SELECT * FROM orders WHERE id = {message.text}")
#         user_id = cur.fetchone()
#         if len(user_id) != 0:
#             cur.execute(f"SELECT * FROM users WHERE user_id = {user_id[8]}")
#             result = cur.fetchall()
#             if len(result) == 0:
#                 await message.answer('Такой пользователь не найден в базе данных.', reply_markup=admin_kb)
#                 await state.finish()
#             else:
#                 id = int(str(result[-1]).split(", ")[3].split(")")[0])
#                 if id == 0:
#                     cur.execute(f"UPDATE users SET blocked = 1 WHERE user_id = {user_id[8]}")
#                     con.commit()
#                     await message.answer('Пользователь успешно добавлен в ЧС.', reply_markup=admin_kb)
#                     await bot.send_message(user_id[8], f'Ты был забанен Администрацией за обращение на тему '
#                                                        f'{user_id[4]} по адресу и фото ниже\n{user_id[1]} <a href='
#                                                        f'"{user_id[3]}">.</a>', parse_mode="HTML")
#                     await state.finish()
#                 else:
#                     await message.answer('Данный пользователь уже получил бан', reply_markup=admin_kb)
#                     await state.finish()
#         else:
#             await message.answer('Данного обращения нет', reply_markup=only_backward)
#     else:
#         await message.answer('Ты вводишь буквы...\nВведи ID')
#
#
# @dp.message_handler(text='Разблокировать пользователя')
# async def start_unlock_user(message: types.Message, state: FSMContext):
#     result = str(get_user_info(message)).split(", ")[2]
#     if result:
#         await message.answer('Введите chat_id обращения, чтобы разблокировать обатившегося.\nДля отмены нажмите кнопку '
#                              'ниже', reply_markup=only_backward)
#         await Admin.unlock.set()
#     else:
#         await message.answer('Доступ запрещён', reply_markup=choose_start)
#
#
# @dp.message_handler(state=Admin.unlock)
# async def unlock_user(message: types.Message, state: FSMContext):
#     if message.text.isdigit():
#         con = pymysql.connect(host='almetkvant.beget.tech', user='almetkvant_bot', passwd='Parol22',
#                               db='almetkvant_bot', charset='utf8')
#         cur = con.cursor()
#         cur.execute(f"SELECT * FROM orders WHERE id = {message.text}")
#         user_id = cur.fetchone()
#         if len(user_id) != 0:
#             cur.execute(f"SELECT * FROM users WHERE user_id = {user_id[8]}")
#             result = cur.fetchall()
#             if len(result) == 0:
#                 await message.answer('Такой пользователь не найден в базе данных.', reply_markup=admin_kb)
#                 await state.finish()
#             else:
#                 id = int(str(result[-1]).split(", ")[3].split(")")[0])
#                 if id == 1:
#                     cur.execute(f"UPDATE users SET blocked = 0 WHERE user_id = {user_id[8]}")
#                     con.commit()
#                     await message.answer('Пользователь был успешно вычеркнут из чёрного списка', reply_markup=admin_kb)
#                     await bot.send_message(user_id[8], 'Ты был разбанен Администрацией')
#                     await state.finish()
#                 else:
#                     await message.answer('Данный пользователь не заблокирован', reply_markup=admin_kb)
#                     await state.finish()
#         else:
#             await message.answer('Данного обращения нет', reply_markup=only_backward)
#     else:
#         await message.answer('Ты вводишь буквы...\nВведи ID')


@dp.message_handler(state=author.wait_author)
async def authorize(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text == "Я таксист":
        await tax.type_service.set()
    elif message.text == "Я не таксист":
        await us.type_service.set()
    await message.answer("Пожалуйста, укажите тип услуги из указанных", reply_markup=choose_service)


@dp.message_handler(state=us.type_service)
async def us_auth(message: types.Message, state: FSMContext):
    if message.text == "Принять заявку":
        await message.answer("*Выкидаваем ссылкy на заявки*", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    elif message.text == "Оставить заявку":
        await message.answer("Впишите данные")
        await message.answer('Шаблон: фамилия имя, возраст, телефон, дата, время, адрес (дата в формате "ГГГГ-ММ-ДД", время - "ЧЧ:ММ")', reply_markup=types.ReplyKeyboardRemove())
        await us.next()


@dp.message_handler(state=tax.type_service)
async def tax_auth(message: types.Message, state: FSMContext):
    if message.text == "Принять заявку":
        await message.answer("*Выкидаваем ссылку на заявки*", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    elif message.text == "Оставить заявку":
        await message.answer("Впишите данные")
        await message.answer('Шаблон: фамилия имя, возраст, телефон, дата, время (дата в формате "ГГГГ-ММ-ДД", время - "ЧЧ:ММ")', reply_markup=types.ReplyKeyboardRemove())
        await tax.next()


@dp.message_handler(state=us.keep_service)
async def us_serv(message: types.Message, state: FSMContext):
    try:
        name, age, phone, date, time, address = message.text.split(",")
        add_service(name, age, phone, date, time, address)
        await message.answer('Хорошо! Заявка составлена', reply_markup=choose_start)
        await state.finish()
    except Exception:
        await message.answer('Извините. Произошла ошибка. Проверьте корректность ввода', reply_markup=types.ReplyKeyboardRemove())
        return


@dp.message_handler(state=tax.keep_service)
async def tax_serv(message: types.Message, state: FSMContext):
    try:
        name, age, phone, date, time = message.text.split(",")
        add_service(name, age, phone, date, time, address=None)
        await message.answer('Хорошо! Заявка составлена', reply_markup=choose_start)
        await state.finish()
    except Exception:
        await message.answer('Извините. Произошла ошибка. Проверьте корректность ввода', reply_markup=types.ReplyKeyboardRemove())
        return


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
