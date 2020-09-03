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

    def move_piece(self, spot):
        #Moves a piece from the coordinates given in a turn. Overwrites the target location, piece removal handled by Player classes.
        self.boardstate[spot[1][0]][spot[1][1]] = self.boardstate[spot[0][0]][spot[0][1]]
        self.boardstate[spot[0][0]][spot[0][1]] = ""

class Opponent(Board, Pawn, Bishop, Knight, Rook, King, Queen):
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

    def find_king(self):
        for x in range(self.pieces.size()):
            if self.pieces[x].name.lower() == "k"
                return x

    def remove_piece(self, ind):
        self.pieces.remove(ind)
        self.pieceCount = self.pieceCount-1

    def inattackrange(self, tar_x, tar_y, field):
        #check for checkmate
        result = false
        for piece in self.pieces:
            #Assume space to attack is owned for the sake of check
            if piece.move_attempt(x,y,field):
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
                    for piece in self.pieces:
                        if piece.move_attempt(x,y,field):
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
                if move_attempt(tar_x, tar_y, field):
                    field.move_piece(sel_x, tar_x, sel_y, tar_y)
                    return occupied
                else:
                    print("You can't move there!")
            else:
                print("That's not a valid piece to move!")




class Player(Board, Pawn, Bishop, Knight, Rook, King, Queen):
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

    def remove_piece(self, ind):
        self.pieces.remove(ind)
        self.pieces.pieceCount = self.pieces.pieceCount-1

    def find_king(self):
        target = [0,0]
        for x in range(self.pieces.size()):
            if self.pieces[x].name.lower() == "k":
                target = [self.pieces[x].xpos, self.pieces[x].ypos]
                return target

    def inattackrange(self, tar_x, tar_y, field):
        #check for checkmate
        result = false
        for piece in self.pieces:
            #Assume space to attack is owned for the sake of check
            if piece.move_attempt(x,y,field):
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
                        if piece.move_attempt(x,y,field):
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
                if move_attempt(tar_x, tar_y, field):
                    coordinates = [[sel_x, sel_y][tar_x, tar_y]]
                    self.pieces[sel_index].act_move(tar_x, tar_y)
                    return coordinates
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

    def play_game(self):
        while true:
            #Engage Player turn
            spot = self.white.turn(self.field)
            #Check for piece taken
            for ind in range(self.black.pieces):
                if (self.black.pieces[ind].xpos == spot[1][0] and self.black.pieces[ind].ypos == spot[1][1]):
                    self.field.move_piece(spot)
                    self.black.remove_piece(ind)
                    break
            #Check for check
            b_loc = self.black.find_king()
            if self.white.inattackrange(b_loc[0], b_loc[1], field):
                print("Black king in check!")
                escape = false
                for x in range(-1,2):
                    for y in range(-1,2):
                        if x == 0 and y == 0:
                            continue
                        else:
                            if not self.white.inattackrange(b_loc[0]+x, b_loc[1]+y, field):
                                escape = true
                                break
                    if escape:
                        break
                if not escape:
                    print("Game over! White wins.")
                    return 0
            #Engage Opponent turn
            spot = self.black.turn(self.field)
            #Check for piece taken
            for ind in range(self.white.pieces):
                if (self.white.pieces[ind].xpos == spot[1][0] and self.white.pieces[ind].ypos == spot[1][1]):
                    self.field.move_piece(spot)
                    self.white.remove_piece(ind)
                    break
            #Check for check
            w_loc = self.white.find_king()
            if self.black.inattackrange(b_loc[0], b_loc[1], field):
                print("White king in check!")
                escape = false
                for x in range(-1,2):
                    for y in range(-1,2):
                        if x == 0 and y == 0:
                            continue
                        else:
                            if not self.black.inattackrange(b_loc[0]+x, b_loc[1]+y, field):
                                escape = true
                                break
                    if escape:
                        break
                if not escape:
                    print("Game over! Black wins.")
                    return 0
        print("You shouldn't be here.")
        return 0

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


    def move_attempt(self, tar_xpos, tar_ypos, field):
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

    def move_attempt(self, tar_xpos, tar_ypos, field):
        #Negative distance means targeting to the up-left
        #Positive distance is to the bot-right
        x_dis = self.xpos - tar_xpos
        y_dis = self.ypos - tar_ypos
        if (x_dis == 0 and y_dis != 0):
            block = false
            if (y_dis > 0):
                #Aim down
                for y in range(0,y_dis):
                    if (len(field[self.xpos][(y-self.ypos)]) != 0):
                        block = true
                if block:
                    return false
                else:
                    return true
            else:
                #Aim up
                for y in range(0,abs(y_dis)):
                    if (len(field[self.xpos][(self.ypos-y)]) != 0):
                        block = true
                if block:
                    return false
                else:
                    return true
        elif (y_dis == 0 and x_dis != 0):
            block = false
            if (x_dis > 0):
                for x in range(0,x_dis):
                    if (len(field[(x-self.xpos)][self.ypos]) != 0):
                        block = true
                if block:
                    return false
                else:
                    return true
            else:
                #Aim up
                for x in range(0,abs(x_dis)):
                    if (len(field[(x-self.xpos)][self.ypos]) != 0):
                        block = true
                if block:
                    return false
                else:
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

    def move_attempt(self, tar_xpos, tar_ypos, field):
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

    def move_attempt(self, tar_xpos, tar_ypos, field):
        x_dis = self.xpos - tar_xpos
        y_dis = self.ypos - tar_ypos
        if (x_dis == y_dis):
            block = false
            #Either x or y works, both funcion
            if (x_dis > 0):
                for x in range(0,x_dis):
                    if (len(field[(x-self.xpos)][x-self.ypos]) != 0):
                        block = true
                if block:
                    return false
                else:
                    return true
                return true
            else:
                for x in range(0,abs(x_dis)):
                    if (len(field[(self.xpos-x)][self.ypos-x]) != 0):
                        block = true
                if block:
                    return false
                else:
                    return true
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

    def move_attempt(self, tar_xpos, tar_ypos, field):
        if Rook.move_attempt(self, tar_xpos, tar_ypos, field) or Bishop.move_attempt(self, tar_xpos, tar_ypos, field):
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


    def move_attempt(self, tar_xpos, tar_ypos, field):
        if (self.ypos == tar_ypos-1):
            if (self.xpos == tar_xpos):
                return true
            elif (((self.xpos == tar_xpos+1) or (self.xpos == tar_xpos-1)) and (len(field[tar_xpos][tar_ypos]) != 0):
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

    def move_attempt(self, tar_xpos, tar_ypos, field):
        if (self.ypos == tar_ypos+1):
            if (self.xpos == tar_xpos):
                return true
            elif (((self.xpos == tar_xpos+1) or (self.xpos == tar_xpos-1)) and (len(field[tar_xpos][tar_ypos]) != 0)):
                return true
        else
            return false

def main():
    #Check PATH?
    print("Compiles and runs.")

if __name__=="__main__":
    main()
