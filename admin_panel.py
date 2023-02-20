from time import strftime, gmtime
from conf import Conf

def private(func):
    async def wrapper(*args, **kwargs):
        print("USER:", args[0].effective_chat.id, f" made request", end=" | ")
        print(strftime('%d %b %Y %H:%M:%S (+0)', gmtime()))
        if args[0].effective_chat.id in Conf.ACCESSORS_LIST:
            return await func(*args, **kwargs)
            # func(*args, **kwargs)
        else:
            print(f"Access refused for {args[0].effective_chat.id}", end = " | ")
            print(strftime('%d %b %Y %H:%M:%S (+0)', gmtime()))
            args[1].bot.send_message(chat_id=args[0].effective_chat.id, text = "Купить подписку, чтобы получить доступ к боту!")
            # return await func(*args, **kwargs) update.callback_query  callback_query.message.chat_id
    return wrapper