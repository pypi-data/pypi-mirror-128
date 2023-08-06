import requests
from uuid import uuid4

class Login:
	def Tiwtter(Email,Pass):
		headers={
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
		'Content-Length': '901',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Cookie': 'personalization_id="v1_aFGvGiam7jnp1ks4ml5SUg=="; guest_id=v1%3A161776685629025416; gt=1379640315083112449; ct0=de4b75112a3f496676a1b2eb0c95ef65; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIA8a6p4AToMY3NyZl9p%250AZCIlM2RlMDA1MzYyNmJiMGQwYzQ1OGU2MjFhODY5ZGU5N2Y6B2lkIiU4ODM0%250AMjM5OTNlYjg0ZGExNzRiYTEwMWE0M2ZhYTM0Mw%253D%253D--f5b0bce9df3870f1a221ae914e684fbdc533d03d; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; _mb_tk=10908ac0975311eb868c135992f7d397',
		'Host': 'twitter.com',
		'Origin': 'https://twitter.com',
		'Referer': 'https://twitter.com/login?lang=ar',
		'TE': 'Trailers',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2708.48 Safari/537.36'
	        }
		data={
		'redirect_after_login': '/',
		'remember_me': '1',
		'authenticity_token': '10908ac0975311eb868c135992f7d397',
		'wfa': '1',
		'ui_metrics': '{\"rf\":{\"ab4c9cdc2d5d097a5b2ccee53072aff6d2b5b13f71cef1a233ff378523d85df3\":1,\"a51091a0c1e2864360d289e822acd0aa011b3c4cabba8a9bb010341e5f31c2d2\":84,\"a8d0bb821f997487272cd2b3121307ff1e2e13576a153c3ba61aab86c3064650\":-1,\"aecae417e3f9939c1163cbe2bde001c0484c0aa326b8aa3d2143e3a5038a00f9\":84},\"s\":\"MwhiG0C4XblDIuWnq4rc5-Ua8dvIM0Z5pOdEjuEZhWsl90uNoC_UbskKKH7nds_Qdv8yCm9Np0hTMJEaLH8ngeOQc5G9TA0q__LH7_UyHq8ZpV2ZyoY7FLtB-1-Vcv6gKo40yLb4XslpzJwMsnkzFlB8YYFRhf6crKeuqMC-86h3xytWcTuX9Hvk7f5xBWleKfUBkUTzQTwfq4PFpzm2CCyVNWfs-dmsED7ofFV6fRZjsYoqYbvPn7XhWO1Ixf11Xn5njCWtMZOoOExZNkU-9CGJjW_ywDxzs6Q-VZdXGqqS7cjOzD5TdDhAbzCWScfhqXpFQKmWnxbdNEgQ871dhAAAAXiqazyE\"}',
		'session[username_or_email]': Email,
		'session[password]': Pass
	        }
		url = 'https://twitter.com/sessions'

		req=requests.post(url,headers=headers,data=data)
		if ("ct0") in req.cookies:
			true="True"
			return true
			pass
		else:
			fall='False'
			return fall
			pass
	
	
	def Facebook(Email,Pass):
		url = 'https://mobile.facebook.com/login.php'
		headers = {
'User-Agent' : 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2687.84 Safari/537.36',
'Accept-Language' : 'en-US,en;q=0.5'
}
		data = {
    'email': Email,
    'pass': Pass
    }
		
		Face = requests.post(url, headers=headers, data=data).text
		if "xc_message" in Face:
			true='True'
			return true
			pass
		elif "checkpointSubmitButton-actual-button" in Face:
			ch='Checkpoint'
			return ch
			pass
			
		else:
			fall='False'
			return fall
			pass
			
			
	def Instagram(Email,Pass):
		r = requests.Session()
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
		req_login = r.post(url,headers=headers,data=data,allow_redirects=True)  
        
        #My Channel 
        
		if ("logged_in_user") in req_login.text:
		      	true='True'
		      	return true
		      	pass
		elif '"message":"challenge_required","challenge"' in req_login.text:
		      	sec='Security'
		      	return sec
		      	pass
		else:
		      	fall='False'
		      	return fall
		      	pass
		      	
		      	
	
	
        	
			
			
			