#Attempt to create sudoku puzzle game
#Starting with a 9x9 grid

#Create a 9x9 grid

import random
import pygame
import copy

Screen_Width = 720
Screen_Height = 540

pygame.init()
    
screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Sudoku")

block_width = (Screen_Width-180) // 9

font = pygame.font.SysFont('Consolas', 30)
        

x = -1
y = -1

empty_value = 0

empty_grid = [[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0]]

sudoku_puzzles = [[[0,8,7,5,0,2,9,0,0],[0,0,0,8,0,3,1,0,0],[0,0,0,0,1,0,5,0,0],
                   [0,0,9,7,8,0,0,0,0],[0,2,0,0,0,4,0,8,0],[0,0,0,6,0,0,0,0,0],
                   [5,0,8,0,0,0,0,6,0],[7,0,1,0,6,0,0,0,4],[3,0,0,0,0,9,0,1,0]],
                  
                  [[9,0,8,5,0,0,0,7,0],[0,0,5,6,0,0,1,0,8],[6,0,1,0,0,7,9,4,5],
                   [0,2,0,0,0,6,0,5,0],[7,0,0,2,1,0,0,0,3],[0,0,9,0,0,0,4,8,0],
                   [0,0,7,9,6,2,0,1,4],[0,9,0,0,8,0,3,6,7],[0,0,0,3,0,4,8,0,0]],
                  
                  [[8,1,0,5,0,7,0,9,0],[5,0,0,6,0,9,0,0,4],[0,4,0,0,0,1,0,5,0],
                   [0,0,0,3,0,5,4,2,0],[0,3,0,2,0,8,5,0,0],[0,0,2,1,9,0,0,6,0],
                   [3,6,0,0,0,0,0,0,1],[9,0,5,7,1,3,6,0,0],[0,0,0,4,8,6,0,0,0]],
                  
                  [[0,0,3,0,9,0,0,5,2],[0,1,5,0,0,0,7,0,0],[4,0,0,0,0,8,3,0,0],
                   [0,0,0,0,0,1,0,2,7],[8,0,0,9,2,0,0,0,0],[0,5,0,4,7,3,1,9,8],
                   [0,0,2,6,0,5,0,0,4],[5,0,0,0,0,4,0,0,0],[0,0,0,0,0,0,8,0,0]]]

current_grid = random.choice(sudoku_puzzles)
user_grid = copy.deepcopy(current_grid)
copy_grid = copy.deepcopy(current_grid)


def main():
    global current_grid
    global user_grid
    global copy_grid
    
    solve_sudoku(current_grid)

    
    draw_grid()  
    
    clock = pygame.time.Clock()
    timer_font = pygame.font.SysFont('Consolas', 20)
    
    seconds = 0
    minutes = 0
    timer_text = timer_font.render(f'Time: {minutes:02}:{seconds:02} ', True, (0,255,0))
    
    
    RandomPuzzle_button = pygame.draw.rect(screen, (50, 200, 50), (720 - 170, 60, 150, 30))
    RandomPuzzle_text = timer_font.render('Random Puzzle', True, (255, 255, 255))
    screen.blit(RandomPuzzle_text, (720 - 170 + 8, 60 + 8))


    check_button = pygame.draw.rect(screen, (50, 200, 50), (720 - 170, 100, 150, 30))
    check_text = timer_font.render('Check Answer', True, (255, 255, 255))
    screen.blit(check_text, (720 - 170 + 18, 100 + 5))

    solve_button = pygame.draw.rect(screen, (50, 200, 50), (720 - 170, 140, 150, 30))
    solve_text = timer_font.render('Solve', True, (255, 255, 255))
    screen.blit(solve_text, (720 - 170 + 48, 140 + 5))
    
    
    pygame.display.update()
    
    
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    
    while True:
        clock.tick(60)
        #set up event listener
        for event in pygame.event.get():
            
            if event.type == timer_event:
                seconds += 1
                if seconds == 60:
                    seconds = 0
                    minutes += 1
                timer_text = timer_font.render(f'Time: {minutes:02}:{seconds:02} ', True, (0,255,0))
            draw_timer(timer_text)
            pygame.display.flip()
            
            if event.type == pygame.QUIT:
                draw_solved_grid()
                pygame.display.update()
                pygame.time.delay(2000)
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if RandomPuzzle_button.collidepoint(pos):
                    Random_Puzzle()
                    seconds = 0
                    minutes = 0
                    time_text = timer_font.render(f'Time: {minutes:02}:{seconds:02} ', True, (0,255,0))
                    draw_timer(time_text)
                elif check_button.collidepoint(pos):
                    check_user_ans(timer_event)
                elif solve_button.collidepoint(pos):
                    solve_puzzle(timer_event)
                else:
                    start(timer_event)
                    change_values()
                pygame.display.update()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    fill_square(1)
                elif event.key == pygame.K_2:
                    fill_square(2)
                elif event.key == pygame.K_3:
                    fill_square(3)
                elif event.key == pygame.K_4:
                    fill_square(4)
                elif event.key == pygame.K_5:
                    fill_square(5)
                elif event.key == pygame.K_6:
                    fill_square(6)
                elif event.key == pygame.K_7:
                    fill_square(7)
                elif event.key == pygame.K_8:
                    fill_square(8)
                elif event.key == pygame.K_9:
                    fill_square(9)
                elif event.key == pygame.K_BACKSPACE:
                    fill_square(empty_value)
                pygame.display.update()
        continue
    
def draw_timer(timer_text):
        screen.fill((0, 0, 0), (Screen_Width - 170, 20, 150, 30))
        screen.blit(timer_text, (Screen_Width - 170, 20))
            
#function to draw and fill grid
def draw_grid():
    for i in range (9):
        for j in range(9):
            if user_grid[i][j] == empty_value:
                #draw white square
                pygame.draw.rect(screen, (255, 255, 255), (i*block_width,j*block_width,block_width+1, block_width+1))
            else:
                #draw yellow square and fill in number
                if(current_grid[i][j] == user_grid[i][j]):
                    pygame.draw.rect(screen, (255, 255, 0,), (i*block_width,j*block_width,block_width+1, block_width+1))
                    text = font.render(str(current_grid[i][j]), True, (0, 0, 0))
                else:
                    if (i,j) in error_coords:    
                        pygame.draw.rect(screen, (255, 0, 0), (i*block_width,j*block_width,block_width+1, block_width+1))
                    else:
                        pygame.draw.rect(screen, (255, 0, 255), (i*block_width,j*block_width,block_width+1, block_width+1))
                    text = font.render(str(user_grid[i][j]), True, (0, 0, 0))
                screen.blit(text, (i*block_width + 20, j*block_width + 20))
    draw_lines()

def draw_lines():
    for l in range(10):
        if l % 3 == 0 :
            thick = 7
        else:
            thick = 1
        #draw lines
        #horizontal
        pygame.draw.line(screen, (0, 0, 255), (0, l * block_width), (Screen_Width-180, l * block_width), thick)
        #vertical
        pygame.draw.line(screen, (0, 0, 255), (l * block_width, 0), (l * block_width, Screen_Height), thick)
        

def draw_solved_grid():
    for i in range (9):
        for j in range(9):
            #draw yellow square and fill in number - display given
            if(current_grid[i][j] == solved_grid[i][j]):
                pygame.draw.rect(screen, (255, 255, 0,), (i*block_width,j*block_width,block_width+1, block_width+1))
                text = font.render(str(current_grid[i][j]), True, (0, 0, 0))
            #shows answers
            else:
                pygame.draw.rect(screen, (144, 238, 144), (i*block_width,j*block_width,block_width+1, block_width+1))  # Light green color
                text = font.render(str(solved_grid[i][j]), True, (0, 0, 0))
            screen.blit(text, (i*block_width + 20, j*block_width + 20))
    draw_lines()           

    
    
#function to change x and y values
def change_values():
    global x
    global y
    #check if block is computer filled
    check_x = (pygame.mouse.get_pos()[0] // block_width)
    check_y = (pygame.mouse.get_pos()[1] // block_width)
    #if computer filled, return
    if(current_grid[check_x][check_y] != empty_value):
        return
    
    #if same square clicked, return
    if(check_x == x and check_y == y):
        pygame.draw.rect(screen, (255, 255, 255), (x*block_width, y*block_width, block_width+1, block_width+1))
        draw_grid()  
        x = -1
        y = -1
        return

    #reset previous square
    pygame.draw.rect(screen, (255, 255, 255), (x*block_width, y*block_width, block_width+1, block_width+1))
    draw_grid()
    #set up values for new square
    x = (pygame.mouse.get_pos()[0] // block_width)
    y = (pygame.mouse.get_pos()[1] // block_width)
    selected_square(x, y)
    return
    
#function to show selected square
def selected_square(x, y):
    #draw black square that is transparent - cannot be done with pygame.draw.rect
    s = pygame.Surface((block_width, block_width))  
    s.set_alpha(128)  # Alpha level for transparency (0 is fully transparent, 255 is fully opaque)
    s.fill((0, 0, 0))  # Fill the surface with black color
    screen.blit(s, (x * block_width, y * block_width))
    draw_lines()
    return

#function to fill square by user
def fill_square(value):
    user_grid[x][y] = value
    problem = check_repeats(user_grid)
    if problem:
        text = font.render(str(value), True, (255,0,0))
    else:
        text = font.render(str(value), True, (0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (x * block_width, y * block_width, block_width + 1, block_width + 1))
    selected_square(x, y)
    screen.blit(text, (x*block_width + 20, y*block_width + 20))
    return

def check_repeats(grid):
    global error_coords
    error_coords = []
    for i in range(9):
        for j in range(9):
            if (grid[i][j] != empty_value):
                    #check row
                    for row in range(9):
                        if grid[i][j] == grid[i][row] and j != row:
                            error_coords.append((i, row))
                            
                    #check column
                    for col in range(9):
                        if grid[i][j] == grid[col][j] and i != col:
                            error_coords.append((col, j))
                            
                    #check square
                    for k in range(3):
                        for l in range(3):
                            if grid[i][j] == grid[i//3*3 + k][j//3*3 + l] and (i != i//3*3 + k or j != j//3*3 + l):
                                error_coords.append((i//3*3 + k, j//3*3 + l))
    if len(error_coords) == 0:
        return False              
    else:
        return True


#function to solve sudoku
#backtracking algorithm
def solve_sudoku(grid):
    global solved_grid
    solved_grid = copy.deepcopy(grid)  
    #loop through grid
    for i in range(9):
        for j in range(9):
            #check if square is empty
            if solved_grid[i][j] == empty_value:
                #loop through numbers 1-9
                for k in range(1, 10):
                    #put number in square
                    solved_grid[i][j] = k
                    #check if number causes a repeat
                    if not check_repeats(solved_grid):
                        #if no repeat, recursively call function
                        #attempt moving to next square
                        if solve_sudoku(solved_grid):
                            #this ends functions
                            #once all square filled
                            return True
                    #if a repeat or solve fails
                    #reset square to empty
                    solved_grid[i][j] = empty_value
                #if all numbers tried and no solution
                return False
    #if all squares filled return True
    return True

def Random_Puzzle():
    global user_grid
    global copy_grid
    global current_grid
    current_grid = random.choice(sudoku_puzzles)
    user_grid = copy.deepcopy(current_grid)
    copy_grid = copy.deepcopy(current_grid)
    solved_grid = copy.deepcopy(current_grid)
    draw_grid()

    

def check_user_ans(timer_event):
    print('Check')
    timer_font = pygame.font.SysFont('Consolas', 15)
    if (user_grid == solved_grid):
        #text display
        Result_text = timer_font.render('Result: Correct', True, (255, 255, 255))
        screen.blit(Result_text, (720 - 170, 180))
        print('Correct')
    else: 
        Result_text = timer_font.render('Result: Incorrect', True, (255, 255, 255))
        screen.blit(Result_text, (720 - 170, 180))
        Result_text = timer_font.render('Continue Working', True, (255, 255, 255))
        screen.blit(Result_text, (720 - 170, 200))
        print('Incorrect')
    pygame.time.set_timer(timer_event, 0)
    return

def solve_puzzle(timer_event):  
    print('Solve')
    draw_solved_grid()
    pygame.display.update()
    pygame.time.set_timer(timer_event, 0)
    return

def start(timer_event):
    print('Start')
    pygame.time.set_timer(timer_event,1000)
    return    

main()
        