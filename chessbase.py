# Initial Board Version
# Currently incomplete, still defining movement of players

class Board:
    def __init__(self):
        #initialize Board
        self.boardstate = []
        for x in range(0,8):
            self.boardstate.append([[""],[""],[""],[""],[""],[""],[""],[""]])

    def ownercheck(tar_x, tar_y, team):
        if self.boardstate[tar_x][tar_y] == "":
            #empty spaces are unowned
            return false
        elif self.boardstate[tar_x][tar_y].isupper == team:
            #Check if same team
            return true
        else
            return false

    def occupation(tar_x, tar_y, team):
        if self.boardstate[tar_x][tar_y] == "":
            #empty spaces are unoccupied
            return false
        elif self.boardstate[tar_x][tar_y].isupper != team:
            #Check if opossing team
            return true
        else
            return false

class Opponent(Board):
    #Class for the opponent/AI, black.
    def __init__(self):
        #Define list for pieces on the side, as well as a counter of total pieces on the board.
        self.pieceCount = 16
        self.pieces = []

        #When initalizing pieces, false implies black
        #Initialize pawns
        for x in range(0,8):
            self.pieces.append(Pawn(x, 6, false))

        #Initialize Bishops
        self.pieces.append(Bishop(2,7, false))
        self.pieces.append(Bishop(5,7, false))

        #Initialize Knights
        self.pieces.append(Knight(1,7, false))
        self.pieces.append(Knight(6,7, false))

        #Initialize Rooks
        self.pieces.append(Rook(0,7, false))
        self.pieces.append(Rook(7,7, false))

        #Initialize King
        self.pieces.append(King(4,7, false))

        #Initialize Queen
        self.pieces.append(Queen(3,7, false))

    def remove_piece(self, ind):
        self.pieces.remove(ind)

    def inattackrange(self, tar_x, tar_y, field):
        #check for checkmate
        result = false
        for piece in self.pieces:
            #Assume space to attack is owned for the sake of check
            if piece.move_attempt(x,y,owned):
                result = true
                break
        return result

    def attackrange(self, field):

        arange = []
        for x in range(0,8):
            arange.append([[false],[false],[false],[false],[false],[false],[false],[false]])

        for piece in self.pieces:
            arange[piece.xpos][piece.ypos] = true

        for x in range(0,8):
            for y in range(0,8):
                if arange[x][y] == true:
                    continue
                else:
                    owned = occupation(x,y,false)
                    for piece in self.pieces:
                        if piece.move_attempt(x,y,owned):
                            arange[x][y] = true
                            break

        return arange

    def turn(self, field):
        #Set as full user control, to be adjusted on a later date
        while true:
            sel_x = input("Input the x coordinate of your piece to move: ")
            sel_y = input("Input the y coordinate of your piece to move: ")
            sel_index = -1
            for x in range(self.pieces.size):
                if sel_x == self.pieces[x].xpos and sel_y = self.pieces[x].ypos
                sel_index = x
                break
            if sel_index != -1:
                tar_x = input("Input the x coordinate to move to: ")
                tar_y = input("Input the y coordinate to move to: ")
                occupied = field.occupation(tar_x, tar_y)
                if move_attempt(tar_x, tar_y, occupied):
                    field.move_piece(sel_x, tar_x, sel_y, tar_y)
                    return occupied
                else:
                    print("You can't move there!")
            else:
                print("That's not a valid piece to move!")




class Player(Board):
    #class for the Player side, white.
    def __init__(self):
        #Define list for pieces on the side, as well as a counter of total pieces on the board.
        self.pieceCount = 16
        self.pieces = []

        #When initalizing pieces, true implies white
        #Initialize pawns
        for x in range(0,8):
            pieces.append(Pawn(x, 1, true))

        #Initialize Bishops
        pieces.append(Bishop(2,0, true))
        pieces.append(Bishop(5,0, true))

        #Initialize Knights
        pieces.append(Knight(1,0, true))
        pieces.append(Knight(6,0, true))

        #Initialize Rooks
        pieces.append(Rook(0,0, true))
        pieces.append(Rook(7,0, true))

        #Initialize King
        pieces.append(King(4,0, true))

        #Initialize Queen
        pieces.append(Queen(3,0, true))

    def inattackrange(self, tar_x, tar_y, field):
        #check for checkmate
        result = false
        for piece in self.pieces:
            #Assume space to attack is owned for the sake of check
            if piece.move_attempt(x,y,true):
                result = true
                break
        return result

    def attackrange(self, field):
        arange = []
        for x in range(0,8):
            arange.append([[false],[false],[false],[false],[false],[false],[false],[false]])

        for piece in self.pieces:
            arange[piece.xpos][piece.ypos] = true

        for x in range(0,8):
            for y in range(0,8):
                if arange[x][y] == true:
                    continue
                else:
                    owned = occupation(x,y,true)
                    for piece in self.pieces:
                        if piece.move_attempt(x,y,owned):
                            arange[x][y] = true
                            break
        return arange

    def turn(self, field):
        #Set as full user control, can be adjusted on a later date
        while true:
            sel_x = input("Input the x coordinate of your piece to move: ")
            sel_y = input("Input the y coordinate of your piece to move: ")
            sel_index = -1
            for x in range(self.pieces.size):
                if sel_x == self.pieces[x].xpos and sel_y = self.pieces[x].ypos
                sel_index = x
                break
            if sel_index != -1:
                tar_x = input("Input the x coordinate to move to: ")
                tar_y = input("Input the y coordinate to move to: ")
                occupied = field.occupation(tar_x, tar_y)
                if move_attempt(tar_x, tar_y, occupied):
                    field.move_piece(sel_x, tar_x, sel_y, tar_y)
                    return occupied
                else:
                    print("You can't move there!")
            else:
                print("That's not a valid piece to move!")


class Game(Player, Opponent, Board):
    #Class for the board itself.
    def __init__(self):
        #Initialize pieces
        self.white = Player()
        self.black = Opponent()

        #initialize Board
        self.field = Board()

        #use piece arrays to occupy board
        for piece in self.white.pieces:
            self.boardstate[piece.xpos][piece.ypos] = piece.name
        for piece in self.black.pieces:
            self.boardstate[piece.xpos][piece.ypos] = piece.name

    def play_game
        #to fill later
        pass





class ChessPiece:
    #Basic methods for all pieces.
    def __init__(self, xcod, ycod):
        self.xpos = xcod
        self.ypos = ycod

    def act_move(self, tar_xpos, tar_ypos):
        self.ypos = tar_ypos
        self.xpos = tar_xpos

class King(ChessPiece):
    #Class and methods for Kings.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        if side:
            self.name = "K"
        else:
            self.name = "k"


    def move_attempt(self, tar_xpos, tar_ypos, occupied):
        x_dis = abs(self.xpos - tar_xpos)
        y_dis = abs(self.ypos - tar_ypos)
        if (x_dis == 0 and y_dis == 1) or (y_dis == 0 and x_dis == 1) or (y_dis == 1 and x_dis == 1):
            return true
        else:
            return false

class Rook(ChessPiece):
    #Classes and methods for Rooks.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        if side:
            self.name = "R"
        else:
            self.name = "r"

    def move_attempt(self, tar_xpos, tar_ypos, occupied):
        x_dis = self.xpos - tar_xpos
        y_dis = self.ypos - tar_ypos
        if (x_dis == 0 and y_dis != 0) or (y_dis == 0 and x_dis != 0):
            return true
        else:
            return false

class Knight(ChessPiece):
    #Class and methods for knights.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        if side:
            self.name = "N"
        else:
            self.name = "n"

    def move_attempt(self, tar_xpos, tar_ypos, occupied):
        x_dis = abs(self.xpos - tar_xpos)
        y_dis = abs(self.ypos - tar_ypos)
        if (x_dis == 1 and y_dis == 2) or (x_dis == 2 and y_dis == 1):
            return true
        else:
            return false

class Bishop(ChessPiece):
    #Class and methods for bishops.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        if side:
            self.name = "B"
        else:
            self.name = "b"

    def move_attempt(self, tar_xpos, tar_ypos, occupied):
        x_dis = self.xpos - tar_xpos
        y_dis = self.ypos - tar_ypos
        if (x_dis == y_dis):
            return true
        else:
            return false

class Queen(ChessPiece, Bishop, Rook):
    #Class and method for queens. Uses the methods from rook and bishop for simplicity's sake.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        if side:
            self.name = "Q"
        else:
            self.name = "q"

    def move_attempt(self, tar_xpos, tar_ypos, occupied):
        if Rook.move_attempt(self, tar_xpos, tar_ypos) or Bishop.move_attempt(self, tar_xpos, tar_ypos):
            return true
        else:
            return false

class BlackPawn(ChessPiece):
    #Class and methods for black pawns. Separated due to movement checks being different between color.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        if side:
            self.name = "P"
        else:
            self.name = "p"


    def move_attempt(self, tar_xpos, tar_ypos, occupied):
        if (self.ypos == tar_ypos-1):
            if (self.xpos == tar_xpos):
                return true
            elif (((self.xpos == tar_xpos+1) or (self.xpos == tar_xpos-1)) and occupied):
                return true
        else
            return false

class WhitePawn(ChessPiece):
    #Class and methods for white pawns. Separated due to movement checks being different between color.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        if side:
            self.name = "P"
        else:
            self.name = "p"

    def move_attempt(self, tar_xpos, tar_ypos, occupied):
        if (self.ypos == tar_ypos+1):
            if (self.xpos == tar_xpos):
                return true
            elif (((self.xpos == tar_xpos+1) or (self.xpos == tar_xpos-1)) and occupied):
                return true
        else
            return false

def main():
    #Check PATH?
    print("Compiles and runs.")

if __name__=="__main__":
    main()
