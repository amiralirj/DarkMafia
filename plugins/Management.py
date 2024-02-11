from random import  choice , randint
from asyncio import sleep
from Classes.MafClass import helper , User , Game , Group , GameState
from Classes.CliClass import Mafia


@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('id') , group=0)
@helper.rate_limit_decorator
async def group_id_cmnd(bot,message):
    await message.reply_text(str(message.chat.id))
    
    
@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('aban') , group=0)
@helper.rate_limit_decorator
async def ban_all(bot,message):
    user_id=str(message.command[1])
    if user_id.isdigit():
        user_id=int(user_id)
    user=await bot.get_users(user_id)
    user = User(user.id)
    user.ban()
    await message.reply_text(f'Done')
    
@Mafia.on_message(  helper.filters.user([helper.owner,helper.co_leader]) & (helper.filters.command('all_group_list')) , group=0)
@helper.rate_limit_decorator
async def groups_lists_owner(bot:Mafia,message):
    days=int(message.command[1])
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
            await message.reply_text(text)
            text=helper.text.best_gaps(abs(days))
            
    if text!=helper.text.best_gaps(abs(days)):
        await message.reply_text(text)
    
@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('aunban') , group=0)
@helper.rate_limit_decorator
async def unban_all(bot,message):
    user_id=str(message.command[1])
    if user_id.isdigit():
        user_id=int(user_id)
    user=await bot.get_users(user_id)
    user = User(user.id)
    user.unban()
    await message.reply_text(f'Done')
        
@Mafia.on_message(  helper.filters.user([helper.owner,helper.co_leader]) & helper.filters.command('add') , group=0)
@helper.rate_limit_decorator
async def Add_GP(bot,message):
    data = str(message.text).split('\n')
    
    gap = Group(int(data[1]))
    
    baz10=helper.bazpors10
    baz12=helper.bazpors12
    baz13=helper.bazpors13
    nato10=helper.nato10
    pedarkhande10=helper.pedarkhande10
    mozakere10=helper.mozakere10
    mitic12=helper.mitic12
    
    gap.add_group(data[2],data[3],data[4],data[5],data[6],data[7])
    gap = Group(int(data[1]))
    gap.update
    gap.add_scenario(baz10[0],{'white':baz10[1],'black':baz10[2],'mos':baz10[3]})
    gap.add_scenario(baz12[0],{'white':baz12[1],'black':baz12[2],'mos':baz12[3]})
    gap.add_scenario(baz13[0],{'white':baz13[1],'black':baz13[2],'mos':baz13[3]})
    gap.add_scenario(nato10[0],{'white':nato10[1],'black':nato10[2],'mos':nato10[3]})
    gap.add_scenario(pedarkhande10[0],{'white':pedarkhande10[1],'black':pedarkhande10[2],'mos':pedarkhande10[3]})
    gap.add_scenario(mozakere10[0],{'white':mozakere10[1],'black':mozakere10[2],'mos':mozakere10[3]})
    gap.add_scenario(mitic12[0],{'white':mitic12[1],'black':mitic12[2],'mos':mitic12[3]})
    
    await message.reply_text(helper.text.gp_added)
    

@Mafia.on_chat_join_request(group=0)
@helper.rate_limit_decorator
async def join_chat_request(bot, message):
    chat = Group(int(message.chat.id))
    user = User(int(message.from_user.id),int(chat))
    user.update
    if chat.join_lock == 0 : return

    try:
       if user.games > chat.join_lock:
           await bot.promote_chat_member(chat_id=int(chat), user_id=int(user))
           return
    except :pass
    
    await bot.send_message(int(user),helper.text.private_not_approved)
    await bot.send_message(chat.support,helper.text.not_approved(message.from_user.mention),reply_markup=helper.buttons.approve(int(user)))


@Mafia.on_callback_query(  helper.filters.regex('^Approve_request_') & (helper.god_only|helper.admin_only) , group=0)
@helper.rate_limit_decorator
@helper.GROUP
async def Approve_request(bot:Mafia,query,chat:Group):
    user = int(str(query.data).split('_')[-1]) 
    bot.promote_chat_member(chat_id=int(chat), user_id=int(user))
    await query.message.delete()
    
@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('change_emoji') , group=0)
@helper.rate_limit_decorator
async def change_emoji_main(bot,message):
    main=int(message.command[1])
    amount=str(message.command[2])
    Group(main).change_emoji(amount)
    await message.reply_text(f'Done')
    
@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('change_main') , group=0)
@helper.rate_limit_decorator
async def change_msg_main(bot,message):
    main=int(message.command[1])
    amount=int(message.command[2])
    Group(main).change_main(amount)
    await message.reply_text(f'Done')
    
@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('change_owner') , group=0)
@helper.rate_limit_decorator
async def change_msg_onwer(bot,message):
    main=int(message.command[1])
    amount=int(message.command[2])
    Group(main).Change_owner(amount)
    await message.reply_text(f'Done')
    
@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('group_point_reset') , group=0)
@helper.rate_limit_decorator
async def reset_gap_point(bot,message):
    main=int(message.command[1])
    Group(main).set_group_0_point()
    await message.reply_text(f'Done')

@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('delete_group') , group=0)
@helper.rate_limit_decorator
async def Delete_group_FNC(bot,message):
    main=int(message.command[1])
    Group(main).DELETE_GROUP()
    await message.reply_text(f'Done')
    
    
@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('support') , group=0)
@helper.rate_limit_decorator
async def change_msg_sup(bot,message):
    main=int(message.command[1])
    amount=int(message.command[2])
    chat=Group(main)
    chat.change_sup(amount)
    await message.reply_text(f'Done')

@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('g2') , group=0)
@helper.rate_limit_decorator
async def change_msg_g2(bot,message):
    main=int(message.command[1])
    amount=int(message.command[2])
    chat=Group(main)
    chat.change_g2(amount)
    await message.reply_text(f'Done')

@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('g3') , group=0)
@helper.rate_limit_decorator
async def change_msg_g3(bot,message):
    main=int(message.command[1])
    amount=int(message.command[2])
    chat=Group(main)
    chat.change_g3(amount)
    await message.reply_text(f'Done')

@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('g4') , group=0)
@helper.rate_limit_decorator
async def change_msg_g4(bot,message):
    main=int(message.command[1])
    amount=int(message.command[2])
    chat=Group(main)
    chat.change_g4(amount)
    await message.reply_text(f'Done')

@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('send') , group=0)
@helper.rate_limit_decorator
async def Send_All(bot,message):
    msg=message.reply_to_message
    X=0
    for i in helper.all_users:
        try:
            await msg.copy(int(i[0]))
            X+=1
        except:pass
        
    await message.reply_text(f'{X} Done.')
    
@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('sups') , group=0)
@helper.rate_limit_decorator
async def Send_All_sups(bot,message):
    msg=message.reply_to_message
    X=0
    for i in helper.all_groups:
        try:
            await msg.copy(int(i[1]))
            X+=1
        except:pass
        
    await message.reply_text(f'{X} Done.')
    
@Mafia.on_message(  helper.filters.user(helper.owner) & helper.filters.command('gaps') , group=0)
@helper.rate_limit_decorator
async def Send_All_gaps(bot,message):
    msg=message.reply_to_message
    X=0
    for i in helper.all_groups:
        try:
            await msg.copy(int(i[0]))
            X+=1
        except:pass
        
    await message.reply_text(f'{X} Done.')