from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup , InlineQueryResultArticle, InputTextMessageContent
from pyrogram.types.bots_and_keyboards import force_reply 

start=ReplyKeyboardMarkup([['امار من👤','گروه ها 👁️'],['🚀 بازی ها'],['پشتیبانی 👨‍💻']],resize_keyboard =True)

start_new_game=InlineKeyboardMarkup([[InlineKeyboardButton('بله', callback_data='Yes_Start_New'),InlineKeyboardButton('خیر', callback_data='No_Dont_start_New')]])

Support=lambda username: InlineKeyboardMarkup([[InlineKeyboardButton('📞 پشتیبانی', url=f'https://t.me/{username}')]])

Channel_Join=lambda username,li_username: InlineKeyboardMarkup([[InlineKeyboardButton('🎩 Dark ', url=f'https://t.me/{username}')],
                                                                [InlineKeyboardButton('🎩 Events ', url=f'https://t.me/{li_username}')]])        
def choose_scenario(scenarios,change=False):
    Inlines=[]
    li=[]
    Stype = 'Start'
    if change : Stype = 'Change'
    if len(scenarios) < 4 : 
        for i in range(len(scenarios)):
            li.append(InlineKeyboardButton(f'{scenarios[i]}', callback_data=f'{Stype}_sen_{scenarios[i]}'))
        Inlines.append(li)
    
    else:
        s_len=len(scenarios)
        R = (s_len% 3)
        n= s_len - R
        for i in range(0,n,3):
            Inlines.append([InlineKeyboardButton(f'{scenarios[i]}', callback_data=f'{Stype}_sen_{scenarios[i]}'),
                        InlineKeyboardButton(f'{scenarios[i+1]}', callback_data=f'{Stype}_sen_{scenarios[i+1]}'),
                        InlineKeyboardButton(f'{scenarios[i+2]}', callback_data=f'{Stype}_sen_{scenarios[i+2]}')])
            
        if R !=0 :
            for i in range(R):
                li=[]
                li.append(InlineKeyboardButton(f'{scenarios[n+i]}', callback_data=f'{Stype}_sen_{scenarios[n+i]}'))
                
            Inlines.append(li)
            
    if change :Inlines.append([InlineKeyboardButton('بازگشت🔙', callback_data='ToHomeBack')])
    return InlineKeyboardMarkup(Inlines) 

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
game_buttons=InlineKeyboardMarkup([[InlineKeyboardButton('تغییر سناریو 🃏', callback_data='Choose_change_sen'),InlineKeyboardButton('Tag', callback_data='TAG'),InlineKeyboardButton('Kick 🗑', callback_data='Edit_The_Game')],
                                   [InlineKeyboardButton('دعوت نامه 📨', callback_data='Send_invitation'),InlineKeyboardButton('احضاریه📢', callback_data='Call_Players')],
                                   [InlineKeyboardButton('نام فارسی 🖋', callback_data='Player_name'),InlineKeyboardButton('پاکسازی ♻️', callback_data='Clean_The_Chats')],
                                   [InlineKeyboardButton('اعلام حضور✅', callback_data='Player_is_ready')],
                                   [InlineKeyboardButton('ران 🌕', callback_data='Run_the_Game')]])

    
def edit_game(players):
    nlist=[i+1 for i in range(players)]
    composite_list = [nlist[x:x+5] for x in range(0, len(nlist),5)]
    
    Inlines=[]
    li=[]
    
    for i in composite_list : 
        for t in i :
            li.append(InlineKeyboardButton(f'{t}', callback_data=f'Delete_Player_{t}'))
            
        Inlines.append(li)
        li=[]
    Inlines.append([InlineKeyboardButton('بازگشت🔙', callback_data='Back')])
    return InlineKeyboardMarkup(Inlines) 

def Add_Warn_Btn(players):
    nlist=[i+1 for i in range(players)]
    composite_list = [nlist[x:x+5] for x in range(0, len(nlist),5)]
    Inlines=[]
    li=[]
    Inlines.append([InlineKeyboardButton('⚠🛑اضافه کردن اخطار🛑⚠', callback_data='NOONE')])
    for i in composite_list : 
        for t in i :
            li.append(InlineKeyboardButton(f'{t}', callback_data=f'Add_Warn_For_{t}'))
            
        Inlines.append(li)
        li=[]
    
    Inlines.append([InlineKeyboardButton('🪣🛑حذف اخطار🛑🪣', callback_data='NOOONE')])
    
    for i in composite_list : 
        for t in i :
            li.append(InlineKeyboardButton(f'{t}', callback_data=f'Delete_Warn_For_{t}'))
            
        Inlines.append(li)
        li=[]
    Inlines.append([InlineKeyboardButton('بازگشت🔙', callback_data='Back')])
    return InlineKeyboardMarkup(Inlines) 

def Ellection_For_Btn(players,delete=False):
    nlist=[i+1 for i in range(len(players))]
    composite_list = [nlist[x:x+5] for x in range(0, len(nlist),5)]
    Inlines=[]
    li=[]
    if not delete:
        Inlines.append([InlineKeyboardButton('📥 رای گیری اولیه', callback_data='First_Election')])
        Inlines.append([InlineKeyboardButton('⬇🛑⬇ رای خروج ⬇🛑⬇  ', callback_data='Help_for_Election')])
    for i in composite_list : 
        for t in i :
            if players[t]:
                li.append(InlineKeyboardButton(f'{t}', callback_data=f'Ellection_For_{t}'))
            
        Inlines.append(li)
        li=[]
    if not delete:
        Inlines.append([InlineKeyboardButton('بازگشت🔙', callback_data='Back')])
    return InlineKeyboardMarkup(Inlines) 

def edit_status(players):
    nlist=[i+1 for i in range(len(players))]
    composite_list = [nlist[x:x+5] for x in range(0, len(nlist),5)]
    Inlines=[]
    li=[]
    for i in composite_list : 
        for t in i :
            li.append(InlineKeyboardButton(f'{t}', callback_data=f'Status_Changed_for_{t}'))
            
        Inlines.append(li)
        li=[]
    Inlines.append([InlineKeyboardButton('بازگشت🔙', callback_data='Back')])
    return InlineKeyboardMarkup(Inlines) 

ingame_edit=InlineKeyboardMarkup([[InlineKeyboardButton('تغییر وضعیت', callback_data='Change_Status'),InlineKeyboardButton('Kick 🗑', callback_data='Edit_The_Game')],
                                  [InlineKeyboardButton('اخطار⚠', callback_data='Add_delete_Warn'),InlineKeyboardButton('ارسال نقش دوباره', callback_data='Send_Roles_Again')],
                                  [InlineKeyboardButton('رای گیری 🗳️', callback_data='Ellection'),InlineKeyboardButton('استعلام وضعیت 🪦', callback_data='Inquiry_Status')],
                                 [InlineKeyboardButton('اتمام 🌑', callback_data='Game_Finished'),InlineKeyboardButton('رندوم مجدد ♻️', callback_data='Change_Random_roles')]])


def win(mos):
    Inlines=[[InlineKeyboardButton('برد مافیا', callback_data='Win_1'),
              InlineKeyboardButton('برد شهر', callback_data='Win_0')]]
    if mos:
        Inlines.append([InlineKeyboardButton('برد مستقل', callback_data='Win_2')])
    
    Inlines.append([InlineKeyboardButton('Bests🥇' ,callback_data='Add_bests')])
    
    Inlines.append([InlineKeyboardButton('بازگشت🔙', callback_data='Back')])
    return InlineKeyboardMarkup(Inlines)

def add_best(players):
    nlist=[i+1 for i in range(players)]
    composite_list = [nlist[x:x+5] for x in range(0, len(nlist),5)]
    
    Inlines=[]
    li=[]
    
    for i in composite_list : 
        for t in i :
            li.append(InlineKeyboardButton(f'{t}', callback_data=f'Add_Best_For_{t}'))
            
        Inlines.append(li)
        li=[]
    Inlines.append([InlineKeyboardButton('بازگشت🔙', callback_data='Back')])
    return InlineKeyboardMarkup(Inlines) 

def add_best_kind(player,bests):
    best=['','','']
    if player in bests.keys():
        if bests[player]==1 :best=['','','🔘']
        if bests[player]==2 :best=['','🔘','']
        if bests[player]==3 :best=['🔘','','']
    return InlineKeyboardMarkup([[InlineKeyboardButton(f'شماره {player}', callback_data=f'Nothing_amiralirj')],
        [InlineKeyboardButton(f'🥇{best[0]}', callback_data=f'Final_BestFor_{player}_3')],
        [InlineKeyboardButton(f'🥈{best[1]}', callback_data=f'Final_BestFor_{player}_2'),InlineKeyboardButton(f'🥉{best[2]}', callback_data=f'Final_BestFor_{player}_1')],
        [InlineKeyboardButton('حذف بست', callback_data=f'Final_BestFor_{player}_0'),InlineKeyboardButton('بازگشت🔙', callback_data='Add_bests')]])
    
approve = lambda user : InlineKeyboardMarkup([[InlineKeyboardButton('تایید ✅', callback_data=f'Approve_request_{user}')]])

def setting_main(title,emoji,username,name_status):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f'{emoji}', url=f'https://t.me/{username}'),InlineKeyboardButton(f'{title}', url=f'https://t.me/{username}'),InlineKeyboardButton(f'{emoji}', url=f'https://t.me/{username}')],
        [InlineKeyboardButton('🛡 قفل جوین', callback_data=f'Join_Lock'),InlineKeyboardButton('🔒محدودیت لیست', callback_data=f'List_Lock')],
        [InlineKeyboardButton('🎩 ایموجی گروه', callback_data=f'Group_Emoji'),InlineKeyboardButton(f'🪶 نام فارسی {name_status}' , callback_data=f'Persian_Name')],
        [InlineKeyboardButton('📜 سناریو ها', callback_data=f'Scenarios_Setting_Main')],
        [InlineKeyboardButton('بستن 🪦', callback_data=f'CloseList')]
        
        ])
    
def lock(mode,n):
    nums=[1,3,5,7,10,13,15,17,20,25,30,40,50,75,100,150,200,250,300,500]
    composite_list = [nums[x:x+5] for x in range(0, len(nums),5)]
    
    Inlines=[]
    li=[]
    
    Inlines.append([InlineKeyboardButton(f'{n}', callback_data=f'Nothing_amiralirj'),InlineKeyboardButton(f'مقدار فعلی :', callback_data=f'Nothing_amiralirj')])
    Inlines.append([InlineKeyboardButton('🔓  "0" غیر فعال کردن', callback_data=f'Lock_Change_{mode}_0')])
    for i in composite_list : 
        for t in i :
            li.append(InlineKeyboardButton(f'{t}', callback_data=f'Lock_Change_{mode}_{t}'))
            
        Inlines.append(li)
        li=[]
    Inlines.append([InlineKeyboardButton('بازگشت🔙', callback_data='SETTINGBACK')])
    return InlineKeyboardMarkup(Inlines) 

def emoji_choose(emoji):
    emoji_list = ['🧬', '💣', '🧨', '🪓', '🕋', '💊', '💉', '🩸', '🦠', '🪬', '🧿', '🔮', '🪦', '🧸', '🕯', '🏝', '🔫', '🤍', '🖤', '💜', '💙', '🩵', '💚', '✨', '🧡', '🩷',  '❤️‍🔥', '🔆', '🔰', '🔱', '⚜️', '♥️', '♦️', '♣️', '♠️', '🐚', '🎴', '🥂', '💰', '🥃', '🍯', '🍷', '💦', '💧', '🌏', '🌗', '🌕', '🌑', '🔥', '🌪', '☘️', '🍀', '🍄', '🐊', '🐶', '🎩', '💍', '👑', '🪖', '🤡', '💩', '👾', '👽', '🛸', '▪️', '▫️', '🌐', '🎩','🚀','❄️']
    composite_list = [emoji_list[x:x+10] for x in range(0, len(emoji_list),10)]
    
    Inlines=[]
    li=[]
    
    Inlines.append([InlineKeyboardButton(f'{emoji}', callback_data=f'Nothing_amiralirj'),InlineKeyboardButton(f'مقدار فعلی :', callback_data=f'Nothing_amiralirj')])
    for i in composite_list : 
        for t in i :
            li.append(InlineKeyboardButton(f'{t}', callback_data=f'Lock_Emoji_{t}'))
            
        Inlines.append(li)
        li=[]
    Inlines.append([InlineKeyboardButton('بازگشت🔙', callback_data='SETTINGBACK')])
    return InlineKeyboardMarkup(Inlines) 

def scenarios_main(emoji,username):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f'{emoji}', url=f'https://t.me/{username}'),InlineKeyboardButton(f'{emoji}', url=f'https://t.me/{username}'),InlineKeyboardButton(f'{emoji}', url=f'https://t.me/{username}')],
        [InlineKeyboardButton('📓 سناریو ها', callback_data=f'See_All_Scenarios')],
        [InlineKeyboardButton('📤🗑 حذف سناریو', callback_data=f'Del_Sen'),InlineKeyboardButton('📥 افزودن سناریو', callback_data=f'Add_Sen')],
        [InlineKeyboardButton('بستن 🪦', callback_data=f'CloseList')]])
    
def all_scenarios(scenarios,delete):
    
    composite_list = [scenarios[x:x+4] for x in range(0, len(scenarios),4)]
    
    Inlines=[]
    li=[]
    
    if delete:kind='delete'
    else:kind='see'
    
    for i in composite_list : 
        for t in i :
            li.append(InlineKeyboardButton(f'{t}', callback_data=f'SettingScenarios_{kind}_{t}'))
            
        Inlines.append(li) 
        li=[]
    Inlines.append([InlineKeyboardButton('بازگشت🔙', callback_data='SCENARIOSBACK')])
    return InlineKeyboardMarkup(Inlines) 


def all_cards(cards,delete=False):
    
    composite_list = [cards[x:x+4] for x in range(0, len(cards),4)]
    
    Inlines=[]
    li=[]
    
    if delete:kind='delete'
    else:kind='see'
    
    for i in composite_list : 
        for t in i :
            li.append(InlineKeyboardButton(f'{t}', callback_data=f'Show_card_{kind}_{t}'))
            
        Inlines.append(li) 
        li=[]
    Inlines.append([InlineKeyboardButton('بازگشت🔙', callback_data='CARDSBACK')])
    return InlineKeyboardMarkup(Inlines) 

def cards_main(emoji,username):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f'{emoji}', url=f'https://t.me/{username}'),InlineKeyboardButton(f'{emoji}', url=f'https://t.me/{username}'),InlineKeyboardButton(f'{emoji}', url=f'https://t.me/{username}')],
        [InlineKeyboardButton('🃏 کارت ها', callback_data=f'See_All_Cards')],
        [InlineKeyboardButton('📤🗑 حذف کارت', callback_data=f'Del_Card'),InlineKeyboardButton('📥 افزودن کارت', callback_data=f'Add_Card')],
        [InlineKeyboardButton('بستن 🪦', callback_data=f'CloseList')]])
    
def pick_card(cards):
    
    composite_list = [cards[x:x+4] for x in range(0, len(cards),4)]
    
    Inlines=[]
    li=[]
    
    for i in composite_list : 
        for t in i :
            li.append(InlineKeyboardButton(f'{t}', callback_data=f'Pic_Card_{t}'))
            
        Inlines.append(li) 
        li=[]
    return InlineKeyboardMarkup(Inlines) 
