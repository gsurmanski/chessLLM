"""
lets play a chess game with AI

prompt engineer:
We are going to play chess using algebraic notation. 
you will be black located at the top of the board. 
Can you say all of your moves referencing the from and to notation 
(for example: a7-a8 would be moving your pawn down)?
After you move, can you immediately send another message saying something 
intimidating and funny? Every time I reply with a move, 
you repeat the process and pick another move. You go first. Go
"""
#import tkinter for window management
from tkinter import *
from tkinter import ttk

#import re for matching regex
import re

"""
Manage functionality of chess game ///////////////////////////////////////////////////
"""

#black pieces collection
CHESS_PIECE = {"bK" : "♔", "bQ" : "♕", "bR" : "♖", \
                "bB" : "♗", "bN" : "♘", "bP" : "♙", \
                "wK" : "♚", "wQ" : "♛", "wR" : "♜", \
                "wB" : "♝", "wN" : "♞", "wP" : "♟︎", \
                }

GRID_NOTATION = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, \
                 'e' : 5, 'f' : 6, 'g' : 7, 'h' : 8
                 }

#list of pieces in object form
pieces = []

#create function to find piece in list, since done so often. returns object
def find_piece(coordinate):
   for piece in pieces:
            if piece.coordinates == coordinate:
                return piece

def find_test():
   for piece in pieces:
        print(piece.name)

class chessPiece(object):
    """
    Define chess pieces class. This is where all pieces will exist, 
    including coordinates and procedures
    """
    #holds on instances in a list, if any are updated, they are also updated in the list

    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        #track all instances
        #chessPiece.pieces.append(self)

    def move(move):
        #sanitize input
        #format cannot be longer than 8 chars and must match letter(num) to letter(num)
        if len(move) > 8 or not re.match(r'([a-h])(\d) to ([a-h])(\d)', move):
            return "Not a valid move"
        
        #match letter and digit of each coordinate in string and swap for number
        match = re.match(r'([a-h])(\d) to ([a-h])(\d)', move)
        sub1 = GRID_NOTATION[match.group(1)]
        sub2 = int(match.group(2))
        sub3 = GRID_NOTATION[match.group(3)]
        sub4 = int(match.group(4))

        old = (sub1, sub2)
        new = (sub3, sub4)
        
        piece = find_piece(old)
        
        #iterate through all pieces, if found piece and valid move, change coordinates
        if piece != False:
            if piece.validMove(old, new):
                piece.coordinates = new
                return f"{piece.name} moved to {new}"
            else:
                return "Not a valid move"
        else:
            return "No piece found at the given coordinates"

    def validMove(self, old, new):
        #check to see if in bounds of board
        if 1 <= new[0] < 9 and 1 <= new[1] < 9:
            # Check if one of your own pieces is there
            if find_piece(new) and find_piece(old).name[0] == find_piece(new).name[0]:
                return False
            #then it's opposite piece, valid move and delete other piece
            elif find_piece(new) and find_piece(old).name[0] != find_piece(new).name[0]:
                pieces.remove(find_piece(new))
                return True
            #no pieces on spot and within board bounds
            return True
        else:
            #not in board bounds
            return False

    def __str__(self):
        return self.name + ' ' + str(self.coordinates)

class Pawn(chessPiece):
    def validMove(self, old, new):
        # Call the parent class's validMove before using own
        if super().validMove(old, new):
            x1, y1 = old
            x2, y2 = new
            valid_moves = [(0, 1), (1, 1)]
            if (x2 - x1, y2 - y1) in valid_moves:
                return True
            else:
                return False

class Rook(chessPiece):
    def validMoves(self, old, new):
        pass

class Bishop(chessPiece):
    def validMoves(self, board):
        pass

class Knight(chessPiece):
    def validMoves(self, board):
        pass

class Queen(chessPiece):
    def validMoves(self, board):
        pass

class King(chessPiece):
    def validMoves(self, board):
        pass


#set up initial pieces
def create_pieces():
    #build white pieces
    pieces.extend([
    Pawn('wP', (1, 2)),
    Pawn('wP', (2, 2)),
    Pawn('wP', (3, 2)),
    Pawn('wP', (4, 2)),
    Pawn('wP', (5, 2)),
    Pawn('wP', (6, 2)),
    Pawn('wP', (7, 2)),
    Pawn('wP', (8, 2)),
    Rook('wR', (1,1)),
    Rook('wR', (8,1)),
    Bishop('wB', (2,1)),
    Bishop('wB', (7,1)),
    Knight('wN', (3,1)),
    Knight('wN', (6,1)),
    King('wK', (4,1)),
    Queen('wQ', (5,1)),
])
  
    #build black pieces
    pieces.extend([
    Pawn('bP', (1,7)), 
    Pawn('bP', (2,7)),
    Pawn('bP', (3,7)), 
    Pawn('bP', (4,7)),
    Pawn('bP', (5,7)), 
    Pawn('bP', (6,7)),
    Pawn('bP', (7,7)), 
    Pawn('bP', (8,7)),
    Rook('bR', (1,8)),
    Rook('bR', (8,8)),
    Bishop('bB', (2,8)),
    Bishop('bB', (7,8)),
    Knight('bN', (3,8)),
    Knight('bN', (6,8)),
    King('bK', (5,8)),
    Queen('bQ', (4,8)),
])

#8x8, x-axis is a-h, y-axis is 1-8
#chess utf-8 border pieces, labelled clockwise from 12oclock for direction of lines 
# ex. rd = right down
#cb = chess borders
cb = {"ud" : "│", "rd" : "┌", "rl" : "─", \
    "rdl" : "┬", "dl" : "┐", "url" : "┴", \
    "urdl" : "┼", "ur" : "└", "ul" : "┘", \
    "urd" : "├", "udl" : "┤" }
"""
create function to render board and pieces on start
-board will have 3 spaces in each square
-8 squares share border left/right
-requires 9 ud lines

calculating board
-each tangible row is 8(squares)*3(spaces) + 9 separator ud characters = 33 chars accross
-board is 8 rows * 33 + 9 separator lines * 33
=264 + 297 
=561 chars total
total rows is 17

32 pieces will be present at start, 16 black and 16 white


result
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ ♜ │ ♟︎ │ ♞ │ ♛ │ ♚ │ ♞ │ ♟︎ │ ♜ │
├───┼───┼───┼───┼───┼───┼───┼───┤
│ ♟︎ │ ♟︎ │ ♟︎ │ ♟︎ │ ♟︎ │ ♟︎ │ ♟︎ │ ♟︎ │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│ ♙ │ ♙ │ ♙ │ ♙ │ ♙ │ ♙ │ ♙ │ ♙ │
├───┼───┼───┼───┼───┼───┼───┼───┤
│ ♖ │ ♗ │ ♘ │ ♔ │ ♕ │ ♘ │ ♗ │ ♖ │
└───┴───┴───┴───┴───┴───┴───┴───┘
"""
def render_board():
    #render grid and create chess piece objects

    #total rows including separator lines, not including 0
    row_total = 16
    column_total = 8
    #render top row and bottom row statically
    topline = (cb['rd'] + cb['rl'] * 3) + (cb['rdl'] + cb['rl'] * 3)*7 \
         + cb['dl']
    botline = (cb['ur'] + cb['rl'] * 3) + (cb['url'] + cb['rl'] * 3)*7 \
         + cb['ul']
    midline = (cb['urd'] + cb['rl'] * 3) + (cb['urdl'] + cb['rl'] * 3)*7 \
         + cb['udl']
    
    #create list to store board so the function can return for printing
    board_lines = []
    #render topline
    board_lines.append(topline)

    #render contents
    #iterate rows in reverse direction to build from ground up like real chess board
    for i in range(row_total, 1, -1):
        #render mid separator line on even rows (because not include top or botline)
        if i % 2 == 1:
            row = midline
        #print each row chars on even rows
        else: 
            #reset then render each row
            row = ''
            #iterate columns
            for j in range(1, column_total + 1):
                    row += '│'
                    #search for pieces in class list at current coordinate 
                    #(j,i//2) is tuple where(i//2) to account for midline 
                    # rows in between that skew current coordinates
                    found_piece = False
                    for piece in pieces:
                        if (j,i//2) == piece.coordinates:
                            #render piece
                            row += ' ' + CHESS_PIECE[piece.name] + ' '
                            found_piece = True
                            break
                    if not found_piece:
                        #empty square
                        row += '   '
                    #close with separator line on last column
                    if j == column_total:
                        row += '│'
        board_lines.append(row)

    board_lines.append(botline)

    return '\n'.join(board_lines)

"""
window/GUI management and initial launch /////////////////////////////////////////
"""

def send_prompt():
    #clear your text and get it via user_input
    user_input = text_input.get("1.0", "end-1c")  # Get all text from the text area
    text_input.delete("1.0", "end")  # Clear the text area

    # Update the output Text widget with the model's response
    text_output.delete("1.0", "end")  # Clear previous content
    text_output.insert("1.0", user_input)  # Insert new content

    #update chessboard
    print(chessPiece.move(user_input))
    
    update_chessboard()

    #print(find_test())
def clear_text(event):
    text_input.delete("1.0", "end")  # Clear the text area
    text_input.unbind("<FocusIn>")  # Unbind this event after the first click

def update_chessboard():
    chess_output.delete("1.0", "end")  # Clear previous content
    chess_output.insert("1.0", render_board())
    #center with tag
    chess_output.tag_add("center", "1.0", "end")

def create_window():
    #create initial frame
    root = Tk()
    root.title("Crazy Chess")
    root.winfo_rgb('#3FF')
    frm = ttk.Frame(root, padding=40)
    frm.grid()

    #create label
    ttk.Label(frm, text="AI Output:").grid(column=0, row=1)

    # Create an output area for Gemini output
    global text_output
    text_output = Text(frm, width=40, height=10, wrap="word")
    text_output.grid(column=0, row=2, columnspan=3, pady=(20, 0))
    text_output.insert("1.0", "Welcome to Crazy Chess...")  # Insert new content

    # Create a Scrollbar widget for the output Text widget
    scrollbar_output = Scrollbar(frm, orient="vertical", command=text_output.yview)
    text_output.config(yscrollcommand=scrollbar_output.set)
    scrollbar_output.grid(column=3, row=2, columnspan=3, sticky="ns", padx=(10))

    #textinput area contains tag to designate text color
    global text_input
    text_input = Text(frm, width=40, height=10, wrap="word")
    text_input.tag_configure("colored", foreground="grey50")
    text_input.insert('1.0', 'Enter move (ex. a2 to a4):', 'colored')
    text_input.grid(column=0, row=6, columnspan=3, pady=(20, 0))
    # Bind the clear_text function to the FocusIn event
    text_input.bind("<FocusIn>", clear_text)

    # Create chessboard area
    global chess_output
    chess_output = Text(frm, width=40, height=17, wrap="word")
    chess_output.grid(column=0, row=5, columnspan=3, pady=(20, 0))
    # Configure the tag for centering text
    chess_output.tag_configure("center", justify='center')

    # Render initial board and center text
    chess_output.insert("1.0", render_board())
    chess_output.tag_add("center", "1.0", "end")

    #send button
    ttk.Button(frm, text="Send", command=send_prompt).grid(column=2, row=0)

    #quit button
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()

#start code
if __name__ == "__main__":
    create_pieces()
    print(render_board())
    
    #create and open window
    create_window()
