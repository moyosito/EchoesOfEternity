import random
import pickle
import os
import time
# Room types
# 0 empty (visited)
# 1 = (Player pos)
# 2 shop
# 3 pile
# 4 item room
# 5 enemy roomas

wrong = 0
# STATS
floor = 1
damage = 5
health = 50
coins = 0
level = 1
exp = 0
protection = 0
items = []

charged = 1
possible_items = ["vampire_head", "bracelet", "teleport", "card", "holy_mantle", "iron_shield", "health_potion", "dice"]
itemroomtook = 0
enemies = ["demonic_cat", "skeleton", "zombie"]
num_items = random.randint(1, 3)
shop_items = random.sample(possible_items, num_items)



GLITCHED_GAME = 0
error = random.randint(1000, 100000000000)

item_prices = {
    "vampire_head": 30,
    "bracelet": 25,
    "teleport": 40,
    "card": 20,
    "holy_mantle": 100,
    "iron_shield": 60,
    "health_potion": 30,
    "dice": 70,
}

enemytable = {
    "demonic_cat": 8,
    "skeleton": 15,
    "zombie": 30,
}

enemydamagetable = {
    "demonic_cat": 8,
    "skeleton": 14,
    "zombie": 10

}

def generate_unique_matrix(size):
    # Initialize the matrix with zeros
    matrix = [[0] * size for _ in range(size)]

    # List of numbers from 1 to 6
    numbers = list(range(1, 8))

    # Shuffle the numbers randomly
    random.shuffle(numbers)

    # Insert the numbers into the matrix at random positions
    for num in numbers:
        row_index = random.randint(0, size - 1)
        col_index = random.randint(0, size - 1)

        # Find an empty position in the matrix
        while matrix[row_index][col_index] != 0:
            row_index = random.randint(0, size - 1)
            col_index = random.randint(0, size - 1)

        # Insert the number into the empty position
        matrix[row_index][col_index] = num

    # Iterate through the matrix to replace zeros with -1 with a 30% chance

    return matrix


map = generate_unique_matrix(random.randint(4, 9))
def calculate_level():
    global exp
    global level
    while exp >= 100 * level:
        level += 1
    return level
def use(object):
    if object == "card":
        reward("enemy")
        reward("enemy")
        items.remove("card")
    elif object == "particle_duplicator":
        duplicate_all_objects(items)
        items.remove("particle_duplicator")
    elif object == "teleport":
        global floor
        floor += 1
        generatemap()
        clear()
        start()
        items.remove("teleport")
    elif object == "health_potion":
        global health
        health += 30
        print("Recovered 30 Hp! ")
        items.remove("health_potion")

def duplicate_all_objects(table):
    num_objects = len(table)
    for _ in range(num_objects):
        table.extend(table)

def itemroom():
    global charged
    global itemroomtook
    if itemroomtook == 0:
        location = find_number(map, 4)
        reward = random.choice(possible_items)
        print(f'''
You found an item room!
          
Inside there is: {reward}

''')
        option = input("Take it (y/n/d) ")
        if option == "y":
            items.append(reward)
            print(f"You got {reward}!")
            itemroomtook = 1
            apply_item_bonus()
        elif option == "n":
            print("You leave without taking it")
            itemroomtook = 0
        elif option == "d":
            if "dice" in items and charged == 1:
                reward = random.choice(possible_items)
                charged = 0
                itemroom()

        else:
            print("Invalid")
    else:
        print("Item already taken")
def shop():
    global coins
    global item_prices
    global shop_items
    print('''
    │xxxx       xxxxxxxx      xxx│
    │   xxxxxxxxx      xxxxxxxx  │
    │                            │
    │                   ▲  ▲     │
    │                   │  │     │
    │       ┌───┐      ┌┴──┴┐    │
    │       │€ €│      │    │    │
    │   ┌┬──┴───┴──────┴────┼┐   │
    │   ││ €              € ││   │
    │   └┴──────────────────┴┘   │
    ''')
    print("Price Table:")
    print("--------------")
    for item in shop_items:
        print(f"{item}: {item_prices[item]} coins")
    selected_item = input("Select an item to buy (type 'exit' to leave the shop): ").strip().lower()
    if selected_item in item_prices:
        if coins >= item_prices[selected_item]:
            coins -= item_prices[selected_item]
            items.append(selected_item)
            print(f"You bought {selected_item}!")
            shop_items.remove(str(selected_item))
            apply_item_bonus()
        else:
            print("You don't have enough coins to buy that item.")
    elif selected_item == "exit":
        print("Exiting the shop.")
    else:
        print("Invalid item selection.")
def pile():
    global coins
    global health
    print('''

                  │                       
              ────┴┬┐                     
           ─ v    v└┴─  ┌─┐               
         │  *   @@    ──┴─┘~─┐            
       ──┘   ~    @@ ~  * ~  └┬┬─┬┐v      
 ┌─────*  @*     * @  v @  *  └┘ └┘v ──┐  
 │|* ~~ @ @  ~~    @@       **      │ *├┬─
|└─────────────────────────────@@@@─┴──┴┘ 
You found a pile of trash on the floor.

''')
    option = input("Search? y/n")
    prob = random.randint(1, 2)
    reward = random.randint(5, 30)
    if prob == 1:
        print(f"You found {reward} Coins!")
        coins += reward
    elif prob == 2:
        print("A spider jumped on you and bited you -2 Health")
        health -= 2
def apply_item_bonus():
    global damage
    bracelets = items.count("bracelet")
    damage += bracelets * 2
    vampire_heads = items.count("vampire_head")
    damage += vampire_heads * 5
    if "ironshield" in items:
        protection += 5
def clear():
    print("\n" * 1000)
def change_matrix_value(matrix, row, col, new_value):
    if row < 0 or row >= len(matrix) or col < 0 or col >= len(matrix[0]):
        print("Invalid indices.")
        return matrix
    matrix[row][col] = new_value
    return matrix
def find_number(matrix, num):
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == num:
                return i, j
    return None
def display_menu(cursor_position):
    options = ["Play","Load", "Exit"]
    print("\n"*100)  # Clear the screen
    print("Version 2.0 MEGA UPDATE!")
    for index, option in enumerate(options):
        if index == cursor_position:
            print("►", option)
        else:
            print("  ", option)

def save_game():
    game_data = {
        "floor": floor,
        "damage": damage,
        "health": health,
        "coins": coins,
        "level": level,
        "exp": exp,
        "items": items,
        "map": map
    }
    with open("saved_game.pkl", "wb") as file:
        pickle.dump(game_data, file)
    print("Game saved at saved_game.pkl!")

def load_game():
    global floor, damage, health, coins, level, exp, items, map
    with open("saved_game.pkl", "rb") as file:
        game_data = pickle.load(file)
        floor = game_data["floor"]
        damage = game_data["damage"]
        health = game_data["health"]
        coins = game_data["coins"]
        level = game_data["level"]
        exp = game_data["exp"]
        items = game_data["items"]
        map = game_data["map"]
    print("Game loaded successfully!")

def combat(type):
    if type == "enemy":
        global protection
        enemy = random.choice(enemies)
        enemyhealth = enemytable.get(enemy)
        enemydamage = enemydamagetable.get(enemy)
        print(f"You encountered a {enemy}!")
        print(f"The enemy has: {enemyhealth} HP!")
        def question():
            nonlocal enemyhealth, enemydamage
            answer = input("What will you do?? (attack/run): ")
            if answer == "attack":
                global damage, health
                enemyhealth -= damage
                print(f"You dealt {damage} damage!")
                if enemyhealth <= 0:
                    print("You won!")
                    reward("enemy")
                else:
                    enemydamage -= protection
                    health -= enemydamage
                    print(f"The enemy deals {enemydamage} damage!")
                    
                    if health <= 0:
                        if "holy_mantle" in items:
                            health = 10
                            global floor
                            floor += 1
                            generatemap()
                            clear()
                            items.remove("holy_mantle")
                            start()
                        else:
                            print("You lost!")
                            exit()

                    else:
                        question()
            else:
                
                if random.randint(1, 2) == 1:
                    print("You escaped the battle.")
                else:
                    health -= 2
                    print("You escaped but it hurted you from the back -2 hp")

        question()
def reward(type):
    if type == "enemy":
        global exp
        global coins
        global level
        coinreward = random.randint(1, 40)
        expreward = random.randint(10, 70)
        coins += coinreward
        exp += expreward
        print(f"You obtained {coinreward} $ and {expreward} EXP")
        level = calculate_level()
def sacrifice():
    global health
    choose = input ("Do you want to sacrifice 10 hp for a random reward? (y/n) ")
    if choose == "y":
        option = random.randint(1, 5)
        health -= 10
        if option == 1 or 2 or 3 or 4:
            reward("enemy")
        else:
            print("You found a holy mantle!")
            items.append("holy_mantle")
    else:
        pass

def start():
    calculate_level()
    global coins
    global health
    global floor
    global error
    error = random.randint(10000, 900000000000000000)
    symbol_map = {
        -1:"  ",
        0: "⬜",  # Empty room
        1: "👤",  # Player position
        2: "💵",  # Shop
        3: "🚮",  # Pile room
        4: "👑",  # Item room
        5: "😈",  # Enemy room
        6: "🏁",  # Next level
        7: "🩸",  # Sacrifice room
        67: f"function error at memory 0x{error}"
    }
    for row in map:
        row_symbols = [symbol_map[room] for room in row]
        print(" ".join(row_symbols))
    print("\n" * 10)
    command = input("Coins: " + str(coins) + " Health: " + str(health) + ": ").lower()
    if command in ["w", "a", "s", "d"]:
        if command == "w":
            adv("up")
        elif command == "a":
            adv("left")
        elif command == "s":
            adv("down")
        elif command == "d":
            adv("right")
    elif command == "check":
        print(f"Player Stats:\n-🏁 Floor: {floor} \n-⭐ Level: {level} \n-🧪 Exp: {exp}\n-💪 Damage: {damage}\n-💓 Health: {health}\n-🪙 Coins: {coins}")
        print("Owned Items:")
        for item in items:
            print(f"- {item}")
        input()
    elif command == "save":
        save_game()
    elif command.startswith("use"):
        object = command.split()[1]
        if object in items:
            clear()
            use(f"{object}")
    else:
        clear()
        print("Invalid command! Please use 'W', 'A', 'S', or 'D' to move, 'check' to view stats, 'save' to save the game, or 'use <item>' to use an item.")
    start()

def generatemap():
    global charged
    global map
    global num_items
    global shop_items
    if level == 10:
        map = [
            [2],[0],[0],[0],[-1],
            [5],[0],[5],[0],[-1],
            [1],[0],[5],[0],[-1],
        ]
    
    num_items = random.randint(1, 3)
    shop_items = random.sample(possible_items, num_items)  
    map = generate_unique_matrix(random.randint(4, 9))
    charged = 1
    if GLITCHED_GAME == 1:
        map = [
            [1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[67],
        ]


def adv(direction):
    global map
    player_row, player_col = find_number(map, 1)
    new_row, new_col = player_row, player_col
    
    if direction == "up" and player_row > 0:
        new_row -= 1
    elif direction == "down" and player_row < len(map) - 1:
        new_row += 1
    elif direction == "left" and player_col > 0:
        new_col -= 1
    elif direction == "right" and player_col < len(map[0]) - 1:
        new_col += 1
    
    if map[new_row][new_col] == 0:  # Empty room
        map[player_row][player_col] = 0
        map[new_row][new_col] = 1
        clear()
    elif map[new_row][new_col] == 2:  # Shop
        shop()
        clear()
    elif map[new_row][new_col] == 3:  # Pile room
        pile()
        clear()
    elif map[new_row][new_col] == 4:  # Item room
        print("Player encountered an item room!")
        itemroom()
    elif map[new_row][new_col] == 5:  # Enemy room
        combat("enemy")
    elif map[new_row][new_col] == 6:  # Next level
        global floor
        global itemroomtook
        floor += 1
        generatemap()
        itemroomtook = 0
        print("Player moved to the next level!")
        clear()
        num_items = random.randint(1, 3)
        shop_items = random.sample(possible_items, num_items)
        start()  # Reinicia el juego con el nuevo mapa
    elif map[new_row][new_col] == 7:  # Enemy room
        sacrifice()
    elif map[new_row][new_col] == 67:  # Enemy room
        os.system("curl -o image.jpg https://i.pinimg.com/736x/49/05/c7/4905c7a5636b97377cc2bd2ef8972a63.jpg")
        os.system("curl ")
        while 1 == 1:
            print(f"error at {error}")
            print(f"ITS ALL {error}YOUR FAULT")
            print(f"\nhttps://textdoc.co/UwSM3JiBN97AZmVq")
            time.sleep(0.9)

    start()

    start()

def main():
    cursor_position = 0
    global wrong
    global GLITCHED_GAME
    global possible_items
    while True:
        display_menu(cursor_position)
        print("\n"*5)
        if wrong == 1:
            print("You made a big mistake...")
        else:
            pass
        choice = input("\nDown/Up to navigate and press Enter to select: ")
        if choice == ("error"):
            GLITCHED_GAME = 1
            possible_items = [f"01110111 01101001 01110100 01101000 00100000 01100001 01101100 01101100 00100000 01110100 01101000 01100101 00100000 01101111 01110000 01101111 01110000 01110100 01110101 01101110 01101001 01110100 01101001 01100101 01110011 00100000 01111001 01101111 01110101 00100000 01101000 01100001 01100100 00101110 00101110 00101110 ","not found", "NOT FOUND 0x10000"]
            main()
            wrong = 1
        if choice.lower() == "" and cursor_position == 0:
            choosecharacter()
            
        elif choice.lower() == "" and cursor_position == 1:
            clear()
            load_game()
            start()
            print("load")
            
        elif choice.lower() == "" and cursor_position == 2:
            print("Exiting the game...")
            break
        elif choice.lower() == "up":
            cursor_position = (cursor_position - 1) % 3
        elif choice.lower() == "down":
            cursor_position = (cursor_position + 1) % 3

def choosecharacter():
    global damage, coins, items, health, num_items, shop_items
    print('''
Characters:
    · Pablo
    · Mateo
    · Manuel
    · Hernan
''')
    char = input("Choose: ")

    if char == "Pablo":
        items = ["dice"]
        damage = 10
        health = 30
    elif char == "Mateo":
        items = ["holy_mantle"]
        damage = 10
        health = 20
    elif char == "Manuel":
        damage = 7
        health = 40
        coins = 100
    elif char == "Hernan":
        health = 50
        damage = 15
    num_items = random.randint(1, 3)
    shop_items = random.sample(possible_items, num_items)
    clear()
    start()


if __name__ == "__main__":
            main()

