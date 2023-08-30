import requests
import json
import csv

# 시즌 리스트
seasons = {'2022' : 20934,    
            '2021' : 19793,
            '2020' : 18685,
            '2019' : 17590,
            '2018' : 16368,
            '2017' : 15151,
            '2016' : 13796,
            '2015' : 12496,
            '2014' : 9155
            }

# json 데이터 받아오기
def crawl_offensive(season):
    url = f"https://1xbet.whoscored.com/StatisticsFeed/1/GetPlayerStatistics?category=summary&subcategory=offensive&statsAccumulationType=0&isCurrent=true&playerId=&teamIds=&matchId=&stageId={season}&tournamentOptions=2&sortBy=Rating&sortAscending=&age=&ageComparisonType=&appearances=&appearancesComparisonType=&field=Overall&nationality=&positionOptions=&timeOfTheGameEnd=&timeOfTheGameStart=&isMinApp=false&page=&includeZeroValues=&numberOfPlayersToPick=600"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    return json_data

# 시즌 넘버 돌며 크롤링
for key in seasons.keys():
    # json data에서 선수 테이블 받아오기
    data = crawl_offensive(seasons[key])['playerTableStats']
    player = []
    season_table = [['Name', 'Team', 'Age', 'Position', 'Apps', 'Mins', 'Goals', 'Assists', 'SpG', 
                    'KeyP', 'Drb', 'Fouled', 'Off', 'Disp', 'UnsTch', 'Rating']]

    # 필요한 feature 가져오기
    for i in range(len(data)):
        row = data[i]
        name = row['name']
        team = row['teamName']
        age = row['age']
        position = row['positionText']
        apps = row['apps']
        mins = row['minsPlayed']
        goal = row['goal']
        assists = row['assistTotal']
        shotsPerGame = row['shotsPerGame']
        keyPasses = row['keyPassPerGame']
        dribbleWonPerGame = row['dribbleWonPerGame']
        fouledPerGame =  row['foulGivenPerGame']
        offsidePerGame = row['offsideGivenPerGame']
        disPerGame = row['dispossessedPerGame']
        turnoverPerGame = row['turnoverPerGame']
        rating = row['rating']
        player = [name, team, age, position, apps, mins, goal, assists, shotsPerGame, keyPasses, 
                    dribbleWonPerGame, fouledPerGame, offsidePerGame, disPerGame, turnoverPerGame, rating]
        season_table.append(player)

    with open(f'data/1xbet_offensive_{key}.csv', 'w', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(season_table)





