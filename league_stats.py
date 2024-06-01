from riot_api_funcs import get_summoner_info, get_match_ids, get_match_infos, get_match_timelines
from parse_funcs import parse_infos, parse_timelines
from plot_funcs import plot_timelines, plot_infos

NAME = "Name#TAGLINE"
API_KEY = "YOUR_API_KEY"
MATCH_AMOUNT = 5

if __name__ == "__main__":
    summoner_info = get_summoner_info(NAME, API_KEY)  # try... except
    assert "status" not in summoner_info, "API rate limit exceeded, please wait."

    match_ids = get_match_ids(summoner_info, MATCH_AMOUNT, API_KEY)
    assert "status" not in match_ids, "API rate limit exceeded, please wait."

    match_infos = get_match_infos(match_ids, API_KEY)
    assert match_infos != [], "API rate limit exceeded, please wait."

    match_timelines = get_match_timelines(match_ids, API_KEY)
    assert match_timelines != [], "API rate limit exceeded, please wait."

    infos = parse_infos(match_infos)
    stats = parse_timelines(match_timelines)

    while True:
        try:
            loaded_games = min(len(match_infos), len(match_timelines))
            game_index = int(input(f"Game index (max: {loaded_games}):\n")) - 1
            assert game_index < loaded_games, "Invalid game entered."

            info_type = int(input("Choose a type of information:\n1: Info\n2: Timeline\n"))
            assert info_type in (1, 2), "Invalid type of information entered."

            formatted_players = "\n".join([f"{i}: {name} ({champ})" for i, (name, champ),  in enumerate(zip(infos[game_index]["riotIdGameName"], infos[game_index]["championName"]), 1)])
            selected_players = input(f"Choose players to plot:\n0: All\n{formatted_players}\n")
            parsed_selected_players = [int("".join([x for x in substr if x.isdigit()])) for substr in selected_players.split(",")]
            assert max(parsed_selected_players) <= len(infos[game_index]["championName"]), "Invalid players entered."

            if parsed_selected_players != [0]:
                selected_infos, selected_stats = ({key: [v for i, v in enumerate(val, 1) if i in parsed_selected_players] for key, val in type[game_index].items()} for type in [infos, stats])
                # selected_stats = {key: [v for i, v in enumerate(val, 1) if i in parsed_selected_players] for key, val in stats[game_index].items()}
            else:
                selected_infos = infos[game_index]
                selected_stats = stats[game_index]

            if info_type == 1:
                selected = selected_infos
                desc = "infos"
            else:
                selected = selected_stats
                desc = "stats"

            formatted = "\n".join([f"{i}: {key}" for i, key in enumerate(selected.keys())])
            indices = input(f"Choose {desc} to plot:\n{formatted}\n")
            parsed_selected = [int("".join([x for x in substr if x.isdigit()])) for substr in indices.split(",")]
            assert max(parsed_selected) < len(selected), f"Invalid {desc} entered."

            chosen_stats = [val for i, val in enumerate(selected.values()) if i in parsed_selected]
            chosen_title = f"Game: {match_ids[game_index]}"
            chosen_name = f"{indices.replace(', ', '-')}_{str(selected_players).replace(', ', '-')}_{match_ids[game_index]}.png"

            if info_type == 1:
                chosen_labels = [info_name for i, info_name in enumerate(selected_infos.keys()) if i in parsed_selected]
                chosen_players = [f"{name} ({champ})" for name, champ in zip(selected_infos["riotIdGameName"], selected_infos["championName"])]
                chosen_name = "i_" + chosen_name

                plot_infos(chosen_stats, chosen_name, chosen_labels, chosen_players, title=chosen_title)
            else:
                chosen_labels = [[f"{name} ({champ}), {stat_name}" for name, champ in zip(selected_infos["riotIdGameName"], selected_infos["championName"])] for i, stat_name in enumerate(selected_stats.keys()) if i in parsed_selected]
                chosen_name = "s_" + chosen_name

                plot_timelines(chosen_stats, chosen_name, chosen_labels, title=chosen_title)
        except ValueError as e:  # Kinda ugly to use to different types of errors
            print(f"There was an error when processing inputs: 'Invalid number entered.' ({e})")
        except AssertionError as e:
            print(f"There was an error when processing inputs: '{e}'")
