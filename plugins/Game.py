from random import  choice , randint , shuffle
from asyncio import sleep
from Classes.MafClass import helper , User , Game , Group , GameState , User_no_intract
from Classes.CliClass import Mafia
import datetime

games = {}
player_ask=[]
@Mafia.on_message(  helper.filters.private & helper.filters.regex('^🚀 بازی ها') , group=0)
@helper.rate_limit_decorator
async def Games_ruuning(bot,message):
    text=''
    for i in games : 
        if not games[i].status:
            try:
                chat_o = (await bot.get_chat(int(i)))
                if chat_o.username : 
                    title = chat_o.username
                else:
                    title = chat_o.title
            except :
                title =int(i)
                
            text+=helper.text.games_running(title , games[i].scenario , games[i].players_count , games[i].link , games[i].god[1] , games[i].run_time ,(int(games[i].players_count) - len(games[i].players))  )
        if text.count(f"{helper.text.lines}") > 7 :
            await message.reply_text(text,quote =True,disable_web_page_preview =False)
            text=''
            
    
    if text !='' :
        await message.reply_text(text,quote =True,disable_web_page_preview =False)
        text=''
        
        
        
        
    
@Mafia.on_message(  helper.filters.command('start_the_bot') & (helper.filters.user(helper.owner)) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Bot_backup(bot: Mafia, message, chat: Group):
    global games
    data = helper.user_sort(helper.all_M_users, 1)
    for t in helper.all_groups:
        for i in t:
            if i in games.keys():continue
            try:
                gp = Group(int(i))
                if gp.have_active:
                    game = Game(int(i))
                    game.update
                    helper.Log(game.god)
                    god = (await bot.get_users(game.god))

                    players_list = {}
                    
                    try:
                        users = await bot.get_users(game.all_players)
                    except Exception as e:
                        print(e)
                        users=[]
                        for player_id in game.all_players:
                            try:
                                users.append((await bot.get_users(player_id)))
                            except :
                                users.append(User_no_intract(player_id))
                                helper.Log(f"User with ID {player_id} not found or cannot be interacted with.")

                        

                    for user_patched in users:
                        players_list[int(user_patched.id)] = user_patched

                    players = {}
                    roles = {}
                    for q in str(game.all_plyrs).split('-'):
                        q = q.split(':')
                        if q[0] in f'NUM{q[-1]}':
                            roles[int(q[-1])] = q[1]
                        else:
                            ID = int(q[0].replace('A', '').replace('D', ''))
                            roles[int(q[-1])] = q[1]
                            P = players_list[ID]
                            user_obj=User(P.id)
                            if gp.farsi:
                                try:
                                    pl_name=P.mention(user_obj.name)
                                except:
                                    pl_name=P.mention('بی نام')
                            else:
                                pl_name=P.mention(helper.limit(P.first_name))
                            players[int(q[2])] = [P.id,pl_name ,
                                                  user_obj.user_emoji(data)]
                    games[int(i)] = GameState(
                        god=[int(god.id), god.mention(helper.limit(god.first_name))],
                        players_count=game.players_count,
                        players=players,
                        main=gp.main,
                        scenario=game.scenario,
                        status=True,
                        mid=int(game.mid),
                        link='no link',
                        roles=roles,
                        time=game.date,
                        warns={},
                        activity={},
                        run_time='',
                        bests={},
                    )

            except Exception as e:
                await message.reply_text(f'{e} in "Bot_backup {i}"')
    await message.reply_text(f'Done')


@Mafia.on_message(  (helper.filters.regex('^cancel$') |helper.filters.regex('^کنسل$') | helper.filters.command('cancel'))  & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def cancel_sign_in(bot: Mafia, message, chat: Group):
    user=int(message.from_user.id)
    if chat.have_active : 
        return
    ex=True
    pdic = games[int(chat)].players
    keys_to_remove = []

    for i in pdic:
        if games[int(chat)].players[i][0] == int(user):
            keys_to_remove.append(i)

    for key in keys_to_remove:
        games[int(chat)].players.pop(key)
        ex = False

        
    if ex:
        return
    x=await message.reply_text(helper.text.cancel_signin)
    players_text=helper.player_list(games[int(chat)].players,games[int(chat)].players_count,games[int(chat)].activity,chat.all_games_players_text,chat.emoji)
    await bot.edit_message_text(int(chat),games[int(chat)].mid , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.game_buttons )
    await x.delete()
    await message.delete()
    
@Mafia.on_message(  helper.filters.command('delete') & (helper.god_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def delete_message_over(bot: Mafia, message, chat: Group):
    id=int(message.id)
    for i in range((int(games[int(chat)].mid)+1),(id+1)):
        try:
            await bot.delete_messages(int(chat),i)
        except:pass
    

@Mafia.on_message(  helper.filters.command('vote') & (helper.god_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def vote_detectior(bot: Mafia, message, chat: Group):
    try : limit= int(message.command[1])
    except: limit=False
    poll = message.reply_to_message.poll
    print('vote')
    txt=''
    for i in poll.options : 
        if i.text[:1] == 'R':continue
        if limit: 
            if i.voter_count >=  limit :
                txt+=helper.text.vvote(i.text[:1] , i.voter_count  )
        else: 
            status=chat.game.status_list_num
            x=0
            
            for s in status :
                if status[s] : x+=1
                
            if i.voter_count >= int(x/2) : 
                txt+=helper.text.vvote(i.text[:1] , i.voter_count  )
        
    await message.reply_text(helper.text.vote_detector( txt))
    
        
@Mafia.on_message(  helper.filters.command('list') & (helper.god_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def send_list_again(bot: Mafia, message, chat: Group):
    game=chat.game
    if chat.have_active or int(chat) in games.keys(): 
        if chat.have_active : 
            players_text=helper.ingame_list(games[int(chat)].players,games[int(chat)].players_count,game.status_list,games[int(chat)].warns,chat.emoji,games[int(chat)].bests)
            x=await bot.send_message(int(chat), helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.ingame_edit)
    
        else:
            players_text=helper.player_list(games[int(chat)].players,games[int(chat)].players_count,games[int(chat)].activity,chat.all_games_players_text,chat.emoji)
            x=await bot.send_message(int(chat), helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.game_buttons) 
        
        try:
            await x.pin()
        except:pass
        try:
            if chat.have_active:
                last_game = Game(int(chat))
                last_game.update
                await bot.delete_messages(int(chat),int(last_game.mid))
            else:
                await bot.delete_messages(int(chat),int(games[int(chat)].mid))
        except :pass
        game.change_mid(int(x.id))
        games[int(chat)].mid=int(x.id)
        
    
@Mafia.on_message(  helper.filters.command('god') & (helper.god_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def set_game_god(bot: Mafia, message, chat: Group):
    user = message.from_user
    if message.reply_to_message :
        if not message.reply_to_message.from_user.is_bot :
            user = message.reply_to_message.from_user
    try:
        games[int(chat)].god= [int(user.id), user.mention(helper.limit(user.first_name))]
        chat.game.change_god(int(user.id))
    except Exception as e:
        helper.Log(f'{e} in SET GAME GOD')
        await message.reply_text(helper.text.aint_started)
        return
    try : 
        if chat.have_active:
            game=chat.game
            game.update
            players_text=helper.ingame_list(games[int(chat)].players,games[int(chat)].players_count,game.status_list,games[int(chat)].warns,chat.emoji,games[int(chat)].bests)
            await bot.edit_message(int(chat),int(game.mid), helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.ingame_edit)
    
        else:
            players_text=helper.player_list(games[int(chat)].players,games[int(chat)].players_count,games[int(chat)].activity,chat.all_games_players_text,chat.emoji)
            await bot.edit_message(int(chat),int(games[int(chat)].mid), helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.game_buttons) 
        
    except Exception as ee :helper.Log(ee)
    await message.reply_text(helper.text.god_changed(user.mention))

@Mafia.on_message(  (helper.filters.regex(r'^/\d{1,3}s$')|helper.filters.regex(r'^\d{1,3}s$')) & (helper.game_god|helper.owner_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def timer_func(bot: Mafia, message, chat: Group):
    if not chat.have_active:return
    if games[int(chat)].timer_status > 3 : return
    sec = int(str(message.text).replace('s','').replace(' ','').replace('/',''))
    if sec > 700 : return 
    if sec < 15 : 
        await message.reply_text(helper.text.timer_start)
        games[int(chat)].timer_status+=1
        await sleep(sec)
        games[int(chat)].timer_status-=1
        await message.reply_text(helper.text.timer_end)
    else : 
        await message.reply_text(helper.text.timer_start)
        games[int(chat)].timer_status+=1
        await sleep((sec-10))
        games[int(chat)].timer_status-=1
        await message.reply_text(helper.text.timer_alarm)
        await sleep(10)
        await message.reply_text(helper.text.timer_end)

@Mafia.on_message(  helper.filters.command('time') & (helper.god_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def set_time(bot: Mafia, message, chat: Group):
    text = str(message.text)[5:]
    if len(text) > 20:
        await message.reply_text(helper.text.error)
        return
    games[int(chat)].run_time = text
    if chat.have_active:
        game=chat.game
        game.update
        players_text=helper.ingame_list(games[int(chat)].players,games[int(chat)].players_count,game.status_list,games[int(chat)].warns,chat.emoji,games[int(chat)].bests)
        await bot.edit_message(int(chat),int(game.mid), helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.ingame_edit)

    else:
        players_text=helper.player_list(games[int(chat)].players,games[int(chat)].players_count,games[int(chat)].activity,chat.all_games_players_text,chat.emoji)
        await bot.edit_message(int(chat),int(games[int(chat)].mid), helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.game_buttons) 
    
    m = await message.reply_text(helper.text.time_added)
    await sleep(4)
    await m.delete()

    
    
@Mafia.on_message(   helper.filters.command('open') & (helper.god_only|helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Open(bot:Mafia,message,chat:Group):
    chat.update
    if chat.have_active or int(chat) in games.keys(): 
        await bot.send_message(int(chat),helper.text.already_have_active_game,reply_markup=helper.buttons.start_new_game)
    else:
        await bot.send_message(int(chat),helper.text.what_scenario,reply_markup=helper.buttons.choose_scenario(chat.all_scenario))
        

@Mafia.on_message(   helper.filters.command('add') & (helper.god_only|helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Add_Player_WC(bot:Mafia,message,chat:Group):
    user = User(message.reply_to_message.from_user.id,int(chat))
    num=int(message.command[1])
    PL=[games[int(chat)].players[i][0] for i in games[int(chat)].players]
    if games[int(chat)].players_count < num : return    
    if int(user) in PL:return
    if user.banned :return
    if num in (games[int(chat)].players).keys() :
        x=(await message.reply_text(helper.text.number_busy))
        await sleep(4)
        await message.delete()
        await x.delete()
        return
    
    data = helper.user_sort(helper.all_M_users,1)
    chat.update
    if chat.farsi:
        try:
            user_name=(user.name)
        except:
            user_name=('بی نام')
    else:
        user_name=helper.limit(message.reply_to_message.from_user.first_name)
    games[int(chat)].players[num] = [int(user),message.reply_to_message.from_user.mention(user_name),user.user_emoji(data)]
    
    if chat.have_active:
        game=chat.game
        if f'NUM{num}' in game.all_plyrs :
            game.add_player(int(user),num)
            players_text=helper.ingame_list(games[int(chat)].players,games[int(chat)].players_count,game.status_list,games[int(chat)].warns,chat.emoji,games[int(chat)].bests)
            await bot.edit_message_text(int(chat),games[int(chat)].mid , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.ingame_edit)
    
        else: return
    else:
        players_text=helper.player_list(games[int(chat)].players,games[int(chat)].players_count,games[int(chat)].activity,chat.all_games_players_text,chat.emoji)
        await bot.edit_message_text(int(chat),games[int(chat)].mid , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.game_buttons )
        
    x=(await message.reply_text(helper.text.signed_in(message.reply_to_message.from_user.mention)))
    
    await sleep(4)
    await x.delete()
    await message.delete()
    
    
@Mafia.on_message(   (helper.filters.regex('^\d{1,3}$')|helper.filters.regex('^/\d{1,3}$')|helper.filters.regex('^/\d{1,3}@DarkMafiaRobot$'))  & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.Join_Channel
@helper.GROUP
async def Sign_in(bot:Mafia,message,chat:Group):
    try:
        num = int(str(message.text).replace('/','').replace('@DarkMafiaRobot',''))
        if games[int(chat)].players_count < num : 
            return         
            
        if num in (games[int(chat)].players).keys() :
            x=(await message.reply_text(helper.text.number_busy))
            await sleep(4)
            await message.delete()
            await x.delete()
            return
        
        chat.update
        user=User(int(message.from_user.id),int(chat))
        

        PL=[games[int(chat)].players[i][0] for i in games[int(chat)].players]
        if int(user) in PL:
            print('in PL returned')
            return

        try:
            if user.banned :
                x=await message.reply_text(helper.text.banned_all,reply_markup=helper.buttons.Support(helper.owner_username))
                await sleep(4)
                await message.delete()
                await x.delete()
                return
                
            if user.is_group_banned():
                data= user.group_show()
                if data[1]=='None':persian_date_string=helper.text.no
                else:persian_date_string = helper.convert_to_persian_calendar(data[1])
                x=(await message.reply_text(helper.text.group_banned(persian_date_string)))
                await sleep(4)
                await message.delete()
                await x.delete()
                return 
                
            if chat.state_lock > user.games :
                x=(await message.reply_text(helper.text.limited))
                await sleep(4)
                await message.delete()
                await x.delete()
                return
        except:pass

        if chat.farsi:
            try:
                user_name=(user.name)
            except:
                user_name=('بی نام')
        else:
            user_name=helper.limit(message.from_user.first_name)
            
        data = helper.user_sort(helper.all_M_users,1)
        games[int(chat)].players[num] = [int(user),message.from_user.mention(user_name),user.user_emoji(data)]
        
        if chat.have_active:
            game=chat.game
            if f'NUM{num}' in game.all_plyrs :
                game.add_player(int(user),num)
                players_text=helper.ingame_list(games[int(chat)].players,games[int(chat)].players_count,game.status_list,games[int(chat)].warns,chat.emoji,games[int(chat)].bests)
                await bot.edit_message_text(int(chat),games[int(chat)].mid , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.ingame_edit)
        
            else: return
        else:
            players_text=helper.player_list(games[int(chat)].players,games[int(chat)].players_count,games[int(chat)].activity,chat.all_games_players_text,chat.emoji)
            await bot.edit_message_text(int(chat),games[int(chat)].mid , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.game_buttons )
            
        x=(await message.reply_text(helper.text.signed_in(message.from_user.mention)))
        
        await sleep(4)
        await x.delete()
        await message.delete()
    except Exception as e : helper.Log(f'{e} IN REGESTER GAME')

    
@Mafia.on_callback_query(  helper.filters.regex('^Yes_Start_New') & (helper.god_only|helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Start_new_game(bot:Mafia,query,chat:Group):
    try:
        if chat.have_active:
            last_game = Game(int(chat))
            last_game.update
            await bot.delete_messages(int(chat),int(last_game.mid))
        else:
            await bot.delete_messages(int(chat),int(games[int(chat)].mid))
    except Exception as e:helper.Log(f'{e} in Start_new_game')
    chat.deactive_all()
    await query.message.edit_text(helper.text.choose_scenario,reply_markup=helper.buttons.choose_scenario(chat.all_scenario))
    games.pop(int(chat))
    
@Mafia.on_callback_query(  helper.filters.regex('^No_Dont_start_New') & (helper.god_only|helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Dont_Start_New_Game(bot:Mafia,query,chat:Group):
    await query.message.delete()
    
@Mafia.on_callback_query(  helper.filters.regex('^Start_sen_') & (helper.god_only|helper.admin_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Start_Scenario(bot:Mafia,query,chat:Group):
    if chat.have_active:return
    scenario = str(query.data).split('_')[-1]
    roles=dict(chat.see_scenario(scenario))
    players= len(str(roles['white']).split('-')) + len(str(roles['black']).split('-')) 
    if 'mos' in roles.keys():
        players += len(str(roles['mos']).split('-'))
        
        
    god=str(query.from_user.first_name)
    
    god = helper.limit(god)
    
    god = str(query.from_user.mention(str(query.from_user.first_name)))
    
    players_text='\n'.join([f'/{i+1}' for i in range(players)])
    mid = await query.message.edit_text(helper.main_list(scenario,god,players_text,chat.title(query.message),chat=chat),reply_markup=helper.buttons.game_buttons)
    try:
        await mid.pin()
    except:pass
    games[int(chat)] = GameState(
        god=[int(query.from_user.id), god],
        players_count=players,
        players={},
        main=chat.main,
        scenario=scenario,
        status=False,
        mid=int(mid.id),
        link=mid.link,
        roles={},
        time=0,
        warns={},
        activity={},
        run_time='',
        bests={}
    )
    if 'mos' in roles.keys():
        send_text=helper.text.show_sen(scenario,'\n'.join(roles['white'].split('-')),'\n'.join(roles['black'].split('-'))) + '\n' + helper.text.mos_sen_show(roles['mos'])
    else:
        send_text=helper.text.show_sen(scenario,'\n'.join(roles['white'].split('-')),'\n'.join(roles['black'].split('-')))

    await query.message.reply_text(send_text)

@Mafia.on_callback_query(  helper.filters.regex('^Choose_change_sen') & (helper.god_only|helper.admin_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Choose_change_sen(bot:Mafia,query,chat:Group):
    await query.message.edit_reply_markup(helper.buttons.choose_scenario(chat.all_scenario,True))
    
    
@Mafia.on_callback_query(  helper.filters.regex('^Change_sen_') & (helper.god_only|helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Change_Scenario(bot:Mafia,query,chat:Group):
    scenario = str(query.data).split('_')[-1] 
    roles=dict(chat.see_scenario(scenario))
    players= len(str(roles['white']).split('-')) + len(str(roles['black']).split('-')) 
    if 'mos' in roles.keys():
        players += len(str(roles['mos']).split('-'))
    
    games[int(chat)].scenario=scenario
    games[int(chat)].players_count=players
    
    r_list=[]
    for pl in games[int(chat)].players :
        if pl > players : 
            r_list.append(pl)
            
    for r_pl in r_list : 
        games[int(chat)].players.pop(r_pl)
        
        
    players_text=helper.player_list(games[int(chat)].players,games[int(chat)].players_count,games[int(chat)].activity,chat.all_games_players_text,chat.emoji)
    await bot.edit_message_text(int(chat),games[int(chat)].mid , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(query.message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.game_buttons) 
    
    if 'mos' in roles.keys():
        send_text=helper.text.show_sen(scenario,'\n'.join(roles['white'].split('-')),'\n'.join(roles['black'].split('-'))) + '\n' + helper.text.mos_sen_show(roles['mos'])
    else:
        send_text=helper.text.show_sen(scenario,'\n'.join(roles['white'].split('-')),'\n'.join(roles['black'].split('-')))

    await query.message.reply_text(send_text)
    
    await query.answer(helper.text.scenario_changed,True)
    
@Mafia.on_callback_query(  helper.filters.regex('^Edit_The_Game') & (helper.god_only|helper.admin_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Edit_Game(bot:Mafia,query,chat:Group):
    await query.message.edit_reply_markup(helper.buttons.edit_game(games[int(chat)].players_count))
    
@Mafia.on_callback_query(  helper.filters.regex('^Delete_Player_') & (helper.god_only|helper.admin_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Delete_Player(bot:Mafia,query,chat:Group):
    num = int(str(query.data).split('_')[-1]) 
    player=games[int(chat)].players.pop(num)[0]
    
    if chat.have_active :
        game=Game(int(chat))
        game.del_player(player,num)
    
    players_text=helper.player_list(games[int(chat)].players,games[int(chat)].players_count,games[int(chat)].activity,chat.all_games_players_text,chat.emoji)
    await bot.edit_message_text(int(chat),int(query.message.id) , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(query.message),games[int(chat)].run_time,chat),reply_markup=query.message.reply_markup) 
    
    

@Mafia.on_callback_query(  helper.filters.regex('^TAG') & (helper.god_only|helper.admin_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def TAG(bot:Mafia,query,chat:Group):
    txt = ''
    for i in games[int(chat)].players :
        txt += f'✣ {games[int(chat)].players[i][1]} \n'
        if len(txt.split('\n')) > 14 : 
            await query.message.reply_text(helper.text.TAG(txt))
            txt = ''
            
    if txt != '' : 
        await query.message.reply_text(helper.text.TAG(txt))
    

@Mafia.on_callback_query(  helper.filters.regex('^Clean_The_Chats') & (helper.god_only|helper.admin_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Clean_extra_chats(bot:Mafia,query,chat:Group):
    id=int((await query.message.reply_text(helper.text.cleaning)).id )
    for i in range((int(games[int(chat)].mid)+2),(id+1)):
        try:
            await bot.delete_messages(int(chat),i)
        except:pass
        
@Mafia.on_callback_query(  helper.filters.regex('^Change_Random_roles') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Change_Random_roles(bot:Mafia,query,chat:Group):
    if not len(games[int(chat)].players) == games[int(chat)].players_count :
            await query.answer(helper.text.list_not_full,True)
            return
        
    roles = chat.see_scenario(games[int(chat)].scenario)
    roles_text=''
    game=chat.game
    all=[]
    all_players=[]
    
    all += str(roles['white']).split('-')
    all += str(roles['black']).split('-')
    
    if 'mos' in roles.keys():
        all += str(roles['mos']).split('-')
    
    shuffle(all)
    for i in sorted(games[int(chat)].players.keys()) : 
        try:
            player_role=choice(all)
            roles_text += f'{i} - {games[int(chat)].players[i][1]} - {player_role} \n'
            
            all.remove(player_role)
            games[int(chat)].roles[i] = player_role
            all_players.append(f'A{games[int(chat)].players[i][0]}:{player_role}:{i}')
            
            await bot.send_message(games[int(chat)].players[i][0],helper.text.send_role(player_role,games[int(chat)].link))
            
        except:
            await bot.send_message(games[int(chat)].god[0],helper.text.role_hasnt_sent(games[int(chat)].players[i][1])) 
            
    all_players='-'.join(all_players)
    game.change_players(all_players)
    await bot.send_message(games[int(chat)].god[0],roles_text) 
    
    
    
    
@Mafia.on_callback_query(  helper.filters.regex('^Run_the_Game') & (helper.god_only|helper.admin_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Run_Game(bot:Mafia,query,chat:Group):
    if games[int(chat)].god[0] != query.from_user.id : return
    try:
        if games[int(chat)].status==True:return
        games[int(chat)].status=True
        
        if chat.have_active: 
            await query.answer(helper.text.active_game_detected,True)
            games[int(chat)].status=False
            return
        
        if not len(games[int(chat)].players) == games[int(chat)].players_count :
            await query.answer(helper.text.list_not_full,True)
            games[int(chat)].status=False
            return
        
        try:
            await bot.send_message(games[int(chat)].god[0],helper.text.game_started(games[int(chat)].link))
        except:
            await query.answer(helper.text.start_bot,True)
            games[int(chat)].status=False
            return
        
        await query.answer(helper.text.is_running,True)
        
        roles = chat.see_scenario(games[int(chat)].scenario)
        roles_text=''
        
        all=[]
        all_players=[]
        
        all += str(roles['white']).split('-')
        all += str(roles['black']).split('-')
        
        if 'mos' in roles.keys():
            all += str(roles['mos']).split('-')
        
        shuffle(all)
        for i in sorted(games[int(chat)].players.keys()) : 
            try:
                player_role=choice(all)
                roles_text += f'{i} - {games[int(chat)].players[i][1]} - {player_role} \n'
                
                all.remove(player_role)
                games[int(chat)].roles[i] = player_role
                all_players.append(f'A{games[int(chat)].players[i][0]}:{player_role}:{i}')
                
                await bot.send_message(games[int(chat)].players[i][0],helper.text.send_role(player_role,games[int(chat)].link))
                
            except:
                await bot.send_message(games[int(chat)].god[0],helper.text.role_hasnt_sent(games[int(chat)].players[i][1])) 
                
        await bot.send_message(games[int(chat)].god[0],roles_text) 
        date=str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M"))
        games[int(chat)].time=date
        game=Game(int(chat))
        dic = games[int(chat)]
        
        
        all_players='-'.join(all_players)
        game.start_game(
            dic.scenario , dic.god[0] ,
            all_players,
            int(query.message.id)
            )
        games[int(chat)].mid=int(query.message.id)
        players_text=helper.ingame_list(games[int(chat)].players,games[int(chat)].players_count,game.status_list,games[int(chat)].warns,chat.emoji,games[int(chat)].bests)
        await bot.edit_message_text(int(chat),query.message.id , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(query.message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.ingame_edit )
    except Exception as e : 
        helper.Log(f'{e} IN RUN GAME ')

    

@Mafia.on_callback_query(  helper.filters.regex('^Inquiry_Status') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Inquiry_Status(bot:Mafia,query,chat:Group):
    text=''
    mos=0
    white=0
    black = 0
    roles=dict(chat.see_scenario(games[int(chat)].scenario))
    status=chat.game.status_list_num
    for i in status:
        if not status[i]:
            if games[int(chat)].roles[(i)] in (roles['white']).split('-'):
                white+=1
            if games[int(chat)].roles[(i)] in (roles['black']).split('-'):
                black+=1
            if 'mos' in roles.keys():
                if games[int(chat)].roles[(i)] in (roles['mos']).split('-'):
                    mos+=1
                


    if white != 0 :text +=f'{helper.text.w_inquiry(white)} \n'
    if black != 0 :text +=f'{helper.text.b_inquiry(black)} \n'
    if mos != 0 :text +=f'{helper.text.m_inquiry(mos)} \n'
    if text =='' : text+=helper.text.no_deaths
    
    await query.message.reply_text(text)
            
            
    
@Mafia.on_callback_query(  helper.filters.regex('^Change_Status') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Change_status_button(bot:Mafia,query,chat:Group):
    games[int(chat)].mid=int(query.message.id)
    game=Game(int(chat))
    game.update
    await query.message.edit_reply_markup(helper.buttons.edit_status(game.all_players))
    
@Mafia.on_callback_query(  helper.filters.regex('^Status_Changed_for_') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Player_status_change(bot:Mafia,query,chat:Group):
    num = int(str(query.data).split('_')[-1]) 
    player = int(games[int(chat)].players[num][0])
    game=Game(chat)
    game.change_status(player)
    players_text=helper.ingame_list(games[int(chat)].players,games[int(chat)].players_count,game.status_list,games[int(chat)].warns,chat.emoji,games[int(chat)].bests)
    await bot.edit_message_text(int(chat),games[int(chat)].mid , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(query.message),games[int(chat)].run_time,chat),reply_markup=query.message.reply_markup)
    
@Mafia.on_callback_query(  helper.filters.regex('^Game_Finished') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Game_finished(bot:Mafia,query,chat:Group):
    scenario = games[int(chat)].scenario
    roles=dict(chat.see_scenario(scenario))
    mos = 0
    if 'mos' in roles.keys():
        mos = 1
    await query.message.edit_reply_markup(helper.buttons.win(mos))
    
@Mafia.on_callback_query(  helper.filters.regex('^Win_') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Win_Ask_End(bot:Mafia,query,chat:Group):
    try:
        win = int(str(query.data).split('_')[-1]) 
        status_list=chat.game.status_list_num
        score = chat.game.end_game(win)
        scenario = games[int(chat)].scenario
        sen_roll=dict(chat.see_scenario(scenario))
        players_text=helper.end_list(games[int(chat)].players,games[int(chat)].players_count,games[int(chat)].roles,sen_roll,win,games[int(chat)].bests,chat.emoji,score,status_list)
        try:await query.message.delete()
        except:pass
        end_list_m=await bot.send_message(int(chat) , text=helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(query.message),games[int(chat)].run_time,chat))
        try:
            await end_list_m.pin()
        except:pass
        chat.change_Ev_num()
        start_date =datetime.datetime.strptime(games[int(chat)].time, "%Y-%m-%d-%H:%M") 
        td = datetime.datetime.now() - start_date 
        minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
        hours, minutes = divmod(minutes, 60)
        time_text = '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)

        await query.message.reply_text(helper.text.end_list(time_text,str(start_date.strftime("%H:%M")),str(datetime.datetime.now().strftime("%H:%M")),games[int(chat)].players_count,games[int(chat)].god[1],score))
        
        games.pop(int(chat))
        
    except Exception as e : helper.Log(f'{e} in end game')
    
@Mafia.on_callback_query(  helper.filters.regex('^Add_delete_Warn') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Warning(bot:Mafia,query,chat:Group):
    game=Game(int(chat))
    await query.message.edit_reply_markup(helper.buttons.Add_Warn_Btn(game.players_count))

@Mafia.on_callback_query(  helper.filters.regex('^Ellection$') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Ellection_Choose(bot:Mafia,query,chat:Group):
    game=Game(int(chat))
    await query.message.edit_reply_markup(helper.buttons.Ellection_For_Btn(game.status_list_num))
    

@Mafia.on_callback_query(  helper.filters.regex('^Delete_Warn_For_') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Delete_Warn(bot:Mafia,query,chat:Group):
    player = int(str(query.data).split('_')[-1]) 
    if player in (games[int(chat)].warns).keys() : games[int(chat)].warns[player] -= 1
    else: games[int(chat)].warns[player] =0
    game=Game(chat)
    players_text=helper.ingame_list(games[int(chat)].players,games[int(chat)].players_count,game.status_list,games[int(chat)].warns,chat.emoji,games[int(chat)].bests)
    await bot.edit_message_text(int(chat),query.message.id , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(query.message),games[int(chat)].run_time,chat),reply_markup=query.message.reply_markup)
    
    
    
@Mafia.on_callback_query(  helper.filters.regex('^Add_Warn_For_') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Add_Warn(bot:Mafia,query,chat:Group):
    player = int(str(query.data).split('_')[-1]) 
    if player in (games[int(chat)].warns).keys() : games[int(chat)].warns[player] += 1
    else: games[int(chat)].warns[player] =1
    game=Game(chat)
    players_text=helper.ingame_list(games[int(chat)].players,games[int(chat)].players_count,game.status_list,games[int(chat)].warns,chat.emoji,games[int(chat)].bests)
    await bot.edit_message_text(int(chat),query.message.id , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(query.message),games[int(chat)].run_time,chat),reply_markup=query.message.reply_markup)
    
    

@Mafia.on_callback_query(  helper.filters.regex('^Ellection_For_') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Ellection(bot:Mafia,query,chat:Group):
    player = int(str(query.data).split('_')[-1]) 
    await bot.send_message(int(chat),helper.text.ellection(player))
    await sleep(5)
    await bot.send_message(int(chat),helper.text.ellection_ends)
    
@Mafia.on_callback_query(  helper.filters.regex('^Player_is_ready')   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Players_activity(bot:Mafia,query,chat:Group):
    [games[int(chat)].players[i] for i in games[int(chat)].players ]
    if int(query.from_user.id) in games[int(chat)].activity : 
        if games[int(chat)].activity[int(query.from_user.id)]==True:return
    games[int(chat)].activity[int(query.from_user.id)]=True
    await query.answer(helper.text.Player_ready,True)
    players_text=helper.player_list(games[int(chat)].players,games[int(chat)].players_count,games[int(chat)].activity,chat.all_games_players_text,chat.emoji)
    await bot.edit_message_text(int(chat),query.message.id , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(query.message),games[int(chat)].run_time,chat),reply_markup=helper.buttons.game_buttons )

@Mafia.on_callback_query(  helper.filters.regex('^Back') & (helper.god_only|helper.admin_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Back_To_Main(bot:Mafia,query,chat:Group):
    if games[int(chat)].status :
        await query.message.edit_reply_markup(helper.buttons.ingame_edit)
    else:
        await query.message.edit_reply_markup(helper.buttons.game_buttons)
    

@Mafia.on_callback_query(  helper.filters.regex('^ToHomeBack') & (helper.god_only|helper.admin_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Back_To_Home(bot:Mafia,query,chat:Group):
    await query.message.edit_reply_markup(helper.buttons.game_buttons)
    
@Mafia.on_callback_query(  helper.filters.regex('^First_Election') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def send_election_poll(bot:Mafia,query,chat:Group):
    try:
        ccsecond= int(games[int(chat)].players_count * 1.5)
        if ccsecond < 10:
            ccsecond = 12
            
        close_date = datetime.datetime.now() + datetime.timedelta( seconds= ccsecond )
    except:
        close_date = datetime.datetime.now() + datetime.timedelta( seconds= 15 )
        
    plyr=games[int(chat)].players
    status=chat.game.status_list_num
    vote_list=[f'{player_id} - {helper.del_mention(plyr[player_id][1],plyr[player_id][0])}' for player_id in sorted(games[int(chat)].players.keys()) if status[player_id]]
    composite_list = [vote_list[x:x+9] for x in range(0, len(vote_list),9)]
    for i in composite_list:
        i.append(helper.text.see_votes)
        await bot.send_poll(
        int(chat),
        helper.text.vote,
        i,
        is_anonymous =False,
        allows_multiple_answers=True,
        close_date=close_date
        )
    game=Game(int(chat))
    await query.message.reply_text(helper.text.second_ell,False,reply_markup=helper.buttons.Ellection_For_Btn(game.status_list_num,True))
    
@Mafia.on_callback_query(  helper.filters.regex('^Help_for_Election') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Help_for_Election(bot:Mafia,query,chat:Group):
    await query.answer(helper.text.election_help,True)
    
@Mafia.on_callback_query(  helper.filters.regex('^Add_bests') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def add_bests_section(bot:Mafia,query,chat:Group):
    await query.message.edit_reply_markup(helper.buttons.add_best(chat.game.players_count))
    
@Mafia.on_callback_query(  helper.filters.regex('^Add_Best_For_') & (helper.game_god|helper.owner_only)   , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def add_bests_player(bot:Mafia,query,chat:Group):
    player = int(str(query.data).split('_')[-1]) 
    await query.message.edit_reply_markup(helper.buttons.add_best_kind(player,games[int(chat)].bests))
    
@Mafia.on_callback_query(  helper.filters.regex('^Final_BestFor_') & (helper.game_god|helper.owner_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def add_bests_final(bot:Mafia,query,chat:Group):
    best = int(str(query.data).split('_')[-1]) 
    player = int(str(query.data).split('_')[-2]) 
    
    games[int(chat)].bests[player]=best
    await query.message.edit_reply_markup(helper.buttons.add_best_kind(player,games[int(chat)].bests))
    await query.answer(helper.text.best_added,True)
    game=Game(chat)
    players_text=helper.ingame_list(games[int(chat)].players,games[int(chat)].players_count,game.status_list,games[int(chat)].warns,chat.emoji,games[int(chat)].bests)
    await bot.edit_message_text(int(chat),query.message.id , helper.main_list(games[int(chat)].scenario,games[int(chat)].god[1],players_text,chat.title(query.message),games[int(chat)].run_time,chat),reply_markup=query.message.reply_markup)
    
    
    
@Mafia.on_callback_query(  helper.filters.regex('^Call_Players') & (helper.god_only|helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def call_players(bot:Mafia,query,chat:Group):
    if games[int(chat)].call > 2 : 
        await query.answer(helper.text.call_limited,True)
        return

    games[int(chat)].call += 1 
    for i in sorted(games[int(chat)].players.keys()) : 
        try:
            await bot.send_message(games[int(chat)].players[i][0],helper.text.call_player) 
        except:
            pass
    await query.answer(helper.text.call_sended,True)
    
@Mafia.on_callback_query(  helper.filters.regex('^Send_Roles_Again') & (helper.game_god|helper.owner_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def send_all_roles(bot:Mafia,query,chat:Group):
    text=''
    for i,r in (sorted((games[int(chat)].roles.items()),key=lambda x:x[0])):
        try:
            text+=f'{i} - {games[int(chat)].players[i][1]} - {r} \n'
        except:text+=f'{i} - ------  - {r} \n'
        try:
            await bot.send_message(games[int(chat)].players[i][0],helper.text.send_role(r,games[int(chat)].link))
        except:
            await bot.send_message(games[int(chat)].god[0],helper.text.role_hasnt_sent(games[int(chat)].players[i][1])) 
    await query.answer(helper.text.role_sended,True)
    
    await bot.send_message(games[int(chat)].god[0],text) 
    

@Mafia.on_callback_query(  helper.filters.regex('^Send_invitation') & (helper.god_only|helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def send_invitation(bot:Mafia,query,chat:Group):
    if games[int(chat)].invite : 
        await query.answer(helper.text.only_one,True)
        return
    try:
        await query.message.forward(helper.list_channel)
    except:pass
    title = query.message.chat.title
    god = games[int(chat)].god[1]
    sen = games[int(chat)].scenario
    link = games[int(chat)].link
    x=0
    games[int(chat)].invite = True
    for i in chat.all_players :
        try : 
            await bot.send_message(i , helper.text.invitation(title , god , sen , link))
            x+=1
        except:pass
    
    await query.answer(helper.text.invitation_sended(x),True)
    
    


@Mafia.on_callback_query(  helper.filters.regex('^Player_name')  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Players_name_ask(bot:Mafia,query,chat:Group):
    global player_ask
    try:
        if int(query.from_user.id) in player_ask :return
        player_ask.append(int(query.from_user.id))
        ask_msg = await query.message.chat.ask(helper.text.ask_name(query.from_user.mention), timeout=20,reply_markup=helper.force_rep(True) ,filters=(helper.filters.chat(int(chat)) & helper.filters.user(int(query.from_user.id))))
        player_ask.remove(int(query.from_user.id))
        name = str(ask_msg.text)
        if len(name) > 15 : 
            name=name[:15]
            
        if helper.is_persian_arabic(name):
            User(query.from_user.id,int(chat)).set_name(name)
        
        await ask_msg.delete()
        await ask_msg.sent_message.delete()
                    
    except :
        player_ask.remove(int(query.from_user.id))
        
        
@Mafia.on_callback_query(  helper.filters.regex('^Pic_Card_') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def pick_card_btn(bot: Mafia, query, chat: Group):
    name=str(query.data).split('_')[-1]
    cards=chat.card(name)
    
    for i in games[int(chat)].chosen_cards :
        if i in cards :
            cards.remove(i)
            
    if cards==[]:
        cards=chat.card(name)
        
    card=choice(cards)
    games[int(chat)].chosen_cards.append(card)
    
    msg=await query.message.reply_text(helper.text.swnd_card_1(randint(700000,1700000)))
    try:await query.message.delete()
    except:pass
    await sleep(1.5)
    await msg.edit_text(helper.text.swnd_card_2)
    await sleep(4)
    await msg.edit_text(helper.text.swnd_card_3(card))