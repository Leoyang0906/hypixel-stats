import requests
import json
def getuuid(name): #获取玩家uuid
    try:
        mojangapi = 'https://api.mojang.com/users/profiles/minecraft/'+name
        uuid = eval(requests.get(mojangapi).text)
        return uuid['id']
    except KeyError: #若uuid获取失败 返回notch的uuid
        return getuuid('notch')
#print(getuuid('eyz2021'))
#换算算法
def getBWStar(bwexp):
    bwPerPrestigeExp = 489000
    bwPerPrestigeLevel = 100
    curPrestige = int(bwexp / bwPerPrestigeExp)
    bwexp = bwexp % bwPerPrestigeExp
    if curPrestige > 5:
        prestigeOver = curPrestige % 5
        bwexp += prestigeOver * bwPerPrestigeExp
        curPrestige -= prestigeOver
    if bwexp < 500: return int(curPrestige * bwPerPrestigeLevel)
    elif bwexp < 1500: return 1 + int(curPrestige * bwPerPrestigeLevel)
    elif bwexp < 3500: return 2 + int(curPrestige * bwPerPrestigeLevel)
    elif bwexp < 5500: return 3 + int(curPrestige * bwPerPrestigeLevel)
    elif bwexp < 9000: return 4 + int(curPrestige * bwPerPrestigeLevel)
    else: return int(((bwexp - 9000) / 5000 + 4) + (curPrestige * bwPerPrestigeLevel))
    #作者：lpmon_ https://www.bilibili.com/read/cv21151032/?spm_id_from=333.999.0.0 出处：bilibili
#print(getBWStar(69796))