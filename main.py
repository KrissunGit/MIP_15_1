import random
import pygame

def generatelist(length):
    global number_list
    number_list = []
    for i in range(length):
        number_list.append(random.randint(1, 4))
    return number_list

def generate_button_pos(number_list, total_width=1280, spacing=10):
    rects = []
    n = len(number_list)
    if n == 0:
        return rects
    square_size = 45
    total_group_width = (n * square_size) + ((n - 1) * spacing)
    start_x = (total_width - total_group_width) // 2
    for i in range(n):
        x = start_x + (i * (square_size + spacing))
        new_rect = pygame.Rect(x, screen_height // 2 - 22.5, square_size, square_size)
        rects.append(new_rect)
    return rects

def ai(number_list):
    for i in number_list:
        pass

def split_func(number_list, index):
    result = number_list[index] // 2
    number_list.pop(index)
    number_list.insert(index,result)
    number_list.insert(index+1,result)
    return number_list

def minimax(current_list, depth, is_maximizing):
    if len(current_list) == 0 or depth == 0:
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(len(current_list)):
            temp_take = current_list[:]
            val = temp_take.pop(i)
            score_take = val + minimax(temp_take, depth - 1, False)
            best_score = max(best_score, score_take)

            if current_list[i] in [2, 4]:
                temp_split = current_list[:]
                bonus = 1 if temp_split[i] == 4 else 0
                
                val_to_split = temp_split.pop(i)
                res = val_to_split // 2
                temp_split.insert(i, res)
                temp_split.insert(i + 1, res)
                
                score_split = bonus + minimax(temp_split, depth - 1, False)
                best_score = max(best_score, score_split)
        return best_score
    else:
        best_score = float('inf')
        for i in range(len(current_list)):
            temp_take = current_list[:]
            val = temp_take.pop(i)
            score = minimax(temp_take, depth - 1, True) - val
            best_score = min(best_score, score)
            
            if current_list[i] in [2, 4]:
                temp_split = current_list[:]
                bonus = 1 if temp_split[i] == 4 else 0
                val_to_split = temp_split.pop(i)
                res = val_to_split // 2
                temp_split.insert(i, res)
                temp_split.insert(i + 1, res)
                
                score_split = minimax(temp_split, depth - 1, True) - bonus
                best_score = min(best_score, score_split)
        return best_score

pygame.init()

player_points = 0
ai_points = 0
turn = 1
whos_turn = "PLAYER"
number_list = []
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

state = "START"
choice = "TAKE"
user_text = ""
input_rect = pygame.Rect(540, 300, 200, 45)
active = False
running = True

msg = font.render("Enter list length and press ENTER", True, "white")
msg_location = screen_width // 2 - 235

split_btn_rect = pygame.Rect(screen_width // 2 - 110, screen_height // 2 + 100, 100, 50)
take_btn_rect = pygame.Rect(screen_width // 2 + 10, screen_height // 2 + 100, 100, 50)
selected_index = -1 

while running:
    mouse_pos = pygame.mouse.get_pos()
    point_counter = font.render(f"{player_points} - {ai_points}", True, "white")
    turn_counter = font.render(f"{turn} gājiens", True, "white")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "START":
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_rect.collidepoint(event.pos)

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if user_text.isdigit() and 15 <= int(user_text) <= 20:
                            numbers = generatelist(int(user_text))
                            state = "PLAYING"
                            player_points = 0
                            ai_points = 0
                            turn = 1
                            whos_turn = "PLAYER"
                        else:
                            msg_location = screen_width // 2 - 175
                            msg = font.render("Outside of scope(15-20)", True, "white")
                            user_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        elif state == "PLAYING":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if whos_turn == "PLAYER":
                    square_rects = generate_button_pos(numbers)
                    for index, rect in enumerate(square_rects):
                        if rect.collidepoint(event.pos):
                            val = numbers[index]
                            if val in [2,4]:
                                selected_index = index 
                                state = "DECIDING"    
                            else:
                                player_points += val
                                numbers.pop(index)
                                if len(numbers) == 0:
                                    state = "END"
                                else:
                                    whos_turn = "AI"
                                    turn += 1
                            break

        elif state == "DECIDING":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if split_btn_rect.collidepoint(event.pos):
                    if numbers[selected_index] == 4: 
                        player_points += 1
                    
                    split_func(numbers, selected_index)
                    state = "PLAYING"
                    whos_turn = "AI"
                    turn += 1

                elif take_btn_rect.collidepoint(event.pos):
                    player_points += numbers[selected_index]
                    numbers.pop(selected_index)
                    state = "PLAYING"
                    whos_turn = "AI"
                    turn += 1
                else:
                    state = "PLAYING"
                    selected_index = -1

                if len(numbers) == 0: 
                    state = "END"

        elif state == "END":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    user_text = ""
                    state = "START"

    screen.fill("gray30")

    if state == "START":
        screen.blit(msg, (msg_location, 250))
        box_color = "white" if active else "gray"
        pygame.draw.rect(screen, box_color, input_rect, 2)
        text_surf = font.render(user_text, True, "white")
        screen.blit(text_surf, (input_rect.x + 5, input_rect.y + 5))

    elif state == "PLAYING" or state == "DECIDING":
        square_rects = generate_button_pos(numbers)
        screen.blit(point_counter, (screen_width // 2 - 50, 100))
        screen.blit(turn_counter, (screen_width // 2 - 50, 50))

        for index, rect in enumerate(square_rects):
            color = "cyan" if rect.collidepoint(mouse_pos) and whos_turn == "PLAYER" else "blue"
            pygame.draw.rect(screen, color, rect)
            val_surf = font.render(str(numbers[index]), True, "white")
            val_rect = val_surf.get_rect(center=rect.center)
            screen.blit(val_surf, val_rect)

        if whos_turn == "AI" and state == "PLAYING" and numbers:
            pygame.display.flip()
            pygame.time.delay(50)
            
            best_val = -float('inf')
            ai_idx = 0
            for i in range(len(numbers)):
                temp = numbers[:]
                v = temp.pop(i)
                res = v + minimax(temp, 4, False)
                if res > best_val:
                    best_val, ai_idx = res, i
            
            ai_points += numbers[ai_idx]
            numbers.pop(ai_idx)
            if not numbers: state = "END"
            else: whos_turn = "PLAYER"
            turn += 1

        if state == "DECIDING":
            pygame.draw.rect(screen, "green", split_btn_rect)
            split_txt = font.render("SPLIT", True, "black")
            screen.blit(split_txt, (split_btn_rect.x + 10, split_btn_rect.y + 10))

            pygame.draw.rect(screen, "red", take_btn_rect)
            take_txt = font.render("TAKE", True, "white")
            screen.blit(take_txt, (take_btn_rect.x + 15, take_btn_rect.y + 10))
            
            pygame.draw.rect(screen, "yellow", square_rects[selected_index], 4)

    elif state == "END":
        end_msg = font.render(f"Player points: {player_points} AI points: {ai_points}", True, "green")
        screen.blit(end_msg, (screen_width // 2 - 320, screen_height // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()