import requests
import random

class Proxy:
	def Checker(prx,proxy):
		if prx == 'Http':
			url = f'http://{proxy}/?noconnect'
			response = requests.get(url)
		
			if response.ok == True:
				true='True'
				return true
				pass
			else:
				fall='False'
				return fall
				pass
		elif prx == 'Https':
			url = f'https://{proxy}/?noconnect'
			response = requests.get(url)
		
			if response.ok == True:
				true='True'
				return true
				pass
			else:
				fall='False'
				return fall
				pass
			
			
	def Generator():
		num = 0
		
		
		m = '0987654321'

		stand = '8080','3128','8100','8888','8000','4004','9200','80','4001','83','10000','9080','999','8001','9090','82','59175','7890','3128','3256','8118','443','31280','30962','9080','41890','6666','53281','3629','9999','8080','8080','443','999','38178'
		us1 = str(''.join(random.choice(m)for i in range(1)))
		us2 = str(''.join(random.choice(m)for i in range(2)))
		us3 = str(''.join(random.choice(m)for i in range(3)))
		us4 = str(''.join(random.choice(m)for i in range(1)))
		us5 = str(''.join(random.choice(m)for i in range(2)))
		us6 = str(''.join(random.choice(m)for i in range(3)))
		us7 = str(''.join(random.choice(m)for i in range(1)))
		us8 = str(''.join(random.choice(m)for i in range(2)))
		us9 = str(''.join(random.choice(m)for i in range(3)))
		us10 = str(''.join(random.choice(m)for i in range(1)))
		us11 = str(''.join(random.choice(m)for i in range(2)))
		us12 = str(''.join(random.choice(m)for i in range(3)))
		us13 = str(''.join(random.choice(m)for i in range(1)))
		us14 = str(''.join(random.choice(m)for i in range(2)))
		us15 = str(''.join(random.choice(m)for i in range(3)))
		us16 = str(''.join(random.choice(m)for i in range(3)))
		us17 = str(''.join(random.choice(m)for i in range(2)))
		us18 = str(''.join(random.choice(m)for i in range(3)))
		us19 = str(''.join(random.choice(m)for i in range(2)))
		us20 = str(''.join(random.choice(m)for i in range(2)))
		us21 = str(''.join(random.choice(m)for i in range(3)))
		us22 = str(''.join(random.choice(m)for i in range(2)))
		us23 = str(''.join(random.choice(m)for i in range(2)))
		us24 = str(''.join(random.choice(m)for i in range(3)))
	
	
		rand = us1,us2,us3,us4,us5,us6,us7,us8,us9,us10,us11,us12,us13,us14,us15,us16,us17,us18,us19,us20,us21,us22,us23,us24
		proxy1 = random.choice(rand)
		proxy2 = random.choice(rand)
		proxy3 = random.choice(rand)
		proxy4 = random.choice(rand)
		proxy5 = random.choice(stand)
		proxy = (proxy1+'.'+proxy2+'.'+proxy3+'.'+proxy4+':'+proxy5)
		return proxy
		pass