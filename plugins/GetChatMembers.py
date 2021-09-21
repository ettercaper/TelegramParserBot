from pyrogram import Client, filters
import json, os




@Client.on_message(filters.command("parse_users", "/", True) & filters.chat("me"))
def parse_users_from_chat(client, message):
	
	target = message.command[1] if len(message.command) > 1 else None
	
	if not target:
		client.send_message("me", "Не указан аргумент для этой функции")
		
	else:
		chat = client.get_chat(target)
		
		if chat.type not in ["prop", "supergroup"]:
			client.send_message("me", "Вы указали не чат")
			return True
		
		chat = chat.username if chat.username else chat.id
		data = []
		
		for m in client.iter_chat_members(target):
			data.append({
				"chat_id": m.user.id,
				"first_name": m.user.first_name,
				"last_name": m.user.last_name,
				"username": m.user.username,
				"phone": m.user.phone_number})
		
		file = f"users_{chat}.json"
		
		with open(file, "w", encoding = "utf-8") as f:
			json.dump(data, f, ensure_ascii = False, indent = 2)
		
		client.send_document("me", open(file, "rb"))
		
		os.remove(file)
		
		