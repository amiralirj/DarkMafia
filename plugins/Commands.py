from random import  choice , randint
from asyncio import sleep
from collections import defaultdict
from Classes.MafClass import helper , User , Game , Group 
from Classes.CliClass import Mafia
from os import remove

is_tagging={}

@Mafia.on_message(  helper.filters.command('dtag') & ( helper.god_only | helper.owner_only | helper.admin_only ) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def tag_start_func(bot: Mafia, message, chat: Group):
    txt =''
    count=0
    chat_id = int(message.chat.id)
    if is_tagging[chat_id]==True:return
    chat.update
    is_tagging[chat_id]=True
    async for usr in bot.get_chat_members(chat_id=chat_id):
        if usr.user.username:
            if is_tagging[chat_id]:
                if not usr.user.is_bot:
                    txt += f"** |{chat.emoji}| {usr.user.mention()} ** \n "
                    count+=1
                    if count==5:
                        await bot.send_message(chat_id,txt)
                        txt =''
                        count=0
                        await sleep(2)
            else:
                return
        is_tagging[chat_id] = False

@Mafia.on_message(  helper.filters.command(['dstop',f'dstop@{helper.bot_username}']) & ( ( helper.god_only | helper.owner_only | helper.admin_only ) ) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def stop_tagging(bot: Mafia, message, chat: Group):
    global is_tagging 
    chat_id = int(message.chat.id)
    is_tagging[chat_id] = False
    await message.edit_text(helper.text.stopped)
    
    
@Mafia.on_message(  helper.filters.command('card') & ( helper.game_god ) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def pick_card(bot: Mafia, message, chat: Group):
    await message.reply_text(helper.text.cards_pick,reply_markup=helper.buttons.pick_card(chat.all_cards()))
    
@Mafia.on_message(  helper.filters.command('cards') & ( helper.god_only | helper.owner_only | helper.admin_only ) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def cards_pannel(bot: Mafia, message, chat: Group):
    chat.update
    await message.reply_text(helper.text.setting,reply_markup=helper.buttons.cards_main(chat.emoji,helper.channel_username))
    
@Mafia.on_message(  helper.filters.command('unbanall') & (helper.owner_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def all_player_unban(bot: Mafia, message, chat: Group):
    chat.unban_all_players()
    await message.reply_text(helper.text.all_player_unbanned)
    
@Mafia.on_message(  helper.filters.command('random') & ( helper.god_only | helper.owner_only | helper.admin_only ) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def generate_random_int_func(bot: Mafia, message, chat: Group):
    x=int(message.command[1])
    y=int(message.command[2])
    await message.reply_text(helper.generate_random_int(x,y))
    
@Mafia.on_message(  helper.filters.command('event') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def add_event_command(bot: Mafia, message, chat: Group):
    x=int(message.command[1])
    if x > 1000000: return
    chat.change_Ev_num(x)
    m=await message.reply_text(helper.text.submited(helper.text.event_word))
    await sleep(4)
    await m.delete()
    
@Mafia.on_message(  helper.filters.command(['groupstate',f'groupstate@{helper.bot_username}']) & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def group_state_command(bot: Mafia, message, chat: Group):
    chat.update
    players=chat.all_players
    try:
        title = (await bot.get_chat(int(chat.main))).title
    except Exception as e:
        title =int(chat.main)
    last_month_games=chat.played_games_last_month()
    file_name=helper.plot_games_per_day(last_month_games)
    await message.reply_photo(file_name,caption = helper.text.group_state(title ,len(last_month_games) , len(players)))
    remove(file_name)

@Mafia.on_message(  helper.filters.command(['godstate',f'godstate@{helper.bot_username}']) & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def godstate(bot: Mafia, message, chat: Group):
    chat.update
    last_month_games=chat.played_games_last_month()
    
    gods_count = defaultdict(int)
    gods_n = defaultdict(int)
    
    gods_time=defaultdict(float)
    
    for gods_list in last_month_games:
        if gods_list[3] == 0 : continue
        god = gods_list[2]
        gods_count[god] +=1
        gods_time[god] += float( (helper.call_time(len((gods_list[-1]).split('-')),gods_list[3])) / 60  )
    
    txt=[]
    for i in list(gods_count.keys()) : 
        try:
            name=helper.limit(((await bot.get_users(i)).first_name))
            gods_n[name]=int(gods_count[i])
            running_time=round(gods_time[i] * 2) / 2
            txt.append(f'{name} ➞ **{running_time}H** - **{gods_count[i]}** \n\n')
        except:
            gods_n[(i)]=int(gods_count[i])
            txt.append(f'{i} ➞**{running_time}H** - **{gods_count[i]}** \n\n')
        

        
    composite_list = [txt[x:x+7] for x in range(0, len(txt),7)]
    file_names=helper.create_bar_chart(gods_n)
    for j,file_name in enumerate(file_names) :
        cap= ''.join(composite_list[j])
        await message.reply_photo(file_name,caption = cap )
        remove(file_name)

        
@Mafia.on_message(  helper.filters.command('template') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def add_template(bot: Mafia, message, chat: Group):
    temp = str((await message.chat.ask(helper.text.ask_template, timeout=60, filters=(helper.filters.chat(int(chat)) & helper.filters.user(int(message.from_user.id))))).text)
    if temp==helper.text.defualt_word : 
        temp='None'
    try:
        chat.change_template(temp)
    except:
        await message.reply_text(helper.text.template_help)
    await message.reply_text(helper.text.submited(helper.text.template_word))
    
    
@Mafia.on_message(  helper.filters.command('delgod') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def del_god(bot: Mafia, message, chat: Group):
    try:
        id=helper.get_command_id(message)
        user=(await bot.get_users(id))
        User(user.id,int(chat))
        chat.del_god(id)
        await message.reply_text(helper.text.god_deleted(user.mention))
    except (helper.errors.PeerIdInvalid, helper.errors.ChatIdInvalid , helper.errors.bad_request_400.UsernameInvalid,helper.errors.bad_request_400.UsernameNotOccupied , helper.errors.bad_request_400.UsernameNotModified)  :
        await message.reply_text(helper.user_name_wrong)
        return
    except :
        await message.reply_text(helper.text.reply_or_command)
        return
    
@Mafia.on_message(  helper.filters.command('addgod') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def add_god(bot: Mafia, message, chat: Group):
    try:
        id=helper.get_command_id(message)
        user=(await bot.get_users(id))
        User(user.id,int(chat))
        chat.add_god(id)
        await message.reply_text(helper.text.god_setted(user.mention))
    except (helper.errors.PeerIdInvalid, helper.errors.ChatIdInvalid , helper.errors.bad_request_400.UsernameInvalid,helper.errors.bad_request_400.UsernameNotOccupied , helper.errors.bad_request_400.UsernameNotModified)  :
        await message.reply_text(helper.user_name_wrong)
        return
    except :
        await message.reply_text(helper.text.reply_or_command)
        return
    
@Mafia.on_message(  helper.filters.command('warn') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def add_warn(bot: Mafia, message, chat: Group):
    try:
        if message.reply_to_message : 
            user=User(message.reply_to_message.from_user.id,int(chat))
            user_name=message.reply_to_message.from_user.mention
        else  : 
            user_id=str(message.command[1])
            if user_id.isdigit():
                user_id=int(user_id)
            user=await bot.get_users(user_id)
            user_name= user.mention
            user = User(user.id,int(chat))
        user.update
    except (helper.errors.PeerIdInvalid, helper.errors.ChatIdInvalid , helper.errors.bad_request_400.UsernameInvalid,helper.errors.bad_request_400.UsernameNotOccupied , helper.errors.bad_request_400.UsernameNotModified)  :
        await message.reply_text(helper.user_name_wrong)
        return
    except Exception as e:
        helper.Log(f'{e} in z_warn ')
        await message.reply_text(helper.text.reply_or_command)
        return
    
    warns= int(user.group_show()[0])
    user.add_warn()
    await message.reply_text(helper.text.add_warn(user_name,warns+1))
    

@Mafia.on_message(  helper.filters.command('delwarn') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def del_warn(bot: Mafia, message, chat: Group):
    try:
        if message.reply_to_message : 
            user=User(message.reply_to_message.from_user.id,int(chat))
            user_name=message.reply_to_message.from_user.mention
        else  : 
            user_id=str(message.command[1])
            if user_id.isdigit():
                user_id=int(user_id)
            user=await bot.get_users(user_id)
            user_name= user.mention
            user = User(user.id,int(chat))
        user.update
    except (helper.errors.PeerIdInvalid, helper.errors.ChatIdInvalid , helper.errors.bad_request_400.UsernameInvalid,helper.errors.bad_request_400.UsernameNotOccupied , helper.errors.bad_request_400.UsernameNotModified)  :
        await message.reply_text(helper.user_name_wrong)
        return
    except Exception as e:
        helper.Log(f'{e} in del_warn ')
        await message.reply_text(helper.text.reply_or_command)
        return

    warns= int(user.group_show()[0])
    if warns != 0:
        user.del_warn()
    await message.reply_text(helper.text.del_warn(user_name,warns-1))


    
@Mafia.on_message(  helper.filters.command('reset') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def reset_warn(bot: Mafia, message, chat: Group):
    try:
        if message.reply_to_message : 
            user=User(message.reply_to_message.from_user.id,int(chat))
            user_name=message.reply_to_message.from_user.mention
        else  : 
            user_id=str(message.command[1])
            if user_id.isdigit():
                user_id=int(user_id)
            user=await bot.get_users(user_id)
            user_name= user.mention
            user = User(user.id,int(chat))
        user.update
    except (helper.errors.PeerIdInvalid, helper.errors.ChatIdInvalid , helper.errors.bad_request_400.UsernameInvalid,helper.errors.bad_request_400.UsernameNotOccupied , helper.errors.bad_request_400.UsernameNotModified)  :
        await message.reply_text(helper.user_name_wrong)
        return
    except Exception as e:
        helper.Log(f'{e} in reset_warn ')
        await message.reply_text(helper.text.reply_or_command)
        return
    
    warns= int(user.group_show()[0])
    for i in range(warns):
        user.del_warn()
        
    await message.reply_text(helper.text.reset_warn(user_name))


@Mafia.on_message(  helper.filters.command('godlist') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def gods_list(bot: Mafia, message, chat: Group):
    gods =chat.see_gods
    text=''
    for i in gods:
        try:
            usr=await bot.get_users(i)
            text+=f'⍣ {usr.mention} ➟  `{usr.id}`  \n'
        except:
            text+=f'⍣  `{i}`  \n'
        if len(text.split('\n')) > 40 :
            text+=f'▪️▫️▪️▫️▪️▫️▪️▫️▪️▫️▪️▫️\n Gods Number : {len(gods)}' 
            await message.reply_text(text)
            text=''
    if text != '' :
        text+=f'▪️▫️▪️▫️▪️▫️▪️▫️▪️▫️▪️▫️\n Gods Number : {len(gods)}'
        await message.reply_text(text)
        
@Mafia.on_message(  helper.filters.command('check') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def see_player(bot: Mafia, message, chat: Group):
    try:
        if message.reply_to_message : 
            user=User(message.reply_to_message.from_user.id,int(chat))
            user_name=message.reply_to_message.from_user.mention
        else  : 
            user_id=str(message.command[1])
            if user_id.isdigit():
                user_id=int(user_id)
            user=await bot.get_users(user_id)
            user_name= user.mention
            user = User(user.id,int(chat))
        user.update
    except (helper.errors.PeerIdInvalid, helper.errors.ChatIdInvalid , helper.errors.bad_request_400.UsernameInvalid,helper.errors.bad_request_400.UsernameNotOccupied , helper.errors.bad_request_400.UsernameNotModified)  :
        await message.reply_text(helper.user_name_wrong)
        return
    except Exception as e:
        helper.Log(f'{e} in see players ')
        await message.reply_text(helper.text.reply_or_command)
        return
    
    data= user.group_show()
    helper.Log(data)
    if data[1]=='None':persian_date_string=helper.text.no
    else:persian_date_string = helper.convert_to_persian_calendar(data[1])
    
    try:
        title = (await bot.get_chat(int(user.group))).title
    except Exception as e:
        title =int(user.group)
    
    await message.reply_text(helper.text.player_cheak(user_name,title,user.games,data[0],persian_date_string))
    
    
@Mafia.on_message(  helper.filters.command('ban') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def ban_group_player(bot: Mafia, message, chat: Group):
    try:
        if message.reply_to_message : 
            user=User(message.reply_to_message.from_user.id,int(chat))
            user_name=message.reply_to_message.from_user.mention
            try:
                ban_date=int(message.command[1])
            except:
                await message.reply_text(helper.text.ban_wrong)
                return
        else  : 
            user_id=str(message.command[1])
            try:
                ban_date=int(message.command[2])
            except:
                await message.reply_text(helper.text.ban_wrong)
                return
            if user_id.isdigit():
                user_id=int(user_id)
            user=await bot.get_users(user_id)
            user_name= user.mention
            user = User(user.id,int(chat))
        user.update
    except (helper.errors.PeerIdInvalid, helper.errors.ChatIdInvalid , helper.errors.bad_request_400.UsernameInvalid,helper.errors.bad_request_400.UsernameNotOccupied , helper.errors.bad_request_400.UsernameNotModified)  :
        await message.reply_text(helper.user_name_wrong)
        return
    except Exception as e:
        helper.Log(f'{e} in see players ')
        await message.reply_text(helper.text.reply_or_command)
        return
    
    try:
        title = (await bot.get_chat(int(chat.main))).title
    except Exception as e:
        title =int(chat.main)

    user.group_ban(ban_date)
    await message.reply_text(helper.text.player_banned(user_name,int(user),message.from_user.mention,message.from_user.id,ban_date,title))
    await bot.send_message(int(user),helper.text.player_banned(user_name,int(user),message.from_user.mention,message.from_user.id,ban_date,title))

@Mafia.on_message(  helper.filters.command('unban') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def unban_group_player(bot: Mafia, message, chat: Group):
    try:
        if message.reply_to_message : 
            user=User(message.reply_to_message.from_user.id,int(chat))
            user_name=message.reply_to_message.from_user.mention
        else  : 
            user_id=str(message.command[1])
            if user_id.isdigit():
                user_id=int(user_id)
            user=await bot.get_users(user_id)
            user_name= user.mention
            user = User(user.id,int(chat))
        user.update
    except (helper.errors.PeerIdInvalid, helper.errors.ChatIdInvalid , helper.errors.bad_request_400.UsernameInvalid,helper.errors.bad_request_400.UsernameNotOccupied , helper.errors.bad_request_400.UsernameNotModified)  :
        await message.reply_text(helper.user_name_wrong)
        return
    except Exception as e:
        helper.Log(f'{e} in see players ')
        await message.reply_text(helper.text.reply_or_command)
        return
    
    try:
        title = (await bot.get_chat(int(chat.main))).title
    except Exception as e:
        title =int(chat.main)

    user.group_ban(-1)
    await message.reply_text(helper.text.player_unbanned(user_name,int(user),message.from_user.mention,message.from_user.id,title))
    await bot.send_message(int(user),helper.text.player_unbanned(user_name,int(user),message.from_user.mention,message.from_user.id,title))
    
@Mafia.on_message(  helper.filters.command('setting') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def setting_command(bot: Mafia, message, chat: Group):
    chat.update
    try:
        title = helper.limit((await bot.get_chat(int(chat.main))).title)
    except Exception as e:
        title =helper.limit(str(chat))
    await message.reply_text(helper.text.setting,reply_markup=helper.buttons.setting_main(title,chat.emoji,helper.channel_username,helper.setting_status(chat.farsi)))
    
@Mafia.on_callback_query(  helper.filters.regex('^Join_Lock') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def join_lock(bot: Mafia, query, chat: Group):
    chat.update
    await query.message.edit_text(helper.text.ask_list_lock,reply_markup=helper.buttons.lock('Join',chat.join_lock))

@Mafia.on_callback_query(  helper.filters.regex('^Lock_Change_Join') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def set_join_lock(bot: Mafia, query, chat: Group):
    amount=int(str(query.data).split('_')[-1])
    chat.Change_join_lock(amount)
    await query.answer(helper.text.submited(amount),True)
    chat.update
    await query.message.edit_text(helper.text.ask_list_lock,reply_markup=helper.buttons.lock('Join',chat.join_lock))
    
    
    
@Mafia.on_callback_query(  helper.filters.regex('^List_Lock') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def list_lock(bot: Mafia, query, chat: Group):
    chat.update
    await query.message.edit_text(helper.text.ask_list_lock,reply_markup=helper.buttons.lock('List',chat.state_lock))
    
@Mafia.on_callback_query(  helper.filters.regex('^Lock_Change_List') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def set_list_lock(bot: Mafia, query, chat: Group):
    amount=int(str(query.data).split('_')[-1])
    chat.change_state_lock(amount)
    await query.answer(helper.text.submited(amount),True)
    chat.update
    await query.message.edit_text(helper.text.ask_list_lock,reply_markup=helper.buttons.lock('List',chat.state_lock))
    
    
@Mafia.on_callback_query(  helper.filters.regex('^Group_Emoji') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def group_emoji(bot: Mafia, query, chat: Group):
    chat.update
    await query.message.edit_text(helper.text.ask_emoji,reply_markup=helper.buttons.emoji_choose(chat.emoji))

@Mafia.on_callback_query(  helper.filters.regex('^Lock_Emoji_') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def set_group_emoji(bot: Mafia, query, chat: Group):
    amount=str(query.data).split('_')[-1]
    chat.change_emoji(amount)
    await query.answer(helper.text.submited(amount),True)
    chat.update
    await query.message.edit_text(helper.text.ask_emoji,reply_markup=helper.buttons.emoji_choose(chat.emoji))
    
@Mafia.on_callback_query(  helper.filters.regex('^CloseList') & (helper.owner_only | helper.admin_only) , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def close_list(bot: Mafia, query, chat: Group):
    await query.message.delete()
    
@Mafia.on_callback_query(  helper.filters.regex('^SETTINGBACK') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def back_to_setting(bot: Mafia, query, chat: Group):
    chat.update
    try:
        title = helper.limit((await bot.get_chat(int(chat.main))).title)
    except Exception as e:
        title =helper.limit(str(chat))
    await query.message.edit_text(helper.text.setting,reply_markup=helper.buttons.setting_main(title,chat.emoji,helper.channel_username,helper.setting_status(chat.farsi)))
    

@Mafia.on_message(  helper.filters.command('scenarios') & (helper.owner_only | helper.admin_only) & helper.filters.group , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def scenarios_setting(bot: Mafia, message, chat: Group):
    chat.update
    await message.reply_text(helper.text.setting,reply_markup=helper.buttons.scenarios_main(chat.emoji,helper.channel_username))
    
    
@Mafia.on_callback_query(  helper.filters.regex('^Scenarios_Setting_Main') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def scenario_button_setting(bot: Mafia, query, chat: Group):
    chat.update
    await query.message.edit_text(helper.text.setting,reply_markup=helper.buttons.scenarios_main(chat.emoji,helper.channel_username))
    
@Mafia.on_callback_query(  helper.filters.regex('^See_All_Scenarios') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def see_all_sen_buttons(bot: Mafia, query, chat: Group):
    await query.message.edit_text(helper.text.setting,reply_markup=helper.buttons.all_scenarios(chat.all_scenario,False))
    
@Mafia.on_callback_query(  helper.filters.regex('^Del_Sen') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def delete_scenario_btn(bot: Mafia, query, chat: Group):
    await query.message.edit_text(helper.text.ask_dell_sen,reply_markup=helper.buttons.all_scenarios(chat.all_scenario,True))
    
    
@Mafia.on_callback_query(  helper.filters.regex('^Add_Sen') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def add_scenario_btn(bot: Mafia, query, chat: Group):
    if (len(chat.all_scenario)) > 30 : 
        await query.answer(helper.text.no_more_sen,True)
        return
    try:
        name = str((await query.message.chat.ask(helper.text.ask_name_sen, timeout=60, filters=(helper.filters.chat(int(chat)) & helper.filters.user(int(query.from_user.id))))).text)
        if name.lower() == helper.text.cancel_word or '-' in name:
            return

        if name in chat.all_scenario : 
            await query.reply_text(helper.text.scenario_name_exist)
            
            return
        
        
        white = str((await query.message.chat.ask(helper.text.ask_white, timeout=60, filters=(helper.filters.chat(int(chat)) & helper.filters.user(int(query.from_user.id))))).text).split('\n')
        if '\n'.join(white).lower() == helper.text.cancel_word or '-' in '\n'.join(white):
            
            return
        white = '-'.join(white)
        

        black = str((await query.message.chat.ask(helper.text.ask_black, timeout=60, filters=(helper.filters.chat(int(chat)) & helper.filters.user(int(query.from_user.id))))).text).split('\n')
        if '\n'.join(black).lower() == helper.text.cancel_word or '-' in '\n'.join(black):
            return
        black = '-'.join(black)
        
        mos = str((await query.message.chat.ask(helper.text.ask_mos, timeout=60, filters=(helper.filters.chat(int(chat)) & helper.filters.user(int(query.from_user.id))))).text)
        if '\n'.join(mos.split('\n')).lower() == helper.text.cancel_word or '-' in mos:
            return

        if mos in helper.text.doesnt:
            mos = 'none'
            mos_c=0
        else:
            mos_c=len(mos.split('\n'))
            mos = '-'.join(mos.split('\n'))
            
            
        if (len(white.split('-'))+len(black.split('-'))+mos_c) > 40 : 
            await query.message.reply_text(helper.text.scenario_name_exist)
            return
        
        approve = str((await query.message.chat.ask(helper.text.approve(name , white , black , mos), timeout=60, filters=(helper.filters.chat(int(chat)) & helper.filters.user(int(query.from_user.id))))).text)

        if approve != helper.text.yes:
            await query.message.reply_text(helper.text.retry)
            return

        roles = {'white': white, 'black': black, 'mos': mos}
        chat.add_scenario(name,roles)

        await query.message.reply_text(helper.text.scenario_added)

    except TimeoutError:
        await query.message.reply_text("Timeout occurred. Please try again.")
    except Exception as e:
        helper.Log(f"An error occurred: {str(e)}")
        # Handle the error appropriately based on your needs

        
@Mafia.on_callback_query(  helper.filters.regex('^SettingScenarios_see') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def show_sen_final(bot: Mafia, query, chat: Group):
    name=str(query.data).split('_')[-1]
    sen=chat.see_scenario(name)
    if 'mos' in sen.keys():
        send_text=helper.text.show_sen(name,'\n'.join(sen['white'].split('-')),'\n'.join(sen['black'].split('-'))) + '\n' + helper.text.mos_sen_show(sen['mos'])
    else:
        send_text=helper.text.show_sen(name,'\n'.join(sen['white'].split('-')),'\n'.join(sen['black'].split('-')))

    await query.message.reply_text(send_text)
    
@Mafia.on_callback_query(  helper.filters.regex('^SettingScenarios_delete') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def delete_sen_final(bot: Mafia, query, chat: Group):
    name=str(query.data).split('_')[-1]
    chat.del_scenario(name)
    await query.message.edit_text(helper.text.setting,reply_markup=helper.buttons.all_scenarios(chat.all_scenario,True))
    

@Mafia.on_callback_query(  helper.filters.regex('^SCENARIOSBACK') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def back_to_scenario_setting(bot: Mafia, query, chat: Group):
    chat.update
    await query.message.edit_text(helper.text.setting,reply_markup=helper.buttons.scenarios_main(chat.emoji,helper.channel_username))
    
@Mafia.on_callback_query(  helper.filters.regex('^CARDSBACK') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def back_to_cards_setting(bot: Mafia, query, chat: Group):
    chat.update
    await query.message.edit_text(helper.text.setting,reply_markup=helper.buttons.cards_main(chat.emoji,helper.channel_username))
    

@Mafia.on_callback_query(  helper.filters.regex('^Persian_Name') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Persian_Name_Change(bot: Mafia, query, chat: Group):
    chat.update
    if chat.farsi :
        am=False
    else:
        am=True
    chat.change_farsi(am)
    try:
        title = helper.limit((await bot.get_chat(int(chat.main))).title)
    except Exception as e:
        title =helper.limit(str(chat))
    await query.message.edit_reply_markup(helper.buttons.setting_main(title,chat.emoji,helper.channel_username,helper.setting_status(chat.farsi)))
    
#-------------------------------------

@Mafia.on_callback_query(  helper.filters.regex('^Show_card_see') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def show_card_final(bot: Mafia, query, chat: Group):
    name=str(query.data).split('_')[-1]
    cards='\n'.join(chat.card(name))
    
    await query.message.reply_text(helper.text.show_card(name,cards))
    
@Mafia.on_callback_query(  helper.filters.regex('^Show_card_delete') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def delete_card_final(bot: Mafia, query, chat: Group):
    name=str(query.data).split('_')[-1]
    chat.delete_card(name)
    await query.message.edit_text(helper.text.ask_dell_sen,reply_markup=helper.buttons.all_cards(chat.all_cards(),True))
    
@Mafia.on_callback_query(  helper.filters.regex('^Add_Card') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def add_card_btn(bot: Mafia, query, chat: Group):
    if (len(chat.all_cards())) > 30 : 
        await query.answer(helper.text.no_more_card,True)
        return
    
    name = str((await query.message.chat.ask(helper.text.ask_name_card, timeout=60, filters=(helper.filters.chat(int(chat)) & helper.filters.user(int(query.from_user.id))))).text)
    if name.lower() == helper.text.cancel_word or '-' in name:
        return

    if name in chat.all_cards() or len(name)>20: 
        await query.message.reply_text(helper.text.card_name_exist)
        return
    
    cards = str((await query.message.chat.ask(helper.text.ask_card, timeout=60, filters=(helper.filters.chat(int(chat)) & helper.filters.user(int(query.from_user.id))))).text)
    if cards.lower() == helper.text.cancel_word or '-' in cards:
        return
    
    chat.add_card(name,'-'.join(cards.split('\n')))
    await query.message.reply_text(helper.text.card_added)
    

    
@Mafia.on_callback_query(  helper.filters.regex('^See_All_Cards') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def see_all_cards_buttons(bot: Mafia, query, chat: Group):
    await query.message.edit_text(helper.text.setting,reply_markup=helper.buttons.all_cards(chat.all_cards(),False))
    
@Mafia.on_callback_query(  helper.filters.regex('^Del_Card') & (helper.owner_only | helper.admin_only)  , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def delete_cards_btn(bot: Mafia, query, chat: Group):
    await query.message.edit_text(helper.text.ask_dell_sen,reply_markup=helper.buttons.all_cards(chat.all_cards(),True))