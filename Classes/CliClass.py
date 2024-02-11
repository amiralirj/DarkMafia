from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Config import (API_ID,API_HASH,BOT_TOKEN,zone)
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode
from Classes.MafClass import Group , helper
from Data.DataBase import DataBase
from pyrogram import Client 
from pyromod import listen
from asyncio import sleep


async def state_send(days,bot):
    groups=helper.get_top_groups(helper.all_games,100,days)
    text=helper.text.best_gaps(abs(days))

    h=0
    for q,i in enumerate(groups):
        if h==20:break
        group_count=0
        group_time=0
        players_count=0
        chat=Group(i)
        chat.update
        last_month_games=chat.played_games_last_month(days)
        for gods_list in last_month_games:
            if gods_list[3] == 0 : continue
            group_count +=1
            group_time += float( (helper.call_time(len((gods_list[-1]).split('-')),gods_list[3])) / 60  )
            players_count+=len((gods_list[-1]).split('-'))
        try:
            group = await bot.get_chat(int(i))
            if group.username :
                text+=helper.text.all_groups_stats(chat.emoji ,  q+1 , group.username , round(group_time,1) , group_count , players_count , int(groups[i]))
                h+=1
            else:
                continue
        except Exception as e:
            helper.Log(f'{e} in Group_List')
            continue
        if len(text.split('\n')) > 30 : 
            await bot.send_message(helper.stats_channel,text)
            text=helper.text.best_gaps(abs(days))
            
    if text!=helper.text.best_gaps(abs(days)):
        await bot.send_message(helper.stats_channel,text)
        
#----------------------------------------------------------------------------------------------------------------| Inheriting from Client(pyrogram)
class Mafia(Client):                                                                                           #-|
    def __init__(self):                                                                                        #-|
        #---------------------------------------------------| Threading Functions in SCADULE                   #-|
        self.mark_down_parse_mode=ParseMode.HTML                                                               #-| 
        scheduler = AsyncIOScheduler(timezone=zone) # your city  time zone                                     #-|
        scheduler.add_job(self.monthly , "cron", day=1)                                                        #-| 
        scheduler.add_job(self.week_stats, "cron", day_of_week=5, hour=0, minute=1 , second=0)                 #-| 
        scheduler.add_job(self.daily_stats, "cron", hour=0, minute=0 , second=1)                              #-| 
        scheduler.start()                                                                                      #-| 
        #---------------------------------------------------|                                                  #-|
        super().__init__(                                                                                      #-|
            ":memory:",                                                                                        #-|
            plugins=dict(root=r'plugins'),                                                                     #-|
            api_id=API_ID,                                                                                     #-|
            api_hash=API_HASH,                                                                                 #-|
            bot_token=BOT_TOKEN,                                                                               #-|
            sleep_threshold=60,                                                                                #-|
            parse_mode=ParseMode.MARKDOWN,                                                                     #-|
            workers=80,                                                                                        #-|
            in_memory=True)                                                                                    #-|
        
        self.data = DataBase
        
    async def send_message(self, *args, **kwargs):
        try:
            return await super().send_message(*args, **kwargs)
        except FloodWait as e:
            if int(e.x) > 5 : raise TimeoutError
            await sleep(e.x)
            return await super().send_message(*args, **kwargs)

    async def edit_message(self, *args, **kwargs):
        try:
            return await super().edit_message_text(*args, **kwargs)
        except FloodWait as e:
            if int(e.x) > 5 : raise TimeoutError
            await sleep(e.x)
            return await super().edit_message_text(*args, **kwargs)
    
    async def monthly(self):
        DataBase.reStart()
        try:
            await state_send(-30,self)
        except Exception as e : helper.Log(f'{e} IN STATS MONTHLY AND DAILY')
    
    async def week_stats(self):
        try:
            await state_send(-7,self)
        except Exception as e : helper.Log(f'{e} IN STATS MONTHLY AND DAILY')
        
    async def daily_stats(self):
        await self.send_message('@amiralirj_g','Daily Runned')
        try:
            await state_send(-1,self)
        except Exception as e : helper.Log(f'{e} IN STATS MONTHLY AND DAILY')
            
            
