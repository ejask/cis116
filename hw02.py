"""
File Name: hw02.py
Name: Emma Jaskowiec
Section: E
Project: Vending Machine
Description: This file implements a Gremlin Vending Machine that allows the user to start the machine, insert coins, select and purchase an item, receive change, and restock. The unexpected behaviors are just a consequence of the low budget.
"""

import random


class VendingMachineItem:
    COST = 1.5

    def __init__(self, name: str, max_stock: int):
        self.name = name
        self.MAX = max_stock
        self.stock = max_stock

    def restock(self):
        """Restocks the item to its initial quantity."""
        # have i mentioned i'm not a big fan of python doc comment syntax? it's fine, i guess, but treesitter highlights it like any other string and it looks kind of cluttered.
        self.stock = self.MAX


class VendingMachine:
    def __init__(self):
        self.state = "A"
        self.total_inserted = 0
        self.total_coins = 0

        # I know this isn't what the assignment specifies (it seems like you wanted invidual variables named item_1, item_2, etc.) but I feel very strongly that this should be an array instead.
        self.items = [
            VendingMachineItem("cola", 3),
            VendingMachineItem("cookie", 5),
            VendingMachineItem("energy drink", 2),
            VendingMachineItem("granola bar", 4),
            VendingMachineItem("live spider", 1),
        ]
        self.selected_item = None
        self.gives_change = True

    def print_stock(self):
        """Print a list of the available items and quantities"""
        for item in self.items:
            print(f"'{item.name}' ({item.stock} left)")

    def idle(self):
        """State A (start/idle): Await and handle the initial user input."""
        option = (
            input(
                "Enter 'start' to start the vending machine, 'restock' to restock, or 'exit' to power off: "
            )
            .strip()
            .lower()
        )
        match option:
            case "start":
                # Check if the machine is empty
                for item in self.items:
                    if item.stock > 0:
                        print("\nThe machine contains:")
                        self.print_stock()
                        self.state = "B"
                        return
                print(
                    "The machine is empty! It should be restocked before you start it again."
                )
            case "restock":
                self.state = "F"
            case "exit":
                self.state = "G"
            case _:
                print("Invalid input")

    def insert(self):
        """State B (insert): Accept coins from the user until the total reaches $1.50."""
        print(
            "The machine will accept a 'penny', 'nickel', 'dime', 'quarter', or 'dollar'."
        )
        option = input("Enter a coin or 'refund' to return change: ").strip().lower()
        if option == "refund":
            self.state = "E"
            return
        coin_input = 0
        match option:
            case "penny":
                coin_input += 0.01
            case "nickel":
                coin_input += 0.05
            case "dime":
                coin_input += 0.1
            case "quarter":
                coin_input += 0.25
            case "dollar":
                coin_input += 1
            case _:
                print("Invalid input; that's not a coin.")
                return
        if random.random() < 0.31:
            print("The machine ate your coin!")
        else:
            self.total_coins += 1
            self.total_inserted += coin_input
            if self.total_inserted >= VendingMachineItem.COST:
                self.state = "C"
        print(f"Total change inserted: ${self.total_inserted:,.2f}")

    def select(self):
        """State C (select): Allows the user to select and purchase an available item."""
        print(
            "Each item in the machine costs $1.50. You can select one of the following items (or 'refund' to refund change): "
        )
        self.print_stock()
        selected = input("Select an item: ").strip().lower()
        if selected == "refund":
            self.state = "E"
            return
        for item in self.items:
            if selected == item.name:
                self.selected_item = item
                break
        if not isinstance(self.selected_item, VendingMachineItem):
            print("The machine doesn't sell that.")
            return
        if self.selected_item.stock <= 0:
            print("Sorry, that item is out of stock.")
        else:
            change = (
                input(
                    f"You selected '{self.selected_item.name}'. Would you like your change? (y/n): "
                )
                .strip()
                .lower()[0]
            )
            self.gives_change = False if change == "n" else True
            self.state = "D"

    def dispense(self):
        """State D (dispense): Dispense one of the selected item to the user (or two, if an even number of coins was inserted)."""
        # We've already done this check in `select()`, but the lsp still complains that `self.selected_item` might be `None`, so we check again
        if not isinstance(self.selected_item, VendingMachineItem):
            print(
                "ERROR: `selected_item` is not a valid instance of `VendingMachineItem`."
            )
            self.state = "G"
            return
        print(f"Dispensing item...")
        self.total_inserted -= VendingMachineItem.COST
        if self.total_coins % 2 == 0 and self.selected_item.stock >= 2:
            self.selected_item.stock -= 2
            print(f"The machine dispensed two {self.selected_item.name}s!")
        else:
            self.selected_item.stock -= 1
            print(f"The machine dispensed one {self.selected_item.name}.")
        self.selected_item = None
        self.state = "E" if self.gives_change else "A"

    def change(self):
        """State E (return change): "Returns" remaining change to the user."""
        print("Returning change...")
        print(f"You got ${self.total_inserted:,.2f} back!")
        self.total_inserted = 0
        self.total_coins = 0
        print(f"Total change inserted: ${self.total_inserted:,.2f}")
        self.state = "A"

    def stock(self):
        """State F (stock): Replenishes items to their inital quantities."""
        for item in self.items:
            item.restock()
        print("The machine has been restocked.")
        self.state = "A"

    def match_state(self):
        """Runs the appropriate function for the machine's current state."""
        match self.state:
            case "A":
                self.idle()
            case "B":
                self.insert()
            case "C":
                self.select()
            case "D":
                self.dispense()
            case "E":
                self.change()
            case "F":
                self.stock()
            case _:
                print("ERROR: Invalid state. How did you manage to do that?")
                self.state = "G"

    def run(self):
        """Internal run method for exit handling and formatting."""
        while self.state != "G":
            self.match_state()
            print()


def main():
    # here we go!!!!!!!!!!!!!
    VendingMachine().run()


if __name__ == "__main__":
    main()
