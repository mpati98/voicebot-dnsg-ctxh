import requests

url = 'https://api.fpt.ai/hmi/tts/v5'

payload = 'xin chào'
headers = {
    'api-key': 'OaGgkRmCMzOoZbnwgX70IDWo77t0g5SW',
    'speed': '',
    'voice': 'banmai'
}

response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)
print(response.text)
