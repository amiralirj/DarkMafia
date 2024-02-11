import sqlite3 as db
import datetime

import os
#SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) 
del os

class Data:
    def __init__(self) -> None:    
        self.con = db.connect(f"MafiaBase.db" , detect_types=db.PARSE_DECLTYPES, check_same_thread = False)
        self.c=self.con.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Groups (group_id INT PRIMARY KEY , support INT , g2 INT , g3 INT , g4 INT , state_lock INT , Membership TEXT , Owner INT , template TEXT ,emoji TEXT , join_lock INT , Ev_num INT , Farsi_name INT)''')
        self.c.execute('CREATE TABLE IF NOT EXISTS Gods (user_id INT , group_id INT , uni_que TEXT PRIMARY KEY )')
        self.c.execute('CREATE TABLE IF NOT EXISTS Users (user_id INT PRIMARY KEY , total_score INT, total_game INT , total_win INT , maf_win INT , shahr_win INT , bests INT , Group_id INT , Banned INT , FarsiName TEXT)'  )
        self.c.execute('CREATE TABLE IF NOT EXISTS Group_User (user_gap INT PRIMARY KEY , User_id INT, Groups INT , Warns INT , Banned TEXT )')
        self.c.execute('CREATE TABLE IF NOT EXISTS Month_Users (user_id INT PRIMARY KEY , total_score INT, total_game INT , total_win INT , maf_win  INT, shahr_win INT , bests INT )'  )
        self.c.execute('CREATE TABLE IF NOT EXISTS Games (group_id INT , scenario TEXT , god INT , point INT , date TEXT, win INT , active INT ,mid INT , all_plyrs TEXT )')
        self.c.execute('CREATE TABLE IF NOT EXISTS Scenario (group_id INT , name TEXT , white TEXT , black TEXT , mos TEXT , uni_que TEXT PRIMARY KEY )')
        self.c.execute('CREATE TABLE IF NOT EXISTS Cards (group_id INT , name TEXT , cards TEXT )')
        self.con.commit()
        print('DataBase Has Successfully Loaded') 
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def delete_card(self,gap,name):
        self.c.execute('DELETE FROM Cards WHERE name=:namee and group_id=:gap ',{'namee':(name),'gap':gap})
        self.con.commit()
    
    def add_card(self,gap,name,cards):
        self.c.execute('INSERT OR IGNORE INTO Cards (group_id,name,cards) VALUES (:group_id,:name,:cards)',
            {'group_id':gap,'name':name,'cards':cards} )
        self.con.commit()
    
    def show_cards(self,group):
        self.c.execute('SELECT name FROM Cards WHERE group_id=:g_id ', {'g_id': int(group)})
        result = self.c.fetchall()
        return result
    
    def see_card(self,group,name):
        self.c.execute('SELECT cards FROM Cards WHERE group_id=:g_id and name=:name ', {'g_id': int(group),'name':name})
        result = self.c.fetchall()[0][0]
        return result
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def FIND_MAIN(self, ID):
        self.c.execute('SELECT group_id FROM Groups WHERE group_id=:g_id OR support=:g_id OR g2=:g_id OR g3=:g_id OR g4=:g_id', {'g_id': int(ID)})
        result = self.c.fetchall()[0][0]
        return result
        # try : 
        #     self.c.execute('SELECT state_lock FROM Groups WHERE group_id=:g_id ', {'g_id': int(ID)})
        #     result = self.c.fetchall()[0][0]
        #     return ID
        # except:
        #     self.c.execute('SELECT group_id FROM Groups WHERE support=:g_id OR g2=:g_id OR g3=:g_id OR g4=:g_id', {'g_id': int(ID)})
        #     result = self.c.fetchall()[0][0]
        #     return result

    def CHANGE_MAIN(self,new_group_id,old_group_id):
        self.c.execute("UPDATE Groups SET group_id = ? WHERE group_id = ?", (new_group_id, old_group_id))
        self.c.execute('DELETE FROM Gods WHERE group_id=:group_id ',{'group_id':int(old_group_id)})
        self.c.execute("UPDATE Users SET Group_id = ? WHERE Group_id = ?", (new_group_id, old_group_id))
        self.c.execute("UPDATE Group_User SET Groups = ? WHERE Groups = ?", (new_group_id, old_group_id))
        self.c.execute("UPDATE Games SET group_id = ? WHERE group_id = ?", (new_group_id, old_group_id))
        self.c.execute("UPDATE Scenario SET group_id = ? WHERE group_id = ?", (new_group_id, old_group_id))
        self.con.commit()
        
    def Add_group(self,group_id,sup,g2,g3,g4,date,Owner):
        self.c.execute('INSERT OR IGNORE INTO Groups (group_id,support,g2,g3,g4,state_lock,Membership,Owner,template,emoji,join_lock,Ev_num,Farsi_name) VALUES (:group_id,:support,:g2,:g3,:g4,:state_lock,:Membership,:Owner,:template,:emoji,:join_lock,:Event_num,:Farsi_name)',
                    {'group_id':int(group_id),'support':int(sup),'g2':int(g2),'g3':int(g3),'g4':int(g4),'state_lock':0,'Membership':'None','Owner':Owner,'template':'None','emoji':'🎩','join_lock':0,'Event_num':1,'Farsi_name':0} )
        self.con.commit()
        self.Add_Membership(int(date),int(group_id))
        
    def DELETE_GROUP(self,group_id):
        self.c.execute('DELETE FROM Groups WHERE group_id=:group_id ',{'group_id':int(group_id)})
        self.con.commit()
    
    def Change_join_lock(self,group_id,join_lock):
        self.c.execute(f'UPDATE Groups SET join_lock=:join_lok WHERE group_id=:groupid',{'groupid':int(group_id),'join_lok':join_lock})
        self.con.commit()
        
    def Change_state(self,group_id,state):
        self.c.execute(f'UPDATE Groups SET state_lock=:state_lock WHERE group_id=:group_id',{'group_id':int(group_id),'state_lock':state})
        self.con.commit()
        
    def Change_template(self,group_id,template):
        self.c.execute(f'UPDATE Groups SET template=:templat WHERE group_id=:group_id',{'group_id':int(group_id),'templat':template})
        self.con.commit()
        
    def Change_emoji(self,group_id,emoji):
        self.c.execute(f'UPDATE Groups SET emoji=:emoj WHERE group_id=:group_id',{'group_id':int(group_id),'emoj':emoji})
        self.con.commit()
        
    def Change_sup(self,group_id,support):
        self.c.execute(f'UPDATE Groups SET support=:support WHERE group_id=:group_id',{'group_id':int(group_id),'support':support})
        self.con.commit()
    
    def Change_owner(self,group_id,owner):
        self.c.execute(f'UPDATE Groups SET Owner=:owner WHERE group_id=:group_id',{'group_id':int(group_id),'owner':owner})
        self.con.commit()
    
    def Change_g2(self,group_id,g2):
        self.c.execute(f'UPDATE Groups SET g2=:g2 WHERE group_id=:group_id',{'group_id':int(group_id),'g2':g2})
        self.con.commit()
        
    def Change_g3(self,group_id,g3):
        self.c.execute(f'UPDATE Groups SET g3=:g3 WHERE group_id=:group_id',{'group_id':int(group_id),'g3':g3})
        self.con.commit()
        
    def Change_g4(self,group_id,g4):
        self.c.execute(f'UPDATE Groups SET g4=:g4 WHERE group_id=:group_id',{'group_id':int(group_id),'g4':g4})
        self.con.commit()

    def Add_Ev_num(self,group_id):
        self.c.execute(f'UPDATE Groups SET Ev_num=Ev_num+1 WHERE group_id=:group_id',{'group_id':int(group_id)})
        self.con.commit()
        
    def Change_Ev_num(self,group_id,Ev_num):
        self.c.execute(f'UPDATE Groups SET Ev_num=:Event_num WHERE group_id=:group_id',{'group_id':int(group_id),'Event_num':int(Ev_num)})
        self.con.commit()
        
    def Change_Farsi_name(self,group_id,amount):
        self.c.execute(f'UPDATE Groups SET Farsi_name=:Fari_name WHERE group_id=:group_id',{'group_id':int(group_id),'Fari_name':int(amount)})
        self.con.commit()

    
    def See_group(self,group_id):
        self.c.execute('SELECT * FROM Groups WHERE  group_id=:group_id OR support=:group_id OR g2=:group_id OR g3=:group_id OR g4=:group_id ',{'group_id':int(group_id)})
        det = (self.c.fetchall())[0]
        return {'group_id':det[0],'support':det[1],'g2':det[2],'g3':det[3],'g4':det[4],'state_lock':det[5],'Membership':det[6],'Owner':det[7],'template':det[8],'emoji':det[9],'join_lock':det[10],'Ev_num':det[11],'Farsi_name':det[12]}
        
    def See_all_groups(self):
        self.c.execute('SELECT group_id,support,g2,g3,g4 FROM Groups')
        det = (self.c.fetchall())
        return det
    

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def show_all_MMMM_users(self):
        self.c.execute('SELECT * FROM Month_Users ')
        return (self.c.fetchall())
    
    def add_MMMM_score(self,user_id,score):
        self.c.execute(f'UPDATE Month_Users SET total_score=total_score+{int(score)} WHERE user_id=:user_id ',{'user_id':int(user_id)})
        self.con.commit()
        
    def Add_MMMM_user(self,user_id):
        self.c.execute('INSERT OR IGNORE INTO Month_Users (user_id,total_score,total_game,total_win,maf_win,shahr_win,bests) VALUES (:user_id,:total_score,:total_game,:total_win,:maf_win,:shahr_win,:bests)',
                    {'user_id':user_id,'total_score':0,'total_game':0,'total_win':0,'maf_win':0,'shahr_win':0,'bests':0} )
        self.con.commit()
    
    def add_MMMM_point(self,user_id,kind):
        '''total_score,total_game,total_win,maf_win,shahr_win,bests'''
        self.c.execute(f'UPDATE Month_Users SET {kind}={kind}+1 WHERE user_id=:user_id ',{'user_id':int(user_id)})
        self.con.commit()
    
    def red_MMMM_point(self,user_id,kind):
        '''total_score,total_game,total_win,maf_win,shahr_win,bests'''
        self.c.execute(f'UPDATE Month_Users SET {kind}={kind}-1 WHERE user_id=:user_id ',{'user_id':int(user_id)})
        self.con.commit()
        
    def Show_MMMM_user(self,user_id):
        self.c.execute('SELECT * FROM Month_Users WHERE  user_id=:user_id ',{'user_id':int(user_id)})
        return (self.c.fetchall())[0]
    
    def reStart(self):
        self.c.execute(f'UPDATE Month_Users SET total_score=0,total_game=0,total_win=0,maf_win=0,shahr_win=0 ')
        self.con.commit()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def show_group_users(self,group):
        self.c.execute('SELECT * FROM Users WHERE Group_id=:gp_id',{'gp_id':group})
        return (self.c.fetchall())
    
    def show_all_users(self):
        self.c.execute('SELECT * FROM Users ')
        return (self.c.fetchall())
    
    def add_score(self,user_id,score):
        self.c.execute(f'UPDATE Users SET total_score=total_score+{int(score)} WHERE user_id=:user_id ',{'user_id':int(user_id)})
        self.con.commit()
        
    def Add_user(self,user_id,group_id):
        self.c.execute('INSERT OR IGNORE INTO Users (user_id,total_score,total_game,total_win,maf_win,shahr_win,bests,Group_id,Banned,FarsiName) VALUES (:user_id,:total_score,:total_game,:total_win,:maf_win,:shahr_win,:bests,:Group_id,:Banned,:FarsiName)',
                    {'user_id':user_id,'total_score':0,'total_game':0,'total_win':0,'maf_win':0,'shahr_win':0,'bests':0,'Group_id':group_id,'Banned':0,'FarsiName':'بی نام'} )
        self.c.execute('INSERT OR IGNORE INTO Group_User (user_gap,User_id,Groups,Warns,Banned) VALUES (:user_gap,:User_id,:Groups,:Warns,:Banned)',
                    {'user_gap':f'{abs(int(user_id))}{abs(int(group_id))}','User_id':user_id,'Groups':group_id,'Warns':0,'Banned':'None'} )
        self.con.commit()
    
    def change_name(self,user_id,name):
        self.c.execute(f'UPDATE Users SET FarsiName=:xxx WHERE user_id=:user_id ',{'user_id':int(user_id),'xxx':name})
        self.con.commit()
        
    def add_point(self,user_id,kind):
        '''total_score,total_game,total_win,maf_win,shahr_win'''
        self.c.execute(f'UPDATE Users SET {kind}={kind}+1 WHERE user_id=:user_id ',{'user_id':int(user_id)})
        self.con.commit()
    
    def red_point(self,user_id,kind):
        '''total_score,total_game,total_win,maf_win,shahr_win'''
        self.c.execute(f'UPDATE Users SET {kind}={kind}-1 WHERE user_id=:user_id ',{'user_id':int(user_id)})
        self.con.commit()
        
    def Show_user(self,user_id):
        self.c.execute('SELECT * FROM Users WHERE user_id=:user_id ',{'user_id':int(user_id)})
        return (self.c.fetchall())[0]

    def ban(self,user_id):
        self.c.execute(f'UPDATE Users SET Banned=1 WHERE user_id=:user_id ',{'user_id':int(user_id)})
        self.con.commit()
    
    def unban(self,user_id):
        self.c.execute(f'UPDATE Users SET Banned=0 WHERE user_id=:user_id ',{'user_id':int(user_id)})
        self.con.commit()
        
    def change_group(self,user_id,group_id):
        self.c.execute(f'UPDATE Users SET Group_id=:gp WHERE user_id=:user_id ',{'user_id':int(user_id),'gp':group_id})
        self.con.commit()
    
    def change_group(self,user_id,group_id):
        self.c.execute(f'UPDATE Users SET Group_id=:gp WHERE user_id=:user_id ',{'user_id':int(user_id),'gp':group_id})
        self.con.commit()
    
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def change_warn(self,user_id,gap,warn):
        '''user_gap,User_id,Groups,Warns,Banned'''
        self.c.execute(f'UPDATE Group_User SET Warns=Warns+{warn} WHERE user_id=:user_id and Groups=:gp ',{'gp':gap,'user_id':int(user_id)})
        self.con.commit()
        
    def group_ban(self,user_id,gap,date='None'):
        self.c.execute(f'UPDATE Group_User SET Banned=:Date WHERE User_id=:user_id  and Groups=:gp',{'gp':gap,'user_id':int(user_id),'Date':date})
        self.con.commit()
    
    def group_all_unban(self,gap):
        self.c.execute(f'UPDATE Group_User SET Banned=:Date WHERE Groups=:gp',{'gp':gap,'Date':'None'})
        self.con.commit()

    def Show_group_user(self,user_id,gap):
        self.c.execute('SELECT * FROM Group_User WHERE User_id=:user_id and Groups=:gp ',{'gp':gap,'user_id':int(user_id)})
        return (self.c.fetchall())[0]
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def Add_god(self,group_id,user_id):
        self.c.execute('INSERT INTO Gods (user_id,group_id,uni_que) VALUES (:user_id,:group_id,:uni_que)',
                       {'user_id':user_id,'group_id':group_id,'uni_que':f'{user_id}{group_id}'} )
        self.con.commit()
        
    def Del_god(self,group_id,user_id):
        self.c.execute('DELETE FROM Gods WHERE group_id=:group_id AND user_id=:user_id',{'group_id':int(group_id),'user_id':user_id})
        self.con.commit()
    
    def Del_all_god(self,group_id):
        self.c.execute('DELETE FROM Gods WHERE group_id=:group_id ',{'group_id':int(group_id)})
        self.con.commit()
        
    def See_gods(self,group_id):
        self.c.execute('SELECT user_id FROM Gods WHERE group_id=:group_id',{'group_id':int(group_id)})
        gods=[i[0] for i in (self.c.fetchall())]
        return gods
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
    
    def Add_match(self,group_id,scenario,god,mid,all_plyrs):   
        date=str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M"))
        self.c.execute('INSERT INTO Games (group_id,scenario,god,point,date,win,active,mid,all_plyrs) VALUES (:group_id,:scenario,:god,:point,:date,:win,:active,:mid,:all_plyrs)',
                       {'group_id':group_id,'scenario':scenario,'god':god,'point':0,'date':date,'win':0,'active':1,'mid':mid,'all_plyrs':all_plyrs})
        self.con.commit()
        
    def End_match(self,point,win,group_id):
        self.c.execute(f'UPDATE Games SET point=:point,win=:win,active=0 WHERE group_id=:group_id AND active=1',{'group_id':int(group_id),'point':point,'win':win})
        self.con.commit()
        
    def set_0_group_point(self,group_id):
        self.c.execute(f'UPDATE Games SET point=0 WHERE group_id=:group_id',{'group_id':int(group_id)})
        self.con.commit()
        
    def unactive(self,group_id):
        self.c.execute(f'UPDATE Games SET active=0 WHERE group_id=:group_id AND active=1',{'group_id':int(group_id)})
        self.con.commit()
    
    def Change_mid(self,group_id,mid):
        self.c.execute(f'UPDATE Games SET mid=:mid WHERE group_id=:group_id AND active=1',{'group_id':int(group_id),'mid':mid})
        self.con.commit()
        
    def Change_god(self,group_id,god):
        self.c.execute(f'UPDATE Games SET god=:god WHERE group_id=:group_id AND active=1',{'group_id':int(group_id),'god':god})
        self.con.commit()
        
    def See_games(self,group_id):
        self.c.execute('SELECT * FROM Games WHERE group_id=:group_id',{'group_id':int(group_id)})
        return (self.c.fetchall())
    
    def see_active_game(self,group_id):
        self.c.execute('SELECT group_id,scenario,god,point,date,win,active,mid,all_plyrs FROM Games WHERE group_id=:group_id AND active=1',{'group_id':int(group_id)})
        return (self.c.fetchall())[0]
    
    def Change_all_players(self,group_id,all_plyrs):
        self.c.execute(f'UPDATE Games SET all_plyrs=:all_plyrs WHERE group_id=:group_id AND active=1',{'group_id':int(group_id),'all_plyrs':all_plyrs})
        self.con.commit()
        
        
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -       
    
    def Add_Membership(self,date,group):
        membership=str(datetime.date.today() + datetime.timedelta(days=date))
        self.c.execute(f'UPDATE Groups SET Membership=:Membership WHERE group_id=:group_id',{'group_id':int(group),'Membership':membership})
        self.con.commit()
        return membership
    
    @property
    def Show_Membership(self,group):
        self.c.execute('SELECT Membership FROM Groups WHERE group_id=:group_id',{'group_id':int(group)})
        M_D=str((self.c.fetchall())[0][0])
        if M_D == 'None':'2004-2-24'
        return M_D
    
    @property
    def Have_Membership(self):
        Day = datetime.datetime.now()
        m_date=self.Show_Membership
        if m_date == 'None': return False
        End_Sub = datetime.datetime.now().strptime(m_date,"%Y-%m-%d")
        if Day < End_Sub:
            return True
        return False
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def Show_roles(self,name,group_id):
        self.c.execute('SELECT white,black,mos FROM Scenario WHERE name=:name AND group_id=:group_id ',{'name':name,'group_id':int(group_id)})
        roles=(self.c.fetchall())[0]
        return {'white':roles[0],'black':roles[1],'mos':roles[2]}
        
    def Add_Scenario(self,group_id,name,roles):
        self.c.execute('INSERT INTO Scenario (group_id,name,white,black,mos,uni_que) VALUES (:group_id,:name,:white,:black,:mos,:uni_que)',
                       {'group_id':group_id,'name':name,'white':roles['white'],'black':roles['black'],'mos':roles['mos'],'uni_que':f'{group_id}{name}'})
        self.con.commit()
    
    def Del_Scenario(self,group_id,name):
        self.c.execute('DELETE FROM Scenario WHERE group_id=:group_id AND name=:name',{'group_id':int(group_id),'name':name})
        self.con.commit()
        
    def Show_All_Scenario(self,group_id):
            self.c.execute('SELECT name FROM Scenario WHERE  group_id=:group_id ',{'group_id':int(group_id)})
            return (self.c.fetchall())
        
DataBase=Data()
