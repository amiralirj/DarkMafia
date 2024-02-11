from random import  choice , randint
from asyncio import sleep
from Classes.MafClass import helper , User , Game , Group 
from Classes.CliClass import Mafia


@Mafia.on_message(  helper.filters.private & helper.filters.regex('^پشتیبانی 👨‍💻') , group=0)
@helper.rate_limit_decorator
async def Support(bot,message):
    await message.reply_text(helper.text.support,reply_markup=helper.buttons.Support(helper.owner_username))
    
@Mafia.on_message(  helper.filters.private & helper.filters.command('start') , group=0)
@helper.rate_limit_decorator
async def Start(bot,message):
    await message.reply_text(helper.text.start,reply_markup=helper.buttons.start)
    
@Mafia.on_message(  (helper.filters.private & helper.filters.regex('^گروه ها 👁️'))|(helper.filters.command('grouplist')) , group=0)
@helper.rate_limit_decorator
async def groups_lists(bot:Mafia,message):
    groups=helper.get_top_groups(helper.all_games,10)
    text=helper.text.best_gaps(30)
    for q,i in enumerate(groups):
        if q==7:break
        chat=Group(i)
        chat.update
        try:
            group = await bot.get_chat(int(i))
            if group.username :
                text+=f'{chat.emoji}{q+1} -@{group.username} \n'
            else:
                text+=f'{chat.emoji}{q+1} -{group.title} \n'
        except Exception as e:
            helper.Log(f'{e} in Group_List')
            continue
        
    if message.chat.type in helper.group_type : 
        if Group(int(message.chat.id)).have_active:
            try:await message.delete()
            except:pass
            await bot.send_message(int(id),text)
            return
        
    await message.reply_text(text)
    
@Mafia.on_message(  (helper.filters.private & helper.filters.regex('^امار من👤'))|(helper.filters.command('profile')) , group=0)
@helper.rate_limit_decorator
async def my_stats(bot:Mafia,message):
    name=message.from_user.first_name
    id=message.from_user.id
    user=User(message.from_user.id)
    user.update
    try:
        title = (await bot.get_chat(int(user.group))).title
    except Exception as e:
        title =int(user.group)
    mall_data=helper.all_M_users
    all_data=helper.all_users
    data = helper.user_sort(mall_data,1)

    all_rank = user.get_player_rank(all_data,2)
    shahr_rank = user.get_player_rank(all_data,5)
    maf_rank = user.get_player_rank(all_data,4)
    mall_rank = user.get_player_rank(mall_data,2)
    mshahr_rank = user.get_player_rank(mall_data,5)
    mmaf_rank = user.get_player_rank(mall_data,4)
    bests_rank = user.get_player_rank(all_data,6)
    point_rank = user.get_player_rank(all_data,1)
    mpoint_rank = user.get_player_rank(mall_data,1)
    
    if  mpoint_rank < 6 :
        txt=helper.text.user_stats_best_a(
                name,
                title,
                id,
                user.games,
                user.shahr,
                user.maf,
                user.MMgames,
                user.shahr,
                user.MMmaf,
                user.user_emoji(data),
                all_rank,
                shahr_rank,
                maf_rank,
                mall_rank,
                mshahr_rank,
                mmaf_rank,
                user.bests,
                bests_rank,
                user.score,
                point_rank,
                user.MMscore,
                mpoint_rank)
    elif  mshahr_rank < 6 :
        txt=helper.text.user_stats_best_c(
                name,
                title,
                id,
                user.games,
                user.shahr,
                user.maf,
                user.MMgames,
                user.shahr,
                user.MMmaf,
                user.user_emoji(data),
                all_rank,
                shahr_rank,
                maf_rank,
                mall_rank,
                mshahr_rank,
                mmaf_rank,
                user.bests,
                bests_rank,
                user.score,
                point_rank,
                user.MMscore,
                mpoint_rank)
    elif  mmaf_rank < 6 :
        txt=helper.text.user_stats_best_m(
                name,
                title,
                id,
                user.games,
                user.shahr,
                user.maf,
                user.MMgames,
                user.shahr,
                user.MMmaf,
                user.user_emoji(data),
                all_rank,
                shahr_rank,
                maf_rank,
                mall_rank,
                mshahr_rank,
                mmaf_rank,
                user.bests,
                bests_rank,
                user.score,
                point_rank,
                user.MMscore,
                mpoint_rank)
    else:
        txt=helper.text.user_stats(
                name,
                title,
                id,
                user.games,
                user.shahr,
                user.maf,
                user.MMgames,
                user.shahr,
                user.MMmaf,
                user.user_emoji(data),
                all_rank,
                shahr_rank,
                maf_rank,
                mall_rank,
                mshahr_rank,
                mmaf_rank,
                user.bests,
                bests_rank,
                user.score,
                point_rank,
                user.MMscore,
                mpoint_rank)
        
    if message.chat.type in helper.group_type : 
        if Group(int(message.chat.id)).have_active:
            try:await message.delete()
            except:pass
            await bot.send_message(int(id),txt)
            return
        
    await message.reply_text(txt)


@Mafia.on_message(  (helper.filters.command('local') & helper.filters.group ) , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def best_local_users(bot: Mafia, message, chat: Group):
    chat.update
    game_players = chat.all_players
    selected_players_data = [user for user in helper.all_M_users if int(user[0]) in game_players]
    bests=helper.get_top_5_players_info(selected_players_data,1)
    text=''
    for n,i in enumerate(bests):
        try :
            user_py = (await bot.get_users(int(i[0])))
            mention=user_py.mention(helper.limit(user_py.first_name))
        except :mention = i[0]
        text += helper.text.best_player_str(chat.emoji,n+1,mention,i[1])
        
    try:
        title = (await bot.get_chat(int(chat.main))).title
    except Exception as e:
        title =int(chat.main)
        
    if message.chat.type in helper.group_type : 
        if Group(int(message.chat.id)).have_active:
            try:await message.delete()
            except:pass
            await bot.send_message(int(message.from_user.id),helper.text.local_users(title,text))
            return
        
    await message.reply_text(helper.text.local_users(title,text))
    
@Mafia.on_message(  (helper.filters.command('global')  ) , group=0)
@helper.rate_limit_decorator
async def best_global_users(bot: Mafia, message):
    players_data =helper.all_M_users 
    bests=helper.get_top_5_players_info(players_data,1)
    text=''
    for n,i in enumerate(bests):
        try :
            user_py = (await bot.get_users(int(i[0])))
            mention=user_py.mention(helper.limit(user_py.first_name))
        except :mention = i[0]
        text += helper.text.best_player_str('🎩',n+1,mention,i[1])
        
        
    if message.chat.type in helper.group_type : 
        if Group(int(message.chat.id)).have_active:
            try:await message.delete()
            except:pass
            await bot.send_message(int(message.from_user.id),helper.text.global_users(text))
            return
        
    await message.reply_text(helper.text.global_users(text))
    
@Mafia.on_message(  (helper.filters.command('register') & helper.filters.group ) , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def regester_player(bot: Mafia, message, chat: Group):
    try:
        title = (await bot.get_chat(int(chat.main))).title
    except Exception as e:
        title =int(chat.main)
    
    all_g=[]
    for i in helper.all_groups :
        for t in i :
            all_g.append(int(t))
            
    user= User(message.from_user.id,chat)
    mention=message.from_user.mention
    
    user.change_group(int(chat),all_g)
    
    if message.chat.type in helper.group_type : 
        if Group(int(message.chat.id)).have_active:
            try:await message.delete()
            except:pass
            await bot.send_message(int(message.from_user.id),helper.text.regester_group(title ,mention,int(user)))
            return
        
    await message.reply_text(helper.text.regester_group(title ,mention,int(user)))