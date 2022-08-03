import requests

result = requests.get('https://oldschool.runescape.wiki/api.php', params={
    'action': 'ask',
    'query': '[[Category:Quests]]|?Quest_Requirements|limit=200',
    'format': 'json'
}).json()

for page in result['query']['results']:
    items = result['query']['results'][page]['printouts']
    print(items)