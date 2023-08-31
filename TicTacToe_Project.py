import os

def validate_name():
    valid_name = False
    
    while not valid_name:
        name = input("Insert a name:")
        
        if isValid(name):
            valid_name = True
            return name
        else:
            print("Please enter a valid name! Without Colons or Line break!!")
            
def isValid(name):
    if name == "":
        return False
    
    invalid_chars = [':', ';', '\\n']
    
    for i in range(len(invalid_chars)):
        if str(name).__contains__(invalid_chars[i]):  
            return False
        
    return True      

def printGrid(grid):
    for row in grid:
        print(' | '.join(row))
        if row != grid[-1]:
            print('---------')

def play(grid, x, y, g):
    if grid[x][y] == ' ':
        grid[x][y] = g
        return True
    return False

def checkRow(grid, x, g):
    return all(cell == g for cell in grid[x])

def checkColumn(grid, y, g):
    return all(row[y] == g for row in grid)

def checkDiagonal1(grid, g):
    return all(grid[i][i] == g for i in range(3))

def checkDiagonal2(grid, g):
    return all(grid[i][2 - i] == g for i in range(3))

def Winner(grid, g):
    for i in range(3):
        if checkRow(grid, i, g) or checkColumn(grid, i, g):
            return True
    if checkDiagonal1(grid, g) or checkDiagonal2(grid, g):
        return True
    return False

def update_scores(scores, player1, player2, result):
    if result == 'draw':
        scores[player1] += 1
        scores[player2] += 1
    elif result == player1:
        scores[player1] += 2
    else:
        scores[player2] += 2

def save_scores(filename, scores):
    with open(filename, 'w') as file:
        for player, score in scores.items():
            file.write(f"{player}:{score}\n")

def load_scores(filename):
    scores = {}
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                player, score = line.strip().split(':')
                scores[player] = int(score)
    return scores

def main():

    player1 = validate_name()
    player2 = validate_name()
    
    print(f"Valid name: {player1}")
    print(f"Valid name: {player2}")
    
    filename = "TicTacToe_Scores.txt"

    scores = load_scores(filename)
    if player1 not in scores:
        scores[player1] = 0
    if player2 not in scores:
        scores[player2] = 0

    while True:
        grid = [[' ' for _ in range(3)] for _ in range(3)]
        player_turn = player1
        print("New play!")
        printGrid(grid)
        while True:
            print(f"{player_turn}'s turn")
            row = int(input("Choose the row (0, 1 or 2): "))
            col = int(input("Choose the column (0, 1 or 2): "))
            if play(grid, row, col, 'X' if player_turn == player1 else 'O'):
                printGrid(grid)
                if Winner(grid, 'X'):
                    print(f"Congratulations {player1}, you win!")
                    update_scores(scores, player1, player2, player1)
                    save_scores(filename, scores)
                    break
                elif Winner(grid, 'O'):
                    print(f"Congratulations {player2}, you win!")
                    update_scores(scores, player1, player2, player2)
                    save_scores(filename, scores)
                    break
                elif all(cell != ' ' for row in grid for cell in row):
                    print("It's a draw!")
                    update_scores(scores, player1, player2, 'draw')
                    save_scores(filename, scores)
                    break
                player_turn = player2 if player_turn == player1 else player1

        play_again = input("Do you want do play again? (Y/N): ").upper()
        if play_again != 'Y':
            break

if __name__ == "__main__":
    
    main()
