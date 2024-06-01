def parse_infos(match_infos):
    infos = [{} for _ in range(len(match_infos))]
    for i, match_timeline in enumerate(match_infos):
        for player in match_timeline["info"]["participants"]:
            for info_key, info_val in player.items():
                if isinstance(info_val, dict):
                    for subinfo_key, subinfo_val in info_val.items():
                        infos[i].setdefault(subinfo_key, []).append(subinfo_val)
                else:
                    infos[i].setdefault(info_key, []).append(info_val)

    return infos


def parse_timelines(match_timelines):
    stats = [{} for _ in range(len(match_timelines))]  # defaultdict(lambda: [[[] for _ in range(len(match_timeline["info"]["frames"]))] for _ in range(len(self.match_timelines))], {})
    for i, match_timeline in enumerate(match_timelines):
        for frame in match_timeline["info"]["frames"]:
            for i2, player in enumerate(frame["participantFrames"].values()):
                for stat_key, stat_val in player.items():
                    if isinstance(stat_val, dict):
                        for substat_key, substat_val in stat_val.items():
                            if substat_key not in stats[i]:
                                stats[i][substat_key] = [[] for _ in range(len(frame["participantFrames"]))]

                            stats[i][substat_key][i2].append(substat_val)
                    else:
                        if stat_key not in stats[i]:
                            stats[i][stat_key] = [[] for _ in range(len(frame["participantFrames"]))]

                        stats[i][stat_key][i2].append(stat_val)

    return stats
