import random

def load_proxies():
    with open("proxies.txt") as f:
        return [line.strip() for line in f if line.strip()]

def get_random_proxy():
    proxies = load_proxies()
    return random.choice(proxies)
