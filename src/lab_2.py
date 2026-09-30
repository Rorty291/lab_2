from functools import reduce, lru_cache
from math import floor
import random

FISH_PRICES: dict[str, dict] = {
    "Large Fish": {
        "price": 50,
        "weight": 5.6
    },
    "Medium Fish": {
        "price": 30,
        "weight": 3.2
    },
    "Regular Fish": {
        "price": 15,
        "weight": 1.4
    },
    "Fast Fish": {
        "price": 25,
        "weight": 1.7
    },
    "Slow Fish": {
        "price": 42,
        "weight": 4.4
    },
}

inventories: dict[str, list] = {}
cash: dict[str, int] = {}

template: dict = {
    "price": 0,
    "weight": 0
}

fish_stat = lambda name: FISH_PRICES.get(name, template)
fish_stat.__doc__ = "Повертає ціну риби за її назвою (0, якщо риби немає в прайсі)."

inventory_value = lambda inv: sum(fish_stat(item)["price"] for item in inv)
inventory_value.__doc__ = "Повертає загальну вартість усієї риби в інвентарі."


def clamp(n, minimum: int, maximum: int):
    #Обмежує число n діапазоном [minimum, maximum]."
    return max(minimum, min(maximum, n))

def start_fishing(tick: int) -> str:
    # Імітує риболовлю: чим більший tick, тим вищий шанс піймати велику рибу.
    percentage = 1 + tick * 0.01
    max_size = 25 * percentage

    random_num = random.randint(1, floor(max_size))

    if random_num <= 1:
        return "Large Fish"
    elif random_num < 6:
        return "Medium Fish"
    else:
        return "Regular Fish"

def sell_fish(player: str, index: int = 0) -> int:
    """
    Продає рибу гравця з позиції index (за замовчуванням — першу).

    Повертає отриману суму або 0, якщо продаж неможливий.
    """
    inventory = inventories[player]
    if not inventory:
        print("У вас немає риби :(\n")
        return 0
    if not 0 <= index < len(inventory):
        print(f"Немає риби з номером {index + 1}. У вас риб: {len(inventory)}\n")
        return 0

    amount = fish_stat(inventory.pop(index))["price"]
    cash[player] += amount
    return amount

def add_fish(inventory: list, *fish: str, **options) -> int:
    """
    Додає довільну кількість риб в інвентар.

    - Параметри (**options):
    - announce (bool) — виводити повідомлення про кожен улов (за замовч. True).
    - Повертає кількість доданих риб.
    """
    for item in fish:
        inventory.append(item)
        if options.get("announce", True):
            print(f"Ви піймали: {item}!")
    return len(fish)

def create_new_profile(player: str):
    # Створює порожній інвентар і нульовий баланс для нового гравця.
    inventories[player] = []
    cash[player] = 0

def output_inventory(inventory: list):
    # Виводить інвентар у вигляді нумерованого списку з цінами.
    print("\nВаш інвентар:")
    if not inventory:
        print("  (порожньо)")

    for number, item in enumerate(inventory, start=1):
        stats = fish_stat(item)
        print(f"  {number}. {item} — {stats["price"]}$ - {stats["weight"]}kg")

    print(f"Загальна вартість: {inventory_value(inventory)}$\n")

def sell_all(player: str) -> int:
    """
    Рекурсивно продає всю рибу гравця й повертає загальну суму.

    Базовий випадок: інвентар порожній — повертаємо 0.
    """
    if not inventories[player]:
        return 0
    return sell_fish(player, 0) + sell_all(player)

def apply_to_fish(data: list, func) -> list:
    """
    Функція вищого порядку: застосовує функцію func до кожного запису data.
    """
    return list(map(func, data))


def show_market(min_price: int = 0):
    """
    Показує ринок: filter — відбір за ціною, map (через apply_to_fish) —
    сезонна надбавка, reduce — підсумкова вартість.
    """
    records = [{"name": name, **stats} for name, stats in FISH_PRICES.items()]

    selected = list(
        filter(
            lambda f: f["price"] >= min_price,
            records
        )
    )
    if not selected:
        print(f"Немає риби з ціною від {min_price}.\n")
        return


    total = reduce(
        lambda acc, f: acc + f["price"],
        selected,
        0
    )

    print(f"\nРинок (ціна від {min_price}")
    print(f"{'Риба':<14}{'Вага, кг':>9}{'Ціна':>8}")

    for f in selected:
        print(f"{f['name']:<14}{f['weight']:>9}{f['price']:>7}$")

    print(f"Позицій: {len(selected)}, сумарна вартість: {total}\n")


def print_help():
    # Виводить меню доступних команд.
    print("\nДійсні команди:")
    print("help - Виводить список команд")
    print("quit - Закриває гру")
    print("fish [кількість] - Ловить рибу (1-10 за раз)")
    print("sell [номер / all] - Продає рибу (без аргументу — першу)")
    print("inventory - Виводить ваш інвентар")
    print("cash - Виводить ваш баланс")
    print("market [мін. ціна] - Ринок риби (filter / map / reduce)")
    print("clear - Очищає ваш інвентар\n")

def read_int(text: str, minimum: int, maximum: int) -> int:
    """
    Перетворює text на ціле число та перевіряє діапазон.
    Викликає ValueError, якщо введення некоректне.
    """
    try:
        value = int(text)
    except ValueError:
        raise ValueError(f"'{text}' — це не ціле число") from None
    if not minimum <= value <= maximum:
        raise ValueError(f"Число має бути від {minimum} до {maximum}")
    return value


def main():
    print("Вітаємо вас у грі")

    username = ""
    while not username:
        try:
            username = input("Введіть ваш нікнейм: ").strip()
            if not username:
                raise ValueError
        except ValueError:
            print("Помилка вводу: нікнейм не може бути порожнім.\n")

    create_new_profile(username)
    inventory = inventories[username]
    tick = 0
    print("\nЩоб ознайомитись зі списком команд, введіть help\n")

    while True:
        tick = clamp(tick + 1, 0, 20)
        try:
            words = input("Введіть команду: ").split()
            if not words:
                continue
            command, args = words[0].lower(), words[1:]

            if command == "quit":
                break

            elif command == "help":
                print_help()

            elif command == "fish":
                if args:
                    count = read_int(args[0], 1, 10)
                else:
                    count = 1

                caught = [start_fishing(tick) for _ in range(count)]
                add_fish(inventory, *caught, announce=True)
                print()

            elif command == "sell":
                if args and args[0].lower() == "all":
                    amount = sell_all(username)
                elif args:
                    amount = sell_fish(username, read_int(args[0], 1, 10**6) - 1)
                else:
                    amount = sell_fish(username)

                if amount:
                    print(f"Ви отримали: {amount}$!\n")

            elif command == "cash":
                print(f"Ваш баланс: {cash[username]}!\n")

            elif command == "inventory":
                output_inventory(inventory)

            elif command == "market":
                if args:
                    show_market(read_int(args[0], 0, 10 ** 6))
                else:
                    show_market()

            elif command == "clear":
                inventory.clear()
                print("Інвентар очищено.\n")

            else:
                print("Невідома команда. Введіть help.\n")

        except ValueError as error:
            print(f"Помилка вводу: {error}\n")
        except (EOFError, KeyboardInterrupt):
            print()
            break

    print("Закриття гри...")
    return 0


if __name__ == "__main__":
    main()