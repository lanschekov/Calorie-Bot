import vk_api

from CalorieBot import CalorieBot

TOKEN = 'vk1.a.sB3u-TlUlSe-NkvWkzkRQnFhOvKkKtnC2y9K9kRhMOUIfTEWCTimj1gVRPt' \
        '0I7Aa7L1s5j7DqB-wD5LwXWZuhFtlA7Y7qGvepso0TUNMpifBWHtLSbR0-CXOvuazTU' \
        'kyU6r7vBkkYUV5LOXRZNE34SUQgz3s-TRyynOfPy5lGovye_mRkupXz2CeKQpLDP2-' \
        'MmOX5wSfYjZa1X1oOpE0SQ'

if __name__ == '__main__':
    # Создаем сессию работы с ВК
    vk_session = vk_api.VkApi(token=TOKEN)

    # Создаем и запускаем бота
    calorie_bot = CalorieBot(vk_session=vk_session)
    calorie_bot.start()
