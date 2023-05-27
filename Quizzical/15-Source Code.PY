# CSE100 - Fundamentals of computer programming
# Final Project

# Author : AU2140058 - Prashansa Shah
#          AU2140060 - Deval Darji
#          AU2140081 - Divya Patel

# Description:
# It's a Quiz/Trivia with different types of topics and genres.
# It can be used both as a fun game and for educational purposes.

import random
import time
from threading import Timer
import pandas as pd
from datetime import datetime
import stdiomask
import csv
import os
from collections import OrderedDict
import smtplib
import email.utils
from email.mime.text import MIMEText 
correct=[]
incorrert=[]

file_name=["Music.csv","Sports.csv","Hindi.csv","English.csv","Food.csv","Travel.csv","Literature.csv","GK.csv","MA.csv","Edu.csv"]
topic_name=["Music","Sports","Hindi","English","Food","Travel","Literature","GK","MA","Edu"]
topic_index="__________________________Topics___________________________\n1.  Music\n2.  Sports\n3.  Bollywood\n4.  Hollywood\n5.  Food\n6.  Travel\n7.  Literature\n8.  General Knowledge\n9.  Mental Ability\n10. Education\n"

timeout=60
totaltime=600

def removeacc(username):
    print("-------------------------------------------------------------------\n")
    password = stdiomask.getpass("Enter your Password: ")
    print("-------------------------------------------------------------------\n")
    lp=passwfunc()
    x=len(lp)
    try:
        for i in range(x):
            if lp[i]==password:
                E1=Emailfunc()
                emailId=E1[i]
                delacc=f"{username},{password},{emailId}\n"
                choice=int(input("Are you sure you want to delete this account?\n1. Yes\n2. No\nEnter your choice:"))
                if choice==1:
                    with open('playerid.txt', 'r') as fr:
                        lines = fr.readlines()
                        j=0 
                        with open('playerid.txt', 'w') as fw:
                            for line in lines:
                                if j!=i: 
                                    fw.write(line)
                                j+=1 
                    file = f"{username}sco.csv"
                    if(os.path.exists(file) and os.path.isfile(file)):
                        os.remove(file)
                    SendEmail("Your account is Deleted",emailId)
                    print("Account Deleted!")
                elif choice==2:
                    playerindex(username)
    except:
        os.system('cls')
        print("Wrong password!")
        removeacc(username)
        
    exit()

def namefunc():
    filetxt=open("playerid.txt")
    x=0
    lista1=[]
    for line in filetxt:
        a=line.split(",")
        for i in a:
            i=i.rstrip() #removing new line from elements in list
            if x%3==0:
                lista1.append(i)
            x+=1
    return lista1

def passwfunc():
    filetxt=open("playerid.txt")
    lista2=[]
    x=2
    for line in filetxt:
        a=line.split(",")
        for i in a:
            i=i.rstrip() #removing new line from elements in list
            if x%3==0:
                lista2.append(i)
            x+=1
    return lista2

def Emailfunc():
    
    filetxt=open("playerid.txt")

    x=1

    lista3=[]
    for line in filetxt:
        a=line.split(",")
        for i in a:
            i=i.rstrip() #removing new line from elements in list
            if x%3==0:
                lista3.append(i)
            x+=1

    return lista3

def SendEmail(msgstr,emailId): 
    msg = MIMEText(msgstr)
    msg['Subject'] = 'WELCOME TO QUIZICLE'
    msg['From'] = "cse100endsemproject@gmail.com"
    msg['To'] = emailId
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login("cse100endsemproject@gmail.com", "03181803")
    s.sendmail("cse100endsemproject@gmail.com",emailId , msg.as_string())
    s.quit()
    return

def playername():
    print("-------------------------------------------------------------------\n")
    name = input("Enter Your User Id: ")
    password = stdiomask.getpass("Enter your Password: ")
    print("-------------------------------------------------------------------\n")
    l1=namefunc()
    l2=passwfunc()
    x=len(l1)
    for i in range(x):
        if l1[i]==name:
            if l2[i]==password:
                E1=Emailfunc()
                emailId=E1[i]
                now=datetime.now()
                timedate=now.strftime("%d/%m/%Y %H:%M:%S")
                SendEmail(f"You have logged into your Quiz account at {timedate}",emailId)
                print(playerindex(name))
    else:
        os.system('cls')
        print("You entered wrong User id or Password! [Note: If you haven't signed up, please sign up first.]")
        print(playername())

def leaderboard(entrylb,name1):
    l12=namefunc()
    x=len(l12)
    leaderdic={}
    for i in range(x-1):
        fname=f"{l12[i+1]}sco.csv"
        fread=pd.read_csv(fname)
        totalpoint=fread['Total Points'].sum()
        points=round(totalpoint,2)
        if points>1000000:
            leaderdic[f"{l12[i+1]}(7*)"]=points
        elif points>500000 and points<1000000:
            leaderdic[f"{l12[i+1]}(6*)"]=points
        elif points>100000 and points<500000:
            leaderdic[f"{l12[i+1]}(5*)"]=points
        elif points>50000 and points<100000:
            leaderdic[f"{l12[i+1]}(4*)"]=points
        elif points>25000 and points<50000:
            leaderdic[f"{l12[i+1]}(3*)"]=points
        elif points>10000 and points<25000:
            leaderdic[f"{l12[i+1]}(2*)"]=points
        elif points>5000 and points<10000:
            leaderdic[f"{l12[i+1]}(1*)"]=points
        else:
            leaderdic[f"{l12[i+1]}(0*)"]=points
    dict=OrderedDict(sorted(leaderdic.items()))
    print("User Id(Star)    Scores\n")
    for key in leaderdic:
        print(key,  ' : ',leaderdic[key])
    print("-------------------------------------------------------------------\n")
    if entrylb==1:
        Exit=input("Press Enter to go back to index: ")
        os.system('cls')
        return index()
    elif entrylb==2:
        Exit=input("Press Enter to go back to index: ")
        os.system('cls')
        return playerindex(name1)

def playerscore(entryps,name3): 
    if entryps==2:
        try:  
            file=f"{name3}sco.csv"
            df=pd.read_csv(file)
            pfile=open(file)
            pread=csv.reader(pfile)
            plength=len(list(pread)) 
            psize=plength-1
            correcttotal=df['Correct answers'].sum()
            sumpoints=df['Total Points'].sum()
            maximumpoint=df['Total Points'].max()
            topic=df['Topic'].mode()
            repetedtopic=topic[0]
            accuracy=(correcttotal/psize)*10
            print(df)
            print(f"Total Score: {sumpoints}\nMaximum Score: {maximumpoint}\nMost Taken Topic: {repetedtopic}\nAccuracy: {accuracy}%")
        except:
            print("You have not played any game yet!")
        print("-------------------------------------------------------------------\n")
        Exit=input("Press Enter to go back to index: ")
        os.system('cls')
        print(playerindex(name3))
    elif entryps==1:
        la=namefunc()
        x=len(la)
        for i in range(x-1):
            print(f"{i+1}.   {la[i+1]}")
        choice=int(input("Enter Your Choice: "))
        print("-------------------------------------------------------------------\n")
        try:
            filenam=f"{la[choice]}sco.csv"
            df=pd.read_csv(filenam)
            pfile=open(filenam)
            pread=csv.reader(pfile)
            plength=len(list(pread))
            psize=plength-1
            correct_total=df['Correct answers'].sum()
            pointsum=df['Total Points'].sum()
            pointmax=df['Total Points'].max()
            mode=df['Topic'].mode()
            topicmode=mode[0]
            accurat=(correct_total/psize)*10
            print(df)
            print(f"Total Score: {pointsum}\nMaximum Score: {pointmax}\nMost Taken Topic: {topicmode}\nAccuracy: {accurat}%")
        except:
            print("This player has not played any game yet!")
        print("-------------------------------------------------------------------\n")
        p=input("Press Enter to go back to index: ")
        os.system('cls')
        print(index())

def question(num,nameof_file):
    df = pd.read_csv(nameof_file)
    print(df['Question'][num])
    print("1.",df['A'][num])
    print("2.",df['B'][num])
    print("3.",df['C'][num])
    print("4.",df['D'][num])
    print("5 Skip Question")
    print("-------------------------------------------------------------------\n")
    t=Timer(timeout,print,["\nSorry, time's up! \n Enter 0 for next Question"])
    t.start()
    x=int(input("Enter your answer: "))
    if x==df['answer'][num]:
        print("Correct\n")
        correct.append(1)
        next=int(input("Enter 0 for next Question: "))
        print("-------------------------------------------------------------------\n")
        os.system('cls')
    elif x==5:
        print("You Skipped this Quetion\n")
        next=int(input("Enter 0 for next Question: "))
        print("-------------------------------------------------------------------\n")
        os.system('cls')
    elif x==1 or x==2 or x==4 or x==3 and x!=df['answer'][num]:
        print("Incorrect\n")
        incorrert.append(1)
        next=int(input("Enter 0 for next Question: "))
        print("-------------------------------------------------------------------\n")
        os.system('cls')
    else:
        print("")
        print("-------------------------------------------------------------------\n")
        os.system('cls')
    t.cancel()

def adduser():
    print("-------------------------------------------------------------------\n")
    newuserid=input("Set Your User name: ")
    newpassword=input("\n(Your password should be 8 characters long.\nMust start with a Capital letter.\nMust include a lowercase character and a numeric character.)\n\nSet your Password: ")
    if len(newpassword)==8:
        if 60<=ord(newpassword[0])<=90:
            for i in range(8):
                if newpassword[i]=='0' or newpassword[i]=='1' or newpassword[i]=='2' or newpassword[i]=='3' or newpassword[i]=='4' or newpassword[i]=='5' or newpassword[i]=='6' or newpassword[i]=='7' or newpassword[i]=='8' or newpassword[i]=='9':
                    if 97<=ord(newpassword[0])<=122 or 97<=ord(newpassword[1])<=122 or 97<=ord(newpassword[2])<=122 or 97<=ord(newpassword[3])<=122 or 97<=ord(newpassword[4])<=122 or 97<=ord(newpassword[5])<=122 or 97<=ord(newpassword[6])<=122 or 97<=ord(newpassword[7])<=122:
                        flag=2
                    else:
                        flag=1
                else:
                    flag=0
        else:
            print("First letter is not uppercase")
            adduser()
            os.system('cls')
        
    else:
        print("The length of password must be 8 characters")
        adduser()
        os.system('cls')
        
    if flag==0:
        print("Numeric value is missing")
        adduser()
        os.system('cls')
        
    elif flag==1:
        print("Lowercase is missing")
        adduser()
        os.system('cls')
        
    elif flag==2:
        emailId=input("\nEnter your email Id here: ")
        print("-------------------------------------------------------------------\n")
        try:
            SendEmail(f"Your account is created. \nUser Id: {newuserid} \nPassword: {newpassword} \n\n\nHope you enjoy the quiz.",emailId)
        except:
            print("Wrong Email id!")
            adduser()

        filenamepass=open("playerid.txt","a")
        namepass=f"{newuserid},{newpassword},{emailId}\n"
        filenamepass.write(namepass)
        filenamepass.close()
        newfile=f"{newuserid}sco.csv"
        
        with open(newfile,"a",newline="") as Fill:
            Writer=csv.writer(Fill)
            Writer.writerow(["Question Points","Total Points","Time","Topic","Correct answers","Incorrect answers"])
        Fill.close()

        os.system('cls')
    return playindex()

def topicacc():
    music=[]
    sports=[]
    hindi=[]
    english=[]
    food=[]
    travel=[]
    politics=[]
    gk=[]
    ma=[]
    edu=[]
    sum1,sum2,sum3,sum4,sum5,sum6,sum7,sum8,sum9,sum10=0,0,0,0,0,0,0,0,0,0
    la1=namefunc()
    x=len(la1)
    for i in range(x-1):
        name=f"{la1[i+1]}sco.csv"
        dp=pd.read_csv(name)
        file=open(name)
        readfile=csv.reader(file)
        length=len(list(readfile))
        for j in range(length-1):
            if dp['Topic'][j]==topic_name[0]:
                music.append(dp['Correct answers'][j])
            elif dp['Topic'][j]==topic_name[1]:
                sports.append(dp['Correct answers'][j])
            elif dp['Topic'][j]==topic_name[2]:
                hindi.append(dp['Correct answers'][j])
            elif dp['Topic'][j]==topic_name[3]:
                english.append(dp['Correct answers'][j])
            elif dp['Topic'][j]==topic_name[4]:
                food.append(dp['Correct answers'][j])
            elif dp['Topic'][j]==topic_name[5]:
                travel.append(dp['Correct answers'][j])
            elif dp['Topic'][j]==topic_name[6]:
                politics.append(dp['Correct answers'][j])
            elif dp['Topic'][j]==topic_name[7]:
                gk.append(dp['Correct answers'][j])
            elif dp['Topic'][j]==topic_name[8]:
                ma.append(dp['Correct answers'][j])
            elif dp['Topic'][j]==topic_name[9]:
                edu.append(dp['Correct answers'][j])
    for i1 in range(len(music)):
        sum1=sum1+music[i1]
    for i2 in range(len(sports)):
        sum2=sum2+sports[i2]
    for i3 in range(len(hindi)):
        sum3=sum3+hindi[i3]
    for i4 in range(len(english)):
        sum4=sum4+english[i4]
    for i5 in range(len(food)):
        sum5=sum5+food[i5]
    for i6 in range(len(travel)):
        sum6=sum6+travel[i6]
    for i7 in range(len(gk)):
        sum8=sum8+gk[i7]
    for i8 in range(len(ma)):
        sum9=sum9+ma[i8]
    for i9 in range(len(politics)):
        sum7=sum7+politics[i9]
    for i10 in range(len(edu)):
        sum10=sum10+edu[i10]
    try:
        sum1=sum1/len(music)*10
    except:
        sum1=0
    try:
        sum2=sum2/len(sports)*10
    except:
        sum2=0
    try:
        sum3=sum3/len(hindi)*10
    except:
        sum3=0
    try:
        sum4=sum4/len(english)*10
    except:
        sum4=0
    try:
        sum5=sum5/len(food)*10
    except:
        sum5=0
    try:
        sum6=sum6/len(travel)*10
    except:
        sum6=0
    try:
        sum7=sum7/len(politics)*10
    except:
        sum7=0
    try:
        sum8=sum8/len(gk)*10
    except:
        sum8=0
    try:
        sum9=sum9/len(ma)*10
    except:
        sum9=0
    try:
        sum10=sum10/len(edu)*10
    except:
        sum10=0
    sum={"Music     ":sum1,"Sports    ":sum2,"Hindi     ":sum3,"English   ":sum4,"Food      ":sum5,"Travel    ":sum6,"Politics  ":sum7,"Gk        ":sum8,"MA        ":sum9,"Edu       ":sum10}
    dict1=OrderedDict(sorted(sum.items()))
    print("Topic       Accuracy")
    print("--------------------")
    for k in dict1:
        ele=f"{k}   {dict1[k]}% "
        print(ele)
    Exit=input("Press Enter to go back to index: ")
    os.system('cls')
    return index()

def playerindex(playersname):
    pfname=f"{playersname}sco.csv"
    pfread=pd.read_csv(pfname)
    totalpoint_=pfread['Total Points'].sum()
    tpoints=round(totalpoint_,2)
    if tpoints>1000000:
        star = "7*"
        starpoint="You have reached maximum stars"
    elif tpoints>500000 and tpoints<1000000:
        star = "6*"
        starpoint=f"You are {round(1000000-tpoints,2)} away from your 7th star."
    elif tpoints>100000 and tpoints<500000:
        star = "5*"
        starpoint=f"You are {round(500000-tpoints,2)} away from your 6th star."
    elif tpoints>50000 and tpoints<100000:
        star = "4*"
        starpoint=f"You are {round(100000-tpoints,2)} away from your 5th star."
    elif tpoints>25000 and tpoints<50000:
        star = "3*"
        starpoint=f"You are {round(50000-tpoints,2)} away from your 4th star."
    elif tpoints>10000 and tpoints<25000:
        star = "2*"
        starpoint=f"You are {round(25000-tpoints,2)} away from your 3rd star."
    elif tpoints>5000 and tpoints<10000:
        star = "1*"
        starpoint=f"You are {round(10000-tpoints,2)} away from your 2nd star."
    else:
        star = "0*"
        starpoint=f"You are {round(5000-tpoints,2)} away from your 1st star."
    newstar=f"Star:{star}"
    file=f"{playersname}sco.csv"
    df=pd.read_csv(file)
    maxpoint=df['Total Points'].max()
    lz=namefunc()
    length=len(lz)
    size=length-1
    leaderdic={}
    l=[]
    for i in range(size):
        fname=f"{lz[i+1]}sco.csv"
        fread=pd.read_csv(fname)
        totalpoint=fread['Total Points'].sum()
        points=round(totalpoint,2)
        l.append(points)
        if points>1000000:
            leaderdic[f"{lz[i+1]}(7*)"]=points
        elif points>500000 and points<1000000:
            leaderdic[f"{lz[i+1]}(6*)"]=points
        elif points>100000 and points<500000:
            leaderdic[f"{lz[i+1]}(5*)"]=points
        elif points>50000 and points<100000:
            leaderdic[f"{lz[i+1]}(4*)"]=points
        elif points>25000 and points<50000:
            leaderdic[f"{lz[i+1]}(3*)"]=points
        elif points>10000 and points<25000:
            leaderdic[f"{lz[i+1]}(2*)"]=points
        elif points>5000 and points<10000:
            leaderdic[f"{lz[i+1]}(1*)"]=points
        else:
            leaderdic[f"{lz[i+1]}(0*)"]=points
    dict=OrderedDict(sorted(leaderdic.items()))
    for k,j in leaderdic.items():
        if k==f"{playersname}({star})":
            b=j
    x=max(l)
    if x!=b:
        lead=x
    else:
        lead=10000000000
    print(f"                  Welcome {playersname}!                {newstar}")
    print("-------------------------------------------------------------------")
    print(f"({starpoint})")
    print("-------------------------------------------------------------------\n")
    print("1. Play Quiz\n2. Leader board\n3. Check your own Scores\n4. Scoreboard\n5. Delete Account\n6. Back to Main Index\n7. Exit")
    print("-------------------------------------------------------------------\n")
    choiceenter=int(input("Enter your choice: "))
    os.system('cls')
    if choiceenter==1:
        os.system('cls')
        print(play(playersname,newstar,maxpoint,lead,star))
    elif choiceenter==2:
        os.system('cls')
        print(leaderboard(2,playersname))
    elif choiceenter==3:
        os.system('cls')
        print(playerscore(2,playersname))
    elif choiceenter==4:
        os.system('cls')
        print(scoreboard(2,playersname))
    elif choiceenter==5:
        os.system('cls')
        print(removeacc(playersname))
    elif choiceenter==6:
        os.system('cls')
        print(playindex())
    elif choiceenter==7:
        os.system('cls')
        print(exit())

def playindex():
    print("-------------------------------------------------------------------\n")
    print("1. Login for existing User\n2. Signup for new User\n3. Exit")
    print("-------------------------------------------------------------------\n")
    enchoice=int(input("Enter Your Choice: "))
    if enchoice==1:
        print(playername())
    elif enchoice==2:
        print(adduser())
    elif enchoice==3:
        print(exit())

def scoreboard(entrysb,name2):
    print("____________________________________________________________________________\n")
    fr=open("Scoreboard.txt","r")
    filereader=fr.read()
    print(filereader)
    print("____________________________________________________________________________\n")
    if entrysb==1:
        p=input("Press Enter to go back to index: ")
        os.system('cls')
        return index()
    elif entrysb==2:
        p=input("Press Enter to go back to index: ")
        os.system('cls')
        return playerindex(name2)

def checkque():
    print(topic_index)
    print("-------------------------------------------------------------------\n")
    choicein=int(input("Enter your choice: "))
    print("-------------------------------------------------------------------\n")
    elem=choicein-1
    df=pd.read_csv(file_name[elem])
    dp=df.set_index('Index')
    dp1=dp.iloc[0:10]
    dp2=dp.iloc[10:20]
    dp3=dp.iloc[20:30]
    dp4=dp.iloc[30:40]
    dp5=dp.iloc[40:50]
    dp6=dp.iloc[50:60]
    dp7=dp.iloc[60:70]
    dp8=dp.iloc[70:80]
    dp9=dp.iloc[80:90]
    dp10=dp.iloc[90:]
    print(dp1,"\n",dp2,"\n",dp3,"\n",dp4,"\n",dp5,"\n",dp6,"\n",dp7,"\n",dp8,"\n",dp9,"\n",dp10,"\n")
    return index()

def changque():
    print(topic_index)
    print("-------------------------------------------------------------------\n")
    inchoice=int(input("Enter your choice: "))
    print("-------------------------------------------------------------------\n")
    listele=inchoice-1
    quetochange(file_name[listele])

def question_add(topicna):
    print("-------------------------------------------------------------------\n")
    addedque=input("Enter new Question: ")
    addedopt1=input("Enter option 1: ")
    addedopt2=input("Enter option 2: ")
    addedopt3=input("Enter option 3: ")
    addedopt4=input("Enter option 4: ")
    addedanswer=int(input("Enter correct option: "))
    print("-------------------------------------------------------------------\n")
    filetopic=open(topicna)
    reader=csv.reader(filetopic)
    lent=len(list(reader))
    filetopic.close()
    with open(topicna,"a",newline="") as File:
        Writer=csv.writer(File)
        Writer.writerow([lent,addedque,addedopt1,addedopt2,addedopt3,addedopt4,addedanswer])
    File.close()
    os.system('cls')
    return index()

def addque():
    print(topic_index)
    print("-------------------------------------------------------------------\n")
    inputchoice=int(input("Enter your choice: "))
    print("-------------------------------------------------------------------\n")
    elemen=inputchoice-1
    os.system('cls')
    question_add(file_name[elemen])

def quetochange(filename):
    df=pd.read_csv(filename)
    dp=df.set_index('Index')
    dp1=dp.iloc[0:10]
    dp2=dp.iloc[10:20]
    dp3=dp.iloc[20:30]
    dp4=dp.iloc[30:40]
    dp5=dp.iloc[40:50]
    dp6=dp.iloc[50:60]
    dp7=dp.iloc[60:70]
    dp8=dp.iloc[70:80]
    dp9=dp.iloc[80:90]
    dp10=dp.iloc[90:]
    print(dp1,"\n",dp2,"\n",dp3,"\n",dp4,"\n",dp5,"\n",dp6,"\n",dp7,"\n",dp8,"\n",dp9,"\n",dp10,"\n")
    print("-------------------------------------------------------------------\n")
    questionnumber=int(input("Enter Number of Question you want to change: "))
    dp.loc[questionnumber, 'Question']=input("Enter new Question: ")
    dp.loc[questionnumber, 'A']=input("Enter Option 1: ")
    dp.loc[questionnumber, 'B']=input("Enter Option 2: ")
    dp.loc[questionnumber, 'C']=input("Enter Option 3: ")
    dp.loc[questionnumber, 'D']=input("Enter Option 4: ")
    dp.loc[questionnumber, 'answer']=input("Enter no. of correct option: ")
    print("-------------------------------------------------------------------\n")
    dp.to_csv(filename)
    os.system('cls')

def index():
    print("                           Welcome Sir/Madam!")
    print("____________________________________________________________________________\n")
    print("1. Check Score Card\n2. Change Questions\n3. Check Questions\n4. Add Question\n5. Leaderboard\n6. Check Indiviual Player Score\n7. Check topic accuracy\n8. Exit")
    print("____________________________________________________________________________\n")
    enterchoice=int(input("Please select one option: "))
    print("____________________________________________________________________________\n")
    if enterchoice==1:
        os.system('cls')
        print(scoreboard(1,"non"))
    elif enterchoice==2:
        os.system('cls')
        print(changque())
    elif enterchoice==3:
        os.system('cls')
        print(checkque())
    elif enterchoice==4:
        os.system('cls')
        print(addque())
    elif enterchoice==5:
        os.system('cls')
        print(leaderboard(1,"non"))
    elif enterchoice==6:
        os.system('cls')
        print(playerscore(1,"non"))
    elif enterchoice==7:
        os.system('cls')
        print(topicacc())
    elif enterchoice==8:
        os.system('cls')
        print(exit())
    else:
        os.system('cls')
        print("Incorrect Input")
        print("____________________________________________________________________________\n")
    return index()

def owner():
    password=stdiomask.getpass("Enter your Password: ")
    print("---------------------------------------------------------------------------\n")
    if password=="Guest123":
        os.system('cls')
        varo=index()
    else:
        os.system('cls')
        print("Wrong Password! Please Try again.")
        print("____________________________________________________________________________\n")
        varo=owner()
    return varo

def play(player_name,star1,maxpoi,lead,st):
    print(topic_index)
    print("-------------------------------------------------------------------\n")
    choice_entered=int(input("Enter your choice: "))
    print("-------------------------------------------------------------------\n")
    os.system('cls')
    print("-------------------------------------------------------------------")
    print("You will get 60 seconds for each question. \nAll the best!")
    print("-------------------------------------------------------------------\n")
    element_list=choice_entered-1
    file_=open(file_name[element_list])
    read_file=csv.reader(file_)
    lengt=len(list(read_file))
    size_=lengt-2
    initial=time.time()
    for i in range(1,11):
        y=random.randint(0,size_)
        question(y,file_name[element_list])     
    timeleft=time.time()-initial
    timeleftround=round(timeleft,2)
    sumc=0
    sumic=0
    for i in range(len(correct)):
        sumc=sumc+correct[i]
    for j in range(len(incorrert)):
        sumic=sumic+incorrert[j]
    correct.clear()
    incorrert.clear()
    timepoints=totaltime-timeleftround
    quepoints=(sumc*100)-(sumic*25)
    point=quepoints+timepoints

    x=f"{player_name}sco.csv"
    with open(x,"a",newline="") as Fil:
        Writer=csv.writer(Fil)
        Writer.writerow([quepoints,point,timeleftround,topic_name[element_list],sumc,sumic])
    Fil.close()
    namelen=len(player_name)
    namespa=(20-namelen)*" "
    quepointslen=len(str(quepoints))
    quepointsspa=(15-quepointslen)*" "
    pointlen=len(str(point))
    pointspa=(15-pointlen)*" "
    timelen=len(str(timeleftround))
    timespace=(10-timelen)*" "
    wrt=player_name+namespa+str(quepoints)+quepointsspa+str(point)+pointspa+str(timeleftround)+timespace+topic_name[element_list]+"\n"
    filesco=open("Scoreboard.txt","a")
    filesco.write(wrt)
    filesco.close()
    pfname=f"{player_name}sco.csv"
    pfread=pd.read_csv(pfname)
    totalpoint_=pfread['Total Points'].sum()
    tpoints=round(totalpoint_,2)
    if tpoints>1000000:
        star = "Star:7*"
    elif tpoints>500000 and tpoints<1000000:
        star = "Star:6*"
    elif tpoints>100000 and tpoints<500000:
        star = "Star:5*"
    elif tpoints>50000 and tpoints<100000:
        star = "Star:4*"
    elif tpoints>25000 and tpoints<50000:
        star = "Star:3*"
    elif tpoints>10000 and tpoints<25000:
        star = "Star:2*"
    elif tpoints>5000 and tpoints<10000:
        star = "Star:1*"
    else:
        star = "Star:0*"
    d1=namefunc()
    x=len(d1)
    leaderdic={}
    l=[]
    for i in range(x-1):
        fname=f"{d1[i+1]}sco.csv"
        fread=pd.read_csv(fname)
        totalpoint=fread['Total Points'].sum()
        points=round(totalpoint,2)
        l.append(points)
        if points>1000000:
            leaderdic[f"{d1[i+1]}(7*)"]=points
        elif points>500000 and points<1000000:
            leaderdic[f"{d1[i+1]}(6*)"]=points
        elif points>100000 and points<500000:
            leaderdic[f"{d1[i+1]}(5*)"]=points
        elif points>50000 and points<100000:
            leaderdic[f"{d1[i+1]}(4*)"]=points
        elif points>25000 and points<50000:
            leaderdic[f"{d1[i+1]}(3*)"]=points
        elif points>10000 and points<25000:
            leaderdic[f"{d1[i+1]}(2*)"]=points
        elif points>5000 and points<10000:
            leaderdic[f"{d1[i+1]}(1*)"]=points
        else:
            leaderdic[f"{d1[i+1]}(0*)"]=points
    dict=OrderedDict(sorted(leaderdic.items()))
    a=0
    for k,j in leaderdic.items():
        if k==f"{player_name}({st})":
            a=j
    for i in range(x-1):
        if d1[i+1]==player_name:  
            E2=Emailfunc()
            emailId=E2[i+1] 
    if star!=star1:
        SendEmail(f"You are upgraded from {star1} to {star}", emailId)
    if maxpoi<point:
        SendEmail(f"You have beaten your high score!\nYour new high score is {point} points!", emailId)
    if lead<a:
        SendEmail(f"You are on top of the leader board with a score of {a}", emailId)


    print(f"You Completed Quiz in {timeleftround} secs\nYou Got {timepoints} points Extra\nCorrect: {sumc}\nIncorrect: {sumic}\nQuestion Points: {quepoints}\nTotal Points: {point}")
    print("-------------------------------------------------------------------\n")
    return playerindex(player_name)

def pmain():
    print("\n_________________________Welcome To Quizzical!__________________________\n")
    print("1. Player \n2. Owner\n3. Exit")
    print("-------------------------------------------------------------------\n")
    choicetype=int(input("Select One: "))
    if choicetype==1:
        os.system('cls') 
        print(playindex())
    elif choicetype==2: 
        os.system('cls')
        print(owner())
    elif choicetype==3:
        exit()


print(pmain())
