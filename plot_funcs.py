import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import lineStyles

def plot_timelines(stats, name, labels, title=""):
    plt.figure(figsize=(10, 5))

    for stat, label, line_style in zip(stats, labels or [[[]]] * len(stats), lineStyles):
        for player_stat, lab in zip(stat, label):
            plt.plot(player_stat, label=lab, linestyle=line_style)

    plt.title(title)
    plt.xlabel("Time")
    plt.legend()

    plt.savefig(name)
    plt.close()


def plot_infos(infos, name, info_names, player_names, title=""):
    fig, ax = plt.subplots(figsize=((4 + 0.125 * len(infos)) * len(player_names), 5))

    x = np.arange(len(player_names))
    width = 0.25
    multiplier = 0

    for info, info_name in zip(infos, info_names):
        offset = width * multiplier
        rects = ax.bar(x + offset, info, width, label=info_name)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    ax.set_title(title)
    ax.set_xticks(x, player_names)
    ax.legend()

    plt.savefig(name)
    plt.close()
