import requests
from urllib.parse import urlencode

def get_summoner_info(riot_id, api_key):
    game_name, tag_line = riot_id.split("#")
    api_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    params = {
        "api_key": api_key
    }

    response = requests.get(api_url, urlencode(params))
    # response.raise_for_status()

    return response.json()


def get_match_ids(summoner_info, match_amount, api_key):
    api_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoner_info['puuid']}/ids"
    params = {
        "api_key": api_key,
        "count": match_amount,
    }

    response = requests.get(api_url, urlencode(params))
    # response.raise_for_status()

    return response.json()


def get_match_infos(match_ids, api_key):
    match_infos = []

    for match_id in match_ids:
        api_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
        params = {
            "api_key": api_key
        }

        response = requests.get(api_url, urlencode(params))

        try:
            response.raise_for_status()
            match_infos.append(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Issue getting summoner match info from API: {e}")
    
    return match_infos


def get_match_timelines(match_ids, api_key):
    match_timelines = []

    for match_id in match_ids:
        api_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
        params = {
            "api_key": api_key
        }

        response = requests.get(api_url, urlencode(params))

        try:
            response.raise_for_status()
            match_timelines.append(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Issue getting summoner match info from API: {e}")
    
    return match_timelines
