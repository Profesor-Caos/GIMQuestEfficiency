import requests

result = requests.get('https://oldschool.runescape.wiki/api.php', params={
    'action': 'ask',
    'query': '[[Quest Items required::+]]|?Quest Items required|limit=500',
    'format': 'json'
}).json()

for page in result['query']['results']:
    items = result['query']['results'][page]['printouts']['Quest Items required']