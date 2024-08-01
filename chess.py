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
chess_piece = {"bK" : "♔", "bQ" : "♕", "bR" : "♖", \
                "bB" : "♗", "bN" : "♘", "bP" : "♙", \
                "wK" : "♚", "wQ" : "♛", "wR" : "♜", \
                "wB" : "♝", "wN" : "♞", "wP" : "♟︎", \
                }

grid_notation = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, \
                 'e' : 5, 'f' : 6, 'g' : 7, 'h' : 8
                 }

class chessPiece(object):
    """
    Define chess pieces class. This is where all pieces will exist, 
    including coordinates and procedures
    """
    #holds on instances in a list, if any are updated, they are also updated in the list
    instances = []

    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        #track all instances
        chessPiece.instances.append(self)

    def move(move):
        #match letter and digit of each coordinate in string and swap for number
        match = re.match(r'([a-h])(\d) to ([a-h])(\d)', move)
        if match:
            sub1 = grid_notation[match.group(1)]
            sub2 = int(match.group(2))
            sub3 = grid_notation[match.group(3)]
            sub4 = int(match.group(4))

            old = (sub1, sub2)
            new = (sub3, sub4)

            #iterate through all pieces, if found piece and valid move, change coordinates
            for piece in chessPiece.get_all_instances():
                if piece.coordinates == old:
                    if piece.validMove(new):
                        piece.coordinates = new
                        return f"{piece.name} moved to {match.group(3)}, {match.group(4)}"
                    else:
                        return "Not a valid move"
            return "No piece found at the given coordinates"
        else:
            return "Not a valid input format"
        
    def get_all_instances():
        return list(chessPiece.instances)
    
    def destroy(self, name):
        pass

    def validMove(self, new):
        #check to see if in bounds of board
        if new[0] < 9 and new[1] < 9:
            return True
        else:
            return False

    def __str__(self):
        return self.name + ' ' + str(self.coordinates)

class Pawn(chessPiece):
    def validMoves(self, board):
        # Call the parent class's validMove before using own
        if super().validMove(board):
            pass

class Rook(chessPiece):
    def validMoves(self, board):
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
    Pawn('wP', (1,2)) 
    Pawn('wP', (2,2))
    Pawn('wP', (3,2)) 
    Pawn('wP', (4,2))
    Pawn('wP', (5,2)) 
    Pawn('wP', (6,2))
    Pawn('wP', (7,2)) 
    Pawn('wP', (8,2))

    Rook('wR', (1,1))
    Rook('wR', (8,1))
    Bishop('wB', (2,1))
    Bishop('wB', (7,1))
    Knight('wN', (3,1))
    Knight('wN', (6,1))
    King('wK', (4,1))
    Queen('wK', (5,1))

    #build black pieces
    Pawn('bP', (1,7)) 
    Pawn('bP', (2,7))
    Pawn('bP', (3,7)) 
    Pawn('bP', (4,7))
    Pawn('bP', (5,7)) 
    Pawn('bP', (6,7))
    Pawn('bP', (7,7)) 
    Pawn('bP', (8,7))

    Rook('bR', (1,8))
    Rook('bR', (8,8))
    Bishop('bB', (2,8))
    Bishop('bB', (7,8))
    Knight('bN', (3,8))
    Knight('bN', (6,8))
    King('bK', (5,8))
    Queen('bK', (4,8))

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
-board will have 3 spaces of padding on left and right of each square
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
                    for piece in chessPiece.get_all_instances():
                        if (j,i//2) == piece.coordinates:
                            #render piece
                            row += ' ' + chess_piece[piece.name] + ' '
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


create_pieces()

print(render_board())

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
    chess_output.delete("1.0", "end")  # Clear previous content
    chess_output.insert("1.0", render_board())

def clear_text(event):
    text_input.delete("1.0", "end")  # Clear the text area
    text_input.unbind("<FocusIn>")  # Unbind this event after the first click

#create initial frame
root = Tk()
root.title("crazy chess")
root.winfo_rgb('#3FF')
frm = ttk.Frame(root, padding=40)
frm.grid()
#create label
ttk.Label(frm, text="crazy chess").grid(column=0, row=0)

#create label
ttk.Label(frm, text="AI Output:").grid(column=0, row=1)

# Create an output area for Gemini output
text_output = Text(frm, width=40, height=10, wrap="word")
text_output.grid(column=0, row=2, columnspan=3, pady=(20, 0))

# Create a Scrollbar widget for the output Text widget
scrollbar_output = Scrollbar(frm, orient="vertical", command=text_output.yview)
text_output.config(yscrollcommand=scrollbar_output.set)
scrollbar_output.grid(column=3, row=2, columnspan=3, sticky="ns", padx=(10))

#textinput area contains tag to designate text color
text_input = Text(frm, width=40, height=10, wrap="word")
text_input.tag_configure("colored", foreground="grey50")
text_input.insert('1.0', 'Enter move (ex. a2 to a4):', 'colored')
text_input.grid(column=0, row=6, columnspan=3, pady=(20, 0))
# Bind the clear_text function to the FocusIn event
text_input.bind("<FocusIn>", clear_text)

# Create chessboard area
chess_output = Text(frm, width=40, height=20, wrap="word")
chess_output.grid(column=0, row=5, columnspan=3, pady=(20, 0))
#render initial board
chess_output.insert("1.0", render_board())

#send button
ttk.Button(frm, text="Send", command=send_prompt).grid(column=2, row=0)

#quit button
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

#open window
root.mainloop()
