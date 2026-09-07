"""
Простая пошаговая игра-бой для тестирования.
Игрок сражается с монстром, бой длится примерно 9-10 ходов.
"""

import random

PLAYER_HP_MAX = 40
MONSTER_HP_MAX = 45
MAX_TURNS = 10


def print_status(turn, player_hp, monster_hp):
    print(f"\n--- Ход {turn}/{MAX_TURNS} ---")
    print(f"Игрок:   {'#' * max(player_hp // 2, 0):<20} {player_hp}/{PLAYER_HP_MAX} HP")
    print(f"Монстр:  {'#' * max(monster_hp // 2, 0):<20} {monster_hp}/{MONSTER_HP_MAX} HP")


def player_turn(monster_hp):
    print("\nВыбери действие:")
    print("1 - Атака (5-10 урона)")
    print("2 - Сильный удар (10-18 урона, но 30% шанс промаха)")
    print("3 - Лечение (+8 HP)")
    choice = input("> ").strip()

    if choice == "2":
        if random.random() < 0.3:
            print("Ты промахнулся сильным ударом!")
            return monster_hp, 0
        dmg = random.randint(10, 18)
        print(f"Мощный удар! Урон: {dmg}")
        return max(monster_hp - dmg, 0), 0
    elif choice == "3":
        heal = 8
        print(f"Ты лечишься на {heal} HP")
        return monster_hp, heal
    else:
        dmg = random.randint(5, 10)
        print(f"Обычная атака. Урон: {dmg}")
        return max(monster_hp - dmg, 0), 0


def monster_turn(player_hp):
    dmg = random.randint(4, 9)
    print(f"Монстр атакует и наносит {dmg} урона!")
    return max(player_hp - dmg, 0)


def main():
    print("=== БОЙ С МОНСТРОМ ===")
    print(f"У тебя {MAX_TURNS} ходов, чтобы победить монстра (или выжить).")

    player_hp = PLAYER_HP_MAX
    monster_hp = MONSTER_HP_MAX

    for turn in range(1, MAX_TURNS + 1):
        print_status(turn, player_hp, monster_hp)

        if monster_hp <= 0:
            print("\n🎉 Монстр повержен! Ты победил!")
            return
        if player_hp <= 0:
            print("\n💀 Ты проиграл...")
            return

        monster_hp, heal = player_turn(monster_hp)
        player_hp = min(player_hp + heal, PLAYER_HP_MAX)

        if monster_hp <= 0:
            print("\n🎉 Монстр повержен! Ты победил!")
            return

        player_hp = monster_turn(player_hp)

        if player_hp <= 0:
            print("\n💀 Ты проиграл...")
            return

    print("\n--- Ходы закончились ---")
    if player_hp >= monster_hp:
        print("Ты продержался и вышел вперёд по здоровью. Условная победа!")
    else:
        print("Монстр оказался сильнее. Условное поражение.")


if __name__ == "__main__":
    main()