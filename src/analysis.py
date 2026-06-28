import sys

import matplotlib.pyplot as plt

from pathlib import Path
import json

plt.style.use('_mpl-gallery')

# Fighter A name : B name, arena name, A HP, B HP
matches: list[tuple[str, str, str, int, int]] = []

for dir in Path("fight_data/").iterdir():
    if dir.is_dir():
        for entry in dir.iterdir():
            if entry.is_file():
                with entry.open() as f:
                    parts = entry.name.split(":")
                    json_dict: dict = json.load(f)
                    a_hp = int(json_dict["a_hp"])
                    b_hp = int(json_dict["b_hp"])
                    new_match = (parts[0], parts[1], parts[2], a_hp, b_hp)
                    matches.append(new_match)


names = list(set([ m[0] for m in matches ] + [ m[1] for m in matches ]))

def show_overall_wins():
    win_dict: dict[str, int] = {}
    for m in matches:

        a_name, b_name, _, a_hp, b_hp = m

        if a_name not in win_dict.keys():
            win_dict[a_name] = 0
        if b_name not in win_dict.keys():
            win_dict[b_name] = 0

        if a_hp > b_hp:
            win_dict[a_name] += 1
        else:
            win_dict[b_name] += 1

    win_list: list[tuple[str, int]] = []
    for name in win_dict.keys():
        win_list.append((name, win_dict[name]))
    win_list = sorted(win_list, key=lambda x: x[1])

    names = [ name for name, _ in win_list ]
    counts = [ count for _, count in win_list ]

    plt.bar(names, counts, color='skyblue')

    plt.title('Overall Fighter Wins')
    plt.xlabel('Fighter Names', fontsize=12)
    plt.ylabel('Number of Wins', fontsize=12)

    plt.tight_layout()
    plt.xticks(rotation=45, ha='right')
    plt.show()


def show_individual_wins(fighter_name: str):

    win_scores: dict[str, int] = {}
    for name in names:
        if name == fighter_name:
            continue
        win_scores[name] = 0
    
    for a_name, b_name, _, a_hp, b_hp in matches:
        
        is_fighter_a = fighter_name == a_name
        is_fighter_b = fighter_name == b_name

        if not is_fighter_a and not is_fighter_b:
            continue
        
        opponent_name = b_name if is_fighter_a else a_name
        a_won = a_hp > 0 and b_hp <= 0
        if (is_fighter_a and a_won) or (not is_fighter_a and not a_won):
            win_scores[opponent_name] += 1
    
    win_score_list = []
    for scores in win_scores.keys():
        win_score_list.append((scores, win_scores[scores]))
    win_score_list = sorted(win_score_list, key=lambda x: x[1], reverse=True)

    x: list[str] = []
    y: list[int] = []
    for key, value in win_score_list:
        value = win_scores[key]
        x.append(f"Wins against {key}")
        y.append(value)
    
    fig, ax = plt.subplots(layout="constrained")
    
    ax.bar(x, y, color='skyblue')

    plt.title(f"{fighter_name}'s Wins")
    plt.xlabel('Opponent Names', fontsize=12)
    plt.ylabel('Number of Wins/Losses', fontsize=12)

    plt.xticks(rotation=45, ha='right')
    plt.show()


if sys.argv[1] == "overall":
    show_overall_wins()
elif sys.argv[1] in names:
    show_individual_wins(sys.argv[1])