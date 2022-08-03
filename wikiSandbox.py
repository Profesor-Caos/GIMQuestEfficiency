import requests

result = requests.get('https://oldschool.runescape.wiki/api.php', params={
    'action': 'ask',
    'query': '[[Quest Requirements::+]]|?Quest Requirements|limit=500',
    'format': 'json'
}).json()

for page in result['query']['results']:
    items = result['query']['results'][page]['printouts']['Quest Requirements']
    print (page + ": ")
    print (items)