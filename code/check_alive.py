import requests


def check_alive(original, list_of_urls):
    alive = []

    for url in list_of_urls:
        try:
            res = requests.get('https://'+url, timeout=5)
            if res.status_code == 200:
                alive.append(url)
        except:
            continue
    if original in alive:
        alive.remove(original)
    return alive
