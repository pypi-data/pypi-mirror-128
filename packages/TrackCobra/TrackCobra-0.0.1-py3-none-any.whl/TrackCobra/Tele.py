import requests

class Telegram:
	def Telegram_Send(token,id,message):
		t = requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text={message}")
		Send='Successfully'
		return Send
		pass
	
	
	
	def Telegram_Edit(token,id,edit):
		
		start_msg = requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text=MrGps").json()
		id_msg=(start_msg['result']["message_id"])
		edit1 = requests.post(f"https://api.telegram.org/bot{token}/editmessagetext?chat_id={id}&message_id={id_msg}&text={edit}")
		Send='Successfully'
		return Send
		pass
       
		
		
		
		
	