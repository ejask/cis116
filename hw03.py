"""
File Name: hw03.py
Author: Emma Jaskowiec
Section: E
Description: Implements the game Pictsie Sticks; each turn, a player takes 1-3 sticks from the board (though they cannot take more sticks than are present). After the player's turn, there is a chance that 1-4 sticks will be magically added back to the board. If the player takes the last stick (and none are added back), they lose.
"""

import random


def not_quite_right(sticks: int) -> int:
    n = random.randint(0, 10)
    if n < 7:
        return 0
    sticks_to_add = random.randint(1, 4)
    if sticks_to_add + sticks > 20:
        return 20 - sticks
    else:
        return sticks_to_add


def display_board(sticks: int):
    """Prints the board to the console (i.e. print a column of pipe characters for each stick remaining.)"""
    print((("|\t" * sticks) + "\n") * 5, end="")
    for stick in range(sticks):
        print(stick + 1, end="\t")
    print()


def get_sticks_to_take(player: int, sticks: int) -> int:
    while True:
        sticks_to_take = int(
            input(f"Player {player}, how many sticks will you take?: ")
        )
        if sticks_to_take <= 0:
            print("You have to take at least 1 stick.")
        elif sticks_to_take > sticks:
            print(
                f"You can't take {sticks_to_take} sticks; there are only {sticks} sticks left."
            )
        elif sticks_to_take > 3:
            print("You can't take more than 3 sticks.")
        else:
            return sticks_to_take


def display_summary(
    player: int, sticks_taken: int, sticks_added: int, sticks_remaining: int
):
    """Prints a summary of the turn."""
    print(
        f"Player {player} took {sticks_taken}, pictsie shenanigans added {sticks_added} back, leaving {sticks_remaining} remaining."
    )


def main():
    player = 1
    sticks = 20
    while sticks > 0:
        display_board(sticks)
        sticks_to_take = get_sticks_to_take(player, sticks)
        sticks_to_add = not_quite_right(sticks)
        sticks += sticks_to_add - sticks_to_take
        display_summary(player, sticks_to_take, sticks_to_add, sticks)
        player = (player % 2) + 1
        print()
    print(f"Player {player} wins!")


main()
