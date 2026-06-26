import requests
import json
import time

DEFAULT_NOTCH_UUID = "069a79f444e94726a5befca90e38aaf5"


def getuuid(name, retries=2, backoff=0.5):
    """Get Mojang UUID for the given player name.
    Returns UUID string or None on failure.
    """
    url = f'https://api.mojang.com/users/profiles/minecraft/{name}'
    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                # Mojang returns JSON like {"id":"...","name":"..."}
                data = resp.json()
                return data.get('id')
            elif resp.status_code == 204 or resp.status_code == 404:
                return None
            else:
                # unexpected status, try again
                time.sleep(backoff * (attempt + 1))
        except (requests.RequestException, ValueError):
            time.sleep(backoff * (attempt + 1))
    # fallback to notch uuid if everything fails
    return DEFAULT_NOTCH_UUID


# Bedwars star/level calculation (kept from original logic)
def getBWStar(bwexp):
    bwPerPrestigeExp = 489000
    bwPerPrestigeLevel = 100
    try:
        bwexp = int(bwexp)
    except Exception:
        return 0
    curPrestige = int(bwexp / bwPerPrestigeExp)
    bwexp = bwexp % bwPerPrestigeExp
    if curPrestige > 5:
        prestigeOver = curPrestige % 5
        bwexp += prestigeOver * bwPerPrestigeExp
        curPrestige -= prestigeOver
    if bwexp < 500:
        return int(curPrestige * bwPerPrestigeLevel)
    elif bwexp < 1500:
        return 1 + int(curPrestige * bwPerPrestigeLevel)
    elif bwexp < 3500:
        return 2 + int(curPrestige * bwPerPrestigeLevel)
    elif bwexp < 5500:
        return 3 + int(curPrestige * bwPerPrestigeLevel)
    elif bwexp < 9000:
        return 4 + int(curPrestige * bwPerPrestigeLevel)
    else:
        return int(((bwexp - 9000) / 5000 + 4) + (curPrestige * bwPerPrestigeLevel))
