import praw
import config
import SubList
import re

AuthRight = SubList.AuthRight
RightUnity = SubList.RightUnity
LibRight = SubList.LibRight
AuthLeft = SubList.AuthLeft
LeftUnity = SubList.LeftUnity
LibLeft = SubList.LibLeft
AuthUnity = SubList.AuthUnity
LibUnity = SubList.LibUnity
Centrist = SubList.Centrist

def bot_login():
    print("Logging in")
    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "PolCompBot v0.1")
    print("Connection accepted...")
    return r    

def run_bot(r):
    for message in r.inbox.unread(limit=None):
        subject = message.subject.lower()
        if subject == 'username mention' and isinstance(message, praw.models.Comment):
            print("found a mention")
            
            #Do program and assign return values
            bod = message.body
            bod = bod.lower()
            secbod = bod.replace("u/polcompbot", "")
            match = re.search(r'u/[\w\.-]+', secbod)
            if match!=None:
                thirbod = match.group(0)
                fobod = thirbod.partition("u/")[2]
                target = r.redditor(fobod)
            else:
                target = message.parent().author


            imp = program(target)
            subs = imp[0]
            AuthLib = imp[1]
            LeftRight = imp[2]
            TotalScore = imp[3]

            #Calculate scores
            Ideology = ""
            if TotalScore !=0:
                ALScore = AuthLib/TotalScore
                LRScore = LeftRight/TotalScore
            
            print("score calcs done")
            if abs(ALScore)>3:
                if ALScore>3:
                    Ideology = "Auth"
                elif ALScore < -3:
                    Ideology = "Lib"
            if abs(LRScore)>3:
                if LRScore>3:
                    Ideology = Ideology+"Right"
                elif LRScore<-3:
                    Ideology = Ideology+"Left"
            if len(Ideology)<=6:
                if Ideology == "":
                    Ideology = "Centrist"
                else:
                    Ideology = Ideology+"Unity"
            if TotalScore == 0:
                Ideology = "Ape political"

            LeansMSG = "The user /u/"+target.name+" has an Auth/Lib score of **" + str(ALScore)+"** and a Right/Left score of **" + str(LRScore) +"**. This would make their quadrant **"+Ideology+"** \n\n"
            print("Leans calculations complete")
            #Table Builder
            Table = "Subreddit|Comment Karma|Quadrant\n:--|:--|:--|"
            print("Table Start Complete")
            for x in range(len(subs)):
                SubName = list(subs.keys())[x]
                
                #Quad name
                Quad = ""
                if SubName in AuthRight:
                    Quad = "AuthRight"
                if SubName in RightUnity:
                    Quad = "RightUnity"
                if SubName in LibRight:
                    Quad = "LibRight"
                if SubName in AuthLeft:
                    Quad = "AuthLeft"
                if SubName in LeftUnity:
                    Quad = "LeftUnity"
                if SubName in LibLeft:
                    Quad = "LibLeft"
                if SubName in AuthUnity:
                    Quad = "AuthUnity"
                if SubName in LibUnity:
                    Quad = "LibUnity"
                if SubName in Centrist:
                    Quad = "Centrist"
            

                Table = Table+"\n"+SubName+"|"+str(subs[SubName])+"|"+Quad
            print("Table Full Complete")
            
            GoodBye = "\n\n\nThank you for using PolCompBot! If you have any questions, comments or concerns, please direct your attention to the pinned messages on my profile. Running my server costs money, so if you'd be so kind, please consider donating some Bitcoin to the address: bc1qxdtt8gl6z8y6fvnvk824hmgvmyzj8s6zh5dm32"
            FinalMSG = LeansMSG+Table+GoodBye
            message.reply(FinalMSG)
            message.mark_read()

def program(user):
    subs = {}
    AuthLib = 0
    LeftRight = 0
    TotalScore = 0
    def DictBuilder(sub, TheList):
        subs
        if sub in TheList:
            if sub not in subs:
                subs[sub] = 0
            subs[sub]+=comment.score
            print(sub+":"+str(subs[sub]))

    for comment in r.redditor(user.name).comments.new(limit=1000):
        sub = comment.subreddit.display_name
        sub = sub.lower()
        DictBuilder(sub, AuthRight)  
        DictBuilder(sub, RightUnity)   
        DictBuilder(sub, LibRight)
        DictBuilder(sub, AuthLeft)
        DictBuilder(sub, LeftUnity)   
        DictBuilder(sub, LibLeft) 
        DictBuilder(sub, AuthUnity)
        DictBuilder(sub, LibUnity)     
        DictBuilder(sub, Centrist)  
        if sub in AuthRight:
            AuthLib += comment.score*10
            LeftRight += comment.score*10
            TotalScore += abs(comment.score)
        if sub in RightUnity:
            AuthLib += comment.score*0
            LeftRight += comment.score*10
            TotalScore += abs(comment.score)
        if sub in LibRight:
            AuthLib += comment.score*-10
            LeftRight += comment.score*10
            TotalScore += abs(comment.score)
        if sub in AuthLeft:
            AuthLib += comment.score*10
            LeftRight += comment.score*-10
            TotalScore += abs(comment.score)
        if sub in LeftUnity:
            AuthLib += comment.score*0
            LeftRight += comment.score*-10
            TotalScore += abs(comment.score)
        if sub in LibLeft:
            AuthLib += comment.score*-10
            LeftRight += comment.score*-10
            TotalScore += abs(comment.score)
        if sub in AuthUnity:
            AuthLib += comment.score*10
            LeftRight += comment.score*0
            TotalScore += abs(comment.score)
        if sub in LibUnity:
            AuthLib += comment.score*-10
            LeftRight += comment.score*0
            TotalScore += abs(comment.score)
        if sub in Centrist:
            AuthLib += comment.score*0
            LeftRight += comment.score*0
            TotalScore += abs(comment.score)
            
    print("Dict Build Complete") 
    return subs, AuthLib, LeftRight, TotalScore 



r = bot_login()

while True:
    run_bot(r)


