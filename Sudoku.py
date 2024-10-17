#Attempt to create sudoku puzzle game

#set up imports
import random
import pygame
import copy

#set up screen size
Screen_Width = 720
Screen_Height = 540

#initialise pygame
pygame.init()
    
#set up screen and caption
screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Sudoku")

#set up block width for grid
block_width = (Screen_Width-180) // 9

#set up main font
font = pygame.font.SysFont('Consolas', 30)
      
#set up positional variables  
x = -1
y = -1

#set up empty value
empty_value = 0
#if puzzle is shown
shown = False

#set up empty grid
empty_grid = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]

#set up array of sudoku puzzles
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

#set up grids
current_grid = random.choice(sudoku_puzzles)
user_grid = copy.deepcopy(current_grid)


def main():
    #set global variables
    global current_grid
    global user_grid
    global shown
    
    #solve puzzle
    solve_sudoku(current_grid)
    
    #draw grid    
    draw_grid()  
    
    #set up timer
    clock = pygame.time.Clock()
    timer_font = pygame.font.SysFont('Consolas', 20)
    seconds = 0
    minutes = 0
    timer_text = timer_font.render(f'Time: {minutes:02}:{seconds:02} ', True, (0,255,0))
    draw_timer(timer_text)
    
    #set up buttons
    RandomPuzzle_button = pygame.draw.rect(screen, (50, 200, 50), (720 - 170, 60, 150, 30))
    RandomPuzzle_text = timer_font.render('Random Puzzle', True, (255, 255, 255))
    screen.blit(RandomPuzzle_text, (720 - 170 + 8, 60 + 8))

    check_button = pygame.draw.rect(screen, (50, 200, 50), (720 - 170, 100, 150, 30))
    check_text = timer_font.render('Check Answer', True, (255, 255, 255))
    screen.blit(check_text, (720 - 170 + 18, 100 + 5))

    solve_button = pygame.draw.rect(screen, (50, 200, 50), (720 - 170, 140, 150, 30))
    solve_text = timer_font.render('Solve', True, (255, 255, 255))
    screen.blit(solve_text, (720 - 170 + 48, 140 + 5))
    
    #update screen
    pygame.display.update()
    
    #set up timer event and start timer
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    
    #main loop
    while True:
        #set up clock ticks
        clock.tick(60)
        
        #set up event listener
        for event in pygame.event.get():
            #update timer
            if event.type == timer_event:
                seconds += 1
                if seconds == 60:
                    seconds = 0
                    minutes += 1
                timer_text = timer_font.render(f'Time: {minutes:02}:{seconds:02} ', True, (0,255,0))
            draw_timer(timer_text)
            pygame.display.flip()
            
            #check if user quits
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            #check if user clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                #get position of mouse
                pos = pygame.mouse.get_pos()
                #check if button clicked
                if RandomPuzzle_button.collidepoint(pos):
                    shown = False
                    Random_Puzzle()
                    seconds = 0
                    minutes = 0
                    time_text = timer_font.render(f'Time: {minutes:02}:{seconds:02} ', True, (0,255,0))
                    draw_timer(time_text)
                #check if button clicked
                elif check_button.collidepoint(pos):
                    check_user_ans(timer_event)
                #check if button clicked
                elif solve_button.collidepoint(pos):
                    solve_puzzle(timer_event)
                else:
                    if not shown:
                        #if not button clicked, ensure timer is running
                        start(timer_event)
                        #change values
                        change_values()
                #update screen
                pygame.display.update()
                
            #check if user types
            if event.type == pygame.KEYDOWN:
                #fill square with number
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
                #update screen
                pygame.display.update()
        continue
    
#function to draw timer
def draw_timer(timer_text):
    #erase previous timer
    screen.fill((0, 0, 0), (Screen_Width - 170, 20, 150, 30))
    #draw new timer
    screen.blit(timer_text, (Screen_Width - 170, 20))
            
#function to draw and fill grid
def draw_grid():
    #loop through grid
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
                        #draw red square if error    
                        pygame.draw.rect(screen, (255, 0, 0), (i*block_width,j*block_width,block_width+1, block_width+1))
                    else:
                        #draw purple square if user filled
                        pygame.draw.rect(screen, (255, 0, 255), (i*block_width,j*block_width,block_width+1, block_width+1))
                    text = font.render(str(user_grid[i][j]), True, (0, 0, 0))
                #fill in number
                screen.blit(text, (i*block_width + 20, j*block_width + 20))
    #draw lines
    draw_lines()

#function to draw lines
def draw_lines():
    #alternate line thickness
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
        

#function to draw solved grid
def draw_solved_grid():
    global shown
    shown = True
    #loop through grid
    for i in range (9):
        for j in range(9):
            #draw yellow square and fill in number - display given
            if(current_grid[i][j] == solved_grid[i][j]):
                pygame.draw.rect(screen, (255, 255, 0,), (i*block_width,j*block_width,block_width+1, block_width+1))
                text = font.render(str(current_grid[i][j]), True, (0, 0, 0))
            #shows answers in green
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
    #if computer filled, return or out of bounds
    if((check_x > 8 or check_y>8) or current_grid[check_x][check_y] != empty_value):
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
    #draw grid to reflect change
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
    #edit user grid
    user_grid[x][y] = value
    #checks for repeats and changes text color
    if check_repeats(user_grid):
        text = font.render(str(value), True, (255,0,0))
    else:
        text = font.render(str(value), True, (0, 0, 0))
    #draw block
    pygame.draw.rect(screen, (255, 255, 255), (x * block_width, y * block_width, block_width + 1, block_width + 1))
    #reselect square
    selected_square(x, y)
    #fill in number
    screen.blit(text, (x*block_width + 20, y*block_width + 20))
    return

#function to check for repeats
def check_repeats(grid):
    #set up global variables
    global error_coords
    error_coords = []
    #loop through grid
    for i in range(9):
        for j in range(9):
            #check if square is empty
            if (grid[i][j] != empty_value):
                #if not empty, check for repeats
                    #check in row
                    for row in range(9):
                        if grid[i][j] == grid[i][row] and j != row:
                            error_coords.append((i, row))
                            
                    #check in column
                    for col in range(9):
                        if grid[i][j] == grid[col][j] and i != col:
                            error_coords.append((col, j))
                            
                    #check in square
                    for k in range(3):
                        for l in range(3):
                            if grid[i][j] == grid[i//3*3 + k][j//3*3 + l] and (i != i//3*3 + k or j != j//3*3 + l):
                                error_coords.append((i//3*3 + k, j//3*3 + l))
    #return if any errors
    if len(error_coords) == 0:
        return False              
    else:
        return True


#function to solve sudoku
#all good sudokus have a solution
#backtracking algorithm
def solve_sudoku(grid):
    #set up global variables
    global solved_grid
    #deep copy grid
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

#create function to draw random puzzle
def Random_Puzzle():
    #redeclare global variables
    global user_grid, current_grid, solved_grid
    #get new grid
    new_grid = random.choice(sudoku_puzzles)
    #repeat until new grid is different
    while( new_grid == current_grid):
        new_grid = random.choice(sudoku_puzzles)
    #set up grids
    current_grid = new_grid
    user_grid = copy.deepcopy(current_grid)
    solve_sudoku(current_grid)
    #draw grid
    draw_grid()
    return

#function to check user answer
def check_user_ans(timer_event):
    print('Check')
    if shown:
        return
    #reset font
    font = pygame.font.SysFont('Consolas', 15)
    #check if same as solved grid
    #if correct, display correct
    if (user_grid == solved_grid):
        #text display
        Result_text = font.render('Result: Correct', True, (255, 255, 255))
        screen.blit(Result_text, (720 - 170, 180))
        print('Correct')
    else: 
        #if incorrect, display incorrect
        Result_text = font.render('Result: Incorrect', True, (255, 255, 255))
        screen.blit(Result_text, (720 - 170, 180))
        Result_text = font.render('Continue Working', True, (255, 255, 255))
        screen.blit(Result_text, (720 - 170, 200))
        print('Incorrect')
    
    #update screen
    pygame.display.update()
    #stop timer
    pygame.time.set_timer(timer_event, 0)
    
    # Set a timer for 5 seconds based on USEREVENT + 2(new event)
    pygame.time.set_timer(pygame.USEREVENT + 2, 5000)
    while True:
        # Check if the event is triggered
        event = pygame.event.wait()
        if event.type == pygame.USEREVENT + 2:
            # Clear the result text area
            screen.fill((0, 0, 0), (720 - 170, 180, 150, 50))  # Clear the result text area
            break
    #update screen
    pygame.display.update()
    #start timer
    start(timer_event)
    return

#function to solve puzzle
def solve_puzzle(timer_event):  
    print('Solve')
    #draw solved grid
    draw_solved_grid()
    #update screen
    pygame.display.update()
    #stop timer
    pygame.time.set_timer(timer_event, 0)
    return

#function to start timer
def start(timer_event):
    print('Start')
    #start timer
    pygame.time.set_timer(timer_event,1000)
    return    


#run main
main()
        