import requests
url = 'https://ipinfo.io/'
class Who_Iam:
	
	def Information(form):
		if form == 'IP':
			response = requests.get(url)
			ip = response.json()['ip']
			return ip
			pass
		elif form == 'City':
			response = requests.get(url)
			city = response.json()['city']
			return city
			pass
		elif form == 'Region':
			response = requests.get(url)
			region = response.json()['region']
			return region
			pass
		elif form == 'Country':
			response = requests.get(url)
			country = response.json()['country']
			return country
			pass
		elif form == 'Location':
			response = requests.get(url)
			loc = response.json()['loc']
			return loc
			pass	
		elif form == 'Org':
			response = requests.get(url)
			org = response.json()['org']
			return org
			pass
		elif form == 'Timezone':
			response = requests.get(url)
			timezone = response.json()['timezone']
			return timezone
			pass
		elif form == 'All':
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