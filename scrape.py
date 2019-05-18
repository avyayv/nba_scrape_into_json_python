import requests
import time
import help
import json

def obj_dict(obj):
    return obj.__dict__

older_seasons = ["1996-97", "1997-98", "1998-99", "1999-00", "2000-01", "2001-02",
"2002-03", "2003-04", "2004-05", "2005-06", "2006-07", "2007-08", "2008-09",
"2009-10", "2010-11", "2010-11", "2011-12", "2012-13", "2013-14", "2014-15",
"2015-16", "2016-17", "2017-18", "2018-19"]

draft_combine_seasons = ["2002-03", "2003-04", "2004-05", "2005-06", "2006-07", "2007-08", "2008-09",
"2009-10", "2010-11", "2010-11", "2011-12", "2012-13", "2013-14", "2014-15",
"2015-16", "2016-17", "2017-18", "2018-19", "2019-20"]

newer_seasons = ["2013-14", "2014-15", "2015-16", "2016-17", "2017-18", "2018-19"]

season_types = ["Playoffs", "Regular+Season"]

stats = ["Drives", "Defense", "CatchShoot", "Passing", "SpeedDistance", "Rebounding", "Possessions", "PullUpShot", "ElbowTouch", "PostTouch", "PaintTouch", "Efficiency"]
distance_from_closest_defender = ["6%2B+Feet+-+Wide+Open", "4-6+Feet+-+Open", "2-4+Feet+-+Tight", "0-2+Feet+-+Very+Tight"]
touch_times = ["Touch+<+2+Seconds", "Touch+2-6+Seconds", "Touch%206%2B%20Seconds"]
dribbles_options = ["0%20Dribbles", "1%20Dribble", "2%20Dribbles", "3-6%20Dribbles", "7%2B%20Dribbles"]
shot_clock_options = ["24-22", "22-18%20Very%20Early", "18-15%20Early", "15-7%20Average", "7-4%20Late", "4-0%20Very%20Late", "ShotClock%20Off"]
overall_options = ["Catch%20and%20Shoot", "Pullups", "Less%20Than%2010%20ft", "Overall"]
basic_options = ["Base", "Advanced", "Misc", "Scoring", "Usage"]

placeholder1_options = ["OpponentByDistance"]
placeholder2_options = ["BaseStats"]
placeholder3_options = ["DraftCombine"]


tracking_url = "https://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&PlayerExperience=&PlayerOrTeam=Player&PlayerPosition=&PtMeasureType=%s&SeasonSegment=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=&Season=%s&SeasonType=%s"
offense_distance_url = "https://stats.nba.com/stats/leaguedashplayerptshot?CloseDefDistRange=%s&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange=&GameScope=&GameSegment=&GeneralRange=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&SeasonSegment=&ShotClockRange=&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange=&VsConference=&VsDivision=&Weight=&Season=%s&SeasonType=%s"
touch_time_url = "https://stats.nba.com/stats/leaguedashplayerptshot?CloseDefDistRange=&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange=&GameScope=&GameSegment=&GeneralRange=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&SeasonSegment=&ShotClockRange=&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange=%s&VsConference=&VsDivision=&Weight=&Season=%s&SeasonType=%s"
dribbles_url = "https://stats.nba.com/stats/leaguedashplayerptshot?CloseDefDistRange=&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange=%s&GameScope=&GameSegment=&GeneralRange=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&SeasonSegment=&ShotClockRange=&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange=&VsConference=&VsDivision=&Weight=&Season=%s&SeasonType=%s"
shot_clock_url = "https://stats.nba.com/stats/leaguedashplayerptshot?CloseDefDistRange=&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange=&GameScope=&GameSegment=&GeneralRange=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&SeasonSegment=&ShotClockRange=%s&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange=&VsConference=&VsDivision=&Weight=&Season=%s&SeasonType=%s"
overall_shooting_url = "https://stats.nba.com/stats/leaguedashplayerptshot?CloseDefDistRange=&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange=&GameScope=&GameSegment=&GeneralRange=Overall&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&SeasonSegment=&ShotClockRange=&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange=&VsConference=&VsDivision=&Weight=&Season=%s&SeasonType=%s"
basic_stats_url = "https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=%s&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=%s&SeasonType=%s&SeasonSegment=&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight="
opponent_stats_url = "https://stats.nba.com/stats/leaguedashplayershotlocations?College=&Conference=&Country=&DateFrom=&DateTo=&DistanceRange=5ft+Range&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Opponent&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&cool=%s&Season=%s&SeasonType=%s&SeasonSegment=&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
bio_url = "https://stats.nba.com/stats/leaguedashplayerbiostats?College=&Conference=&Country=&DateFrom=&placeholderOptions=%s&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&Season=%s&SeasonType=%s&SeasonSegment=&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
draft_combine_url = "https://stats.nba.com/stats/draftcombineplayeranthro?LeagueID=00&combine=%s&SeasonYear=%s&SeasonType=%s"

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

def scrape(seasons, stats_array, variable_url, num1, num2):
    countit = 0
    for season_type in season_types:
        for season in seasons:
            for stat in stats_array:
                try:
                    countit += 1
                    open_this = variable_url % (stat, season, season_type)
                    json_data = requests.get(open_this, headers=headers).json()

                    if isinstance(json_data["resultSets"], list):
                        headers_for_this_one = json_data["resultSets"][0]["headers"]
                        rowSets = json_data["resultSets"][0]["rowSet"]
                    else:
                        headers_for_this_one = json_data["resultSets"]["headers"][0]["columnNames"]
                        rowSets = json_data["resultSets"]["rowSet"]

                    for rowSet in rowSets:
                        player = help.find_player(rowSet[num1], rowSet[num2])
                        print(player.name)
                        if (stat + ' ' + season_type) in player.nice_dict:
                            player.nice_dict[stat + ' ' + season_type].append(help.get_dict(headers_for_this_one, rowSet, season))
                        else:
                            player.nice_dict[stat + ' ' + season_type] = [help.get_dict(headers_for_this_one, rowSet, season)]

                    file = open('51719research.json', 'w')
                    file.write(json.dumps(help.players, default=obj_dict))
                    print(countit, len(stats_array)*len(seasons)*2, )
                    time.sleep(1)
                except (json.decoder.JSONDecodeError):
                    print('hey')

scrape(newer_seasons, distance_from_closest_defender, offense_distance_url, 0, 1)
scrape(newer_seasons, stats, tracking_url, 0, 1)
scrape(newer_seasons, touch_times, touch_time_url, 0, 1)
scrape(newer_seasons, dribbles_options, dribbles_url, 0, 1)
scrape(newer_seasons, shot_clock_options, shot_clock_url, 0, 1)
scrape(older_seasons, basic_options, basic_stats_url, 0, 1)
scrape(older_seasons, placeholder1_options, opponent_stats_url, 0, 1)
scrape(older_seasons, placeholder2_options, bio_url, 0, 1)
scrape(draft_combine_seasons, placeholder3_options, draft_combine_url, 1, 4)
