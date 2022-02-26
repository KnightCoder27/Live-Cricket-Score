import requests
import time

url="https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?lang=en&latest=true"

Data = requests.get(url).json()
'''
ALITER: W/O USING List COMPREHENSION
__________________________________________________________________________

for match in Data['matches']:
        if match['status'] == "Live":
            #print(match)
            alive = []
            live_match = alive.append(match['series']['longName'])
            for i in alive:
                print(f"Live {j} ->> ",i)
                j+1
______________________________________________________________________________ 
'''           

live = [[match['scribeId'], match['series']['objectId'], match['series']['longName']] for match in Data['matches'] if match['status'] == "Live" ]
#print(live)
if live == []:
    print("No Live Matches".upper())
    
else:
    for i,live_match in enumerate(live):
        selected_live = f"Live {i+1} ->> "+str(live_match[2])+'\n'
        print(selected_live)
        
    selected_match =input("Select Your Live match: ").lower()

    user_input = selected_match.strip("live ") or selected_match.strip("live") or selected_match
    user_input = int(user_input)
    #print(user_input)



    while True:
        current_match = live[user_input-1]
        #print(current_match)
        url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?&seriesId={live[user_input-1][1]}&matchId={live[user_input-1][0]}&latest=true"
        #print(url)
        data = requests.get(url).json()
        #print(data)
        

        c = data['recentBallCommentary']['ballComments'][0]
        #print(c['oversActual'],c['title'],c['totalRuns'])
        #o = data['over']
        #print(o)
        if c:
            com= c['commentTextItems']
            #print(com)
            if com == None:       
                a = c['oversActual'],c['title'],c['totalRuns']
                print("----------No Commentary Available----------")
                print("Over: ",a[0])
                print("Title: ",a[1])
                print("Runs: ",a[2])
                time.sleep(15)
                '\n'
                        
                #print("\10n END OF OVER \10n")

            else:    
                a = c['oversActual'],c['title'],c['totalRuns']
                print("---------Commentary Available-----------")                         
                print("Over: ",a[0])
                print("Title: ",a[1])
                print("Runs: ",a[2])
                print("Commentary: ",com[0]['html'])
                time.sleep(15)
                '\n'









