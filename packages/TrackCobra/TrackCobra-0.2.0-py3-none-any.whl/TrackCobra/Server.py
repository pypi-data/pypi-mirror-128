import requests
from uuid import uuid4
from secrets import token_hex
import secrets
import os

class Connection:
	def phone_country(phone):
		if '964' in phone[0:4]:
			con1='Iraq 🇮🇶'
			return con1
			pass
			
		elif '20' in phone[0:3]:
			con='Egypt 🇪🇬'
			return con
			pass
			
		elif '593' in phone[0:4]:
			con='Ecuador 🇪🇨'
			return con
			pass
			
		elif '93' in phone[0:3]:
			con='Afghanistan 🇦🇫'
			return con
			pass
			
		elif '355' in phone[0:4]:
			con='Albania 🇦🇱'
			return con
			pass
			
		elif '684' in phone[0:4]:
			con='American Samoa 🇦🇸'
			return con
			pass
			
		elif '376' in phone[0:4]:
			con='Andorra 🇦🇩'
			return con
			pass
			
		elif '244' in phone[0:4]:
			con='Angola 🇦🇴'
			return con
			pass
			
		elif '264' in phone[0:4]:
			con='Anguilla 🇦🇮'
			return con
			pass
			
		elif '268' in phone[0:4]:
			con='Antigua and Barbuda'
			return con
			pass
			
		elif '54' in phone[0:3]:
			con='Argentina 🇦🇷'
			return con
			pass
			
		elif '374' in phone[0:4]:
			con='Armenia 🇦🇲'
			return con
			pass
			
		elif '297' in phone[0:4]:
			con='Aruba 🇦🇼'
			return con
			pass
			
		elif '61' in phone[0:3]:
			con='Australia 🇦🇺'
			return con
			pass
			
		elif '43' in phone[0:3]:
			con='Austria 🇦🇹'
			return con
			pass
			
		elif '994' in phone[0:4]:
			con='Azerbaijan 🇦🇿'
			return con
			pass
			
		elif '242' in phone[0:4]:
			con='Bahamas 🇧🇸'
			return con
			pass
			
		elif '973' in phone[0:4]:
			con='Bahrain 🇧🇭'
			return con
			pass
			
		elif '880' in phone[0:4]:
			con='Bangladesh 🇧🇩'
			return con
			pass
			
		elif '246' in phone[0:4]:
			con='Barbados 🇧🇧'
			return con
			pass
			
		elif '375' in phone[0:4]:
			con='Belarus 🇧🇾'
			return con
			pass
			
		elif '32' in phone[0:3]:
			con='Belgium 🇧🇪'
			return con
			pass
			
		elif '501' in phone[0:4]:
			con='Belize 🇧🇿'
			return con
			pass
			
		elif '229' in phone[0:4]:
			con='Benin 🇧🇯'
			return con
			pass
			
		elif '411' in phone[0:4]:
			con='Bermuda 🇧🇲'
			return con
			pass
			
		elif '974' in phone[0:4]:
			con='Bhutan 🇧🇹'
			return con
			pass
			
		elif '591' in phone[0:4]:
			con='Bolivia 🇧🇴'
			return con
			pass
			
		elif '267' in phone[0:4]:
			con='Botswana 🇧🇼'
			return con
			pass
			
		elif '264' in phone[0:4]:
			con='Anguilla 🇦🇮'
			return con
			pass
			
		elif '387' in phone[0:4]:
			con='Bosnia and Herzegovina'
			return con
			pass
			
		elif '55' in phone[0:3]:
			con='Brazil 🇧🇷'
			return con
			pass
			
		elif '359' in phone[0:4]:
			con='Bulgaria 🇧🇬'
			return con
			pass
			
		elif '673' in phone[0:4]:
			con='Brunei Darussalam'
			return con
			pass
			
		elif '226' in phone[0:4]:
			con='Burkina Faso 🇧🇫'
			return con
			pass
			
		elif '257' in phone[0:4]:
			con='Burundi 🇧🇮'
			return con
			pass
			
		elif '855' in phone[0:4]:
			con='Cambodia 🇰🇭'
			return con
			pass
			
		elif '237' in phone[0:4]:
			con='Cameroon 🇨🇲'
			return con
			pass
			
		elif '01' in phone[0:2]:
			con='Canada 🇨🇦'
			return con
			pass
			
		elif '238' in phone[0:4]:
			con='Cape Verde 🇨🇻'
			return con
			pass
			
		elif '345' in phone[0:4]:
			con='Cayman Islands 🇰🇾'
			return con
			pass
			
		elif '236' in phone[0:4]:
			con='Central African Republic 🇨🇫'
			return con
			pass
			
		elif '235' in phone[0:4]:
			con='Chad 🇹🇩'
			return con
			pass
			
		elif '56' in phone[0:3]:
			con='Chile 🇨🇱'
			return con
			pass
			
		elif '86' in phone[0:3]:
			con='China 🇨🇳'
			return con
			pass
			
		elif '61' in phone[0:3]:
			con='Christmas Island 🇨🇽'
			return con
			pass
			
		elif '61' in phone[0:3]:
			con='Cocos (Keeling) Islands 🇨🇨'
			return con
			pass
			
		elif '57' in phone[0:3]:
			con='Colombia 🇨🇴'
			return con
			pass
			
		elif '269' in phone[0:4]:
			con='Comoros 🇰🇲'
			return con
			pass
			
		elif '242' in phone[0:4]:
			con='Congo (Brazzaville) 🇨🇬'
			return con
			pass
			
		elif '243' in phone[0:4]:
			con='Congo (Kinshasa) 🇨🇩'
			return con
			pass
			
		elif '682' in phone[0:4]:
			con='Cook Islands 🇨🇰'
			return con
			pass
			
		elif '506' in phone[0:4]:
			con='Costa Rica 🇨🇷'
			return con
			pass
			
		elif '225' in phone[0:4]:
			con="Côte D'Ivoire (Ivory Coast) 🇨🇮"
			return con
			pass
			
		elif '385' in phone[0:4]:
			con='Croatia (Hrvatska) 🇭🇷'
			return con
			pass
			
		elif '53' in phone[0:3]:
			con='Cuba 🇨🇺'
			return con
			pass
			
		elif '357' in phone[0:4]:
			con='Cyprus 🇨🇾'
			return con
			pass
			
		elif '220' in phone[0:4]:
			con='Czech Republic 🇨🇿'
			return con
			pass
				
		elif '45' in phone[0:3]:
			con='Denmark 🇩🇰'
			return con
			pass
			
		elif '253' in phone[0:4]:
			con='Djibouti 🇩🇯'
			return con
			pass
			
		elif '767' in phone[0:4]:
			con='Dominica 🇩🇲'
			return con
			pass
			
		elif '809' and '829' in phone[0:4]:
			con='Dominican Republic 🇩🇴'
			return con
			pass
			
		elif '503' in phone[0:4]:
			con='El Salvador 🇸🇻'
			return con
			pass
			
		elif '240' in phone[0:4]:
			con='Equatorial Guinea 🇬🇶'
			return con
			pass
			
		elif '291' in phone[0:4]:
			con='Eritrea 🇪🇷'
			return con
			pass
			
		elif '372' in phone[0:4]:
			con='Estonia 🇪🇪'
			return con
			pass
			
		elif '251' in phone[0:4]:
			con='Ethiopia 🇪🇹'
			return con
			pass
			
		elif '500' in phone[0:4]:
			con='Falkland Islands (Malvinas) 🇫🇰'
			return con
			pass
			
		elif '298' in phone[0:4]:
			con='Faroe Islands 🇫🇴'
			return con
			pass
			
		elif '679' in phone[0:4]:
			con='Fiji 🇫🇯'
			return con
			pass
			
		elif '358' in phone[0:3]:
			con='Finland 🇫🇮'
			return con
			pass
			
		elif '33' in phone[0:3]:
			con='France 🇫🇷'
			return con
			pass
			
		elif '594' in phone[0:4]:
			con='French Guiana 🇬🇫'
			return con
			pass
			
		elif '689' in phone[0:4]:
			con='French Polynesia 🇵🇫'
			return con
			pass
			
		elif '241' in phone[0:4]:
			con='Gabon 🇬🇦'
			return con
			pass
			
		elif '220' in phone[0:4]:
			con='Gambia 🇬🇲'
			return con
			pass
			
		elif '995' in phone[0:4]:
			con='Georgia 🇬🇪'
			return con
			pass
			
		elif '49' in phone[0:3]:
			con='Germany 🇩🇪'
			return con
			pass
			
		elif '233' in phone[0:4]:
			con='Ghana 🇬🇭'
			return con
			pass
			
		elif '350' in phone[0:4]:
			con='Gibraltar 🇬🇮'
			return con
			pass
			
		elif '30' in phone[0:4]:
			con='Greece 🇬🇷'
			return con
			pass
			
		elif '299' in phone[0:4]:
			con='Greenland 🇬🇱'
			return con
			pass
			
		elif '473' in phone[0:4]:
			con='Grenada 🇬🇩'
			return con
			pass
			
		elif '590' in phone[0:4]:
			con='Guadeloupe 🇬🇵'
			return con
			pass
			
		elif '671' in phone[0:4]:
			con='Guam 🇬🇺'
			return con
			pass
			
		elif '502' in phone[0:4]:
			con='Guatemala 🇬🇹'
			return con
			pass
			
		elif '224' in phone[0:4]:
			con='Guinea 🇬🇳'
			return con
			pass
			
		elif '245' in phone[0:4]:
			con='Guinea-Bissau 🇬🇼'
			return con
			pass
			
		elif '592' in phone[0:4]:
			con='Guyana 🇬🇾'
			return con
			pass
			
		elif '509' in phone[0:4]:
			con='Haiti 🇭🇹'
			return con
			pass
			
		elif '379' in phone[0:4]:
			con='Holy See (Vatican City State)🇻🇦'
			return con
			pass
			
		elif '504' in phone[0:4]:
			con='Honduras 🇭🇳'
			return con
			pass
			
		elif '852' in phone[0:4]:
			con='Hong Kong 🇭🇰'
			return con
			pass
			
		elif '36' in phone[0:3]:
			con='Hungary 🇭🇺'
			return con
			pass
			
		elif '354' in phone[0:4]:
			con='Iceland 🇮🇸'
			return con
			pass
			
		elif '91' in phone[0:3]:
			con='India 🇮🇳'
			return con
			pass
			
		elif '62' in phone[0:3]:
			con='Indonesia 🇮🇩'
			return con
			pass
			
		elif '98' in phone[0:3]:
			con='Iran 🇮🇷'
			return con
			pass
			
		elif '353' in phone[0:4]:
			con='Ireland 🇮🇪'
			return con
			pass
			
		elif '972' in phone[0:4]:
			con='Israel 🇮🇱💩 --> Free Palestinian 🇵🇸'
			return con
			pass
			
		elif '39' in phone[0:3]:
			con='Italy 🇮🇹'
			return con
			pass
			
		elif '876' in phone[0:4]:
			con='Jamaica 🇯🇲'
			return con
			pass
			
		elif '81' in phone[0:3]:
			con='Japan 🇯🇵'
			return con
			pass
			
		elif '962' in phone[0:4]:
			con='Jordan 🇯🇴'
			return con
			pass
			
		elif '6' in phone[0:1]:
			con='Kazakhstan 🇰🇿'
			return con
			pass
			
		elif '254' in phone[0:4]:
			con='Kenya 🇰🇪'
			return con
			pass
			
		elif '686' in phone[0:4]:
			con='Kiribati 🇰🇮'
			return con
			pass
			
		elif '850' in phone[0:4]:
			con='Korea (North) 🇰🇵'
			return con
			pass
			
		elif '82' in phone[0:3]:
			con='Korea (South) 🇰🇷'
			return con
			pass
			
		elif '965' in phone[0:4]:
			con='Kuwait 🇰🇼'
			return con
			pass
			
		elif '996' in phone[0:3]:
			con='Kyrgyzstan 🇰🇬'
			return con
			pass
			
		elif '856' in phone[0:4]:
			con='Laos 🇱🇦'
			return con
			pass
			
		elif '371' in phone[0:4]:
			con='Latvia 🇱🇻'
			return con
			pass
			
		elif '961' in phone[0:4]:
			con='Lebanon 🇱🇧'
			return con
			pass
			
		elif '266' in phone[0:4]:
			con='Lesotho 🇱🇸'
			return con
			pass
			
		elif '231' in phone[0:4]:
			con='Liberia 🇱🇷'
			return con
			pass
			
		elif '218' in phone[0:4]:
			con='Libya 🇱🇾'
			return con
			pass
			
		elif '423' in phone[0:4]:
			con='Liechtenstein 🇱🇮'
			return con
			pass
			
		elif '370' in phone[0:4]:
			con='Lithuania 🇱🇹'
			return con
			pass
			
		elif '352' in phone[0:4]:
			con='Luxembourg 🇱🇺'
			return con
			pass
			
		elif '853' in phone[0:4]:
			con='Macao 🇲🇴'
			return con
			pass
			
		elif '389' in phone[0:4]:
			con='Macedonia 🇲🇰'
			return con
			pass
			
		elif '261' in phone[0:4]:
			con='Madagascar 🇲🇬'
			return con
			pass
			
		elif '265' in phone[0:4]:
			con='Malawi 🇲🇼'
			return con
			pass
			
		elif '60' in phone[0:3]:
			con='Malaysia 🇲🇾'
			return con
			pass
			
		elif '960' in phone[0:4]:
			con='Maldives 🇲🇻'
			return con
			pass
			
		elif '233' in phone[0:4]:
			con='Mali 🇲🇱'
			return con
			pass
			
		elif '356' in phone[0:4]:
			con='Malta 🇲🇹'
			return con
			pass
			
		elif '692' in phone[0:4]:
			con='Marshall Islands 🇲🇭'
			return con
			pass
			
		elif '596' in phone[0:4]:
			con='Martinique 🇲🇶'
			return con
			pass
			
		elif '222' in phone[0:4]:
			con='Mauritania 🇲🇷'
			return con
			pass
			
		elif '230' in phone[0:4]:
			con='Mauritius 🇲🇺'
			return con
			pass
			
		elif '262' in phone[0:4]:
			con="Mayotte 🇾🇹"
			return con
			pass
			
		elif '52' in phone[0:3]:
			con='Mexico 🇲🇽'
			return con
			pass
			
		elif '691' in phone[0:4]:
			con='Micronesia 🇫🇲'
			return con
			pass
			
		elif '373' in phone[0:4]:
			con='Moldova 🇲🇩'
			return con
			pass
			
		elif '377' in phone[0:4]:
			con='Monaco 🇲🇨'
			return con
			pass
			
		elif '976' in phone[0:4]:
			con='Mongolia 🇲🇳'
			return con
			pass
			
		elif '382' in phone[0:4]:
			con='Montenegro 🇲🇪'
			return con
			pass
			
		elif '664' in phone[0:4]:
			con='Montserrat 🇲🇸'
			return con
			pass
			
		elif '212' in phone[0:4]:
			con='Morocco 🇲🇦'
			return con
			pass
			
		elif '258' in phone[0:4]:
			con='Mozambique 🇲🇿'
			return con
			pass
			
		elif '95' in phone[0:3]:
			con='Myanmar 🇲🇲'
			return con
			pass
			
		elif '264' in phone[0:4]:
			con='Namibia 🇳🇦'
			return con
			pass
			
		elif '674' in phone[0:4]:
			con='Nauru 🇳🇷'
			return con
			pass
			
		elif '977' in phone[0:4]:
			con='Nepal🇳🇵'
			return con
			pass
			
		elif '31' in phone[0:3]:
			con='Netherlands 🇳🇱'
			return con
			pass
			
		elif '599' in phone[0:4]:
			con='Netherlands Antilles 🇳🇱'
			return con
			pass
			
		elif '687' in phone[0:4]:
			con='New Caledonia 🇳🇨'
			return con
			pass
			
		elif '64' in phone[0:3]:
			con='New Zealand 🇳🇿'
			return con
			pass
			
		elif '505' in phone[0:4]:
			con='Nicaragua 🇳🇮'
			return con
			pass
			
		elif '227' in phone[0:4]:
			con='Niger 🇳🇪'
			return con
			pass
			
		elif '234' in phone[0:4]:
			con='Nigeria 🇳🇬'
			return con
			pass
			
		elif '683' in phone[0:4]:
			con='Niue 🇳🇺'
			return con
			pass
			
		elif '672' in phone[0:4]:
			con='Norfolk Island 🇳🇫'
			return con
			pass
			
		elif '670' in phone[0:4]:
			con='Northern Mariana Islands 🇲🇵'
			return con
			pass
			
		elif '47' in phone[0:3]:
			con='Norway 🇳🇴'
			return con
			pass
			
		elif '968' in phone[0:4]:
			con='Oman 🇴🇲'
			return con
			pass
			
		elif '92' in phone[0:3]:
			con='Pakistan 🇵🇰'
			return con
			pass
			
		elif '680' in phone[0:4]:
			con='Palau 🇵🇼'
			return con
			pass
			
		elif '970' in phone[0:4]:
			con='Palestinian 🇵🇸'
			return con
			pass
			
		elif '507' in phone[0:4]:
			con='Panama 🇵🇦'
			return con
			pass
			
		elif '675' in phone[0:4]:
			con='Papua New Guinea 🇵🇬'
			return con
			pass
			
		elif '595' in phone[0:4]:
			con='Paraguay 🇵🇾'
			return con
			pass
			
		elif '51' in phone[0:3]:
			con='Peru 🇵🇪'
			return con
			pass
			
		elif '63' in phone[0:3]:
			con='Philippines 🇵🇭'
			return con
			pass
			
		elif '870' in phone[0:4]:
			con='Pitcairn'
			return con
			pass
			
		elif '48' in phone[0:3]:
			con='Poland 🇵🇱'
			return con
			pass
			
		elif '351' in phone[0:4]:
			con='Portugal 🇵🇹'
			return con
			pass
			
		elif '787'  in phone[0:4]:
			con='Puerto Rico 🇵🇷'
			return con
			pass
			
		elif '974' in phone[0:4]:
			con='Qatar 🇶🇦'
			return con
			pass
			
		elif '262' in phone[0:4]:
			con='Réunion 🇷🇪'
			return con
			pass
			
		elif '40' in phone[0:3]:
			con='Romania 🇷🇴'
			return con
			pass
			
		elif '07' in phone[0:1]:
			con='Russian 🇷🇺'
			return con
			pass
			
		elif '250' in phone[0:4]:
			con='Rwanda 🇷🇼'
			return con
			pass
			
		elif '290' in phone[0:4]:
			con='Saint Helena'
			return con
			pass
			
		elif '869' in phone[0:4]:
			con='Saint Kitts'
			return con
			pass
			
		elif '758' in phone[0:4]:
			con='Saint Lucia'
			return con
			pass
			
		elif '508' in phone[0:4]:
			con='Saint Pierre'
			return con
			pass
			
		elif '784' in phone[0:4]:
			con='Saint Vincent'
			return con
			pass
			
		elif '685' in phone[0:4]:
			con='Samoa 🇼🇸'
			return con
			pass
			
		elif '378' in phone[0:4]:
			con='San Marino 🇸🇲'
			return con
			pass
			
		elif '239' in phone[0:4]:
			con='São Tomé'
			return con
			pass
			
		elif '966' in phone[0:4]:
			con='Saudi Arabia 🇸🇦'
			return con
			pass
			
		elif '221' in phone[0:4]:
			con='Senegal 🇸🇳'
			return con
			pass
			
		elif '381' in phone[0:4]:
			con='Serbia 🇷🇸'
			return con
			pass
			
		elif '248' in phone[0:4]:
			con='Seychelles 🇸🇨'
			return con
			pass
			
		elif '232' in phone[0:4]:
			con='Sierra Leone 🇸🇱'
			return con
			pass
			
		elif '65' in phone[0:3]:
			con='Singapore 🇸🇬'
			return con
			pass
			
		elif '421' in phone[0:4]:
			con='Slovakia 🇸🇰'
			return con
			pass
			
		elif '386' in phone[0:4]:
			con='Slovenia 🇸🇮'
			return con
			pass
			
		elif '677' in phone[0:4]:
			con='Solomon Islands 🇸🇧'
			return con
			pass
			
		elif '252' in phone[0:4]:
			con='Somalia 🇸🇴'
			return con
			pass
			
		elif '27' in phone[0:3]:
			con='South Africa 🇿🇦'
			return con
			pass
			
		elif '34' in phone[0:3]:
			con='Spain 🇪🇸'
			return con
			pass
			
		elif '94' in phone[0:3]:
			con='Sri Lanka 🇱🇰'
			return con
			pass
			
		elif '249' in phone[0:4]:
			con='Sudan 🇸🇩'
			return con
			pass
			
		elif '597' in phone[0:4]:
			con='Suriname 🇸🇷'
			return con
			pass
			
		elif '47' in phone[0:3]:
			con='Svalbard'
			return con
			pass
			
		elif '268' in phone[0:4]:
			con='Swaziland 🇸🇿'
			return con
			pass
			
		elif '46' in phone[0:3]:
			con='Sweden 🇸🇪'
			return con
			pass
			
		elif '41' in phone[0:3]:
			con='Switzerland🇨🇭'
			return con
			pass
			
		elif '963' in phone[0:4]:
			con='Syria 🇸🇾'
			return con
			pass
			
		elif '886' in phone[0:4]:
			con='Taiwan 🇹🇼'
			return con
			pass
			
		elif '992' in phone[0:4]:
			con='Tajikistan 🇹🇯'
			return con
			pass
			
		elif '255' in phone[0:4]:
			con='Tanzania 🇹🇿'
			return con
			pass
			
		elif '66' in phone[0:3]:
			con='Thailand 🇹🇭'
			return con
			pass
			
		elif '670' in phone[0:4]:
			con='Timor-Leste 🇹🇱'
			return con
			pass
			
		elif '228' in phone[0:4]:
			con='Togo 🇹🇬'
			return con
			pass
			
		elif '690' in phone[0:4]:
			con='Tokelau 🇹🇰'
			return con
			pass
			
		elif '676' in phone[0:4]:
			con='Tonga 🇹🇴'
			return con
			pass
			
		elif '868' in phone[0:4]:
			con="Trinidad"
			return con
			pass
			
		elif '216' in phone[0:4]:
			con='Tunisia 🇹🇳'
			return con
			pass
			
		elif '90' in phone[0:3]:
			con='Turkey 🇹🇷'
			return con
			pass
			
		elif '993' in phone[0:4]:
			con='Turkmenistan 🇹🇲'
			return con
			pass
			
		elif '649' in phone[0:4]:
			con='Turks'
			return con
			pass
			
		elif '688' in phone[0:4]:
			con='Tuvalu 🇹🇻'
			return con
			pass
			
		elif '256' in phone[0:4]:
			con='Uganda 🇺🇬'
			return con
			pass
			
		elif '380' in phone[0:4]:
			con='Ukraine 🇺🇦'
			return con
			pass
			
		elif '971' in phone[0:4]:
			con='United Arab Emirates 🇦🇪'
			return con
			pass
			
		elif '44' in phone[0:3]:
			con='United Kingdom 🇬🇧'
			return con
			pass
			
		elif '1' in phone[0:1]:
			con='United States of America 🇺🇸'
			return con
			pass
			
		elif '598' in phone[0:4]:
			con='Uruguay 🇺🇾'
			return con
			pass
			
		elif '998' in phone[0:4]:
			con='Uzbekistan 🇺🇿'
			return con
			pass
			
		elif '678' in phone[0:4]:
			con='Vanuatu 🇻🇺'
			return con
			pass
			
		elif '58' in phone[0:3]:
			con='Venezuela 🇻🇪'
			return con
			pass
			
		elif '84' in phone[0:3]:
			con='Viet Nam'
			return con
			pass
			
		elif '284' in phone[0:4]:
			con='Virgin Islands'
			return con
			pass
			
		elif '340' in phone[0:4]:
			con='Virgin Islands'
			return con
			pass
			
		elif '681' in phone[0:4]:
			con='Wallis'
			return con
			pass
			
		elif '967' in phone[0:4]:
			con='Yemen 🇾🇪'
			return con
			pass
			
		elif '260' in phone[0:4]:
			con='Zambia 🇿🇲'
			return con
			pass
			
		elif '263' in phone[0:4]:
			con='Zimbabwe 🇿🇼'
			return con
			pass
			
		else:
			inot="Soon..."
			return inot
			pass

	def Info_Back(u_py,Pass,Email):
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
		professional = str(req_id['graphql']['user']['is_professional_account'])
		response = requests.get(f"https://o7aa.pythonanywhere.com/?id={id}")   
		re = response.json()
		data = re['data']
		
		c4 = Connection
		country = c4.phone_country(Email)
		f1 = name # Name
		f2 = u_py # Username
		f3 = Pass # Passwd
		f4 = followers # Followers
		f5 = following # Following
		f6 = professional # Professional Acc
		f7 = id # ID Acc
		f8 = data # Data Acc
		f9 = country # Country Acc
		
		f = open('All_The_Information.txt','w')
		f.write(f'''Name:{name}
User:{u_py}
Pass:{Pass}
Followers:{followers}
Following:{following}
Professional:{professional}
ID:{id}
Data:{data}
Country:{country}''')


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
		      info = c.Info_Back(u_py,Pass,Email)
		      true='True'
		      return true
		      pass
		      
		elif 'message' and "challenge_required" and "challenge" in req.text:
		      	sec='Security'
		      	return sec
		      	pass
		      
		else:
		      Status='False'
		      return Status
		      pass
		      
	def Information(passwd,formation):
		if passwd == 'Show':
		      f = open('All_The_Information.txt','r')
		      insta1 = f.readline()
		      insta2 = f.readline()
		      insta3 = f.readline()
		      insta4 = f.readline()
		      insta5 = f.readline()
		      insta6 = f.readline()
		      insta7 = f.readline()
		      insta8 = f.readline()
		      insta9 = f.readline()		      
		      if formation == 'Name':
		      	return insta1
		      	pass
		      	
		      elif formation == 'User':
		      	return insta2
		      	pass

		      elif formation == 'Pass':
		      	return insta3
		      	pass

		      elif formation == 'Followers':
		      	return insta4
		      	pass

		      elif formation == 'Following':
		      	return insta5
		      	pass

		      elif formation == 'Pro':
		      	return insta6
		      	pass

		      elif formation == 'ID':
		      	return insta7
		      	pass

		      elif formation == 'Data':
		      	return insta8
		      	pass

		      elif formation == 'Country':
		      	return insta9
		      	pass

		      elif formation == 'All':
		      	fil = open('All_The_Information.txt','r')
		      	all = fil.read()
		      	return all
		      	pass

		      	
		      	
		      
		   
		   
		   
	def Bin(bin,choice):
		url = f'https://lookup.binlist.net/{bin}'
		response = requests.get(url)
		if 'Scheme' and 'Se' in choice:
			if 'number' in response.text:
				scheme = response.json()['scheme']
				print(scheme)
			else:
				fall='False'
				return fall
				pass
				
		elif 'Type' and 'Te' in choice:
			if 'number' in response.text:
				type = response.json()['type']
				print(type)
			else:
				fall='False'
				return fall
				pass
				
		elif 'Brand' and 'Bd' in choice:
			if 'number' in response.text:
				brand = response.json()['brand']
				print(brand)
			else:
				fall='False'
				return fall
				pass
				
		elif 'Alpha2' and 'A2' in choice:
			if 'number' in response.text:
				alpha2 = response.json()['country']['alpha2']
				print(alpha2)
			else:
				fall='False'
				return fall
				pass
				
		elif 'Name' and 'Ne' in choice:
			if 'number' in response.text:
				name = response.json()['country']['name']
				print(name)
			else:
				fall='False'
				return fall
				pass
				
		elif 'Emoji' and 'Ei' in choice:
			if 'number' in response.text:
				emoji = response.json()['country']['emoji']
				print(emoji)
			else:
				fall='False'
				return fall
				pass
				
		elif 'Currency' and 'Cy' in choice:
			if 'number' in response.text:
				currency = response.json()['country']['currency']
				print(currency)
			else:
				fall='False'
				return fall
				pass
				
		elif 'Latitude' and 'La' in choice:
			if 'number' in response.text:
				latitude = response.json()['country']['latitude']
				print(latitude)
			else:
				fall='False'
				return fall
				pass
		elif 'Longitude' and 'Lo' in choice:
			if 'number' in response.text:
				longitude = response.json()['country']['longitude']
				print(longitude)
			else:
				fall='False'
				return fall
				pass
				
		elif 'Bank' and 'Bk' in choice:
			if 'number' in response.text:
				bank = response.json()['bank']['name']
				print(Bank)
			else:
				fall='False'
				return fall
				pass
				
		elif 'Url' in choice:
			if 'number' in response.text:
				url = response.json()['bank']['url']
				print(url)
			else:
				fall='False'
				return fall
				pass
			
		elif 'Phone' and 'Pe' in choice:
			if 'number' in response.text:
				phone = response.json()['bank']['phone']				
				print(phone)
			else:
				fall='False'
				return fall
				pass		
				
		elif 'All' in choice:
			if 'number' in response.text:
				scheme = response.json()['scheme']
				type = response.json()['type']
				brand = response.json()['brand']
				alpha2 = response.json()['country']['alpha2']
				name = response.json()['country']['name']
				emoji = response.json()['country']['emoji']
				currency = response.json()['country']['currency']
				latitude = response.json()['country']['latitude']
				longitude = response.json()['country']['longitude']
				bank = response.json()['bank']['name']
				url = response.json()['bank']['url']
				phone = response.json()['bank']['phone']
				information=f'''Scheme : {scheme}
Type : {type}
Brand : {brand}
Alpha2 : {alpha2}
Name : {name}
Emoji : {emoji}
Currency : {currency}
Latitude : {latitude}
Longitude : {longitude}
Bank : {bank}
Url : {url}
Phone : {phone}
'''
				return information
				pass
			else:
				fall='False'
				return fall
				pass