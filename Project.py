import logging
import requests
import time
from aiogram import Bot, Dispatcher, executor, types                                                    

API_TOKEN = '5068695480:AAGFjq07b11NkmxMOSRNCZBhCv5_gmiU4Bs'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


url="https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?lang=en&latest=true"
dup = ""
Data = requests.get(url).json()

def batsmen(data,c):
    
    bat = data['supportInfo']['liveSummary']['batsmen']
    name = bat[0]['player']['longName']
    
    if c['isFour'] :
        score= "FOUR " + " From  " + str(name)
        #print(score)
        #time.sleep(15)
        return score

    if c['isSix'] :
        score= "SIX " + " From " + str(name)
        #print(score)
        #time.sleep(15)
        return score

def bowler(data,w):
    bowl = data['supportInfo']['liveSummary']['bowlers']
    name = bowl[0]['player']['longName']
    wicket = str(name) + " Took the Wicket of " + str(data['supportInfo']['liveSummary']['batsmen'][0]['player']['longName'])
    #print(wicket)
    time.sleep(15)
    return wicket

def bover(data):
    bat=[]
    for batsmen in data['supportInfo']['liveSummary']['batsmen']:
        bat.append(batsmen['player']['longName']+'     '+str(batsmen['runs'])+'('+str(batsmen['balls'])+')')
    return bat

def bwer(data):
    a=[]
    for bowler in data['supportInfo']['liveSummary']['bowlers']:
        a.append(bowler['player']['longName']+'          '+str(bowler['overs'])+'-'+str(bowler['maidens'])+'-'+str(bowler['conceded'])+'-'+str(bowler['wickets']))
    return a

def over(data,w,c):
    batters=bover(data)
    bowlers=bwer(data)
    ever = int(c['oversActual']+1)
    eo = "End of an Over "+str(ever).strip(".6") + "\n" + "Score card"
    while True:
        try:
            output= eo + "\n"+ str(c['over']['team']['abbreviation'])+' - '+str(c['over']['totalRuns'])+'/'+ str(c['over']['totalWickets']) + ' \n' + str(c['over']['overRuns'])+' Runs & '+ str(c['over']['overWickets'])+' Wickets'+'\n'+'batting=> '+' || '.join(batters) +'\n'+ 'bowling=> '+' || '.join(bowlers) 
            print(output)
        except TypeError:
            print("HI")
            time.sleep(5)
            print("HELLO")
        else: 
            print(output)
            break   
    return output
        
           

live = [[match['scribeId'], match['series']['objectId'], match['series']['longName'],match['teams'][0]['team']['longName'],match['teams'][1]['team']['longName']] for match in Data['matches'] if match['status'] == "Live" ]
#print(live)
selected_live = ""
for i,live_match in enumerate(live):
            selected_live += f"Live {i+1} ->> "+str(live_match[2])+'\n' 
            #print(selected_live)
            


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    
    if live == []:
        await message.reply("No Live Matches".upper())
    
    else:
        await message.reply(selected_live)
        

            
        
@dp.message_handler()
async def echo(message: types.Message):

            selected_match = message.text
            #selected_match =input("Select Your Live match: ").lower()
            #await message.answer(selected_match)

            user_input = selected_match.strip("live ") or selected_match.strip("live") or selected_match
            user_input = int(user_input)
            current_match = live[user_input-1]
            m = "\n" + str(live[user_input-1][2]) + "\n" + str(live[user_input-1][3]) + " VS " + str(live[user_input-1][4]) + "\n" 
            #vs = str(live[0][3]) + " VS " + str(live[0][4])
            await bot.send_message(-644768316,m)
            dup=""
            d = ""
            while True:
                url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?&seriesId={live[user_input-1][1]}&matchId={live[user_input-1][0]}&latest=true"
                
                data = requests.get(url).json()
                #print(data)
                
                
                #batsmen(data)
                
                c = data['recentBallCommentary']['ballComments'][0]    
                a = c['oversActual'],c['title'],c['totalRuns']
                s = c['isFour'] or c['isSix'] 
                w =  c['isWicket']
                #print(sets)
                if c:
                    com= c['commentTextItems']

                    
                    
                    if s:
                        a = c['oversActual'],c['title'],c['totalRuns']
                        
                        #NC = "----------No Commentary Available----------"
                        if com != None:
                            NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nRuns : " + str(batsmen(data,c)) + "\nCommentary: " + str(c['commentTextItems'][0]['html']).capitalize()
                            if dup == NCM:
                                time.sleep(5)
                            else:              
                                await bot.send_message(-644768316,NCM)
                                dup = NCM 
                            
                        else:
                            NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nRuns : " + str(batsmen(data,c))
                            if dup == NCM:
                                time.sleep(5)
                            else:              
                                await bot.send_message(-644768316,NCM)
                                dup = NCM 

                        if str(c['oversActual']).find('.6')!=-1:
                            #time.sleep(5)
                            o = over(data,w,c)
                            if d == o:
                                time.sleep(3)
                            else:              
                                await bot.send_message(-644768316,o)
                                d = o 

                    elif w:
                        a = c['oversActual'],c['title'],c['totalRuns']
                        #NC = "----------No Commentary Available----------"
                        if com != None:
                            NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nWicket : " + bowler(data,w) + "\nCommentary: " + str(com[0]['html']).capitalize()
                            #NC = "Commentary: ",com[0]['html'] 
                            if dup == NCM:
                                time.sleep(5)
                            else:              
                                await bot.send_message(-644768316,NCM)
                                dup = NCM                       
                                   
                        else:
                            NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nWicket : " + bowler(data,w)
                            if dup == NCM:
                                time.sleep(5)
                            else:              
                                await bot.send_message(-644768316,NCM)
                                dup = NCM 
                        
                        if str(c['oversActual']).find('.6')!=-1:
                            #time.sleep(5)
                            o = over(data,w,c)
                            if d == o:
                                time.sleep(3)
                            else:              
                                await bot.send_message(-644768316,o)
                                d = o 
                            

                    else:
                        a = c['oversActual'],c['title'],c['totalRuns']
                        NC = "----------No Commentary Available----------"
                        if com!=None:
                            NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nRuns : " + str(a[2]) + "\nCommentary: " + str(c['commentTextItems'][0]['html']).capitalize()
                            if dup == NCM:
                                time.sleep(5)
                            else:              
                                await bot.send_message(-644768316,NCM)
                                dup = NCM 
                            
                        else:
                            NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nRuns : " + str(a[2])
                            if dup == NCM:
                                time.sleep(5)
                            else:              
                                await bot.send_message(-644768316,NCM)
                                dup = NCM 

                        if str(c['oversActual']).find('.6')!=-1:
                            #time.sleep(5)
                            o = over(data,w,c)
                            if d == o:
                                time.sleep(3)
                            else:              
                                await bot.send_message(-644768316,o)
                                d = o 

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
