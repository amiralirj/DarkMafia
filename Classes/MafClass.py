from Config import OWNER , OWNER_USERNAME  , BOT_ID , TEXTS , BUTTONS , CHANNEL_USERNAME , LIST_USERNAME , CO_LEADER , emoji_list , STATS_CHANNEL , BOT_USERNAME
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from matplotlib.dates import  DateFormatter
from Data.DataBase  import  DataBase
from collections import defaultdict
from pyrogram.enums import ChatType
import matplotlib.pyplot as plt
from random import choice , randint
import jdatetime 
import datetime
import string
import os 

class User:
    def __init__(self,user_id,group_id=111111) -> None:
        self.user_id = int(user_id)
        if not group_id == 111111 :
            group_id=Group(group_id)
            self.group_id=group_id.main
            DataBase.Add_user(self.user_id,int(self.group_id))
            DataBase.Add_MMMM_user(self.user_id)
        self.update
    
    @property
    def update(self):
        det=DataBase.Show_user(self.user_id)
        self.score = det[1]
        self.games = det[2]
        self.wins = det[3]
        self.maf = det[4]
        self.shahr = det[5]
        self.bests=det[6]
        self.group=det[7]
        self.banned=det[8]
        self.name=det[9]

        det=DataBase.Show_MMMM_user(self.user_id)
        self.MMscore = det[1]
        self.MMgames = det[2]
        self.MMwins = det[3]
        self.MMmaf = det[4]
        self.MMshahr = det[5]
        self.MMbests=det[6]
        
    #-------------------------------------------------------------------------------------------------------
    def group_show(self):
        'user_gap,User_id,Group,Warns,Banned'
        row = DataBase.Show_group_user(self.user_id,self.group_id) 
        return [row[3],row[4]]
    
    def set_name(self,name):
        DataBase.change_name(self.user_id , name )
        
    def is_group_banned(self):
        date = self.group_show()[1]
        if date == 'None': return False
        date =datetime.datetime.strptime(date, "%Y-%m-%d-%H:%M") 
        if  datetime.datetime.now() < date :return str(date)
        else:return False
        
    def add_warn(self):
        DataBase.change_warn(self.user_id,self.group_id,1)
    
    def del_warn(self):
        DataBase.change_warn(self.user_id,self.group_id,-1)
        
    def group_ban(self,date):
        ban_date=str((datetime.datetime.now() + datetime.timedelta(days=date)).strftime("%Y-%m-%d-%H:%M"))
        DataBase.group_ban(self.user_id,self.group_id,ban_date)
        
    @property
    def group_unban(self):
        DataBase.group_ban(self.user_id,self.group_id,'None')
    #-------------------------------------------------------------------------------------------------------
    def ban(self):
        DataBase.ban(self.user_id)
        
    def unban(self):
        DataBase.unban(self.user_id)
        
    def change_group(self,group_id,all_groups):
        chat = Group(group_id).main
        if chat in all_groups:
            DataBase.change_group(self.user_id,group_id)
        else: raise KeyError
        
    #-------------------------------------------------------------------------------------------------------
    def user_emoji(self,data:list):
        try : 
            if self.user_id in emoji_list : return emoji_list[self.user_id]
        except:pass
        try:
            percentage=[[1,'👑'],[3,'💎'],[7,'🏆'],[10,'🎖'],[15,'🎗']]
            rank=data.index(self.user_id)
            user_percentage= (rank / len(data)) * 100 
            for i in percentage : 
                if i[0] > user_percentage : 
                    return i[1]
            
            else : return ''
        except: return ''
            
            
    @property
    def bwin(self):
        '''black win'''
        DataBase.add_point(self.user_id,'maf_win')
        DataBase.add_point(self.user_id,'total_win')
        DataBase.add_MMMM_point(self.user_id,'maf_win')
        DataBase.add_MMMM_point(self.user_id,'total_win')
        
    @property
    def wwin(self):
        '''white win'''
        DataBase.add_point(self.user_id,'shahr_win')
        DataBase.add_point(self.user_id,'total_win')
        DataBase.add_MMMM_point(self.user_id,'shahr_win')
        DataBase.add_MMMM_point(self.user_id,'total_win')
        
    @property
    def game_done(self):
        DataBase.add_point(self.user_id,'total_game')
        DataBase.add_MMMM_point(self.user_id,'total_game')
        
    def add_score(self,score):
        DataBase.add_score(self.user_id,score)
        DataBase.add_MMMM_score(self.user_id,score)
        
    @property
    def add_best(self):
        DataBase.add_point(self.user_id,'bests')
        DataBase.add_MMMM_point(self.user_id,'bests')

    def get_player_rank(self,all_users_data , kind):
        '''1 score - 2 games - 3 wins - 4 maf wins - 5 shahr win - 6 bests '''
        sorted_users = sorted(all_users_data, key=lambda user: user[kind], reverse=True)
        target_user_index = next((index for index, user in enumerate(sorted_users) if user[0] == self.user_id), None)
        target_user_rank = target_user_index + 1 if target_user_index is not None else None

        return target_user_rank

    def __int__(self):
        return self.user_id


class Game:
    def __init__(self,group_id,) -> None:
        self.group=int(group_id)
        try:self.update
        except:pass
    
    @property
    def update(self):
        #group_id INT , scenario TEXT , god INT , white TEXT , black TEXT , mos TEXT , point TEXT , date TEXT, win INT , active INT ,mid INT )')

        det=DataBase.see_active_game(self.group)
        self.scenario = det[1]
        self.god = det[2]
        self.point = det[3]
        self.date = det[4]
        self.win = det[5]
        self.active=det[6]
        self.mid = det[7]
        self.all_plyrs = det[8]
        self.players_count=len((self.all_plyrs).split('-'))

        
    def start_game(self,scenario,god,all_plyrs,mid):
        DataBase.Add_match(self.group,scenario,god,mid,all_plyrs)
    
    @property
    def del_game(self):
        DataBase.unactive(self.group)
    
    def change_mid(self,mid):
        DataBase.Change_mid(self.group,mid)
        
    @property
    def status_list(self):
        self.update
        P = {}
        for i in str(self.all_plyrs).split('-'):
            i=i.split(':')[0]
            if 'A' in i : 
                P[int(i[1:])] = True
            else:
                P[int(i[1:])] = False
        return P
    
    @property
    def status_list_num(self):
        self.update
        P = {}
        for i in str(self.all_plyrs).split('-'):
            i=i.split(':')
            if 'A' in i[0] : 
                P[int(i[-1])] = True
            else:
                P[int(i[-1])] = False
        return P
            
        
    def change_status(self,player):
        status = self.status_list[player]
        self.update
        if status : 
            ST=[f'A{player}',f'D{player}']
        else:
            ST=[f'D{player}',f'A{player}']
            
        self.all_plyrs=self.all_plyrs.replace(ST[0],ST[1])
        DataBase.Change_all_players(self.group , self.all_plyrs)
        
    def end_game(self,win):
        score = self.cal_score()
        DataBase.End_match(score,win,self.group)
        return score
    
    def change_god(self,god):
        DataBase.Change_god(self.group,int(god))
        self.god = int(god) 
        
    def change_players(self,all_plyrs):
        DataBase.Change_all_players(self.group,all_plyrs)
        
    def del_player(self,user_id,num):
        self.update
        all_plyrs=str(self.all_plyrs).replace(f'{user_id}',f'NUM{num}')
        self.change_players(all_plyrs)
        
    @property
    def all_players(self):
        self.update
        all=[]
        for i in self.all_plyrs.split('-'):
            try:
                all.append(int((i.split(':')[0]).replace('D','').replace('A','')))
            except:pass
        
        return all
    
    
        
    def add_player(self,user_id,num):
        self.update
        self.all_plyrs = self.all_plyrs.replace(f'NUM{num}',f'{user_id}')
                       
        self.change_players(self.all_plyrs)

        
    def cal_score(self):
        self.update
        start_date =datetime.datetime.strptime(self.date, "%Y-%m-%d-%H:%M") 
        td = datetime.datetime.now() - start_date 
        time = abs((td.total_seconds()) // 60)
        
        if time >= 180 : z = 3
        
        elif time >= 150 : z = 2.50
        
        elif time >= 120 : z = 2.25
        
        elif time >= 105 : z = 2.10

        elif time >= 90  : z = 2
        
        elif time >= 75  : z = 1.8
        
        elif time >= 60  : z = 1.6
        
        elif time >= 40  : z = 1.3
        
        elif time < 20  : z = 0.5
        
        elif time < 40  : z = 1
        
        players =self.players_count
        
        if players * (4) > time :
            return 0
        
        players_int=players
        if players > players_int:
            players_int=13
            
        return int( z * players_int )
        
    
    
class Group :
    def __init__(self,group_id) -> None:
        #(group_id INT PRIMARY KEY , support INT , g2 INT , g3 INT , g4 INT , state_lock INT , Membership TEXT , Owner INT 
        #(group_id INT , name TEXT , white TEXT , black TEXT , mos TEXT , uni_que TEXT PRIMARY KEY )
        self.group=int(group_id)
        try:
            self.main= DataBase.FIND_MAIN(self.group)
        except Exception as e:helper.Log(f'{e} in Group init ')
        try:self.update
        except:pass

    @property
    def game(self):
        return Game(self.group)
    
    def card(self,name):
        x=DataBase.see_card( self.main , name )
        return x.split('-')
    
    def add_card(self,name,cards):
        DataBase.add_card(self.main,name,cards)
    
    def all_cards(self):
        x=DataBase.show_cards( self.main )
        return [i[0] for i in x ]
        
    def delete_card(self,name):
        DataBase.delete_card(self.main,name)
        
        
    def set_group_0_point(self):
        DataBase.set_0_group_point(self.main)
        DataBase.set_0_group_point(self.g2)
        DataBase.set_0_group_point(self.g3)
        DataBase.set_0_group_point(self.g4)
        
    @property
    def all_games(self):
        '''group_id,scenario,god,point,date,win,active,mid,all_plyrs'''
        g=DataBase.See_games(self.main)
        g+=DataBase.See_games(self.g2)
        g+=DataBase.See_games(self.g3)
        g+=DataBase.See_games(self.g4)
        return g 
    
    @property
    def all_games_players_text(self):
        text=''
        for i in self.all_games:
            text+=i[-1]
            
        return text
            
        
    
    def title(self,message):
        if message.chat.username :
            return f'@{message.chat.username}'
        else: return message.chat.title
    
    @property
    def update(self):
        det = DataBase.See_group(self.main)
        self.support = det['support']
        self.g2 = det['g2']
        self.g3 = det['g3']
        self.g4 = det['g4']
        self.state_lock = int(det['state_lock'])
        self.Membership = det['Membership']
        self.Owner = det['Owner']
        self.template = det['template']
        if det['template'] == 'None':self.template = False
        self.emoji = det['emoji']
        self.join_lock= int(det['join_lock'])
        self.ev_num= int(det['Ev_num'])
        self.farsi= bool(int(det['Farsi_name']))
    
    def unban_all_players(self):
        DataBase.group_all_unban()
        
    def change_Ev_num(self,num=None):
        self.update
        if num==None:
            DataBase.Add_Ev_num(self.main)
        else:DataBase.Change_Ev_num(self.main,num)
        
    def add_group(self,support,g2,g3,g4,Membership,Owner):
        DataBase.Add_group(int(self.group),int(support),int(g2),int(g3),int(g4),int(Membership),Owner)
        
    def DELETE_GROUP(self):
        self.update
        DataBase.DELETE_GROUP(self.main)
        
    @property
    def all_players(self):
        row=DataBase.show_group_users(self.main)
        ids=[i[0] for i in row]
        return ids
        
    def change_farsi(self,amount):
        DataBase.Change_Farsi_name(self.main,int(amount))
        self.farsi=bool(amount)
        
    def Change_join_lock(self,lock):
        DataBase.Change_join_lock(self.main,int(lock))
        
    def change_sup(self,sup):
        self.update
        DataBase.Change_sup(self.main,int(sup))
        
    def change_g2(self,amount):
        self.update
        DataBase.Change_g2(self.main,int(amount))
        
    def change_g3(self,amount):
        self.update
        DataBase.Change_g3(self.main,int(amount))
        
    def change_g4(self,amount):
        self.update
        DataBase.Change_g4(self.main,int(amount))
    
    def change_owner(self,user_id):
        self.update
        DataBase.Change_owner(self.main,int(user_id))
    
    def change_state_lock(self,amount):
        DataBase.Change_state(self.main,int(amount))
    
    def add_god(self,user_id):
        DataBase.Add_god(self.main , int(user_id))
    
    def del_god(self,user_id):
        DataBase.Del_god(self.main , int(user_id))
        
    def change_template(self,temp):
        if temp=='None':
            DataBase.Change_template(self.main,temp)
            return
        for i in ['{DATE_TEXT}','{PLAYERS_TEXT}','{SENATIO_TEXT}','{GOD_NAME_TEXT}','{GROUP_USERNAME_TEXT}','{TIME_TEXT}','{EVENT_TEXT}']:
            if i not in temp: raise AttributeError
        DataBase.Change_template(self.main,temp)
        
    def change_emoji(self,emoji):
        DataBase.Change_emoji(self.main,emoji)
        
    @property    
    def see_gods(self):
        return DataBase.See_gods(self.main)
    
    def add_scenario(self,name,roles):
        DataBase.Add_Scenario(self.main,name,roles)
        
    def del_scenario(self,name):
        DataBase.Del_Scenario(self.main,name)
        
    @property
    def all_scenario(self):
        try:
            return [i[0] for i in DataBase.Show_All_Scenario(self.main)]
        except: return ['هیج سناریویی وجود ندارد']
            
    def see_scenario(self,name):
        r=DataBase.Show_roles(name,self.main)
        if r['mos']=='none': r.pop('mos')
        return  r
    
    @property
    def have_active(self):
        try:
            d=DataBase.see_active_game(self.group)[0]
            return True
        except: return False
        
    def deactive_all(self):
        DataBase.unactive(self.group)
        
    def __int__(self):
        return self.group
    
    def __str__(self):
        return  str(DataBase.See_group(self.main))
    
    def played_games_last_month(self,days=-30):
        delta =(datetime.datetime.now() + datetime.timedelta(days=days ))
        last_month_games=[]
        for game in self.all_games:
            try:
                game_time=datetime.datetime.strptime(game[4], "%Y-%m-%d-%H:%M")
            except : 
                helper.Log(game)
            if ( delta - datetime.timedelta(minutes=(helper.call_time(  (int(len(game[8].split('-')))) , (int(game[3])))+20) ) ) <=  game_time :
                last_month_games.append(game)
                
        return (last_month_games)
    
    def change_main(self,new):
        self.update
        DataBase.CHANGE_MAIN(self.main,int(new))
        
from pyrogram import  errors , filters 
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import ForceReply
import time

from collections import deque
import time
from functools import wraps

user_message_info = {}
day_usr_info={}
# Rate limit settings

LIMIT = 300
MESSAGE_LIMIT = 40
TIME_WINDOW = 10  # seconds
MIN_INTERVAL = 0.7  # seconds

def rate_limit_decorator(func):
    @wraps(func)
    async def wrapper(client, message):
        user_id = message.from_user.id
        current_time = time.time()
        
        x=False
        
        if user_id not in day_usr_info:
            day_usr_info[user_id] = {'count': 1, 'timestamp': current_time}
            x=True
            
        if abs(current_time - day_usr_info[user_id]['timestamp']) > LIMIT:
            day_usr_info[user_id] = {'count': 1, 'timestamp': current_time}
            x=True
            
        if day_usr_info[user_id]['count'] >= MESSAGE_LIMIT:
            return   

        if not x :
            day_usr_info[user_id]['count'] += 1
            
            
        
        
        if user_id not in user_message_info:
            user_message_info[user_id] = 0
        if abs(current_time - user_message_info[user_id]) < MIN_INTERVAL:
            user_message_info[user_id] = current_time
            return  
        user_message_info[user_id] = current_time
        await func(client, message)

    return wrapper



async def bot_added(_, __, msg):
    if msg.new_chat_members:
        for i in msg.new_chat_members:
            if int(i.id)==int(BOT_ID):
                return True
    return False 

async def god_only(_, __, msg):
    try:
        try:
            chat=msg.chat.id
        except:chat=msg.message.chat.id
        gp=Group(int(chat))
        if int(msg.from_user.id) in gp.see_gods :
            return True
        return False 
    except:return False

async def admin_only(_, __, msg):
    try:
        chat=msg.chat
    except:chat=msg.message.chat
    admins = [int(i.user.id) async for i in chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS)]
    if int(msg.from_user.id) in admins:
        return True
    return False 

def game_god(_, __, msg):
    try:
        try:
            chat=msg.chat
        except:chat=msg.message.chat
        gp=Group(int(chat.id))
        game=gp.game
        game.update
        if int(msg.from_user.id) == game.god:
            return True
        return False 
    except:return False

def owner_only(_, __, msg):
    try:
        chat=msg.chat
    except:chat=msg.message.chat
    gp=Group(int(chat.id))
    gp.update
    if int(msg.from_user.id) == gp.Owner :
        return True
    return False 


class Helper:
    def __init__(self) -> None:
        self.text= TEXTS
        self.buttons = BUTTONS
        self.filters=filters
        self.errors = errors
        self.owner = OWNER
        self.co_leader=CO_LEADER
        self.channel_username= CHANNEL_USERNAME
        self.owner_username= OWNER_USERNAME
        self.list_channel= LIST_USERNAME
        self.list_channel= LIST_USERNAME
        self.stats_channel = STATS_CHANNEL
        self.bot_username = BOT_USERNAME
        self.bot_added = filters.create(bot_added)
        self.god_only = filters.create(god_only)
        self.admin_only = filters.create(admin_only)
        self.owner_only = filters.create(owner_only)
        self.game_god = filters.create(game_god)
        self.group_type =[ChatType.GROUP,ChatType.SUPERGROUP]
        self.force_rep = ForceReply
        self.rate_limit_decorator=rate_limit_decorator
        
        self.pedarkhande10 = ['پدرخوانده 10' , 'دکتر واتسون-همشهری کین-لئون-کنستانتین-خبرنگار-شهروند','گادفادر-ساول گودمن-ماتادور','نوستراداموس']
        self.mozakere10 = ['مذاکره 10' , 'دکتر-کاراگاه-زره پوش-خبرنگار-شهروندساده-شهروندساده','گادفادر-مذاکره کننده-مافیا ساده','none']
        self.bazpors10 = ['بازپرس 10' , 'بازپرس-هانتر-دکتر-کاراگاه-شهروندساده-شهروندساده-رویین تن','گادفادر-ناتو-شیاد','none']
        self.nato10 = ['ناتو10' , 'نگهبان-تفنگدار-دکتر-کاراگاه-شهروندساده-شهروندساده-تکاور','گادفادر-ناتو-گروگانگیر','none']
        self.mitic12 = ['میتیک' , 'دکتر-کاراگاه-اسنایپر-بادیگارد-شهروندساده-شهروندساده-شهروندساده-شهروندساده','گادفادر-کانسورت-نینجا-تروریست','none']
        self.bazpors12 = ['بازپرس 12' , 'بازپرس-هانتر-دکتر-کاراگاه-اسنایپر-شهروندساده-رویین تن-شهروندساده','گادفادر-ناتو-شیاد-مافیا ساده','none']
        self.bazpors13 = ['بازپرس 13' , 'بازپرس-هانتر-دکتر-کاراگاه-اسنایپر-شهروندساده-شهروندساده-رویین تن-شهروندساده','گادفادر-ناتو-شیاد-مافیا ساده','none']
        
#----------------------------------------------------------------------------------------------------------------|
    def GROUP(self,Func):                                                                                      #-| <Give User Group Instance to Func>
        async def Wrapper(cli, message):                                                                       #-|
            try:ID=message.chat.id                                                                             #-|
            except:ID=message.message.chat.id                                                                  #-|
            await Func(cli,message,Group(ID))                                                                  #-|
        return Wrapper           
    
    def USER_GROUP(self,Func):                                                                                      #-| <Give User Group Instance to Func>
        async def Wrapper(cli, message):                                                                       #-|
            try:ID=message.chat.id                                                                             #-|
            except:ID=message.message.chat.id                                                                  #-|
            await Func(cli,message,Group(ID),User(message.from_user.id,ID))                                                                  #-|
        return Wrapper           
    
    def status(self,S):
        if S : return '🟢'
        else : return '❌'
    
    def setting_status(self,S):
        if S : return '✅'
        else : return '❌'
    
    def del_mention(self,name,id):
        return (name.replace(f'](tg://user?id={id})',''))[1:]
    
    def user_sort(self,data,kind):
        '''1 score - 2 games - 3 wins - 4 maf wins - 5 shahr win - 6 bests '''
        main_data=[[int(i[0]),i[kind]] for i in data]
        main_data.sort(key=lambda x: x[1],reverse=True)
        return [i[0] for i in main_data]
    
    def limit(self,name):
        name=str(name)
        if not self.is_english_string(name):name='l' + name
        if len(name) > 13 :
            return name[:13].replace('💎','.').replace('🏆','.').replace('🎖','.').replace('🎗','.').replace('👑','.').replace('@','.')
        return name.replace('💎','.').replace('🏆','.').replace('🎖','.').replace('🎗','.').replace('👑','.').replace('@','.')
    
    def activity_emoji(self,activities,i):
        try:
            user=activities[i]
        except:return ''
        if user: return '✅'
        
    def player_list(self,players,c,activities,all_player_text,emoji):
        txt = ''
        for i in range(c):
            if i+1 in players.keys():
                name=str(players[i+1][1]).replace('💎','.').replace('🥇','.').replace('🥈','.').replace('🥉','.').replace('👑','.')
                
                if f'{players[i+1][0]}' in all_player_text:new=''
                else:new='🆕'
                
                txt+=f'{emoji}{i+1}- {name}{players[i+1][2]} {self.activity_emoji(activities,(players[i+1][0]))}{new}\n'
            else:
                txt+=f'/{i+1} \n'
                
        return txt
    
    def warnings(self,dic,i):
        try:
            amount = dic[i]
        except: return ''
        if amount==0: return ''
        elif amount < 5 : return '❗' * amount
        elif amount >= 5 : return f'❗{amount}❗'
    
    def ingame_list(self,players,c,statuses,WARNS,emoji,bests={}):
        txt = ''
        for i in range(c):
            i+=1
            if i in players.keys():
                best=''
                if i in bests.keys():
                    if bests[i]==3:best='🥇'
                    if bests[i]==2:best='🥈'
                    if bests[i]==1:best='🥉'
                name=str(players[i][1]).replace('💎','.').replace('🏆','.').replace('🎖','.').replace('🎗','.').replace('👑','.')
                if statuses[players[i][0]] :
                    txt+=f'{emoji}{i}- {name}{players[i][2]} {self.status(statuses[players[i][0]])}{self.warnings(WARNS,i)}{best}\n'
                else:
                    txt+=f'{emoji}{i}- ~~{name}{players[i][2]}~~ {self.status(statuses[players[i][0]])}{self.warnings(WARNS,i)}{best}\n'
            else:
                txt+=f'/{i} \n'
                
        return txt

    def end_list(self,players,c,roles,sen_rolls:dict,win_n:int,bests,emoji,score,statuses):
        win_text=''
        if win_n ==0 :
            win_text=TEXTS.win0
            win = sen_rolls['white']
        elif win_n == 1 :
            win_text=TEXTS.win1
            win = sen_rolls['black']
        elif win_n == 2  and 'mos' in sen_rolls.keys():
            win_text=TEXTS.win2
            win = sen_rolls['mos']
        txt = ''
        no_death=[]
        for i in range(c):
            i=i+1
            if i in players.keys():
                user=User(int(players[i][0]))
                user.game_done
                name=str(players[i][1]).replace('💎','.').replace('🏆','.').replace('🎖','.').replace('🎗','.').replace('👑','.')
                best=''
                if i in bests.keys():
                    if bests[i]==3:best='🥇'
                    if bests[i]==2:best='🥈'
                    if bests[i]==1:best='🥉'
                    if score > 12 :
                        for t in range(bests[i]):
                            user.add_best

                if  str(roles[i]) in win.split('-') :  
                    if win_n==0:
                        no_death.append(statuses[i])
                        if score > 12 :
                            user.wwin
                            user.add_score((score)* 2)
                    elif win_n==1:
                        no_death.append(statuses[i])
                        if score > 12 :
                            user.bwin
                            user.add_score((score)* 3)
                    else:
                        no_death.append(statuses[i])
                        if score > 12 :
                            user.add_score((score)* 5)
                            user.wwin
                            user.bwin
                        
                    txt+=f'{emoji}{i}- {name}{players[i][2]}l {roles[i]}{self.text.winner}{best}\n'
                else:
                    if score > 12 :
                        user.add_score((score)* 1)
                    txt+=f'{emoji}{i}- {name}{players[i][2]}l {roles[i]}{best}\n'
            else:
                txt+=f'{i}  \n'
        if all(no_death) : win_text = win_text + TEXTS.no_death
        
        txt += f'\n🔅: {win_text} '
        return txt

    @property
    def all_users(self):
        return DataBase.show_all_users()
        
    @property
    def all_M_users(self):
        return DataBase.show_all_MMMM_users()
    
    @property
    def all_groups(self):
        return DataBase.See_all_groups()
    
    @property
    def all_games(self):
        games=[]
        for i in self.all_groups:
            g=Group(int(i[0]))
            games+=g.all_games
        return games
        
    def is_english_string(self,sentence):
        arabic_range = set(range(0x600, 0x700))
        arabic_with_hamza_range = set([0x621, 0x622, 0x623, 0x624, 0x625, 0x626, 0x627, 0x628, 0x629])
        arabic_extended_range = set([0x62A, 0x62B, 0x62C, 0x62D, 0x62E, 0x62F, 0x630, 0x631, 0x632, 0x633,
                                    0x634, 0x635, 0x636, 0x637, 0x638, 0x639, 0x63A, 0x641, 0x642, 0x643,
                                    0x644, 0x645, 0x646, 0x647, 0x648, 0x649, 0x64A, 0x651])
        persian_range = set([0x6A9, 0x6AF, 0x6CC, 0x6C0, 0x6CC, 0x6CE, 0x6D0, 0x6D1, 0x6D2, 0x6D3])

        arabic_and_persian_chars = arabic_range.union(arabic_with_hamza_range, arabic_extended_range, persian_range)

        r= any(ord(char) in arabic_and_persian_chars for char in str(sentence))
        if r : return False
        else:return True

    def replace_main_list(self,template:str,sen,god,plyrs,username,time,date,event):
        return template.replace('{DATE_TEXT}',date).replace('{PLAYERS_TEXT}',plyrs).replace('{SENATIO_TEXT}',sen).replace('{GOD_NAME_TEXT}',god).replace('{GROUP_USERNAME_TEXT}',username).replace('{TIME_TEXT}',time).replace('{EVENT_TEXT}',event)
    
    def main_list(self,sen,god,plyrs,username,time='نامشخص',chat:Group=None):
        chat.update
        event= f'#Event_{(chat.ev_num)}'
        date=self.get_persian_date()
        if chat.template :
            return self.replace_main_list(chat.template,sen,god,plyrs,username,time,date,event)
            
        else:
            return self.text.main_list(sen,god,plyrs,username,time,event,date)
        
    def get_persian_date(self):
        today = jdatetime.date.today()
        persian_date = today.strftime('%Y/%m/%d')
        persian_date_str = persian_date.replace('-', '/')
        return persian_date_str

    def get_command_id(self,message):
        if message.reply_to_message : 
            user_id=message.reply_to_message.from_user.id
        else  : 
            user_id=str(message.command[1])
            if user_id.isdigit():
                user_id=int(user_id)
                
        return user_id
    
    def convert_to_persian_calendar(self,gregorian_date_string, date_format='%Y-%m-%d-%H:%M'):
        gregorian_date = jdatetime.datetime.strptime(gregorian_date_string, date_format).date()
        persian_date = jdatetime.date.fromgregorian(date=gregorian_date)
        return persian_date.strftime(date_format)

    def get_top_groups(self,all_games, top_count=5,days=-30):
        '''group_id,scenario,god,point,date,win,active,mid,all_plyrs'''
        delta =(datetime.datetime.now() + datetime.timedelta(days=days))        
        group_scores = defaultdict(float)
        for game in all_games:
            game_date = datetime.datetime.strptime(game[4], "%Y-%m-%d-%H:%M") 
            if ( delta - datetime.timedelta(minutes=(int(self.call_time(  (int(len(game[8].split('-')))) , (int(game[3]))))+20) ) ) <= game_date :
                try:
                    group_scores[int(Group(game[0]).main)] += int(game[3])  
                except Exception as e : self.Log(f'{e} in get_top_groups')

        sorted_groups = sorted(group_scores.keys(), key=lambda x :group_scores[x] , reverse=True)
        top_groups = sorted_groups[:top_count]
        finall={}
        for i in top_groups : 
            finall[i]=group_scores[i]
            

        return finall

    def get_top_5_players_info(self,all_users_data,kind):
        '''1 score - 2 games - 3 wins - 4 maf wins - 5 shahr win - 6 bests '''
        sorted_users = sorted(all_users_data, key=lambda user: user[kind], reverse=True)
        top_5_players_info = [(user[0], user[kind]) for user in sorted_users[:10]]

        return top_5_players_info

    def get_all_player_ranks(self,all_users_data):
        sorted_users = sorted(all_users_data, key=lambda user: user[2], reverse=True)
        user_ranks = {user[0]: rank + 1 for rank, user in enumerate(sorted_users)}
        return user_ranks

    def plot_games_per_day(self,last_month_games):
        games_per_day = {}

        for game in last_month_games:
            date_str = game[4]  
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d-%H:%M')
            date_str = date_obj.strftime('%Y-%m-%d')

            games_per_day[date_str] = games_per_day.get(date_str, 0) + 1

        sorted_dates = sorted(games_per_day.keys())

        game_counts = [games_per_day[date] for date in sorted_dates]

        sorted_dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in sorted_dates]
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(sorted_dates, game_counts, marker='o', linestyle='-', color='b', label='Games Played')
        
        ax.xaxis.set_major_locator(plt.MaxNLocator(6))  
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))  
        
        plt.xticks(rotation=45)
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Games Played')
        ax.set_title('Games Played Per Day Last Month')
        
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        random_string = ''.join(choice(string.ascii_letters) for _ in range(10))
        plt.savefig(f'{random_string}.png')
        return f'{random_string}.png'
    
    def Join_Channel(self,Func):
        async def Wrapper(client, message):
            try:
                await client.get_chat_member(self.channel_username,int(message.from_user.id))
                await client.get_chat_member(self.list_channel,int(message.from_user.id))
                try:
                    await Func(client,message)
                except:pass
            except:await message.reply_text(TEXTS.Join_Channel(self.channel_username,self.list_channel),reply_markup=BUTTONS.Channel_Join(self.channel_username,self.list_channel))
        return Wrapper
    
    def create_bar_chart(self,gods_count):
        names = []

        gods, counts = zip(*gods_count.items())

        # Custom design parameters
        bar_edge_color = 'black'
        bar_width = 0.5

        # Calculate the number of subplots needed
        num_subplots = (len(gods) // 7) + (len(gods) % 7 > 0)

        # Create subplots
        for i in range(num_subplots):
            start_idx = i * 7
            end_idx = (i + 1) * 7
            subset_gods = gods[start_idx:end_idx]
            bar_colors = [choice(['skyblue', 'lightcoral', 'lightgreen', 'lightsalmon', 'lightblue', 'lightpink', 'lightyellow']) for _ in subset_gods]
            subset_counts = [gods_count[god] for god in subset_gods]

            x_values = range(len(subset_gods))
            plt.figure(figsize=(12, 8))
            plt.bar(x_values, subset_counts, color=bar_colors, edgecolor=bar_edge_color, width=bar_width)

            # Set x-axis tick labels
            plt.xticks(x_values, subset_gods, rotation=45, ha='right')

            plt.xlabel('Game Gods')
            plt.ylabel('Games ')
            plt.title(f'Gods Stats ')

            plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

            plt.grid(axis='y', linestyle='--', alpha=0.7)

            # Use tight layout
            plt.tight_layout()

            random_string = ''.join(choice(string.ascii_letters) for _ in range(10))
            plt.savefig(f'plot_{random_string}.png')
            names.append(f'plot_{random_string}.png')

            plt.clf()

        # Return a list of saved file names
        return names
        

    def Log(self,message=None):                                                                        
        with open('Logs.txt','a+',encoding='utf-8') as f :                                                    
            f.write(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}  → {message} \n \n ' ) 
    
    
    def generate_random_int(self,min_value, max_value):
        return randint(min_value, max_value)

    def call_time(self,players,score):
        
        if score==0:return 0
        
        if players > 13:
            players=13
            
        ad_score=( score / players )
        if ad_score >= 3 : return 180
        elif ad_score >= 2.50 :return 150
        elif ad_score >= 2.25 :return 120
        elif ad_score >= 2.10 :return 105
        elif ad_score >= 2 :return 90
        elif ad_score >= 1.8 :return 75
        elif ad_score >= 1.6 :return 60
        elif ad_score >= 1.3 :return 40
        elif ad_score >= 1 :return 30
        elif ad_score >= 0.5 :return 20
        else:return 0
        
    def is_persian_arabic(self,sentence):
        persian_range = (0x0600, 0x06FF)  
        arabic_range = (0x0750, 0x077F)   

        for char in str(sentence):
            if char.isspace() or char == '.':
                continue  
            char_code = ord(char)
            if not (persian_range[0] <= char_code <= persian_range[1] or arabic_range[0] <= char_code <= arabic_range[1]):
                return False
        return True
        
class GameState:
    def __init__(self, god, players_count, players, main, scenario, status, mid, link, roles, time, warns, activity, run_time, bests):
        self.god = god
        self.players_count = players_count
        self.players = players
        self.main = main
        self.scenario = scenario
        self.status = status
        self.mid = mid
        self.link = link
        self.roles = roles
        self.time = time
        self.warns = warns
        self.activity = activity
        self.run_time = run_time
        self.bests = bests
        self.call=0
        self.invite=False
        self.timer_status = 0
        self.chosen_cards=[]
    
class User_no_intract:
    def __init__(self, id):
        self.id = id
        self.mention =lambda x: x
        self.first_name = id
        
helper = Helper()