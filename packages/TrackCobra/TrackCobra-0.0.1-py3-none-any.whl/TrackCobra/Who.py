import requests
url = 'https://ipinfo.io/'
class Who_Iam:
	
	def Ip():
		response = requests.get(url)
		ip = response.json()['ip']
		return ip
		pass
		
		
	def City():
		response = requests.get(url)
		city = response.json()['city']
		return city
		pass
		
	
	def Region():
		response = requests.get(url)
		region = response.json()['region']
		return region
		pass
		
		
	def Country():
		response = requests.get(url)
		country = response.json()['country']
		return country
		pass
		
		
	def Loc():
		response = requests.get(url)
		loc = response.json()['loc']
		return loc
		pass
		
		
	def Org():
		response = requests.get(url)
		org = response.json()['org']
		return org
		pass
		
	
	def Timezone():
		response = requests.get(url)
		timezone = response.json()['timezone']
		return timezone
		pass
		
		
	def All():
		response = requests.get(url)
		all = f"""IP : {response.json()['ip']}
City : {response.json()['city']}
Region : {response.json()['region']}
Country : {response.json()['country']}
Timezone : {response.json()['timezone']}
Loc : {response.json()['loc']}
Org : {response.json()['org']}"""
		return all
		pass	
	
		
		
