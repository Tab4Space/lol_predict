import requests, json, sqlite3
import time, os, sys
import csv, pandas


try:
    conn = sqlite3.connect("user_ID_Nick1.db")
    conn.isolation_level = None
    cur = conn.cursor()
    print("Success connect DB File...")
except Exception as e:
    print(e)
    sys.exit()



def getRecentGames(region, summonerID, APIKEY):
    url = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.3/game/by-summoner/" + summonerID + "/recent?api_key=" + APIKEY
    responseJSON = requests.get(url).json()
    try:
        if len(responseJSON['games']) < 10:
            return
        else:
            for i in range(0, 10):
                """
                gameAttr=[gameMode, gameType, subType]

                """
                # i번째 게임의 타입 확인
                gameAttr = []
                checkGameAttr(responseJSON['games'][i], gameAttr)

                if gameAttr == ['CLASSIC', 'MATCHED_GAME', 'RANKED_FLEX_SR']:
                    continue

                elif gameAttr == ['CLASSIC', 'MATCHED_GAME', 'NORMAL']:
                    continue

                elif gameAttr == ['ARAM', 'MATCHED_GAME', 'ARAM_UNRANKED_5x5']:
                    getRankGameInfo(responseJSON, i)
                else:
                    continue
    except Exception as e:
        print(summonerID, e)



def checkGameAttr(jsonData, gameAttr):
    gameAttr.append(jsonData['gameMode'])
    gameAttr.append(jsonData['gameType'])
    gameAttr.append(jsonData['subType'])



def getRankGameInfo(responseJSON, i):
    gameResult = ""
    team100, team200 = [], []
    myTeam, enemyTeam = 0, 0

    gameID = responseJSON['games'][i]['gameId']

    if responseJSON['games'][i]['teamId'] == 100:
        myTeam, enemyTeam = 100, 200
    else:
        myTeam, enemyTeam = 200, 100

    if responseJSON['games'][i]['teamId'] == 100:
        team100.append(responseJSON['games'][i]['championId'])
    else:
        team200.append(responseJSON['games'][i]['championId'])

    for j in range(0, len(responseJSON['games'][i]['fellowPlayers'])):
        if responseJSON['games'][i]['fellowPlayers'][j]['teamId'] == 100:
            team100.append(responseJSON['games'][i]['fellowPlayers'][j]['championId'])
        else:
            team200.append(responseJSON['games'][i]['fellowPlayers'][j]['championId'])

    if myTeam == responseJSON['games'][i]['stats']['team']:
        if responseJSON['games'][i]['stats']['win']:
            gameResult = "W"

        else:
            gameResult = "L"

    makeCSV(gameID, myTeam, team100, team200, gameResult)



def makeCSV(gameID, myTeam, team100, team200, gameResult):
    if myTeam == 100:
        team200.append(gameResult)
        csvWrite.writerow(team100+team200)
    else:
        team100.append(gameResult)
        csvWrite.writerow(team200+team100)


def makeDB(gameID, myTeam, team100,team200, gameResult):
    pass



if __name__ == '__main__':
    summonerRegion = 'kr'
    APIKEY = 'INPUT YOUR RIOT GAMES API KEY'
    count = 0


    cur.execute("SELECT summonerId from User")
    rows = cur.fetchall()

    fcsv = open("rankData.csv", 'wb')
    csvWrite = csv.writer(fcsv, dialect='excel')

    for row in rows:
        summonerId = row[0]
        getRecentGames(summonerRegion, summonerId, APIKEY)
        time.sleep(1)

    sys.exit()