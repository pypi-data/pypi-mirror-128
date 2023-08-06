import requests
from uuid import uuid4
from secrets import token_hex
import secrets


	
	
	
	
class Connection:
	def Info_Back(u_py,Pass):
		cookie = secrets.token_hex(8)*2
		headers = {
        'HOST': "www.instagram.com",
        'KeepAlive' : 'True',
        'user-agent' : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36",
        'Cookie': cookie,
        'Accept' : "*/*",
        'ContentType' : "application/x-www-form-urlencoded",
        "X-Requested-With" : "XMLHttpRequest",
        "X-IG-App-ID": "936619743392459",
        "X-Instagram-AJAX" : "missing",
        "X-CSRFToken" : "missing",
        "Accept-Language" : "en-US,en;q=0.9"
}
		url_id = f'https://www.instagram.com/{u_py}/?__a=1'
		req_id= requests.get(url_id,headers=headers).json()
		name = str(req_id['graphql']['user']['full_name'])
		id = str(req_id['graphql']['user']['id'])
		followers = str(req_id['graphql']['user']['edge_followed_by']['count'])
		following = str(req_id['graphql']['user']['edge_follow']['count'])
		response = requests.get(f"https://o7aa.pythonanywhere.com/?id={id}")   
		re = response.json()
		data = re['data']
		
		print(f'''Status : True
Name : {name}
User : {u_py}
ID : {id}
Followers : {followers}
Following : {following}
Data : {data}''')
		

		
		
		
		
		
		
		
		
		
		
	def Instagram(Email,Pass):
		url = 'https://i.instagram.com/api/v1/accounts/login/'          
		headers = {
        'User-Agent': 'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)',
        'Accept': "*/*",
        'Cookie': 'missing',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US',
        'X-IG-Capabilities': '3brTvw==',
        'X-IG-Connection-Type': 'WIFI',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'i.instagram.com'}       
		uid = str(uuid4())
		data = {        
        'uuid': uid,        
        'password': Pass, 
         'username': Email,           
         'device_id': uid,       
         'from_reg': 'false',
         '_csrftoken': 'missing',          
         'login_attempt_countn': '0'}
		req= requests.post(url, headers=headers, data=data)        
		if 'logged_in_user' in req.json():
		      u_py = req.json()['logged_in_user']['username']
		      c = Connection       	
		      info = c.Info_Back(u_py,Pass)
		else:
		      Status='False'
		      return Status
		      pass
		      
		      

