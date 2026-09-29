from math import floor
import random

isRunning = True

inventories: dict[str, list] = {}
cash: dict[str, int] = {}

def clamp(n, minimum: int, maximum: int):
    return max(minimum, min(maximum, n))

def create_new_profile(player: str):
    inventories[player] = []
    cash[player] = 0
    return

def retrieve_player_inventory(player : str) -> list:
    return inventories[player]

def output_inventory(inventory : list):
    print("\nВаш інвентар:")
    for item in inventory:
        print(item)

def sell_fish(player: str, index : int | str=0) -> int:
    inventory = retrieve_player_inventory(player)
    amount = 0
    if not inventory:
        print("У вас немає риби :(\n")
        return 0

    if type(index) == str:
        if not index == "all":
            return 0
        i = 0
        while i < len(inventory):
            amount += sell_fish(player, i)

        return amount

    if type(index) == int:
        if not inventory[index]:
            print("У вас немає риби :(\n")
            return 0
        fish = inventory.pop(index)
        if not fish:
            return 0
        amount = (fish == "Large Fish" and 50 or
                        fish == "Medium Fish" and 30 or
                        fish == "Regular Fish" and 15)
        cash[player] += amount

    return amount


def start_fishing(tick: int) -> str:
    percentage = 1 + tick * 0.01
    max_size = 25 * percentage

    random_num = random.randint(1, floor(max_size))

    if random_num <= 1:
        return "Large Fish"
    elif random_num < 6:
        return "Medium Fish"
    else:
        return "Regular Fish"

def main():
    global isRunning
    username = ""

    tick = 0
    print("Вітаємо вас у грі")

    while (not username):
        try:
            username = input("Введіть ваш нікнейм: ")
        except ValueError:
            print("Помилка вводу.\n")


    create_new_profile(username)
    inventory = retrieve_player_inventory(username)
    print("\nЩоб ознайомитись зі списком команд, введіть help\n")
    while isRunning:
        tick = clamp(tick + 1, 0, 20)
        try:
            player_input = input("Введіть команду: ")

            str_list = player_input.split(" ")

            command, additional = "", ""
            for item in str_list:
                if not command:
                    command = item
                    continue
                additional = item

            if command == "quit":

                isRunning = False

            elif command == "help":

                print("\nДійсні команди:")
                print("help - Виводить список команд")
                print("quit - Закриває гру")
                print("fish - Ловить рибу")
                print("sell [number / all] - Продає рибу")
                print("inventory - Виводить ваш інвентар")
                print("cash - Виводить ваш баланс")
                print("clear - Очищає ваш інвентар\n")

            elif command == "fish":

                fish = start_fishing(tick)
                print(f"Ви піймали: {fish}!\n")
                inventory.append(fish)

            elif command == "sell":
                cash_amount = 0

                if len(additional) > 0:
                    cash_amount = sell_fish(username, additional)
                else:
                    cash_amount = sell_fish(username)


                if cash_amount != 0:
                    print(f"Ви отримали: {cash_amount}!\n")

            elif command == "cash":

                print(f"Ваш баланс: {cash[username]}!\n")

            elif command == "inventory":

                output_inventory(inventory)

            elif command == "clear":

                inventory.clear()

            else:
                continue
        except ValueError:
            print("Помилка вводу.\n")


    print("Закриття гри...")
    return 0

if __name__ == "__main__":
    main()