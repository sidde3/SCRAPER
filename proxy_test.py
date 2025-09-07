import os
import requests
import random

os.environ['http_proxy'] = 'http://localhost:9090'

proxies = [
    {'http': 'http://localhost:9090'},
    {'http': 'http://localhost:9091'}
]

def get_random_proxy():
    return random.choice(proxies)

def make_request(url):
    proxy = get_random_proxy()
    try:
        response = requests.get(url, proxies=proxy, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Proxy {proxy['http']} failed: {e}")
        return None

url = 'http://localhost:8080/'
response = make_request(url)

if response:
    print(response)
