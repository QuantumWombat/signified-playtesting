from typing import List
import pandas as pd
import nltk

DAMAGE = "damage"
BLOCK = "block"
END_TURN = "endturn"
RESET_TURNS = "resetturns"
SHOW = "show"
TEAM = "team"
HELP = "help"

HELP_STR = {
    DAMAGE: "Usage: `damage <num>`",
    BLOCK: "Usage: `block <num>`",
    END_TURN: "End the turn. Usage: `endturn`",
    RESET_TURNS: "Reset the turn counter. Usage: `resetturns`",
    SHOW: "Show the current results. Usage: `show`",
    TEAM: "Set the current team. Usage `team Aborah pythia entropy",
    HELP: "Display the usage for a command. Usage: `help <command>",
}
ACTIONS = list(HELP_STR.keys())
COMPANIONS = ["Pythia", "Aborah", "Architect", "Clown", "Entropy"]


def closest_word(word: str, words: List[str]) -> str:
    edit_distances = [nltk.edit_distance(word, w) for w in words]
    for i, _ in enumerate(edit_distances):
        if words[i].lower()[:2] == word.lower()[:2]:
            edit_distances[i] -= 5
    min_distance = min(edit_distances)
    chosen = words[edit_distances.index(min_distance)]
    return chosen


def get_cleaned_input() -> List[str]:
    raw = input()
    sep = [s.strip().lower() for s in raw.split(" ")]
    return [s for s in sep if len(s) > 0]


def main():
    print(f"Available actions: {', '.join(ACTIONS)}")

    print("Please enter starting list of companions: ", end="")
    sep_companions = get_cleaned_input()
    selected_companions = [closest_word(c, COMPANIONS) for c in sep_companions]
    print("Selected companions:", selected_companions)

    turn_counter = 1
    current_turn_data = {
        "turn": turn_counter,
        "block": 0,
        "damage": 0,
        "companions": selected_companions[:],
    }
    turns = []

    while True:
        print("> ", end="")
        split = get_cleaned_input()
        raw_action = split[0]

        chosen_action = closest_word(raw_action, ACTIONS)
        print(f"Chosen action: {chosen_action}")

        if chosen_action == DAMAGE:
            if len(split) < 2:
                print(HELP_STR[DAMAGE])
                continue

            num = int(split[1])
            current_turn_data["damage"] += num
        elif chosen_action == BLOCK:
            if len(split) < 2:
                print(HELP_STR[BLOCK])
                continue

            num = int(split[1])
            current_turn_data["block"] += num
        elif chosen_action == END_TURN:
            current_turn_data["turn"] = turn_counter
            print("Totals")
            print(current_turn_data)
            turns.append(current_turn_data)

            turn_counter += 1
            current_turn_data = {
                "turn": turn_counter,
                "block": 0,
                "damage": 0,
                "companions": selected_companions[:],
            }
        elif chosen_action == RESET_TURNS:
            turn_counter = 1
            current_turn_data["turn"] = turn_counter
        elif chosen_action == SHOW:
            df = pd.DataFrame(turns)
            print("Cumulative data")
            print(df)

            print("Current turn data")
            print(current_turn_data)
        elif chosen_action == TEAM:
            input_companions = split[1:]
            if len(input_companions) == 0:
                print(HELP_STR[TEAM])
                continue

            selected_companions = [
                closest_word(c, COMPANIONS) for c in input_companions
            ]
            print("Selected companions:", selected_companions)
            current_turn_data["companions"] = selected_companions[:]
        elif chosen_action == HELP:
            cmd = split[1]
            help_action = closest_word(cmd, ACTIONS)
            print(HELP_STR[help_action])


if __name__ == "__main__":
    main()
