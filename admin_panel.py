from time import strftime, gmtime
from conf import Conf

def private(func):
    async def wrapper(*args, **kwargs):
        print("USER:", args[0].effective_chat.id, f" made request", end=" | ")
        print(strftime('%d %b %Y %H:%M:%S (+0)', gmtime()))
        if args[0].effective_chat.id in Conf.ACCESSORS_LIST:
            func(*args, **kwargs)
        else:
            print(f"Access refused for {args[0].effective_chat.id}", end = " | ")
            print(strftime('%d %b %Y %H:%M:%S (+0)', gmtime()))
            args[0].message.reply_text("Купите подписку")
            return await func(*args, **kwargs)
    return wrapper