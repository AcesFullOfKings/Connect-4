import random
from time import sleep
from copy import deepcopy

class ColumnFullException(Exception):
    def __init__(self, value):
         self.value = value
    def __str__(self):
         return repr(self.value)

class OutOfRangeException(Exception):
    def __init__(self, value):
         self.value = value
    def __str__(self):
         return repr(self.value)

class player:
    def set_name(self, new_name):
        self.name = new_name
    def get_name(self):
        return self.name
    def set_colour(self, colour):
        self.colour = colour

class human(player):
    def __init__(self, name):
        self.type = "human"
        self.set_name(name)

    def make_move(self, board):
        while True:
            try:
                move = int(input(self.get_name() + ", make a move: "))
                if move not in range(0,7):
                    raise OutOfRangeException("Column index out of range.")
                if not board.column_full(move):
                    return move
                else:
                    raise ColumnFullException
            except ValueError:
                print("Not an integer! Try again.")
            except OutOfRangeException:
                print("Must be between 0 and 6")
            except ColumnFullException:
                print("Column is full - choose another.")
            else:
                return move

class bot(player):
    def __init__(self, name):
        self.type = "bot"
        self.set_name(name)

    def make_move(self, board):
        move_score = [0] * 7 # score for each of 7 possible moves is initialised to 0

        enemy = human("e")

        if self.colour == "x":
            enemy.colour = "o"
        else:
            enemy.colour = "x"

        for i in range(7): # move into a winning column if one exists
            board_copy_1 = deepcopy(board)
            try:
                if board_copy_1.move(self, i) == "win":
                    return i
                else:
                    move_score[i] = self.assess_board(board_copy_1, self.colour)
                for j in range(7):
                    board_copy_2 = deepcopy(board_copy_1)
                    
                    try:
                        if board_copy_2.move(enemy, i) == "win":
                            move_score[i] -= 1000
                        else:
                            move_score[i] -= self.assess_board(board_copy_2, enemy.colour)
                    except ColumnFullException:
                        pass
                #        board_copy_2 = deepcopy(board_copy)
                #        if board_copy_2.move(enemy, j) == "win":
                #            move_score[i] += -1
                #            raise ColumnFullException("")
                #    except ColumnFullException:
                #         pass
            except ColumnFullException:
                pass
            
        max = -999999
        moves = []
        for i in range(7):
            if not board.column_full(i):
                if move_score[i] > max:
                    max = move_score[i]
                    moves = [i]
                elif move_score[i] == max:
                    moves.append(i)

        while True:
            move = random.choice(moves)
            if not board.column_full(move):
                 return move
            else:
                moves.remove(move)
    def assess_board(self, board, colour):
        score = 0
        if colour == "x":
            enemy_colour = "o"
        else:
            enemy_colour = "x"

        """ Score is +1 for each possible win on the board.
            This means being closer to a win, ie having 3/4 pieces, is preferable as 
            that will score 3.
        """
        for c in range(7): # for each column
            column = board.board[c]
            for r in range(6): # for each row
                piece = column[r]
                if piece == colour: #for each of my pieces,
                    count = 0
                    potential_win = True
                    for i in range(-3,4): # vertical wins
                        try:
                            if r+i < 0 or i==0:
                                raise OutOfRangeException("")

                            if (board.board[c][r+i] == colour): #don't count the current piece?
                                count += 1
                            
                            if (board.board[c][r+i] == enemy_colour): #don't count the current piece?
                                potential_win = False
                            
                        except IndexError:
                            pass
                        except OutOfRangeException:
                            pass

                    if potential_win:
                        score += count**2

                    count = 0
                    potential_win = True
                    for i in range(-3,4): # horizontal wins
                        try:
                            if c+i < 0 or i==0:
                                raise OutOfRangeException("")

                            if board.board[c+i][r] == colour:
                                count += 1

                            if board.board[c+i][r] == enemy_colour:
                                potential_win = False
                        except IndexError:
                            pass
                        except OutOfRangeException:
                            pass

                    if potential_win:
                        score += count**2

                    count = 0
                    potential_win = True
                    for i in range(-3,4): # diagonal / wins
                        try:
                            if (r+i < 0) or (c+i < 0) or i==0:
                                raise OutOfRangeException("")

                            if board.board[c+i][r+i] == colour:
                                count += 1

                            if board.board[c+i][r+i] == enemy_colour:
                                potential_win = False
                        except IndexError:
                            pass
                        except OutOfRangeException:
                            pass

                    if potential_win:
                        score += count**2

                    count = 0
                    potential_win = True
                    for i in range(-3,4): # diagonal \ wins
                        try:
                            if (r+i < 0) or (c-i < 0) or i==0:
                                raise OutOfRangeException("")

                            if board.board[c-i][r+i] == colour:
                                count += 1

                            if board.board[c-i][r+i] == enemy_colour:
                                potential_win = False
                        except IndexError:
                            pass
                        except OutOfRangeException:
                            pass

                    if potential_win:
                        score += count**2
        return score
                    

class board():
    def __init__(self):
        self.board = [["-" for r in range(6)] for c in range(7)] # ref by board[column][row]

        # remeber 0 is the top row and 5 is the bottom row;
        # and 0 is the left column and 6 is the right column

    def move(self, player, column):
        if self.column_full(column):
            raise ColumnFullException("Invalid move - that column is full")
        else:
            row = self.next_row(column)
            self.board[column][row] = player.colour
            if self.is_win(row, column):
                return "win"
            return True

    def column_full(self, column):
        return self.next_row(column) == 7

    def next_row(self, column):
        for r in range(6):
            if self.board[column][r] ==  "-":
                return r
        return 7

    def show(self):
        for r in range(6)[::-1]: # row 0 is the bottom so should be printed last
            for c in range(7):
                print (self.board[c][r], end="")
                print ("|", end="")
            print ("")
        print("--------------")
        print("0 1 2 3 4 5 6\n")

    def is_win(self, r, c):
        def four_in_a_row(list, colour):
            if len(list) < 4:
                return False
        
            for i in range(len(list)-3):
                if list[i] == list[i+1] == list[i+2] == list[i+3] == colour:
                    return True
            return False
        
        b = self.board
        colour = b[c][r]

        win_list = []

        # vertical
        for i in range(6):
            try:
                if r - i < 0:
                    raise IndexError
                win_list.append(b[c][r-i])
            except IndexError:
                pass

        if four_in_a_row(win_list, colour):
            return True

        win_list = []

        # horizontal
        for i in range(-3, 4):
            try:
                if c + i < 0:
                    raise IndexError
                win_list.append(b[c+i][r])
            except IndexError:
                pass

        if four_in_a_row(win_list, colour):
            return True

        win_list = []

        # diagonal \
        for i in range(-3, 4):
            try:
                if (r - i < 0) or (c + i < 0):
                    raise IndexError
                win_list.append(b[c+i][r-i])
            except IndexError:
                pass

        if four_in_a_row(win_list, colour):
            return True

        win_list = []

        # diagonal /
        for i in range(-3, 4):
            try:
                if c + i < 0 or r+i < 0:
                    raise IndexError
                win_list.append(b[c+i][r+i])
            except IndexError:
                pass

        if four_in_a_row(win_list, colour):
            return True



game_board = board()

name = input("Enter player 1's name: ")
player_1 = human(name)
player_1.set_colour("x")

yn = ""

while yn != "y" and yn != "n":
    yn = input("Play against the computer? y/n:")

if yn == "n":
    player_2 = human(input("Enter player 2's name: "))
else:
    player_2 = bot("The Computer")

player_2.set_colour("o")

turn_player = player_1#random.choice([player_1, player_2])
print("\n" + turn_player.get_name() + " moves first!")
print("Begin!")
print("-" * 20)

game_over = False

while not game_over:
    game_board.show()

    board_copy = deepcopy(game_board)
    print(turn_player.get_name() + "'s move.")
    if game_board.move(turn_player, turn_player.make_move(board_copy)) == "win":
        game_board.show()
        print(turn_player.get_name() + " wins!")
        game_over = True

    if turn_player == player_2:
        turn_player = player_1
    else:
        turn_player = player_2
i = input("End")