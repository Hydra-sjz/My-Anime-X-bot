from anibot.utils2.Database.mongo import db


db = db.CHATS


def get_chats():
    chats = []
    for x in db.find():
        chats.append(x["chat_id"])
    return chats

def add_chat(chat_id: int):
    if chat_id in get_chats():
         return
    db.insert_one({"chat_id": chat_id})

def remove_chat(chat_id: int):
    if not chat_id in get_chats():
        return
    x = db.find_one({"chat_id": chat_id})
    db.delete_one(x)
