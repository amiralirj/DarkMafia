moon = '🌕                    🌓                     🌑'
start='''👤 سلام به ربات دارک مافیا خوش اومدی 
این ربات به صورت هوشمند تمامی امار شما را ثبت میکند . 
ساده ترین دستیار مافیا :))) '''
    
support = '🔰 پاسخ دهی به سریع ترین حالت ممکن در حال انجام است و لطفا صبور باشید ! \n برای ورود به پیوی روی دکمه ی زیر کلیک کنید 🧑🏼‍💻'

Join_Channel=lambda channel,channel2 : f'''🔥 کاربر گرامی 🔥

برای استفاده از دارک مافیا اول باید در‌ چنل ربات جوین بشید 💎
🔅 - @{channel}
🔅 - @{channel2}
'''

main_list = lambda sen , god , plyrs , username , time,event,date:  f'''
▪️ ایونت : {event}
▪️ تاریخ : {date}
▪️ شروع : {time}
▪️ سناریو : {sen}
▪️ گرداننده : {god}
▪️ گروه : ✦{username}✦

                 
                
            🌘لیست بازیکنان🌒                                                                                     
               

{plyrs}

راهنمایی : لطفا ربات را استارت کنید تا امتیاز کامل و نقش برای شما ارسال بشود !
{moon}
'''
choose_scenario = 'لطفا سناریو مد نظرتون رو انتخاب کنید :'

scenario_changed = 'سناریو با موفقیت تغییر کرد ✅'

number_busy = 'شماره مورد نظر اشغال است !'

limited = '''بازیکن عزیز :
مقدار بازی شما کمتر از مقدار بازی حداقل گروه هست ، متاسفانه نمیتوانید در این لیست ثبت نام کنید 😢'''

signed_in =lambda x :  f'شما {x} با موفقیت وارد بازی شدید ✅'

list_not_full = ' لیست به صورت کامل پر نیست ! '

game_started = lambda link : f'''
گرداننده ی عزیز 
لطفا به گروه مراجعه فرمایید بازی شروع شد 
{link}'''

start_bot = 'لطفا ربات را استارت کنید !'

send_role =lambda role , link : f'''بازیکن گرامی 
بازی شما شروع شده است 

⚜️ نقش : {role}
⚜️ گروه : {link}
🎩 @DarkMafiaRobot

'''

role_hasnt_sent = lambda name : f'''نقش برای کاربر {name} ارسال نشد .
🔰علت : عدم استارت ربات '''

gp_added = 'گروه مورد نظر در دیتا بیس ثبت شد .'

what_scenario = 'سناریو مد نظر خود را انتخاب کنید '

winner = '🎉 '


end_list=lambda time , start , end , PC , god , score: f''' 🔰 بازی تمام شد !

⚜️ گرداننده : {god}

⚜️ تایم بازی :{time}

⚜️تعداد پلیر : {PC}

⚜️ تایم شروع : {start}

⚜️ تایم اتمام : {end}

⚜️ امتیاز بازی : {score}
🎩 @DarkMafiaRobot
'''


already_have_active_game='شما یک بازی ناتمام دارید \n ایا میخواهید که بازی قبلی را حذف و لیست جدید را وارد کنید ؟ '

Player_ready = 'اعلام حضور شما ثبت شد . لطفا بر روی مایک باشید🙏'

active_game_detected = 'شما یک بازی فعال در حال حاضر دارید !'

ellection=lambda x : f'رای گیری نهایی برای شماره {x} :'
ellection_ends='تمام'


TAG=lambda x : f'''
🎩بازی درحال شروع شدن هست , بازیکنان لطفا در سریع ترین زمان به روی مایک بیاییند :

{x} 


'''
vote='به چه کسی رای میدهید ؟ '

error = ' مقدار داده شده قابل قبول نیست \n ممکن است به علت طولانی بودن مقدار باشد ! '

election_help='از اعداد زیر شماره ی مورد نظر را برای رای خروج انتخاب کنید '

see_votes='Results          دیدن نتایج'

best_added='تغییرات ثبت شد , بعد از مشخص کردن برد و اتمام بازی در لیست مشخص میشود🪓'

time_added='زمان مورد نظر بر روی لیست اضافه شد ✅ '

is_running='بازی در حال ران شدن است لطفا کمی صبر کنید تا ربات نقش ها را ارسال کند ✅'

call_player='''بازیکن گرامی :
🛑🛑 بازی در حال ران شدن است 🛑🛑 
🛑🛑لطفا به روی مایک بیایید 🛑🛑  '''

call_limited = 'شما با هر لیست فقط میتوانید دو بار بازیکنان را فرا بخوانید 🛑  '

call_sended= 'احضاریه با موفقیت ارسال شد ✅'

god_changed = lambda x : f'''🎩 ادمین/گرداننده {x} ، گرداننده ی بازی شد:'''

aint_started='''🎩 گرداننده/ادمین گرامی :
هیچ بازی ای درحال حاضر شناسایی نشد ! 
لطفا برای باز کردن لیست جدید از دستور /open استفاده کنید :'''

role_sended='🎩 نقش ها با موفقیت ارسال شدند '

no_death = ' ** بدون تلفات ** ' 
win0='برد شهر'
win1='برد مافیا'
win2='برد مستقل'

add_warn=lambda name , warns : f'''🎩ادمین گرامی :
یک اخطار به {name} اضافه شد !
اخطار های پلیر: {warns}'''

del_warn=lambda name , warns : f'''🎩ادمین گرامی :
یک اخطار از {name} کم شد !
اخطار های پلیر: {warns}'''

reset_warn=lambda name:f'''🎩ادمین گرامی :
 اخطار های {name} به صفر تغییر یافت :'''
 
 
private_not_approved='🎩کاربر گرامی : \n متاسفانه تعداد بازی شما کمتر از تعداد محدود است \n درخاست شما برای ادمین ها ارسال شد لطفا منتظر باشید : '
not_approved=lambda mention : f'''🎩ادمین گرامی :
کاربر {mention} درخواست جوین به گروه داد اما تعداد بازی های ایشون کمتر از مقدار ثبت شده است ,شما میتوانید با دکمه ی زیر فرد را تایید کنید: '''


only_one='🎩 شما فقط یکبار در هر لیست میتوانید دعوت نامه ارسال بکنید  : '


invitation = lambda title , god , sen , link: f'''
🎩🔥 بازی جدید در گروه {title} 🔥🎩

▪️ شما میتوانید در بازی جدید گروهتان هم اکنون ثبت نام کنید

🎩 گرداننده : {god}
🎩 سناریو : {sen}

▪️ link : {link}

🎩 : همچنین میتوانید با استفاده دستور /register در گروه مورد نظر گروه خود را عوض کنید
'''

invitation_sended=lambda x : f'🎩 {x} پلیر به بازی دعوت شدند ! '

user_name_wrong='''🎩 کاربر گرامی : 
ایدی عددی یا یوزرنیم فردی که فرستادید نامعتبر میباشید :'''
 
reply_or_command='''🎩 کاربر گرامی : 
این دستور یا باید بر روی فردی ریپلای شود یا مقدار مورد نظر را جلوی دستور بنویسید !'''

god_deleted= lambda name : f'''
🎩 کاربر {name} از لیست گاد ها پاک شد :'''
god_setted= lambda name : f'''
🎩 کاربر {name} به لیست گاد ها اضافه شد :'''



player_cheak = lambda name,group,plays,warns,ban : f'''
👤 استعلام پلیر : 

🔅نام : {name}
🔅گروه : {group}
🔅بازی کل : {plays} 
⚠️وارن ها : {warns}
⛔️بن :
{ban}

'''


no = 'خیر'
yes='بله'



banned_all = '⛔️⛔️ شما به صورت کلی از ربات بن شدید ⛔️⛔️ \n ⚠️⛔️برای حل موضوع به پشتیبانی مراجعه کنید⛔️⚠️'
group_banned = lambda ban_date : f'''
🎩 پلیر گرامی : 
متاسفانه ادمین ها محدودیت بازی را بر روی شما اعمال کردند !
شما تا تاریخ زیر نمیتوانید در بازی های **این گروه** بنشینید :
⚠️ تاریخ محدودیت : 
{ban_date}
'''


ban_wrong='''
🎩 ادمین گرامی : 
راهنمایی برای دستور بن:  

مثال : /ban [id or username] [date]
- در قسمت [date] مقدار روز محدودیت را بنویسید 

همچنین میتوانید بر روی پیام فرد مورد نظر ریپلای کنید در این شرایط لازم نیست ایدی یا ایدی عددی فرد را در دستور قرار بدهید :
'''

player_banned=lambda name,user_id,admin,admin_id,ban,title:f'''🎩⚠️ محدودیت بر روی کاربر قرار گرفت :
▪️ نام کاربر : {name}
▪️ ایدی عددی کاربر : {user_id}
▪️ نام ادمین : {admin}
▪️ ایدی عددی ادمین : {admin_id}
▪️ گروه : {title}
⚠️ محدودیت : {ban} روز'''

player_unbanned=lambda name,user_id,admin,admin_id,title:f'''🎩🤍 محدودیت از روی کاربر برداشته شد  :
▪️ نام کاربر : {name}
▪️ ایدی عددی کاربر : {user_id}
▪️ نام ادمین : {admin}
▪️ ایدی عددی ادمین : {admin_id}
▪️ گروه : {title}
✅ پلیر بدون هیچ محدودیتی است '''


setting='⚙️ تنظیمات ⚙️'


ask_list_lock='''🎩 ادمین گرامی : مقدار محدودیتی که میخواهید روی لیست ها اعمال بشود را ارسال بفرمایید 


پلیر هایی که زیر تعداد ارسال شده بازی دارند نمیتوانند در لیست ثبت نام کنند'''

ask_emoji='🎩 ایموجی مورد نظر خود را انتخاب کنید : '

submited=lambda x : f'مقدار مورد نظر بر روی {x} ثبت شد 👍🏻'

ask_dell_sen= '🎩 سناریو مد نظر خود را که میخواهید حذف شود را انتخاب کنید :'

ask_see_sen= '🎩 سناریو مد نظر خود را که میخواهید حذف شود را انتخاب کنید :'


ask_name_sen='''🎩 کاربر گرامی :  نام سناریو را ارسال کنید :

مثال : 
بازپرس13
ناتو10


🔰 برای کنسل کردن واژه **cancel** را بنویسید :
🎩 @DarkMafiaChannel'''


ask_white='''🎩 کاربر گرامی : نقش های مورد نظر خود را که در گروه شهروندی هستند ارسال کنید : 
🔰 هیج علامت منفی" - " نباید در نقش ها باشد 

مثال : 
```شهروند ساده 
شهروند ساده 
دکتر
رویین تن```


🔰 برای کنسل کردن واژه **cancel** را بنویسید :
🎩 @DarkMafiaChannel'''

ask_black='''
🎩 کاربر گرامی : نقش های مورد نظر خود را که در گروه مافیایی هستند ارسال کنید : 
🔰 هیج علامت منفی" - " نباید در نقش ها باشد 

مثال : 
``شیاد
ناتو
گادفادر``


🔰 برای کنسل کردن واژه **cancel** را بنویسید :
🎩 @DarkMafiaChannel'''

ask_mos='''
🎩 کاربر گرامی : نقش های مورد نظر خود را که مستقل هستند را ارسال کنید : 
🔰 هیج علامت منفی" - " نباید در نقش ها باشد 

مثال : 
``زعوس 
ونوم ``

🔰 : اگر مستقلی وجود ندارد :
▪️ واژه  ** ندارد **  را ارسال کنید :


🔰 برای کنسل کردن واژه **cancel** را بنویسید :
🎩 @DarkMafiaChannel'''

doesnt='ندارد'

retry='c اگر هنوز قصد دارید سناریو اضافه کنید از اول شروع کنید 🔰'

cancel_word='cancel'

show_sen= lambda name , white , black : f'''
🎩 سناریو 🎩

▪️ نام : {name}

🤍تیم شهروندان :
🤍🤍🤍🤍🤍🤍
{white}


🖤تیم مافیا :
🖤🖤🖤🖤🖤🖤
{black}

'''

mos_sen_show=lambda mos :f'''
👽 تیم مستقل :
{mos}'''

scenario_added='🎩 سناریو مورد نظر اضافه شد :'

approve=lambda name,white,black,mos: f'''
🎩 ایا سناریو زیر مورد به لیست سناریو ها اضافه شود ؟ 

بله/خیر

➖➖➖➖➖➖➖➖➖➖

▪️ نام : {name}

🤍تیم شهروندان :
{white}

🖤تیم مافیا :
{black}

👽 تیم مستقل :
{mos}
'''

scenario_len_error='⚠️ نقش های سناریو بیشتر از 30 نقش است !'
scenario_name_exist='⚠️ نام سناریو با یک نام دیگر یکسان است و تداخل دارد !'


best_gaps=lambda x : f'🔥لیست بهترین گروه ها🔥 \n 🎩 در {x} روز گذشته : \n'


user_stats=lambda name,gap,id,all,shahr,maf,mall,mshahr,mmaf,emoji,all_rank,shahr_rank,maf_rank,mall_rank,mshahr_rank,mmaf_rank,bests,bests_rank,point,point_rank,mpoint,mpoint_rank : f'''
👤 پروفایل


{emoji}{emoji}{emoji}{emoji}{emoji}{emoji}{emoji}{emoji}{emoji}{emoji}
🎩نام : {name}
🎩ایدی : {id}
گروه : {gap}

🔅امار کل 🔅

🌟امتیاز :{point} ➞ رتبه {point_rank} ام
🎩 بازی ها :{all} ➞ رتبه {all_rank} ام
🎩برد شهر :{shahr} ➞ رتبه {shahr_rank} ام
🎩برد مافیا :{maf} ➞ رتبه {maf_rank} ام
🎩 بست ها :{bests}➞ رتبه {bests_rank} ام

🔅 امار ماهانه 🔅

🌟امتیاز :{mpoint} ➞ رتبه {mpoint_rank} ام
🎩 بازی ها :{mall} ➞ رتبه {mall_rank} ام
🎩برد شهر :{mshahr} ➞ رتبه {mshahr_rank} ام
🎩برد مافیا :{mmaf} ➞ رتبه {mmaf_rank} ام



🎩@DarkMafiaChannel
'''

user_stats_best_a=lambda name,gap,id,all,shahr,maf,mall,mshahr,mmaf,emoji,all_rank,shahr_rank,maf_rank,mall_rank,mshahr_rank,mmaf_rank,bests,bests_rank,point,point_rank,mpoint,mpoint_rank : f'''
💎💎💎 👑 👑 💎💎💎
💎       ʙᴇꜱᴛ  ᴘʟᴀʏᴇʀ       💎
👑 نام : {name}
👑 ایدی : {id}
👑 گروه : {gap}

💎       🔅امار کل🔅       💎     

🌟امتیاز :{point} ➞ رتبه {point_rank} ام
👑بازی ها :{all} ➞ رتبه {all_rank} ام
👑برد شهر :{shahr} ➞ رتبه {shahr_rank} ام
👑برد مافیا :{maf} ➞ رتبه {maf_rank} ام
👑بست ها :{bests}➞ رتبه {bests_rank} ام

💎    🔅امار ماهیانه🔅    💎

🌟امتیاز :{mpoint} ➞ رتبه {mpoint_rank} ام
👑بازی ها :{mall} ➞ رتبه {mall_rank} ام
👑برد شهر :{mshahr} ➞ رتبه {mshahr_rank} ام
👑برد مافیا :{mmaf} ➞ رتبه {mmaf_rank} ام

🎩 @DarkMafiaChannel'''

user_stats_best_c=lambda name,gap,id,all,shahr,maf,mall,mshahr,mmaf,emoji,all_rank,shahr_rank,maf_rank,mall_rank,mshahr_rank,mmaf_rank,bests,bests_rank,point,point_rank,mpoint,mpoint_rank : f'''
🕋🕋🕋  📿📿  🕋🕋🕋
🕋       ʙᴇꜱᴛ ᴄɪᴛɪᴢᴇɴ       🕋
🤍 نام : {name}
🤍 ایدی : {id}
🤍 گروه : {gap}

🕋       🔅امار کل🔅       🕋     

🌟امتیاز :{point} ➞ رتبه {point_rank} ام
🤍بازی ها :{all} ➞ رتبه {all_rank} ام
🤍برد شهر :{shahr} ➞ رتبه {shahr_rank} ام
🤍برد مافیا :{maf} ➞ رتبه {maf_rank} ام
🤍بست ها :{bests}➞ رتبه {bests_rank} ام

🕋    🔅امار ماهیانه🔅    🕋

🌟امتیاز :{mpoint} ➞ رتبه {mpoint_rank} ام
🤍بازی ها :{mall} ➞ رتبه {mall_rank} ام
🤍برد شهر :{mshahr} ➞ رتبه {mshahr_rank} ام
🤍برد مافیا :{mmaf} ➞ رتبه {mmaf_rank} ام

🎩 @DarkMafiaChannel'''

user_stats_best_m=lambda name,gap,id,all,shahr,maf,mall,mshahr,mmaf,emoji,all_rank,shahr_rank,maf_rank,mall_rank,mshahr_rank,mmaf_rank,bests,bests_rank,point,point_rank,mpoint,mpoint_rank : f'''
🎩🎩🎩  ☠️☠️  🎩🎩🎩
🎩         ʙᴇꜱᴛ ᴍᴀꜰɪᴀ         🎩
🖤 نام :{name}
🖤 ایدی :{id}
🖤 گروه :{gap}
🎩       🔅امار کل🔅       🎩     
🌟امتیاز :{point} ➞ رتبه {point_rank} ام
🖤بازی ها :{all} ➞ رتبه {all_rank} ام
🖤برد شهر :{shahr} ➞ رتبه {shahr_rank} ام
🖤برد مافیا :{maf} ➞ رتبه {maf_rank} ام
🖤بست ها :{bests}➞ رتبه {bests_rank} ام
🎩    🔅امار ماهیانه🔅    🎩
🌟امتیاز :{mpoint} ➞ رتبه {mpoint_rank} ام
🖤بازی ها :{mall} ➞ رتبه {mall_rank} ام
🖤برد شهر :{mshahr} ➞ رتبه {mshahr_rank} ام
🖤برد مافیا :{mmaf} ➞ رتبه {mmaf_rank} ام

🎩 @DarkMafiaChannel'''








local_users=lambda title , players :f'''🏆 بهترین بازیکنان 🏆  
گروه : {title} 

{players}

🔰 میتوانید با استفاده دستور /register در گروه مورد نظر گروه خود را عوض کنید

🎩@DarkMafiaChannel'''


global_users=lambda players : f'''
👑💎        🌎بهترین بازیکنان کل🌎        💎👑

{players}

💎 👑 💎 👑 💎 👑 💎 👑 💎 👑 💎 
'''

best_player_str=lambda emoji,n,mention,score: f'{emoji}{n}- {mention} ➞ {score} \n'

regester_group=lambda title ,user,id:f''''
🎩 پلیر گرامی : 
گروه شما با موفقیت عوض شد ✅
▪️ نام :  {user}
▪️ ایدی : {id}
▪️ گروه : {title}
🎩@DarkMafiaChannel'''

cancel_signin='شما از بازی با موفقیت حذف شدید ✅'


template_word='قالب'
ask_template='''
🎩 لطفا قالب لیست پیشفرض خود را ارسال کنید 
▪️ لیست پیشفرض باید تمامی مقادیر زیر را دارا باشد 
در جاهایی که میخواهید اطلاعات قرار بگیرد هر یک از عنصر های زیر را جا گذاری کنید : 

▪️ تاریخ : {DATE_TEXT}
▪️ لیست پلیر ها : {PLAYERS_TEXT}
▪️ سناریو : {SENATIO_TEXT}
▪️ نام گاد : {GOD_NAME_TEXT}
▪️ یوزنیم گروه : {GROUP_USERNAME_TEXT}
▪️ زمان مشخص شده : {TIME_TEXT}
▪️ تعداد ایونت : {EVENT_TEXT}

🔰 برای حالت پیشفرض واژه ی ** پیشفرض ** را ارسال کنید :
'''

template_help='''🎩 کاربر گرامی : 
قالب ارسال شده نامعتبر میباشید :
▪️ شما باید از تمامی عنصر ها استفاده بکنید !
'''


timer_start = '⏱ تایمر شروع شد '
timer_end = ' ⏰ تایمر تمام شد '

defualt_word='پیشفرض'


group_state=lambda title ,games_len , players_len : f'''
🎩 امار گروه

▪️ نام : {title}

▪️ بازی های این ماه : {games_len}

▪️ تعداد پلیر : {players_len}

🎩@DarkMafiaChannel'''

event_word='ایونت'

no_more_sen=' شما بیشتر  از 35 عدد سناریو نمیتوانید اضافه کنید'

  


w_inquiry=lambda w :f'''
▪️تعداد  ** {w} ** شهروند 🤍 '''

b_inquiry=lambda b :f'''
▫️تعداد  ** {b} ** مافیا 🖤 '''

m_inquiry=lambda m :f'''
🃏تعداد  ** {m} ** مستقل 😈 '''

no_deaths = '🪩 هیچ کشته وجود ندارد '


lines ='➖➖➖➖➖➖➖➖➖➖➖➖'
games_running=lambda group , scen , player_c , link , god , time  , cap: f'''

▪️ گروه : {group}
▪️ سناریو : {scen}
▪️ تعداد پلیر : {player_c}
▪️ جای خالی : {cap} 
▪️ گرداننده : {god}
▪️ ساعت : {time}
▪️ لینک : {link}
{lines}
'''

second_ell = ' رای گیری خروج برای : '

cleaning= 'درحال پاکسازی ... '


all_groups_stats=lambda emoji ,  num , username , hours , games , players , score : f'''{emoji}{num} - @{username} 
** {score} ** امتیاز , {games} بازی , {players} بازیکن , {hours} ساعت  \n {lines} \n 
'''


timer_alarm='لطفا جمع بندی بکنید 10 ثانیه باقی مانده !'


ask_name=lambda n : f'''کاربر {n} لطفا فارسی خود را ارسال کنید : '''

all_player_unbanned='همه ی پلیر ها انبن شدند !'

cards_pick='کارت مورد نظر خود را انتخاب کنید :'

swnd_card_1=lambda x :f'🃏 درحال قرعه کشی به تعداد : {x} بار'
swnd_card_2='-🃏🃏🃏🃏🃏🃏🃏🃏🃏-'
swnd_card_3=lambda card :f'🃏 کارت : {card}'

show_card=lambda name,x : f'''🃏 اطلاعات کارت {name} :

🃏 کارت ها : 
{x}'''


deleted= 'مقدار مورد نظر پاک شد !'
card_added = '🃏 کارت مورد نظر اضافه شد :'

no_more_card = ' شما بیشتر از 35 عدد کارت نمیتوانید اضافه کنید'

card_name_exist = '⚠️ نام کارت با یک نام دیگر یکسان است و تداخل دارد !'

ask_name_card='🃏 لطفا نام کارت را ارسال کنید : '

ask_card ='''🃏 لطفا کارت های مورد نظر را خط به خط ارسال کنید : 
🔰 هیج علامت منفی" - " نباید در کارت ها باشد 

مثال :

``مسیر سبز 
فیس اف 
سکوت بره‌ها
تغییر چهره ``'''

ask_dell_sen= '🃏 کارت مد نظر خود را که میخواهید حذف شود را انتخاب کنید :'

stopped='متوقف شد !'

vote_detector=lambda de : f'''

🗳️ دفاعیه :
{de}
'''

vvote=lambda p , v : f'شماره ** {p} ** با {v} رای \n'