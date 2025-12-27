print('使用方法：按ctrl')

# 信息配置
hypixelApi="2447816c-43ca-4463-a51c-086af3de4ef0"
playerName='eyz2021_bilibili'
hotkey='Ctrl+slash'


from hypixelapi import HypixelAPI, HypixelError, PlayerNotFoundError
from apitools import *



def getBWStats(playerName):
    api = HypixelAPI(hypixelApi) #初始化api对象
    pInfo = api.get_player_json(getuuid(playerName)) #获取玩家信息
    pName=pInfo['player']['displayname']
    pBWInfo=pInfo['player']['stats']['Bedwars']
    pBWLevel=getBWStar(pBWInfo['Experience'])
    pBWWLR=round(pBWInfo['wins_bedwars']/pBWInfo['losses_bedwars'],2)
    pBWKDR=round(pBWInfo['kills_bedwars']/pBWInfo['deaths_bedwars'],2)
    pBWFKDR=round(pBWInfo['final_kills_bedwars']/pBWInfo['final_deaths_bedwars'],2)
    return f"player {pName}'s Bedwars Info\nLevel:{pBWLevel}\nKDR:{pBWKDR}\nFKDR:{pBWFKDR}\nWLR:{pBWWLR}"

import keyboard
stat=False
pNameInput=''
def on_press(key):
    global stat
    global pNameInput
    if stat:
        key=str(key).replace('KeyboardEvent(','').replace(' down)','')
        
        if len(key)==1:
            pNameInput+=key
        elif key=='backspace':
            pNameInput=pNameInput[:-1]
        elif key=='enter':
            stat=False
            pBWInfo=getBWStats(pNameInput.replace('/',''))
            infoPrint.config(text=pBWInfo)
            pNameInput=''
            
        #print(pNameInput)
        pNameView.config(text=pNameInput)
# 快捷键控制开关函数
def change_stat():
    global stat
    if stat:
        stat=False
    else:
        stat=True
keyboard.on_press(on_press)
keyboard.add_hotkey(hotkey,change_stat)

from tkinter import *
window=Tk()
window.geometry('+200+200')
window.title('bedwarsinfo')
window.overrideredirect(True)
window.config(bg='#114514')
window.wm_attributes('-transparentcolor','#114514')
window.attributes('-topmost','true')
window.attributes('-alpha',0.8)
pNameView=Label(text='test',bg='#114514',font=('微软雅黑',15,"bold"),fg='red')
pNameView.pack()
infoPrint=Label(text='test',bg='#114514',font=('DFPOP1W5-GB',15,"bold"),fg='green')
infoPrint.pack()
window.mainloop()
