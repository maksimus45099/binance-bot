import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
from binance import get_data, write_file
import random

logging.basicConfig(level=logging.INFO)

bot = Bot(token='2019856862:AAFwrxfz1loNOnQx7Gz2hLEjilSBLK52l6M')

# задаем уровень логов
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались на новости Binance")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        with open("data.txt", "r") as f:
            text = f.read()
        data = get_data('https://www.binance.com/ru/support/announcement/c-48?navId=48')
        if data == text:
            print('Всё ок, ничего нового')
        else:
            write_file(data)
            subscriptions = db.get_subscriptions()
            for s in subscriptions:
                await bot.send_message(s[1],
                                       'Для тебя есть новость!\n' + str(data))





# запускаем лонг поллинг
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(random.randrange(100, 480)))
    executor.start_polling(dp, skip_updates=True)