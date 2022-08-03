import requests

result = requests.get('https://oldschool.runescape.wiki/api.php', params={
    'action': 'paraminfo',
    'modules': 'ask',
    'helpformat': 'none',
    'format': 'json'
}).json()

print(result)

# for page in result['query']['results']:
#     items = result['query']['results'][page]['printouts']
#     print(items)