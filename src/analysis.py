import itertools

import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
import json

plt.style.use('_mpl-gallery')

# Fighter A name : B name, arena name, a_hp, b_hp
matches: dict[str, list[tuple[str, str, int, int, bool]]] = {}

for dir in Path("fight_data/").iterdir():
    if dir.is_dir():
        for entry in dir.iterdir():
            if entry.is_file():
                with entry.open() as f:
                    parts = entry.name.split(":")
                    json_dict: dict = json.load(f)
                    a_hp = int(json_dict["a_hp"])
                    b_hp = int(json_dict["b_hp"])
                    new_match = (parts[1], parts[2], a_hp, b_hp, a_hp > b_hp)
                    if not parts[0] in matches.keys():
                        matches[parts[0]] = []
                    matches[parts[0]].append(new_match)


# Overall wins:
names = list(matches.keys())
wins = []
for name in names:
    fights = matches[name]
    i = 0
    for fight in fights:
        if fights[5]:
            i += 1
    wins.append(i)


plt.bar(names, wins, color='skyblue')

# Add the overall X-axis and Y-axis labels
plt.xlabel('Fighter Names', fontsize=12)
plt.ylabel('Number of Wins', fontsize=12)
plt.title('Overall Fighter Wins')

plt.tight_layout()
plt.xticks(rotation=45, ha='right')
plt.show()