#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.dispatch import dispatcher
from django.db.models import signals
import geotagging.models as models
from geotagging.models import Continent, Country


def init_data():
    CONTINENTS = [
        ('AS', {'slug': 'asia', 'name': 'Asia'}),
        ('AF', {'slug': 'africa', 'name': 'Africa'}),
        ('EU', {'slug': 'europe', 'name': 'Europe'}),
        ('NA', {'slug': 'north-america', 'name': 'North America'}),
        ('SA', {'slug': 'south-america', 'name': 'South America'}),
        ('OC', {'slug': 'oceania', 'name': 'Oceania'}),
        ('AN', {'slug': 'antarctica', 'name': 'Antarctica'}),
        ]

    if settings.DEBUG:
        print "Geotagging: Populating Continents"

    for code, defaults in CONTINENTS:
        cont, c = Continent.objects.get_or_create(code=code, defaults=defaults)
        if not c:
            break

    COUNTRIES = [
        ('AF', {'continent': 'AS', 'name': 'Afghanistan', 'slug'
         : 'afghanistan'}),
        ('AL', {'continent': 'EU', 'name': 'Albania', 'slug': 'albania'
         }),
        ('DZ', {'continent': 'AF', 'name': 'Algeria', 'slug': 'algeria'
         }),
        ('AS', {'continent': 'OC', 'name': 'American Samoa', 'slug'
         : 'american-samoa'}),
        ('AD', {'continent': 'EU', 'name': 'Andorra', 'slug': 'andorra'
         }),
        ('AO', {'continent': 'AF', 'name': 'Angola', 'slug': 'angola'
         }),
        ('AI', {'continent': 'SA', 'name': 'Anguilla', 'slug'
         : 'anguilla'}),
        ('AQ', {'continent': 'AN', 'name': 'Antarctica', 'slug'
         : 'antarctica'}),
        ('AG', {'continent': 'SA', 'name': 'Antigua and Barbuda', 'slug'
         : 'antigua-and-barbuda'}),
        ('AR', {'continent': 'SA', 'name': 'Argentina', 'slug'
         : 'argentina'}),
        ('AM', {'continent': 'AS', 'name': 'Armenia', 'slug': 'armenia'
         }),
        ('AW', {'continent': 'SA', 'name': 'Aruba', 'slug': 'aruba'}),
        ('AP', {'continent': 'AS', 'name': "Asia\/Pacific Region",
         'slug': 'asiapacific-region'}),
        ('AU', {'continent': 'OC', 'name': 'Australia', 'slug'
         : 'australia'}),
        ('AT', {'continent': 'EU', 'name': 'Austria', 'slug': 'austria'
         }),
        ('AZ', {'continent': 'AS', 'name': 'Azerbaijan', 'slug'
         : 'azerbaijan'}),
        ('BS', {'continent': 'SA', 'name': 'Bahamas', 'slug': 'bahamas'
         }),
        ('BH', {'continent': 'AS', 'name': 'Bahrain', 'slug': 'bahrain'
         }),
        ('BD', {'continent': 'AS', 'name': 'Bangladesh', 'slug'
         : 'bangladesh'}),
        ('BB', {'continent': 'SA', 'name': 'Barbados', 'slug'
         : 'barbados'}),
        ('BY', {'continent': 'EU', 'name': 'Belarus', 'slug': 'belarus'
         }),
        ('BE', {'continent': 'EU', 'name': 'Belgium', 'slug': 'belgium'
         }),
        ('BZ', {'continent': 'SA', 'name': 'Belize', 'slug': 'belize'
         }),
        ('BJ', {'continent': 'AF', 'name': 'Benin', 'slug': 'benin'}),
        ('BM', {'continent': 'SA', 'name': 'Bermuda', 'slug': 'bermuda'
         }),
        ('BT', {'continent': 'AS', 'name': 'Bhutan', 'slug': 'bhutan'
         }),
        ('BO', {'continent': 'SA', 'name': 'Bolivia', 'slug': 'bolivia'
         }),
        ('BA', {'continent': 'EU', 'name': 'Bosnia and Herzegovina',
         'slug': 'bosnia-and-herzegovina'}),
        ('BW', {'continent': 'AF', 'name': 'Botswana', 'slug'
         : 'botswana'}),
        ('BV', {'continent': 'AF', 'name': 'Bouvet Island', 'slug'
         : 'bouvet-island'}),
        ('BR', {'continent': 'SA', 'name': 'Brazil', 'slug': 'brazil'
         }),
        ('IO', {'continent': 'AS', 'name'
         : 'British Indian Ocean Territory', 'slug'
         : 'british-indian-ocean-territory'}),
        ('BN', {'continent': 'AS', 'name': 'Brunei Darussalam', 'slug'
         : 'brunei-darussalam'}),
        ('BG', {'continent': 'EU', 'name': 'Bulgaria', 'slug'
         : 'bulgaria'}),
        ('BF', {'continent': 'AF', 'name': 'Burkina Faso', 'slug'
         : 'burkina-faso'}),
        ('BI', {'continent': 'AF', 'name': 'Burundi', 'slug': 'burundi'
         }),
        ('KH', {'continent': 'AS', 'name': 'Cambodia', 'slug'
         : 'cambodia'}),
        ('CM', {'continent': 'AF', 'name': 'Cameroon', 'slug'
         : 'cameroon'}),
        ('CA', {'continent': 'NA', 'name': 'Canada', 'slug': 'canada'
         }),
        ('CV', {'continent': 'AF', 'name': 'Cape Verde', 'slug'
         : 'cape-verde'}),
        ('KY', {'continent': 'SA', 'name': 'Cayman Islands', 'slug'
         : 'cayman-islands'}),
        ('CF', {'continent': 'AF', 'name': 'Central African Republic',
         'slug': 'central-african-republic'}),
        ('TD', {'continent': 'AF', 'name': 'Chad', 'slug': 'chad'}),
        ('CL', {'continent': 'SA', 'name': 'Chile', 'slug': 'chile'}),
        ('CN', {'continent': 'AS', 'name': 'China', 'slug': 'china'}),
        ('CX', {'continent': 'AS', 'name': 'Christmas Island', 'slug'
         : 'christmas-island'}),
        ('CC', {'continent': 'AS', 'name': 'Cocos (Keeling) Islands',
         'slug': 'cocos-keeling-islands'}),
        ('CO', {'continent': 'SA', 'name': 'Colombia', 'slug'
         : 'colombia'}),
        ('KM', {'continent': 'AF', 'name': 'Comoros', 'slug': 'comoros'
         }),
        ('CG', {'continent': 'AF', 'name': 'Congo', 'slug': 'congo'}),
        ('CD', {'continent': 'AF', 'name'
         : 'Congo, The Democratic Republic of the', 'slug'
         : 'congo-the-democratic-republic-of-the'}),
        ('CK', {'continent': 'OC', 'name': 'Cook Islands', 'slug'
         : 'cook-islands'}),
        ('CR', {'continent': 'SA', 'name': 'Costa Rica', 'slug'
         : 'costa-rica'}),
        ('CI', {'continent': 'AF', 'name': "Cote d'Ivoire", 'slug'
         : 'cote-divoire'}),
        ('HR', {'continent': 'EU', 'name': 'Croatia', 'slug': 'croatia'
         }),
        ('CU', {'continent': 'SA', 'name': 'Cuba', 'slug': 'cuba'}),
        ('CY', {'continent': 'AS', 'name': 'Cyprus', 'slug': 'cyprus'
         }),
        ('CZ', {'continent': 'EU', 'name': 'Czech Republic', 'slug'
         : 'czech-republic'}),
        ('DK', {'continent': 'EU', 'name': 'Denmark', 'slug': 'denmark'
         }),
        ('DJ', {'continent': 'AF', 'name': 'Djibouti', 'slug'
         : 'djibouti'}),
        ('DM', {'continent': 'SA', 'name': 'Dominica', 'slug'
         : 'dominica'}),
        ('DO', {'continent': 'SA', 'name': 'Dominican Republic', 'slug'
         : 'dominican-republic'}),
        ('EC', {'continent': 'SA', 'name': 'Ecuador', 'slug': 'ecuador'
         }),
        ('EG', {'continent': 'AF', 'name': 'Egypt', 'slug': 'egypt'}),
        ('SV', {'continent': 'SA', 'name': 'El Salvador', 'slug'
         : 'el-salvador'}),
        ('GQ', {'continent': 'AF', 'name': 'Equatorial Guinea', 'slug'
         : 'equatorial-guinea'}),
        ('ER', {'continent': 'AF', 'name': 'Eritrea', 'slug': 'eritrea'
         }),
        ('EE', {'continent': 'EU', 'name': 'Estonia', 'slug': 'estonia'
         }),
        ('ET', {'continent': 'AF', 'name': 'Ethiopia', 'slug'
         : 'ethiopia'}),
        ('EU', {'continent': 'EU', 'name': 'Europe', 'slug': 'europe'
         }),
        ('FK', {'continent': 'SA', 'name': 'Falkland Islands (Malvinas)'
         , 'slug': 'falkland-islands-malvinas'}),
        ('FO', {'continent': 'EU', 'name': 'Faroe Islands', 'slug'
         : 'faroe-islands'}),
        ('FJ', {'continent': 'OC', 'name': 'Fiji', 'slug': 'fiji'}),
        ('FI', {'continent': 'EU', 'name': 'Finland', 'slug': 'finland'
         }),
        ('FR', {'continent': 'EU', 'name': 'France', 'slug': 'france'
         }),
        ('GF', {'continent': 'SA', 'name': 'French Guiana', 'slug'
         : 'french-guiana'}),
        ('PF', {'continent': 'OC', 'name': 'French Polynesia', 'slug'
         : 'french-polynesia'}),
        ('TF', {'continent': 'AF', 'name': 'French Southern Territories'
         , 'slug': 'french-southern-territories'}),
        ('GA', {'continent': 'AF', 'name': 'Gabon', 'slug': 'gabon'}),
        ('GM', {'continent': 'AF', 'name': 'Gambia', 'slug': 'gambia'
         }),
        ('GE', {'continent': 'AS', 'name': 'Georgia', 'slug': 'georgia'
         }),
        ('DE', {'continent': 'EU', 'name': 'Germany', 'slug': 'germany'
         }),
        ('GH', {'continent': 'AF', 'name': 'Ghana', 'slug': 'ghana'}),
        ('GI', {'continent': 'EU', 'name': 'Gibraltar', 'slug'
         : 'gibraltar'}),
        ('GR', {'continent': 'EU', 'name': 'Greece', 'slug': 'greece'
         }),
        ('GL', {'continent': 'SA', 'name': 'Greenland', 'slug'
         : 'greenland'}),
        ('GD', {'continent': 'SA', 'name': 'Grenada', 'slug': 'grenada'
         }),
        ('GP', {'continent': 'SA', 'name': 'Guadeloupe', 'slug'
         : 'guadeloupe'}),
        ('GU', {'continent': 'OC', 'name': 'Guam', 'slug': 'guam'}),
        ('GT', {'continent': 'SA', 'name': 'Guatemala', 'slug'
         : 'guatemala'}),
        ('GN', {'continent': 'AF', 'name': 'Guinea', 'slug': 'guinea'
         }),
        ('GW', {'continent': 'AF', 'name': 'Guinea-Bissau', 'slug'
         : 'guinea-bissau'}),
        ('GY', {'continent': 'SA', 'name': 'Guyana', 'slug': 'guyana'
         }),
        ('HT', {'continent': 'SA', 'name': 'Haiti', 'slug': 'haiti'}),
        ('HM', {'continent': 'AF', 'name'
         : 'Heard Island and McDonald Islands', 'slug'
         : 'heard-island-and-mcdonald-islands'}),
        ('VA', {'continent': 'EU', 'name'
         : 'Holy See (Vatican City State)', 'slug'
         : 'holy-see-vatican-city-state'}),
        ('HN', {'continent': 'SA', 'name': 'Honduras', 'slug'
         : 'honduras'}),
        ('HK', {'continent': 'AS', 'name': 'Hong Kong', 'slug'
         : 'hong-kong'}),
        ('HU', {'continent': 'EU', 'name': 'Hungary', 'slug': 'hungary'
         }),
        ('IS', {'continent': 'EU', 'name': 'Iceland', 'slug': 'iceland'
         }),
        ('IN', {'continent': 'AS', 'name': 'India', 'slug': 'india'}),
        ('ID', {'continent': 'AS', 'name': 'Indonesia', 'slug'
         : 'indonesia'}),
        ('IR', {'continent': 'AS', 'name': 'Iran, Islamic Republic of',
         'slug': 'iran-islamic-republic-of'}),
        ('IQ', {'continent': 'AS', 'name': 'Iraq', 'slug': 'iraq'}),
        ('IE', {'continent': 'EU', 'name': 'Ireland', 'slug': 'ireland'
         }),
        ('IL', {'continent': 'AS', 'name': 'Israel', 'slug': 'israel'
         }),
        ('IT', {'continent': 'EU', 'name': 'Italy', 'slug': 'italy'}),
        ('JM', {'continent': 'SA', 'name': 'Jamaica', 'slug': 'jamaica'
         }),
        ('JP', {'continent': 'AS', 'name': 'Japan', 'slug': 'japan'}),
        ('JO', {'continent': 'AS', 'name': 'Jordan', 'slug': 'jordan'
         }),
        ('KZ', {'continent': 'AS', 'name': 'Kazakhstan', 'slug'
         : 'kazakhstan'}),
        ('KE', {'continent': 'AF', 'name': 'Kenya', 'slug': 'kenya'}),
        ('KI', {'continent': 'OC', 'name': 'Kiribati', 'slug'
         : 'kiribati'}),
        ('KP', {'continent': 'AS', 'name'
         : "Korea, Democratic People's Republic of", 'slug'
         : 'korea-democratic-peoples-republic-of'}),
        ('KR', {'continent': 'AS', 'name': 'Korea, Republic of', 'slug'
         : 'korea-republic-of'}),
        ('KW', {'continent': 'AS', 'name': 'Kuwait', 'slug': 'kuwait'
         }),
        ('KG', {'continent': 'AS', 'name': 'Kyrgyzstan', 'slug'
         : 'kyrgyzstan'}),
        ('LA', {'continent': 'AS', 'name'
         : "Lao People's Democratic Republic", 'slug'
         : 'lao-peoples-democratic-republic'}),
        ('LV', {'continent': 'EU', 'name': 'Latvia', 'slug': 'latvia'
         }),
        ('LB', {'continent': 'AS', 'name': 'Lebanon', 'slug': 'lebanon'
         }),
        ('LS', {'continent': 'AF', 'name': 'Lesotho', 'slug': 'lesotho'
         }),
        ('LR', {'continent': 'AF', 'name': 'Liberia', 'slug': 'liberia'
         }),
        ('LY', {'continent': 'AF', 'name': 'Libyan Arab Jamahiriya',
         'slug': 'libyan-arab-jamahiriya'}),
        ('LI', {'continent': 'EU', 'name': 'Liechtenstein', 'slug'
         : 'liechtenstein'}),
        ('LT', {'continent': 'EU', 'name': 'Lithuania', 'slug'
         : 'lithuania'}),
        ('LU', {'continent': 'EU', 'name': 'Luxembourg', 'slug'
         : 'luxembourg'}),
        ('MO', {'continent': 'AS', 'name': 'Macao', 'slug': 'macao'}),
        ('MK', {'continent': 'EU', 'name': 'Macedonia', 'slug'
         : 'macedonia'}),
        ('MG', {'continent': 'AF', 'name': 'Madagascar', 'slug'
         : 'madagascar'}),
        ('MW', {'continent': 'AF', 'name': 'Malawi', 'slug': 'malawi'
         }),
        ('MY', {'continent': 'AS', 'name': 'Malaysia', 'slug'
         : 'malaysia'}),
        ('MV', {'continent': 'AS', 'name': 'Maldives', 'slug'
         : 'maldives'}),
        ('ML', {'continent': 'AF', 'name': 'Mali', 'slug': 'mali'}),
        ('MT', {'continent': 'EU', 'name': 'Malta', 'slug': 'malta'}),
        ('MH', {'continent': 'OC', 'name': 'Marshall Islands', 'slug'
         : 'marshall-islands'}),
        ('MQ', {'continent': 'SA', 'name': 'Martinique', 'slug'
         : 'martinique'}),
        ('MR', {'continent': 'AF', 'name': 'Mauritania', 'slug'
         : 'mauritania'}),
        ('MU', {'continent': 'AF', 'name': 'Mauritius', 'slug'
         : 'mauritius'}),
        ('YT', {'continent': 'AF', 'name': 'Mayotte', 'slug': 'mayotte'
         }),
        ('MX', {'continent': 'NA', 'name': 'Mexico', 'slug': 'mexico'
         }),
        ('FM', {'continent': 'OC', 'name'
         : 'Micronesia, Federated States of', 'slug'
         : 'micronesia-federated-states-of'}),
        ('MD', {'continent': 'EU', 'name': 'Moldova, Republic of',
         'slug': 'moldova-republic-of'}),
        ('MC', {'continent': 'EU', 'name': 'Monaco', 'slug': 'monaco'
         }),
        ('MN', {'continent': 'AS', 'name': 'Mongolia', 'slug'
         : 'mongolia'}),
        ('MS', {'continent': 'SA', 'name': 'Montserrat', 'slug'
         : 'montserrat'}),
        ('MA', {'continent': 'AF', 'name': 'Morocco', 'slug': 'morocco'
         }),
        ('MZ', {'continent': 'AF', 'name': 'Mozambique', 'slug'
         : 'mozambique'}),
        ('MM', {'continent': 'AS', 'name': 'Myanmar', 'slug': 'myanmar'
         }),
        ('NA', {'continent': 'AF', 'name': 'Namibia', 'slug': 'namibia'
         }),
        ('NR', {'continent': 'OC', 'name': 'Nauru', 'slug': 'nauru'}),
        ('NP', {'continent': 'AS', 'name': 'Nepal', 'slug': 'nepal'}),
        ('NL', {'continent': 'EU', 'name': 'Netherlands', 'slug'
         : 'netherlands'}),
        ('AN', {'continent': 'SA', 'name': 'Netherlands Antilles',
         'slug': 'netherlands-antilles'}),
        ('NC', {'continent': 'OC', 'name': 'New Caledonia', 'slug'
         : 'new-caledonia'}),
        ('NZ', {'continent': 'OC', 'name': 'New Zealand', 'slug'
         : 'new-zealand'}),
        ('NI', {'continent': 'SA', 'name': 'Nicaragua', 'slug'
         : 'nicaragua'}),
        ('NE', {'continent': 'AF', 'name': 'Niger', 'slug': 'niger'}),
        ('NG', {'continent': 'AF', 'name': 'Nigeria', 'slug': 'nigeria'
         }),
        ('NU', {'continent': 'OC', 'name': 'Niue', 'slug': 'niue'}),
        ('NF', {'continent': 'OC', 'name': 'Norfolk Island', 'slug'
         : 'norfolk-island'}),
        ('MP', {'continent': 'OC', 'name': 'Northern Mariana Islands',
         'slug': 'northern-mariana-islands'}),
        ('NO', {'continent': 'EU', 'name': 'Norway', 'slug': 'norway'
         }),
        ('OM', {'continent': 'AS', 'name': 'Oman', 'slug': 'oman'}),
        ('PK', {'continent': 'AS', 'name': 'Pakistan', 'slug'
         : 'pakistan'}),
        ('PW', {'continent': 'OC', 'name': 'Palau', 'slug': 'palau'}),
        ('PS', {'continent': 'AS', 'name': 'Palestinian Territory',
         'slug': 'palestinian-territory'}),
        ('PA', {'continent': 'SA', 'name': 'Panama', 'slug': 'panama'
         }),
        ('PG', {'continent': 'OC', 'name': 'Papua New Guinea', 'slug'
         : 'papua-new-guinea'}),
        ('PY', {'continent': 'SA', 'name': 'Paraguay', 'slug'
         : 'paraguay'}),
        ('PE', {'continent': 'SA', 'name': 'Peru', 'slug': 'peru'}),
        ('PH', {'continent': 'AS', 'name': 'Philippines', 'slug'
         : 'philippines'}),
        ('PN', {'continent': 'OC', 'name': 'Pitcairn', 'slug'
         : 'pitcairn'}),
        ('PL', {'continent': 'EU', 'name': 'Poland', 'slug': 'poland'
         }),
        ('PT', {'continent': 'EU', 'name': 'Portugal', 'slug'
         : 'portugal'}),
        ('PR', {'continent': 'SA', 'name': 'Puerto Rico', 'slug'
         : 'puerto-rico'}),
        ('QA', {'continent': 'AS', 'name': 'Qatar', 'slug': 'qatar'}),
        ('RE', {'continent': 'AF', 'name': 'Reunion', 'slug': 'reunion'
         }),
        ('RO', {'continent': 'EU', 'name': 'Romania', 'slug': 'romania'
         }),
        ('RU', {'continent': 'AS', 'name': 'Russian Federation', 'slug'
         : 'russian-federation'}),
        ('RW', {'continent': 'AF', 'name': 'Rwanda', 'slug': 'rwanda'
         }),
        ('SH', {'continent': 'AF', 'name': 'Saint Helena', 'slug'
         : 'saint-helena'}),
        ('KN', {'continent': 'SA', 'name': 'Saint Kitts and Nevis',
         'slug': 'saint-kitts-and-nevis'}),
        ('LC', {'continent': 'SA', 'name': 'Saint Lucia', 'slug'
         : 'saint-lucia'}),
        ('PM', {'continent': 'SA', 'name': 'Saint Pierre and Miquelon',
         'slug': 'saint-pierre-and-miquelon'}),
        ('VC', {'continent': 'SA', 'name'
         : 'Saint Vincent and the Grenadines', 'slug'
         : 'saint-vincent-and-the-grenadines'}),
        ('WS', {'continent': 'OC', 'name': 'Samoa', 'slug': 'samoa'}),
        ('SM', {'continent': 'EU', 'name': 'San Marino', 'slug'
         : 'san-marino'}),
        ('ST', {'continent': 'AF', 'name': 'Sao Tome and Principe',
         'slug': 'sao-tome-and-principe'}),
        ('SA', {'continent': 'AS', 'name': 'Saudi Arabia', 'slug'
         : 'saudi-arabia'}),
        ('SN', {'continent': 'AF', 'name': 'Senegal', 'slug': 'senegal'
         }),
        ('SC', {'continent': 'AF', 'name': 'Seychelles', 'slug'
         : 'seychelles'}),
        ('SL', {'continent': 'AF', 'name': 'Sierra Leone', 'slug'
         : 'sierra-leone'}),
        ('SG', {'continent': 'AS', 'name': 'Singapore', 'slug'
         : 'singapore'}),
        ('SK', {'continent': 'EU', 'name': 'Slovakia', 'slug'
         : 'slovakia'}),
        ('SI', {'continent': 'EU', 'name': 'Slovenia', 'slug'
         : 'slovenia'}),
        ('SB', {'continent': 'OC', 'name': 'Solomon Islands', 'slug'
         : 'solomon-islands'}),
        ('SO', {'continent': 'AF', 'name': 'Somalia', 'slug': 'somalia'
         }),
        ('ZA', {'continent': 'AF', 'name': 'South Africa', 'slug'
         : 'south-africa'}),
        ('GS', {'continent': 'SA', 'name'
         : 'South Georgia and the South Sandwich Islands', 'slug'
         : 'south-georgia-and-the-south-sandwich-islands'}),
        ('ES', {'continent': 'EU', 'name': 'Spain', 'slug': 'spain'}),
        ('LK', {'continent': 'AS', 'name': 'Sri Lanka', 'slug'
         : 'sri-lanka'}),
        ('SD', {'continent': 'AF', 'name': 'Sudan', 'slug': 'sudan'}),
        ('SR', {'continent': 'SA', 'name': 'Suriname', 'slug'
         : 'suriname'}),
        ('SJ', {'continent': 'EU', 'name': 'Svalbard and Jan Mayen',
         'slug': 'svalbard-and-jan-mayen'}),
        ('SZ', {'continent': 'AF', 'name': 'Swaziland', 'slug'
         : 'swaziland'}),
        ('SE', {'continent': 'EU', 'name': 'Sweden', 'slug': 'sweden'
         }),
        ('CH', {'continent': 'EU', 'name': 'Switzerland', 'slug'
         : 'switzerland'}),
        ('SY', {'continent': 'AS', 'name': 'Syrian Arab Republic',
         'slug': 'syrian-arab-republic'}),
        ('TW', {'continent': 'AS', 'name': 'Taiwan', 'slug': 'taiwan'
         }),
        ('TJ', {'continent': 'AS', 'name': 'Tajikistan', 'slug'
         : 'tajikistan'}),
        ('TZ', {'continent': 'AF', 'name'
         : 'Tanzania, United Republic of', 'slug'
         : 'tanzania-united-republic-of'}),
        ('TH', {'continent': 'AS', 'name': 'Thailand', 'slug'
         : 'thailand'}),
        ('TG', {'continent': 'AF', 'name': 'Togo', 'slug': 'togo'}),
        ('TK', {'continent': 'OC', 'name': 'Tokelau', 'slug': 'tokelau'
         }),
        ('TO', {'continent': 'OC', 'name': 'Tonga', 'slug': 'tonga'}),
        ('TT', {'continent': 'SA', 'name': 'Trinidad and Tobago', 'slug'
         : 'trinidad-and-tobago'}),
        ('TN', {'continent': 'AF', 'name': 'Tunisia', 'slug': 'tunisia'
         }),
        ('TR', {'continent': 'AS', 'name': 'Turkey', 'slug': 'turkey'
         }),
        ('TM', {'continent': 'AS', 'name': 'Turkmenistan', 'slug'
         : 'turkmenistan'}),
        ('TC', {'continent': 'SA', 'name': 'Turks and Caicos Islands',
         'slug': 'turks-and-caicos-islands'}),
        ('TV', {'continent': 'OC', 'name': 'Tuvalu', 'slug': 'tuvalu'
         }),
        ('UG', {'continent': 'AF', 'name': 'Uganda', 'slug': 'uganda'
         }),
        ('UA', {'continent': 'EU', 'name': 'Ukraine', 'slug': 'ukraine'
         }),
        ('AE', {'continent': 'AS', 'name': 'United Arab Emirates',
         'slug': 'united-arab-emirates'}),
        ('GB', {'continent': 'EU', 'name': 'United Kingdom', 'slug'
         : 'united-kingdom'}),
        ('US', {'continent': 'NA', 'name': 'United States', 'slug'
         : 'united-states'}),
        ('UM', {'continent': 'OC', 'name'
         : 'United States Minor Outlying Islands', 'slug'
         : 'united-states-minor-outlying-islands'}),
        ('UY', {'continent': 'SA', 'name': 'Uruguay', 'slug': 'uruguay'
         }),
        ('UZ', {'continent': 'AS', 'name': 'Uzbekistan', 'slug'
         : 'uzbekistan'}),
        ('VU', {'continent': 'OC', 'name': 'Vanuatu', 'slug': 'vanuatu'
         }),
        ('VE', {'continent': 'SA', 'name': 'Venezuela', 'slug'
         : 'venezuela'}),
        ('VN', {'continent': 'AS', 'name': 'Vietnam', 'slug': 'vietnam'
         }),
        ('VG', {'continent': 'SA', 'name': 'Virgin Islands, British',
         'slug': 'virgin-islands-british'}),
        ('VI', {'continent': 'SA', 'name': 'Virgin Islands, U.S.',
         'slug': 'virgin-islands-us'}),
        ('WF', {'continent': 'OC', 'name': 'Wallis and Futuna', 'slug'
         : 'wallis-and-futuna'}),
        ('EH', {'continent': 'AF', 'name': 'Western Sahara', 'slug'
         : 'western-sahara'}),
        ('YE', {'continent': 'AS', 'name': 'Yemen', 'slug': 'yemen'}),
        ('ZM', {'continent': 'AF', 'name': 'Zambia', 'slug': 'zambia'
         }),
        ('ZW', {'continent': 'AF', 'name': 'Zimbabwe', 'slug'
         : 'zimbabwe'}),
        ]

    if settings.DEBUG:
        print "Geotagging: Populating Countries"

    continents = Continent.objects.all()
    for (code, defaults) in COUNTRIES:
        continent = continents.get(pk=defaults.pop('continent', None))
        co, c = Country.objects.get_or_create(code=code, continent=continent, defaults=defaults)
        if not c:
            break

dispatcher.connect(init_data, sender=models, signal=signals.post_syncdb)
