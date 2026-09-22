from math import floor
import random

isRunning = True

def clamp(n, minimum: int, maximum: int):
    return max(minimum, min(maximum, n))

def output_inventory(inventory : list):
    print("\nВаш інвентар:")
    for item in inventory:
        print(item)

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
    inventory: list = []

    tick = 0
    print("Вітаємо вас у грі")
    print("\nЩоб ознайомитись зі списком команд, введіть help\n")
    while isRunning:
        tick = clamp(tick + 1, 0, 20)
        try:
            player_input = input("Введіть команду: ")

            if player_input == "quit":
                isRunning = False
            elif player_input == "help":
                print("\nДійсні команди:")
                print("help - Виводить список команд")
                print("quit - Закриває гру")
                print("fish - Ловить рибу")
                print("clear - Очищає ваш інвентар")
                print("inventory - Виводить ваш інвентар\n")
            elif player_input == "fish":
                fish = start_fishing(tick)
                print(f"Ви піймали: {fish}!\n")
                inventory.append(fish)
            elif player_input == "inventory":
                output_inventory(inventory)
            elif player_input == "clear":
                inventory.clear()
            else:
                continue
        except ValueError:
            print("Помилка вводу.\n")


    print("Закриття гри...")
    return 0

if __name__ == "__main__":
    main()