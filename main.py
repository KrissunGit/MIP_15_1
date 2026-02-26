import random

player_1_point_score = 0
player_2_point_score = 0
possible_nums = [1, 2, 3, 4]
cur_row = []
num_of_turns = 0

def generate_row(length):
    cur_row.append(random.choice(possible_nums))
    length -= 1
    if length > 0:
        generate_row(length)
    else:
        pass

def print_row():
    for i in cur_row:
        print(i, end=" ")    

def player_take_num(player, taken_index):
    global player_1_point_score
    global player_2_point_score
    match player:
        case 1:
            player_1_point_score += int(cur_row[taken_index])
        case 2:
            player_2_point_score += int(cur_row[taken_index])
    cur_row.pop(taken_index)

def player_split_num(player, split_index):
    global player_1_point_score
    global player_2_point_score
    match cur_row[split_index]:
        case 2:
            cur_row.pop(split_index)
            cur_row.insert(split_index, 1)
            cur_row.insert(split_index, 1)
        case 4:
            match player:
                case 1:
                    player_1_point_score += 1
                case 2:
                    player_2_point_score += 1
            cur_row.pop(split_index)
            cur_row.insert(split_index, 2)
            cur_row.insert(split_index, 2)

def end_game():
    global player_1_point_score
    global player_2_point_score
    if player_1_point_score > player_2_point_score:
        print("Player 1 wins!")
    elif player_2_point_score > player_1_point_score:
        print("Player 2 wins!")
    else:
        print("It's a tie!")
    quit()

def end_game_check():
    if len(cur_row) == 0:
        print("Game over!")
        end_game()

def player_take_turn():
    Possible_Action_List = get_possible_actions()
    print(Possible_Action_List)
    player_action_input_text = "Would you like to "
    for i in Possible_Action_List:
        player_action_input_text += ", "
        player_action_input_text += str(i)
    PlayerAction = input(player_action_input_text).upper()
    match PlayerAction:
        case "TAKE":
            Player_Decide_Which_Goddamn_Number_To_Take()
        case "SPLIT2":
            player_split_num(1, cur_row.index(2))
        case "SPLIT4":
            player_split_num(1, cur_row.index(4))
        case _:
            player_take_turn()

def Player_Decide_Which_Goddamn_Number_To_Take():
    res = sorted(list(dict.fromkeys(cur_row)))
    player_action_text = "You can take: "
    for i in res:
        player_action_text += str(i)
        player_action_text += " "
    playeraction = int(input(player_action_text))
    print(playeraction)
    match playeraction:
        case 1:
            player_take_num(1, cur_row.index(1))
        case 2:
            player_take_num(1, cur_row.index(2))
        case 3:
            player_take_num(1, cur_row.index(3))
        case 4:
            player_take_num(1, cur_row.index(4))
        case _:
            Player_Decide_Which_Goddamn_Number_To_Take()

def get_possible_actions():
    PossibleActions = ['TAKE']
    if 2 in cur_row:
        PossibleActions.append('SPLIT2')
    if 4 in cur_row:
        PossibleActions.append('SPLIT4')
    return PossibleActions

def ai_take_turn(): #TO DO - aizvietot ar AI :D
    Random_AI_Choice = random.choice(get_possible_actions())
    match Random_AI_Choice:
        case 'TAKE':
            rand_choice = random.randint(0, len(cur_row)-1)
            print(f"AI takes {cur_row[rand_choice]}")
            player_take_num(2, rand_choice)
        case 'SPLIT2':
            player_split_num(2, cur_row.index(2))
            print("AI splits two")
        case 'SPLIT4':
            player_split_num(2, cur_row.index(4))
            print("AI splits four")

### virknes garuma inputiņš :)
length_of_row = int(input("choose length for row: between 15 and 20 "))
if length_of_row < 15 or length_of_row > 20:
    print("too short or too long! pick between 15-20")
else:
    generate_row(length_of_row)

#Main Game Loop - this is idiotic but for a first prototype good enough
while True:
    print_row()
    print(f"POINTS: {player_1_point_score} - {player_2_point_score}")
    player_take_turn()
    print_row()
    print(f"POINTS: {player_1_point_score} - {player_2_point_score}")
    end_game_check()
    ai_take_turn()
    end_game_check()
    print(f"POINTS: {player_1_point_score} - {player_2_point_score}")
