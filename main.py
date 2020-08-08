import requests
import json
from bs4 import BeautifulSoup

def print_player(player):
    print(player['champion'] + ' (' + player['name'] + ')')
    print(player['items'])
    print('')


def print_game(game):
    print('##########')
    print(game['blue_team_name'] + ' vs ' + game['red_team_name'])
    print('##########')
    print('')

    for p in game['players'][:5]:
        print_player(p)

    print('----------')
    print('')

    for p in game['players'][5:]:
        print_player(p)

    print('##########')
    print('')


def process_raw_player(p, pteam):
    player = {}

    pname = p.find('div', class_='sb-p-name').a.text
    pchampion = p.find('div', class_='sb-p-champion').find('span')['title']
    span = p.find('div', class_='sb-p-items').find_all('span')
    pitems = []
    for s in span:
        pitems.append(s['title'])

    player['name'] = pname
    player['champion'] = pchampion
    player['items'] = pitems
    player['team'] = pteam
    return player


def process_raw_game(raw_game):
    game = {}
    game['players'] = []

    game['blue_team_name'] = raw_game.find_all('th', class_='sb-teamname')[0].text
    game['red_team_name'] = raw_game.find_all('th', class_='sb-teamname')[1].text

    players = raw_game.find_all('div', class_='sb-p')
    #print(len(players))

    for p in players[:5]:
        game['players'].append(process_raw_player(p, 'blue'))
    for p in players[5:]:
        game['players'].append(process_raw_player(p, 'red'))
    return game


def query_item_count(games, name):
    count = 0
    for game in games:
        for player in game['players']:
            for item in player['items']:
                if item == name:
                    count += 1
    print(str(count) + ' ' + name)
    return count


def gather_data(games):
    for week_n in range(1, 14):
        for day_n in range(1, 7):
            url_suffix = ''
            if week_n > 1 or day_n > 1:
                url_suffix = '/Week_' + str(week_n)
                if day_n > 1:
                    url_suffix += '_(' + str(day_n) + ')'

            url = 'https://lol.gamepedia.com/LPL/2020_Season/Summer_Season/Scoreboards' + url_suffix
            page = requests.get(url)
            if page.status_code != 200:
                break #go to next week

            print('Found url: ' + url)

            soup = BeautifulSoup(page.content, 'html.parser')

            #print(soup.prettify())

            raw_games = soup.find_all('table', class_='sb')

            for raw_game in raw_games:
                games.append(process_raw_game(raw_game))

    print(str(len(games)) + ' games recorded')

    with open('lpl_summer_season_2020.txt', 'w') as file:
        file.write(json.dumps(games))


games = []

## UNCOMMENT THIS TO GATHER DATA
#gather_data(games)


## prints all games, not very useful
#for game in games:
    #print_game(game)


with open('lpl_summer_season_2020.txt', 'r') as json_file:
    games = json.load(json_file)

    print(str(len(games)) + ' games recorded')
    query_item_count(games, 'Morellonomicon')
    query_item_count(games, "Banshee's Veil")
    query_item_count(games, "Rabadon's Deathcap")
    query_item_count(games, "Void Staff")
    query_item_count(games, "Rylai's Crystal Scepter")
    query_item_count(games, "Luden's Echo")
    query_item_count(games, 'Blade of the Ruined King')
    query_item_count(games, 'Infinity Edge')
    query_item_count(games, "Death's Dance")
    query_item_count(games, "Trinity Force")
    query_item_count(games, "Spellbinder")
    query_item_count(games, "Mercury's Treads")
    query_item_count(games, "Ninja Tabi")
    query_item_count(games, "Berserker's Greaves")
    query_item_count(games, "Sorcerer's Shoes")
    query_item_count(games, "Boots of Swiftness")
    query_item_count(games, "Ionian Boots of Lucidity")
    query_item_count(games, "Boots of Mobility")
    query_item_count(games, "Boots of Speed")


