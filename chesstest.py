# Initial Board Version
import time
import random
import DavidBoard
import DavidChessEngine
import pygame as david

#Todos: fix check behavior, implement pawn promotion and sorting of piece set by value
#Piece sort may be unnecessary given the swap being inserted

class ChessPiece:
    #Basic methods for all pieces.
    def __init__(self, xcod, ycod):
        self.xpos = xcod
        self.ypos = ycod

    def act_move(self, tar_xpos, tar_ypos):
        self.ypos = tar_ypos
        self.xpos = tar_xpos
        david.display.update()


class Board:
    def __init__(self):
        #initialize Board
        self.boardstate = [["_","_","_","_","_","_","_","_"],
                           ["_","_","_","_","_","_","_","_"],
                           ["_","_","_","_","_","_","_","_"],
                           ["_","_","_","_","_","_","_","_"],
                           ["_","_","_","_","_","_","_","_"],
                           ["_","_","_","_","_","_","_","_"],
                           ["_","_","_","_","_","_","_","_"],
                           ["_","_","_","_","_","_","_","_"]]

    def getname(tar_x, tar_y, team):
        return boardstate[tar_x][tar_y]

    def move_piece(self, spot):

        a = spot[0][0]
        b = spot[0][1]
        c = spot[1][0]
        d = spot[1][1]
        print(a)
        print(b)
        print(c)
        print(d)

        #move = DavidChessEngine.Move(spot[0],spot[1], self.boardstate)
        #DavidChessEngine.GameState.makeMove(move)
        #DavidChessEngine.GameState.toDavidEngine(spot)


        #Moves a piece from the coordinates given in a turn. Overwrites the target location, piece removal handled by Player classes.
        self.boardstate[spot[1][0]][spot[1][1]] = self.boardstate[spot[0][0]][spot[0][1]]
        self.boardstate[spot[0][0]][spot[0][1]] = "_"
        david.display.update()

    def find_piece(self, identifier):
        collection = []
        for x in range(0,8):
            for y in range(0,8):
                if self.boardstate[x][y] == identifier:
                    collection.append([x,y])
        return collection

class King(ChessPiece):
    #Class and methods for Kings.

    def __init__(self, xcod, ycod, side):
        ChessPiece.__init__(self, xcod, ycod)
        #Value is set exceptionally high to disregard other attack attempts
        self.value = 999999
        if side:
            self.name = "wK"
        else:
            self.name = "bK"

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                x_dis = abs(tar_xpos - a)
                y_dis = abs(tar_ypos - b)
                if (x_dis == 0 and y_dis == 1) or (y_dis == 0 and x_dis == 1) or (y_dis == 1 and x_dis == 1):
                    if (field.boardstate[tar_xpos][tar_ypos].isupper() != self.name.isupper()) or (field.boardstate[a][b] == "_"):
                        targets.append([a, b])
        return targets

    def move_attempt(self, tar_xpos, tar_ypos, field):
        x_dis = abs(self.xpos - tar_xpos)
        y_dis = abs(self.ypos - tar_ypos)
        if (self.name.isupper() != field.boardstate[tar_xpos][tar_ypos].isupper()):
            if (x_dis == 0 and y_dis == 1) or (y_dis == 0 and x_dis == 1) or (y_dis == 1 and x_dis == 1):
                if (field.boardstate[tar_xpos][tar_ypos].isupper() != self.name.isupper()) or (field.boardstate[tar_xpos][tar_ypos] == "_"):
                    return True
        return False

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if self.move_attempt(a, b, field):
                    targets.append([a, b])
        return targets

class Rook(ChessPiece):
    #Classes and methods for Rooks.

    def __init__(self, xcod, ycod, side):
        ChessPiece.__init__(self, xcod, ycod)
        self.value = 5
        if side:
            self.name = "wR"
        else:
            self.name = "bR"

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        #Negative distance means targeting to the bot-right
        #Positive distance is to the up-left
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if (field.boardstate[a][b].isupper() != field.boardstate[tar_xpos][tar_ypos].isupper()) or (field.boardstate[a][b] == "_"):
                    x_dis = tar_xpos - a
                    y_dis = tar_ypos - b
                    if (x_dis == 0 and y_dis != 0):
                        block = False
                        if (y_dis > 0):
                            #Aim up
                            for y in range(1,y_dis):
                                if (field.boardstate[tar_xpos][(tar_ypos-y)]) != "_":
                                    block = True
                            if not block:
                                targets.append([a,b])
                        else:
                            #Aim down
                            for y in range(1,abs(y_dis)):
                                if (field.boardstate[tar_xpos][(tar_ypos+y)]) != "_":
                                    block = True
                            if not block:
                                targets.append([a,b])
                    elif (y_dis == 0 and x_dis != 0):
                        block = False
                        if (x_dis > 0):
                            #Aim left
                            for x in range(1,x_dis):
                                if (field.boardstate[tar_xpos-x][(tar_ypos)]) != "_":
                                    block = True
                            if not block:
                                targets.append([a,b])
                        else:
                            #Aim right
                            for x in range(1,abs(x_dis)):
                                if (field.boardstate[tar_xpos+x][(tar_ypos)]) != "_":
                                    block = True
                            if not block:
                                targets.append([a,b])
        return targets

    def move_attempt(self, tar_xpos, tar_ypos, field):
        #Negative distance means targeting to the bot-right
        #Positive distance is to the up-left
        x_dis = self.xpos - tar_xpos
        y_dis = self.ypos - tar_ypos
        if (self.name.isupper() != field.boardstate[tar_xpos][tar_ypos].isupper()) or (field.boardstate[tar_xpos][tar_ypos] == "_"):
            if (x_dis == 0 and y_dis != 0):
                block = False
                if (y_dis > 0):
                    #Aim up
                    for y in range(1,y_dis):
                        if (field.boardstate[self.xpos][(self.ypos-y)]) != "_":
                            block = True
                    if not block:
                        return True
                else:
                    #Aim down
                    for y in range(1,abs(y_dis)):
                        if (field.boardstate[self.xpos][(self.ypos+y)]) != "_":
                            block = True
                    if not block:
                        return True
            elif (y_dis == 0 and x_dis != 0):
                block = False
                if (x_dis > 0):
                    #Aiming left
                    for x in range(1,x_dis):
                        if (field.boardstate[(self.xpos-x)][self.ypos]) != "_":
                            block = True
                    if not block:
                        return True
                else:
                    #Aim right
                    for x in range(1,abs(x_dis)):
                        if (field.boardstate[(self.xpos+x)][self.ypos]) != "_":
                            block = True
                    if not block:
                        return True
        return False

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if self.move_attempt(a, b, field):
                    targets.append([a, b])
        return targets

class Knight(ChessPiece):
    #Class and methods for knights.

    def __init__(self, xcod, ycod, side):
        ChessPiece.__init__(self, xcod, ycod)
        self.value = 3
        if side:
            self.name = "wN"
        else:
            self.name = "bN"

    def move_attempt(self, tar_xpos, tar_ypos, field):
        x_dis = abs(self.xpos - tar_xpos)
        y_dis = abs(self.ypos - tar_ypos)
        if (self.name.isupper() != field.boardstate[tar_xpos][tar_ypos].isupper()) or (field.boardstate[tar_xpos][tar_ypos] == "_"):
            if ((x_dis == 1 and y_dis == 2) or (x_dis == 2 and y_dis == 1)):
                return True
        return False

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if self.move_attempt(a, b, field):
                    targets.append([a, b])
        return targets

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if (field.boardstate[a][b].isupper() != field.boardstate[tar_xpos][tar_ypos].isupper()) or (field.boardstate[a][b] == "_"):
                    x_dis = abs(tar_xpos - a)
                    y_dis = abs(tar_ypos - b)
                    if (x_dis == 1 and y_dis == 2) or (x_dis == 2 and y_dis == 1):
                        targets.append([a, b])
        return targets

class Bishop(ChessPiece):
    #Class and methods for bishops.

    def __init__(self, xcod, ycod, side):
        ChessPiece.__init__(self, xcod, ycod)
        self.value = 3
        if side:
            self.name = "wB"
        else:
            self.name = "bB"

    def move_attempt(self, tar_xpos, tar_ypos, field):
        if (field.boardstate[tar_xpos][tar_ypos].isupper() != self.name.isupper()) or (field.boardstate[tar_xpos][tar_ypos] == "_"):
            #print(f"Target at {tar_xpos}, {tar_ypos} is a {field.boardstate[tar_xpos][tar_ypos]}")
            x_dis = self.xpos - tar_xpos
            y_dis = self.ypos - tar_ypos
            if (abs(x_dis) == abs(y_dis)) and (abs(x_dis) != 0):
                #print(f'Target is at distance of {abs(x_dis)} diagonally')
                #print("x_dis: ", x_dis)
                #print("y_dis: ", y_dis)
                block = False
                #Either x or y works, both function
                if (x_dis > 0 and y_dis > 0):
                    #Downright
                    for x in range(1,abs(x_dis)):
                        #print(f"Checking ({self.xpos-x}, {self.ypos-x}), which should be {field.boardstate[self.xpos-x][self.ypos-x]}")
                        if (field.boardstate[(self.xpos-x)][self.ypos-x]) != "_":
                            #print("Blocked")
                            block = True
                            break
                    if not block:
                        return True
                elif (x_dis > 0 and y_dis < 0):
                    #Upright
                    for x in range(1,abs(x_dis)):
                        #print(f"Checking ({self.xpos-x}, {self.ypos+x}), which should be {field.boardstate[self.xpos-x][self.ypos+x]}")
                        if (field.boardstate[(self.xpos-x)][self.ypos+x]) != "_":
                            #print("Blocked")
                            block = True
                            break
                    if not block:
                        return True
                elif (x_dis < 0 and y_dis > 0):
                    #Upleft
                    for x in range(1,abs(x_dis)):
                        #print(f"Checking ({self.xpos+x}, {self.ypos-x}), which should be {field.boardstate[self.xpos+x][self.ypos-x]}")
                        if (field.boardstate[(self.xpos+x)][self.ypos-x]) != "_":
                            #print("Blocked")
                            block = True
                            break
                    if not block:
                        return True
                else:
                    #Downleft
                    for x in range(1,abs(x_dis)):
                        #print(f"Checking ({self.xpos+x}, {self.ypos+x}), which should be {field.boardstate[self.xpos+x][self.ypos+x]}")
                        if (field.boardstate[(self.xpos+x)][self.ypos+x]) != "_":
                            #print("Blocked")
                            block = True
                            break
                    if not block:
                        return True
        #print("Failed move check")
        return False

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if (field.boardstate[a][b].isupper() != field.boardstate[tar_xpos][tar_ypos].isupper()) or (field.boardstate[a][b] == "_"):
                    x_dis = tar_xpos - a
                    y_dis = tar_ypos - b
                    block = False
                    if (abs(x_dis) == abs(y_dis)) and (abs(x_dis) != 0):
                        if (x_dis > 0 and y_dis > 0):
                            #Downright
                            for x in range(1,abs(x_dis)):
                                #print(f"Checking ({tar_xpos-x}, {tar_ypos-x}), which should be {field.boardstate[(tar_xpos-x)][tar_ypos-x]}")
                                if (field.boardstate[(tar_xpos-x)][tar_ypos-x]) != "_":
                                    #print("Blocked")
                                    block = True
                                    break
                            if not block:
                                targets.append([a, b])
                        elif (x_dis > 0 and y_dis < 0):
                            #Upright
                            for x in range(1,abs(x_dis)):
                                #print(f"Checking ({tar_xpos-x}, {tar_ypos+x}), which should be {field.boardstate[(tar_xpos-x)][tar_ypos+x]}")
                                if (field.boardstate[(tar_xpos-x)][tar_ypos+x]) != "_":
                                    #print("Blocked")
                                    block = True
                                    break
                            if not block:
                                targets.append([a, b])
                        elif (x_dis < 0 and y_dis > 0):
                            #Upleft
                            for x in range(1,abs(x_dis)):
                                #print(f"Checking ({tar_xpos+x}, {tar_ypos-x}), which should be {field.boardstate[(tar_xpos+x)][tar_ypos-x]}")
                                if (field.boardstate[(tar_xpos+x)][tar_ypos-x]) != "_":
                                    #print("Blocked")
                                    block = True
                                    break
                            if not block:
                                targets.append([a, b])
                        else:
                            #Downleft
                            for x in range(1,abs(x_dis)):
                                #print(f"Checking ({tar_xpos+x}, {tar_ypos-x}), which should be {field.boardstate[(tar_xpos+x)][tar_ypos-x]}")
                                if (field.boardstate[(tar_xpos+x)][tar_ypos+x]) != "_":
                                    #print("Blocked")
                                    block = True
                                    break
                            if not block:
                                targets.append([a, b])
        return targets

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if self.move_attempt(a, b, field):
                    targets.append([a, b])
        return targets

class Queen(ChessPiece):
    #Class and method for queens. Uses the methods from rook and bishop for simplicity's sake.

    def __init__(self, xcod, ycod, side):
        ChessPiece.__init__(self, xcod, ycod)
        self.value = 9
        if side:
            self.name = "wQ"
        else:
            self.name = "bQ"

    def move_attempt(self, tar_xpos, tar_ypos, field):
        #Negative distance means targeting to the up-left
        #Positive distance is to the bot-right
        if (self.name.isupper() != field.boardstate[tar_xpos][tar_ypos].isupper()) or (field.boardstate[tar_xpos][tar_ypos] == "_"):
            x_dis = self.xpos - tar_xpos
            y_dis = self.ypos - tar_ypos
            if (x_dis == 0 and y_dis != 0):
                block = False
                if (y_dis > 0):
                    #Aim down
                    for y in range(0,y_dis):
                        if (field.boardstate[self.xpos][(self.ypos-y)]) != "_":
                            block = True
                    if not block:
                        return True
                else:
                    #Aim up
                    for y in range(0,abs(y_dis)):
                        if (field.boardstate[self.xpos][(self.ypos+y)]) != "_":
                            block = True
                    if not block:
                        return True
            elif (y_dis == 0 and x_dis != 0):
                block = False
                if (x_dis > 0):
                    #Aim right
                    for x in range(0,abs(x_dis)):
                        if (field.boardstate[(self.xpos-x)][self.ypos]) != "_":
                            block = True
                    if not block:
                        return True
                else:
                    #Aim left
                    for x in range(0,abs(x_dis)):
                        if (field.boardstate[(self.xpos+x)][self.ypos]) != "_":
                            block = True
                    if not block:
                        return True
            elif (abs(x_dis) == abs(y_dis)) and (abs(x_dis) != 0):
                block = False
                #Either x or y works, both function
                if (x_dis > 0 and y_dis > 0):
                    #Downright
                    for x in range(0,abs(x_dis)):
                        if (field.boardstate[(self.xpos-x)][self.ypos-x]) != "_":
                            block = True
                    if not block:
                        return True
                elif (x_dis > 0 and y_dis < 0):
                    #Upright
                    for x in range(0,abs(x_dis)):
                        if (field.boardstate[(self.xpos-x)][self.ypos+x]) != "_":
                            block = True
                    if not block:
                        return True
                elif (x_dis < 0 and y_dis > 0):
                    #Upleft
                    for x in range(0,abs(x_dis)):
                        if (field.boardstate[(self.xpos+x)][self.ypos-x]) != "_":
                            block = True
                    if not block:
                        return True
                else:
                    #Downleft
                    for x in range(0,abs(x_dis)):
                        if (field.boardstate[(self.xpos+x)][self.ypos+x]) != "_":
                            block = True
                    if not block:
                        return True
        return False

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if self.move_attempt(a, b, field):
                    targets.append([a, b])
        return targets

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if (field.boardstate[a][b].isupper() != field.boardstate[tar_xpos][tar_ypos].isupper()) or (field.boardstate[a][b] == "_"):
                    x_dis = tar_xpos - a
                    y_dis = tar_ypos - b
                    if (x_dis == 0 and y_dis != 0):
                        block = False
                        if (y_dis > 0):
                            #Aim down
                            for y in range(0,y_dis):
                                if (field.boardstate[tar_xpos][(tar_ypos-y)]) != "_":
                                    block = True
                            if not block:
                                targets.append([a, b])
                        else:
                            #Aim up
                            for y in range(0,abs(y_dis)):
                                if (field.boardstate[tar_xpos][(tar_ypos+y)]) != "_":
                                    block = True
                            if not block:
                                targets.append([a, b])
                    elif (y_dis == 0 and x_dis != 0):
                        block = False
                        if (x_dis > 0):
                            for x in range(0,x_dis):
                                if (field.boardstate[tar_xpos-x][(tar_ypos)]) != "_":
                                    block = True
                            if not block:
                                targets.append([a, b])
                        else:
                            #Aim up
                            for x in range(0,abs(x_dis)):
                                if (field.boardstate[tar_xpos+x][(tar_ypos)]) != "_":
                                    block = True
                            if not block:
                                targets.append([a, b])
                    elif (x_dis == y_dis):
                        block = False
                        if (abs(x_dis) == abs(y_dis)) and (abs(x_dis) != 0):
                            if (x_dis > 0 and y_dis > 0):
                                #Downright
                                for x in range(0,abs(x_dis)):
                                    if (field.boardstate[(tar_xpos-x)][tar_ypos-x]) != "_":
                                        block = True
                                if not block:
                                    targets.append([a, b])
                            elif (x_dis > 0 and y_dis < 0):
                                #Upright
                                for x in range(0,abs(x_dis)):
                                    if (field.boardstate[(tar_xpos-x)][tar_ypos+x]) != "_":
                                        block = True
                                if not block:
                                    targets.append([a, b])
                            elif (x_dis < 0 and y_dis > 0):
                                #Upleft
                                for x in range(0,abs(x_dis)):
                                    if (field.boardstate[(tar_xpos+x)][tar_ypos-x]) != "_":
                                        block = True
                                if not block:
                                    targets.append([a, b])
                            else:
                                #Downleft
                                for x in range(0,abs(x_dis)):
                                    if (field.boardstate[(tar_xpos+x)][tar_ypos+x]) != "_":
                                        block = True
                                if not block:
                                    targets.append([a, b])
        return targets

class BlackPawn(ChessPiece):
    #Class and methods for black pawns. Separated due to movement checks being different between color.

    def __init__(self, xcod, ycod, side):
        ChessPiece.__init__(self, xcod, ycod)
        self.value = 1
        if side:
            self.name = "wP"
        else:
            self.name = "bP"


    def move_attempt(self, tar_xpos, tar_ypos, field):
        if (self.ypos == tar_ypos-1):
            if (self.xpos == tar_xpos) and (field.boardstate[tar_xpos][tar_ypos]) == "_":
                return True
            elif ((self.xpos == tar_xpos+1) or (self.xpos == tar_xpos-1)):
                type = field.boardstate[tar_xpos][tar_ypos]
                if type == "wQ" or type == "wK" or type == "wP" or type == "wB" or type == "wN" or type == "wR":
                    return True
        return False

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if (tar_ypos == b-1):
                    if (tar_xpos == a) and (field.boardstate[a][b]) == "_":
                        targets.append([a, b])
                    elif ((tar_xpos == a+1) or (tar_xpos == a-1)):
                        type = field.boardstate[a][b]
                        if type == "wQ" or type == "wK" or type == "wP" or type == "wB" or type == "wN" or type == "wR":
                            targets.append([a, b])
        return targets

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for x in range(-1,2):
            if (self.xpos+x >= 0) and (self.xpos+x <= 7):
                if self.move_attempt(self.xpos+x, self.ypos-1, field):
                    targets.append([self.xpos+x, self.ypos-1])
        return targets

class WhitePawn(ChessPiece):
    #Class and methods for white pawns. Separated due to movement checks being different between color.

    def __init__(self, xcod, ycod, side):
        ChessPiece.__init__(self, xcod, ycod)
        self.value = 1
        if side:
            self.name = "wP"
        else:
            self.name = "bP"

    def move_attempt(self, tar_xpos, tar_ypos, field):
        if (self.ypos == tar_ypos+1):
            if (self.xpos == tar_xpos) and (field.boardstate[tar_xpos][tar_ypos]) == "_":
                return True
            elif ((self.xpos == tar_xpos+1) or (self.xpos == tar_xpos-1)):
                type = field.boardstate[tar_xpos][tar_ypos]
                if type == "bQ" or type == "bK" or type == "bP" or type == "bB" or type == "bN" or type == "bR":
                    return True
        return False

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if (tar_ypos == b+1):
                    if (tar_xpos == a) and (field.boardstate[a][b] == "_"):
                        targets.append([a, b])
                    elif ((tar_xpos == a+1) or (tar_xpos == a-1)):
                        type = field.boardstate[tar_xpos][tar_ypos]
                        if type == "bQ" or type == "bK" or type == "bP" or type == "bB" or type == "bN" or type == "bR":
                            targets.append([a, b])
        return targets

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for x in range(-1,2):
            if (self.xpos+x >= 0) and(self.xpos+x <= 7):
                if self.move_attempt(self.xpos+x, self.ypos+1, field):
                    targets.append([self.xpos+x, self.ypos+1])
        return targets

class Opponent(Board, BlackPawn, Bishop, Knight, Rook, King, Queen):
    #Class for the opponent/AI, black.
    def __init__(self):
        #Define list for pieces on the side, as well as a counter of total pieces on the board.
        self.pieceCount = 16
        self.pieces = []

        #When initalizing pieces, false implies black
        #Initialize pawns
        for x in range(0,8):
            self.pieces.append(BlackPawn(x, 6, False))

        #Initialize Bishops
        self.pieces.append(Bishop(2,7, False))
        self.pieces.append(Bishop(5,7, False))

        #Initialize Knights
        self.pieces.append(Knight(1,7, False))
        self.pieces.append(Knight(6,7, False))

        #Initialize Rooks
        self.pieces.append(Rook(0,7, False))
        self.pieces.append(Rook(7,7, False))

        #Initialize Queen
        self.pieces.append(Queen(3,7, False))

        #Initialize King
        self.pieces.append(King(4,7, False))



    def find_king(self):
        for piece in self.pieces:
            if piece.name.lower() == "bK":
                target = [piece.xpos, piece.ypos]
                return target
        raise Exception("King missing?")

    def remove_piece(self, ind):
        self.pieces.pop(ind)
        self.pieceCount = self.pieceCount-1

    def canattack(self, tar_x, tar_y, field):
        #Checks what pieces can attack the spot
        result = []
        for x in range(len(self.pieces)):
            if self.pieces[x].move_attempt(tar_x,tar_y,field):
                result.append(x)
        return result

    def inattackrange(self, tar_x, tar_y, field):
        #check for checkmate
        #print(f"Checking the target {tar_x}, {tar_y}")
        result = False
        for piece in self.pieces:
            if piece.move_attempt(tar_x,tar_y,field):
                #print(f"In range of {piece.name} at {piece.xpos}, {piece.ypos}")
                result = True
                break
        return result

    def attackrange(self, field):

        atrange = []
        for x in range(0,8):
            atrange.append([[False],[False],[False],[False],[False],[False],[False],[False]])

        for piece in self.pieces:
            atrange[piece.xpos][piece.ypos] = True

        for x in range(0,8):
            for y in range(0,8):
                if atrange[x][y] == True:
                    continue
                else:
                    for piece in self.pieces:
                        if piece.move_attempt(x,y,field):
                            atrange[x][y] = True
                            break

        return atrange

    def can_move(self, field):
        atrange = self.attackrange(field)
        count = 0
        for x in range(8):
            for y in range(8):
                if atrange[x][y]:
                    count += 1
        if count > len(self.pieces):
            return True
        #if condition falls through
        return False

    def pawn_promote(self, field):
        for i in range(len(self.pieces)):
            #Check if a pawn is at the back
            if self.pieces[i].name == "bP" and self.pieces[i].ypos == 0:
                #keep its coordinates
                y_spot = self.pieces[i].ypos
                x_spot = self.pieces[i].xpos
                print(f"Moving pawn located at ({x_spot}, {y_spot}).")
                #Remove and reintroduce as queen
                self.pieces.pop(i)
                self.pieces.append(Queen(x_spot, y_spot, False))
                #Swap last index and index prior, knowing they are the king and new queen
                self.pieces[len(self.pieces)-2], self.pieces[len(self.pieces)-1] = self.pieces[len(self.pieces)-1], self.pieces[len(self.pieces)-2]
                #Reassign the field queen to not break
                field[x_spot][yy_spot] = "bQ"

    def turn(self, field):
        #Search for highest value piece to take. If can't take, aim at highest in range next turn. If none in range, random move.
        #Don't need to check if king can be attacked, assumed not if game is going
        #Check for queen
        target = field.find_piece("wQ")
        #print("Queen attack check")
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for x in range(len(target)):
                if self.inattackrange(target[0][0], target[0][1], field):
                    attack_list = self.canattack(target[0][0], target[0][1], field)
                    #Piece to use, random from the available attackers
                    ptu = random.choice(attack_list)
                    coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos], [target[0][0], target[0][1]]]
                    print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({target[0][0]}, {target[0][1]}).')
                    self.pieces[ptu].act_move(target[0][0], target[0][1])
                    return coordinates
        #Queen out of range, try to attack rook
        target = field.find_piece("wR")
        #print("Rook attack check")
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for x in range(len(target)):
                if self.inattackrange(target[x][0], target[x][1], field):
                    attack_list = self.canattack(target[x][0], target[x][1], field)
                    #Piece to use, random from the available attackers
                    ptu = random.choice(attack_list)
                    coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos], [target[x][0], target[x][1]]]
                    print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({target[x][0]}, {target[x][1]}).')
                    self.pieces[ptu].act_move(target[x][0], target[x][1])
                    return coordinates
        #No rooks, sample both bishops and knights at the same time
        target = field.find_piece("wB")
        target.extend(field.find_piece("wN"))
        #print("Bishop and knight attack check")
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for x in range(len(target)):
                #print(f"Checking the target at ({target[x][0]}, {target[x][1]})")
                if self.inattackrange(target[x][0], target[x][1], field):
                    #print("In attack range of someone")
                    attack_list = self.canattack(target[x][0], target[x][1], field)
                    #print("In range of: ", attack_list)
                    #Piece to use, random from the available attackers
                    ptu = random.choice(attack_list)
                    coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos], [target[x][0], target[x][1]]]
                    print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({target[x][0]}, {target[x][1]}).')
                    self.pieces[ptu].act_move(target[x][0], target[x][1])
                    return coordinates
        #No knights or bishops, pawns
        target = field.find_piece("wP")
        #print("Pawn attack check")
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for x in range(len(target)):
                if self.inattackrange(target[x][0], target[x][1], field):
                    attack_list = self.canattack(target[x][0], target[x][1], field)
                    #Piece to use, random from the available attackers
                    ptu = random.choice(attack_list)
                    coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos], [target[x][0], target[x][1]]]
                    print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({target[x][0]}, {target[x][1]}).')
                    self.pieces[ptu].act_move(target[x][0], target[x][1])
                    return coordinates
        #No pawns, try and check king
        #use piece's attack range from king's position?
        target = field.find_piece("wK")
        #Iterates through pieces, lower value first
        if len(target) >0:
            for i in range(len(self.pieces)):
                #farside returns a two layer array containing the indicies that can attack target
                #nearside returns a two layer array containing the indicies that the piece can reach now
                #nearside and farside locations must match for a valid move
                #Use target as location to evaluate for
                farside = self.pieces[i].distant_range(target[0][0],target[0][1],field)
                nearside = self.pieces[i].arange(field)
                #Valid location if piece.arange == piece.distant_range
                for x in range(len(farside)):
                    for y in range(len(nearside)):
                        if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                            #farside and nearside match, valid move
                            coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                            self.pieces[i].act_move(farside[x][0], farside[x][1])
                            print(f'Moving {self.pieces[i].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[x][0]}, {farside[x][1]}).')
                            return coordinates
        #Falling through loop assumes unable to check king, check queen
        target = field.find_piece("wQ")
        #Iterates through pieces, lower value first
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for item in target:
                for i in range(len(self.pieces)):
                    #farside returns a two layer array containing the indicies that can attack target
                    #nearside returns a two layer array containing the indicies that the piece can reach now
                    #nearside and farside locations must match for a valid move
                    #Use target as location to evaluate for
                    farside = self.pieces[i].distant_range(item[0],item[1],field)
                    nearside = self.pieces[i].arange(field)
                    #Valid location if piece.arange == piece.distant_range
                    for x in range(len(farside)):
                        for y in range(len(nearside)):
                            if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                                #farside and nearside match, valid move
                                coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                                print(f'Moving {self.pieces[i].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[x][0]}, {farside[x][1]}).')
                                self.pieces[i].act_move(farside[x][0], farside[x][1])
                                return coordinates
        #Queen not checked, check rook?
        target = field.find_piece("wR")
        #Iterates through pieces, lower value first
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for item in target:
                for i in range(len(self.pieces)):
                    #farside returns a two layer array containing the indicies that can attack target
                    #nearside returns a two layer array containing the indicies that the piece can reach now
                    #nearside and farside locations must match for a valid move
                    #Use target as location to evaluate for
                    farside = self.pieces[i].distant_range(item[0],item[1],field)
                    nearside = self.pieces[i].arange(field)
                    #Valid location if piece.arange == piece.distant_range
                    for x in range(len(farside)):
                        for y in range(len(nearside)):
                            if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                                #farside and nearside match, valid move
                                coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                                print(f'Moving {self.pieces[i].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[x][0]}, {farside[x][1]}).')
                                self.pieces[i].act_move(farside[x][0], farside[x][1])
                                return coordinates
        #No rook, check bishop/knight?
        target = field.find_piece("wB")
        target.extend(field.find_piece("wN"))
        #Iterates through pieces, lower value first
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for x in target:
                for i in range(len(self.pieces)):
                    #farside returns a two layer array containing the indicies that can attack target
                    #nearside returns a two layer array containing the indicies that the piece can reach now
                    #nearside and farside locations must match for a valid move
                    #Use target as location to evaluate for
                    farside = self.pieces[i].distant_range(item[0],item[1],field)
                    nearside = self.pieces[i].arange(field)
                    #Valid location if piece.arange == piece.distant_range
                    for x in range(len(farside)):
                        for y in range(len(nearside)):
                            if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                                #farside and nearside match, valid move
                                coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                                print(f'Moving {self.pieces[i].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[x][0]}, {farside[x][1]}).')
                                self.pieces[i].act_move(farside[x][0], farside[x][1])
                                return coordinates
        #No bishop/knight, pawns?
        target = field.find_piece("wP")
        #Iterates through pieces, lower value first
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for item in target:
                for i in range(len(self.pieces)):
                    #farside returns a two layer array containing the indicies that can attack target
                    #nearside returns a two layer array containing the indicies that the piece can reach now
                    #nearside and farside locations must match for a valid move
                    #Use target as location to evaluate for
                    farside = self.pieces[i].distant_range(item[0],item[1],field)
                    nearside = self.pieces[i].arange(field)
                    #Valid location if piece.arange == piece.distant_range
                    for x in range(len(farside)):
                        for y in range(len(nearside)):
                            if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                                #farside and nearside match, valid move
                                coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                                print(f'Moving {self.pieces[i].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[x][0]}, {farside[x][1]}).')
                                self.pieces[i].act_move(farside[x][0], farside[x][1])
                                return coordinates

        #Unable to check any piece, take a random move
        list_indicies = []
        for i in range(len(self.pieces)):
            list_indicies.append(i)
        random.shuffle(list_indicies)
        move_available = False
        while not move_available:
            ptu = list_indicies[0]
            attacklist = self.pieces[ptu].arange(field)
            if len(attacklist) == 0:
                list_indicies.pop(0)
            else:
                random.shuffle(attacklist)
                move_available = True
        coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos],[attacklist[0][0], attacklist[0][1]]]
        print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({attacklist[0][0]}, {attacklist[0][1]}).')
        self.pieces[ptu].act_move(attacklist[0][0], attacklist[0][1])
        return coordinates

class Player(Board, WhitePawn, Bishop, Knight, Rook, King, Queen):
    #class for the Player side, white.
    def __init__(self):
        #Define list for pieces on the side, as well as a counter of total pieces on the board.
        self.pieceCount = 16
        self.pieces = []
        #Value to be used later
        #self.value = 39
        truth = True

        #When initalizing pieces, true implies white
        #Initialize pawns
        for x in range(0,8):
            self.pieces.append(WhitePawn(x, 1, True))

        #Initialize Bishops
        self.pieces.append(Bishop(2,0, True))
        self.pieces.append(Bishop(5,0, True))

        #Initialize Knights
        self.pieces.append(Knight(1,0, True))
        self.pieces.append(Knight(6,0, True))

        #Initialize Rooks
        self.pieces.append(Rook(0,0, True))
        self.pieces.append(Rook(7,0, True))

        #Initialize Queen
        self.pieces.append(Queen(3,0, True))

        #Initialize King
        self.pieces.append(King(4,0, True))


    def remove_piece(self, ind):
        #Value to be used later
        #self.value -= self.pieces[ind].value
        self.pieces.pop(ind)
        selfpieceCount = self.pieceCount-1

    def find_king(self):
        target = [0,0]
        for piece in self.pieces:
            if piece.name.lower() == "wK":
                target = [piece.xpos, piece.ypos]
                return target
        raise Exception("King missing?")

    def inattackrange(self, tar_x, tar_y, field):
        #check for checkmate
        result = False
        for piece in self.pieces:
            #Assume space to attack is owned for the sake of check
            if piece.move_attempt(tar_x,tar_y,field):
                result = True
                break
        return result

    def attackrange(self, field):
        atrange = []
        for x in range(0,8):
            atrange.append([[False],[False],[False],[False],[False],[False],[False],[False]])

        for piece in self.pieces:
            atrange[piece.xpos][piece.ypos] = True

        for x in range(0,8):
            for y in range(0,8):
                if atrange[x][y]:
                    continue
                else:
                    for piece in self.pieces:
                        if piece.move_attempt(x,y,field):
                            atrange[x][y] = True
                            break
        return atrange

    def canattack(self, tar_x, tar_y, field):
        #Checks what pieces can attack the spot
        result = []
        for x in range(len(self.pieces)):
            #Assume space to attack is owned for the sake of check
            if self.pieces[x].move_attempt(tar_x,tar_y,field):
                result.append(x)
                break
        return result

    def can_move(self, field):
        atrange = self.attackrange(field)
        count = 0
        for x in range(8):
            for y in range(8):
                if atrange[x][y]:
                    count += 1
        if count > len(self.pieces):
            return True
        #if condition falls through
        return False

    def pawn_promote(self, field):
        for i in range(len(self.pieces)):
            #Check if a pawn is at the back
            if self.pieces[i].name == "wP" and self.pieces[i].ypos == 7:
                #keep its coordinates
                y_spot = self.pieces[i].ypos
                x_spot = self.pieces[i].xpos
                print(f"Moving pawn located at ({x_spot}, {y_spot}).")
                #Remove and reintroduce as queen
                self.pieces.pop(i)
                self.pieces.append(Queen(x_spot, y_spot, False))
                #Swap last index and index prior, knowing they are the king and new queen
                self.pieces[len(self.pieces)-2], self.pieces[len(self.pieces)-1] = self.pieces[len(self.pieces)-1], self.pieces[len(self.pieces)-2]
                #Reassign the field queen to not break
                field[x_spot][yy_spot] = "wQ"

    def turn(self, field):
        #Search for highest value piece to take. If can't take, aim at highest in range next turn. If none in range, random move.
        #Don't need to check if king can be attacked, assumed not if game is going
        #Check for queen
        target = field.find_piece("bQ")
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for x in range(len(target)):
                if self.inattackrange(target[x][0], target[x][1], field):
                    attack_list = self.canattack(target[0][0], target[0][1], field)
                    #Piece to use, random from the available attackers
                    ptu = random.choice(attack_list)
                    coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos], [target[0][0], target[0][1]]]
                    print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({target[0][0]}, {target[0][1]}).')
                    self.pieces[ptu].act_move(target[0][0], target[0][1])
                    return coordinates
        #Queen out of range, try to attack rook
        target = field.find_piece("bR")
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for x in range(len(target)):
                if self.inattackrange(target[x][0], target[x][1], field):
                    attack_list = self.canattack(target[x][0], target[x][1], field)
                    #Piece to use, random from the available attackers
                    ptu = random.choice(attack_list)
                    coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos], [target[x][0], target[x][1]]]
                    print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({target[x][0]}, {target[x][1]}).')
                    self.pieces[ptu].act_move(target[x][0], target[x][1])
                    return coordinates
        #No rooks, sample both bishops and knights at the same time
        target = field.find_piece("bB")
        target.extend(field.find_piece("bN"))
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for x in range(len(target)):
                if self.inattackrange(target[x][0], target[x][1], field):
                    attack_list = self.canattack(target[x][0], target[x][1], field)
                    #Piece to use, random from the available attackers
                    ptu = random.choice(attack_list)
                    coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos], [target[x][0], target[x][1]]]
                    print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({target[x][0]}, {target[x][1]}).')
                    self.pieces[ptu].act_move(target[x][0], target[x][1])
                    return coordinates
        #No knights or bishops, pawns
        target = field.find_piece("bP")
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for x in range(len(target)):
                if self.inattackrange(target[x][0], target[x][1], field):
                    attack_list = self.canattack(target[x][0], target[x][1], field)
                    #Piece to use, random from the available attackers
                    ptu = random.choice(attack_list)
                    coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos], [target[x][0], target[x][1]]]
                    print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({target[x][0]}, {target[x][1]}).')
                    self.pieces[ptu].act_move(target[x][0], target[x][1])
                    return coordinates
        #No pawns, try and check king
        #use piece's attack range from king's position?
        target = field.find_piece("bK")
        #Iterates through pieces, lower value first
        if len(target) >0:
            for i in range(len(self.pieces)):
                #farside returns a two layer array containing the indicies that can attack target
                #nearside returns a two layer array containing the indicies that the piece can reach now
                #nearside and farside locations must match for a valid move
                #Use target as location to evaluate for
                farside = self.pieces[i].distant_range(target[0][0],target[0][1],field)
                nearside = self.pieces[i].arange(field)
                #Valid location if piece.arange == piece.distant_range
                for x in range(len(farside)):
                    for y in range(len(nearside)):
                        if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                            #farside and nearside match, valid move
                            coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                            self.pieces[i].act_move(farside[x][0], farside[x][1])
                            print(f'Moving {self.pieces[i].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[x][0]}, {farside[x][1]}).')
                            return coordinates
        #Falling through loop assumes unable to check king, check queen
        target = field.find_piece("bQ")
        #Iterates through pieces, lower value first
        if len(target) >0:
            #Shuffle target to randomize targeat
            if(len(target) >1):
                random.shuffle(target)
            #Check each piece through the list
            for item in target:
                for i in range(len(self.pieces)):
                    #farside returns a two layer array containing the indicies that can attack target
                    #nearside returns a two layer array containing the indicies that the piece can reach now
                    #nearside and farside locations must match for a valid move
                    #Use target as location to evaluate for
                    #print("target: ", len(target))
                    #print("x: ",x)
                    #print("pieces: ", len(self.pieces))
                    #print("i: ", i)
                    farside = self.pieces[i].distant_range(item[0],item[1],field)
                    nearside = self.pieces[i].arange(field)
                    #Valid location if piece.arange == piece.distant_range
                    for x in range(len(farside)):
                        for y in range(len(nearside)):
                            if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                                #farside and nearside match, valid move
                                coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                                print(f'Moving {self.pieces[i].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[x][0]}, {farside[x][1]}).')
                                self.pieces[i].act_move(farside[x][0], farside[x][1])
                                return coordinates
        #Queen not checked, check rook?
        target = field.find_piece("bR")
        #Iterates through pieces, lower value first
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for item in target:
                for i in range(len(self.pieces)):
                    #farside returns a two layer array containing the indicies that can attack target
                    #nearside returns a two layer array containing the indicies that the piece can reach now
                    #nearside and farside locations must match for a valid move
                    #Use target as location to evaluate for
                    farside = self.pieces[i].distant_range(item[0],item[1],field)
                    nearside = self.pieces[i].arange(field)
                    #Valid location if piece.arange == piece.distant_range
                    for x in range(len(farside)):
                        for y in range(len(nearside)):
                            if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                                #farside and nearside match, valid move
                                coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                                print(f'Moving {self.pieces[i].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[x][0]}, {farside[x][1]}).')
                                self.pieces[i].act_move(farside[x][0], farside[x][1])
                                return coordinates
        #No rook, check bishop/knight?
        target = field.find_piece("bB")
        target.extend(field.find_piece("bN"))
        #Iterates through pieces, lower value first
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for item in target:
                for i in range(len(self.pieces)):
                    #farside returns a two layer array containing the indicies that can attack target
                    #nearside returns a two layer array containing the indicies that the piece can reach now
                    #nearside and farside locations must match for a valid move
                    #Use target as location to evaluate for
                    farside = self.pieces[i].distant_range(item[0],item[1],field)
                    nearside = self.pieces[i].arange(field)
                    #Valid location if piece.arange == piece.distant_range
                    for x in range(len(farside)):
                        for y in range(len(nearside)):
                            if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                                #farside and nearside match, valid move
                                coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                                print(f'Moving {self.pieces[i].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[x][0]}, {farside[x][1]}).')
                                self.pieces[i].act_move(farside[x][0], farside[x][1])
                                return coordinates
        #No bishop/knight, pawns?
        target = field.find_piece("bP")
        #Iterates through pieces, lower value first
        if len(target) >0:
            #Shuffle target to randomize target
            random.shuffle(target)
            #Check each piece through the list
            for item in target:
                for i in range(len(self.pieces)):
                    #farside returns a two layer array containing the indicies that can attack target
                    #nearside returns a two layer array containing the indicies that the piece can reach now
                    #nearside and farside locations must match for a valid move
                    #Use target as location to evaluate for
                    farside = self.pieces[i].distant_range(item[0],item[1],field)
                    nearside = self.pieces[i].arange(field)
                    #Valid location if piece.arange == piece.distant_range
                    for x in range(len(farside)):
                        for y in range(len(nearside)):
                            if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                                #farside and nearside match, valid move
                                coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                                print(f'Moving {self.pieces[i].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[x][0]}, {farside[x][1]}).')
                                self.pieces[i].act_move(farside[x][0], farside[x][1])
                                return coordinates

        #Unable to check any piece, take a random move
        list_indicies = []
        for i in range(len(self.pieces)):
            list_indicies.append(i)
        random.shuffle(list_indicies)
        for i in list_indicies:
            attacklist = self.pieces[i].arange(field)
            if len(attacklist) > 0:
                ptu = i
                random.shuffle(attacklist)
                break
        coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos],[attacklist[0][0], attacklist[0][1]]]
        print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({attacklist[0][0]}, {attacklist[0][1]}).')
        self.pieces[ptu].act_move(attacklist[0][0], attacklist[0][1])
        return coordinates




david.init()
WIDTH = HEIGHT = 512
DIMENSION = 8 #8x8
SQ_SIZE = HEIGHT //DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionary of images. this will be call exactly once in main
'''
def loadImages():
    #IMAGES['wp'] = p.image.load("Images/P.png") #from folder images / 'the picture to use for that piece.'
    #IMAGES['bp'] = p.image.load("Images/bp.png")
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = david.transform.scale(david.image.load("Images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def drawGameState(screen, gs):  # this draws the squares on the board
    drawBoard(screen)
    # add piece highlighting or move suggestions (later?)
    drawPieces(screen, gs)  # draw pieces on the squares
'''
Draw squares on board
'''
def drawBoard(screen):
    colors = [david.Color("white"), david.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            david.draw.rect(screen, color, david.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            # Don't draw pieces here just incase we want to implement highlighting
            # Extra loop isn't that expensive
'''
Draw pieces on board using current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "_":  # not empty squares
                screen.blit(IMAGES[piece],
                            p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # Puts the piece in for us


class Game(Player, Opponent, Board):
    #Class for the board itself.
    def __init__(self):
        #Initialize pieces
        self.white = Player()
        self.black = Opponent()
        #initialize Board
        self.field = Board()
        #initialize GUI
        self.david_running = False
        self.title = 'GUI of AI'
        self.WIDTH = self.HEIGHT = 500
        self.DIMENSION = 8
        self.SQ_SIZE = self.HEIGHT // self.DIMENSION
        self.MAX_FPS = 15
        self.screen = david.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = david.time.Clock()
        self.screen.fill(david.Color("white"))
        self.gs = Board().boardstate



        #use piece arrays to occupy board
        for piece in self.black.pieces:
            self.field.boardstate[piece.xpos][piece.ypos] = piece.name
        for piece in self.white.pieces:
            self.field.boardstate[piece.xpos][piece.ypos] = piece.name


    def play_game(self):
        w_check = False
        b_check = False
        for y in range(7,-1,-1):
            print(self.field.boardstate[0][y], self.field.boardstate[1][y], self.field.boardstate[2][y], self.field.boardstate[3][y], self.field.boardstate[4][y],
			self.field.boardstate[5][y], self.field.boardstate[6][y], self.field.boardstate[7][y])

        #p.init()
        #screen = p.display.set_mode((WIDTH, HEIGHT))
        clock = david.time.Clock()
        #screen.fill(p.Color("white"))
        #gs = self.field.boardstate
        #print("Printing gs")
        #print(gs)
        #print("DONE PRINTING GS")
        #loadImages()



        running = True
        while running:




            # David's GUI logic;;;;;;;;;;;;;;issue is that the rest of this class is far to involved..
            #drawGameState(screen, gs)
            #clock.tick(MAX_FPS)
            #p.display.flip()

            for event in david.event.get():
                if event.type == david.QUIT:
                    self.david_running = False
                    running = False
                    david.quit()


			

			# David's GUI logic;;;;;;;;;;;;;;issue is that the rest of this class is far to involved..
            drawGameState(self.screen, self.gs)
            self.clock.tick(MAX_FPS)






            #Engage Player turn
            if not w_check:
                spot = self.white.turn(self.field)
                #throw pawn_promote to let it handle promtions
                #Check for piece taken
                for ind in range(len(self.black.pieces)):
                    if (self.black.pieces[ind].xpos == spot[1][0] and self.black.pieces[ind].ypos == spot[1][1]):
                        print(f'Claiming piece {self.black.pieces[ind].name} at ({spot[1][0]}, {spot[1][1]}).')
                        self.black.remove_piece(ind)
                        break
                self.field.move_piece(spot)


                drawGameState(self.screen, self.gs)


                self.white.pawn_promote
                for y in range(7,-1,-1):
                    print(self.field.boardstate[0][y], self.field.boardstate[1][y], self.field.boardstate[2][y], self.field.boardstate[3][y], self.field.boardstate[4][y], 
					self.field.boardstate[5][y], self.field.boardstate[6][y], self.field.boardstate[7][y])
                #Check for check
                b_loc = self.black.find_king()
                if self.white.inattackrange(b_loc[0], b_loc[1], self.field):
                    print("Black king in check!")
                    b_check = True
                    escape = False
                    for x in range(-1,2):
                        for y in range(-1,2):
                            if x == 0 and y == 0:
                                continue
                            else:
                                if ((b_loc[0]+x) >= 0 and (b_loc[0]+x) <= 7):
                                    if((b_loc[1]+y) >= 0 and (b_loc[1]+y) <= 7):
                                        if not self.white.inattackrange(b_loc[0]+x, b_loc[1]+y, self.field):
                                            escape = True
                                            break
                            if escape:
                                break
                    if not escape:
                        print("Game over! White wins.")
                        return 0
            else:
                print("Entering white king check behavior.")
                #Logic control for white to escape
                b_range = self.black.attackrange(self.field)
                w_loc = self.white.find_king()
                w_ind = -1
                for x in range(len(self.white.pieces)):
                    if self.white.pieces[x].name == "bK":
                        w_ind = x
                        break
                b_checker = self.black.canattack(w_loc[0], w_loc[1], self.field)
                if len(b_checker) == 1:
                    w_range = self.white.canattack(self.black.pieces[b_checker[0]].xpos, self.black.pieces[b_checker[0]].ypos, self.field)
                    if len(w_range) > 0:
                        #Use index 0 for lowest value piece that can attack
                        spot = [[self.white.pieces[w_range[0]].xpos, self.white.pieces[w_range[0]].ypos], [self.black.pieces[b_checker[0]].xpos, self.black.pieces[b_checker[0]].ypos]]
                        print(f'Moving {self.white.pieces[w_range[0]].name} from ({spot[0][0]}, {spot[0][1]}) to ({spot[1][0]}, {spot[1][1]}).')
                        self.white.pieces[w_range[0]].act_move(spot[1][0], spot[1][1])
                        w_check = False
                else:
                    #Checked by more than one piece, try and move to escape instead
                    for x in range(-1,2):
                        if not w_check:
                            break
                        else:
                            for y in range(-1,2):
                                if x == 0 and y == 0:
                                    continue
                                elif not w_check:
                                    break
                                else:
                                    #Keep bounds in board
                                    if ((w_loc[0]+x) >= 0 and (w_loc[0]+x) <= 7):
                                        if((w_loc[1]+y) >= 0 and (w_loc[1]+y) <= 7):
                                            if not b_range[w_loc[0]+x][w_loc[1]+y]:
                                                spot = [[w_loc[0], w_loc[1]], [w_loc[0]+x, w_loc[1]+y]]
                                                print(f'Moving {self.white.pieces[w_ind].name} from ({spot[0][0]}, {spot[0][1]}) to ({spot[1][0]}, {spot[1][1]}).')
                                                self.white.pieces[w_ind].act_move(spot[1][0], spot[1][1])
                                                w_check = False
                                                break
                print(f"spot is ({spot[0][0]}, {spot[0][1]}) to ({spot[1][0]}, {spot[1][1]}).")
                for ind in range(len(self.black.pieces)):
                    if (self.black.pieces[ind].xpos == spot[1][0] and self.black.pieces[ind].ypos == spot[1][1]):
                        print(f'Claiming piece {self.black.pieces[ind].name} at ({spot[1][0]}, {spot[1][1]}).')
                        self.black.remove_piece(ind)
                        break
                self.field.move_piece(spot)
                self.white.pawn_promote
                for y in range(7,-1,-1):
                    print(self.field.boardstate[0][y], self.field.boardstate[1][y], self.field.boardstate[2][y], self.field.boardstate[3][y], self.field.boardstate[4][y], self.field.boardstate[5][y], self.field.boardstate[6][y], self.field.boardstate[7][y])
                #Check for check
                b_loc = self.black.find_king()
                if self.white.inattackrange(b_loc[0], b_loc[1], self.field):
                    print("Black king in check!")
                    b_check = True
                    escape = False
                    for x in range(-1,2):
                        for y in range(-1,2):
                            if x == 0 and y == 0:
                                continue
                            else:
                                if ((b_loc[0]+x) >= 0 and (b_loc[0]+x) <= 7):
                                    if((b_loc[1]+y) >= 0 and (b_loc[1]+y) <= 7):
                                        if not self.white.inattackrange(b_loc[0]+x, b_loc[1]+y, self.field):
                                            escape = True
                                            break
                            if escape:
                                break
                    if not escape:
                        print("Game over! White wins.")
                        return 0
            #Check if black can move at all
            if not self.black.can_move(self.field):
                print("Game over! Black can't move, thus stalemate.")
            #Engage Opponent turn

            drawGameState(self.screen, self.gs.boardstate)

            #time.sleep(1)
            input("Press Enter to continue...")
            if not b_check:
                spot = self.black.turn(self.field)
                #Check for piece taken
                for ind in range(len(self.white.pieces)):
                    if (self.white.pieces[ind].xpos == spot[1][0] and self.white.pieces[ind].ypos == spot[1][1]):
                        print(f'Claiming piece {self.white.pieces[ind].name} at ({spot[1][0]}, {spot[1][1]}).')
                        self.white.remove_piece(ind)
                        break
                self.field.move_piece(spot)
                self.black.pawn_promote
                #Check for check
                for y in range(7,-1,-1):
                    print(self.field.boardstate[0][y], self.field.boardstate[1][y], self.field.boardstate[2][y], self.field.boardstate[3][y], self.field.boardstate[4][y], self.field.boardstate[5][y], self.field.boardstate[6][y], self.field.boardstate[7][y])
                w_loc = self.white.find_king()
                if self.black.inattackrange(w_loc[0], w_loc[1], self.field):
                    print("White king in check!")
                    w_check = True
                    escape = False
                    for x in range(-1,2):
                        for y in range(-1,2):
                            if x == 0 and y == 0:
                                continue
                            else:
                                if ((w_loc[0]+x) >= 0 and (w_loc[0]+x) <= 7):
                                    if((w_loc[1]+y) >= 0 and (w_loc[1]+y) <= 7):
                                        if not self.white.inattackrange(w_loc[0]+x, w_loc[1]+y, self.field):
                                            escape = True
                                            break
                            if escape:
                                break
                    if not escape:
                        print("Game over! Black wins.")
                        return 0
            else:
                #Logic control for black to escape
                print("Entering black king check behavior")
                w_range = self.white.attackrange(self.field)
                b_loc = self.black.find_king()
                b_ind = -1
                for x in range(len(self.black.pieces)):
                    if self.black.pieces[x].name == "wK":
                        b_ind = x
                        break
                w_checker = self.white.canattack(b_loc[0], b_loc[1], self.field)
                if len(w_checker) == 1:
                    b_range = self.black.canattack(self.white.pieces[w_checker[0]].xpos, self.white.pieces[w_checker[0]].ypos, self.field)
                    if len(b_range) > 0:
                        #Use index 0 for lowest value piece that can attack
                        spot = [[self.black.pieces[b_range[0]].xpos, self.black.pieces[b_range[0]].ypos], [self.white.pieces[w_checker[0]].xpos, self.white.pieces[w_checker[0]].ypos]]
                        print(f'Moving {self.black.pieces[b_range[0]].name} from ({spot[0][0]}, {spot[0][1]}) to ({spot[1][0]}, {spot[1][1]}).')
                        self.black.pieces[b_range[0]].act_move(spot[1][0], spot[1][1])
                        b_check = False
                else:
                    #Checked by more than one piece, try and move to escape instead
                    for x in range(-1,2):
                        if not b_check:
                            break
                        else:
                            for y in range(-1,2):
                                if x == 0 and y == 0:
                                    continue
                                elif not b_check:
                                    break
                                else:
                                    #Keep bounds in board
                                    if ((b_loc[0]+x) >= 0 and (b_loc[0]+x) <= 7):
                                        if((b_loc[1]+y) >= 0 and (b_loc[1]+y) <= 7):
                                            if not b_range[b_loc[0]+x][b_loc[1]+y]:
                                                spot = [[b_loc[0], b_loc[1]], [b_loc[0]+x, b_loc[1]+y]]
                                                print(f'Moving {self.black.pieces[b_ind].name} from ({spot[0][0]}, {spot[0][1]}) to ({spot[1][0]}, {spot[1][1]}).')
                                                self.black.pieces[b_ind].act_move(spot[1][0], spot[1][1])
                                                b_check = False
                                                break
                #Check for piece taken
                print(f"spot is ({spot[0][0]}, {spot[0][1]}) to ({spot[1][0]}, {spot[1][1]}).")
                for ind in range(len(self.white.pieces)):
                    if (self.white.pieces[ind].xpos == spot[1][0] and self.white.pieces[ind].ypos == spot[1][1]):
                        print(f'Claiming piece {self.white.pieces[ind].name} at ({spot[1][0]}, {spot[1][1]}).')
                        self.white.remove_piece(ind)
                        break
                self.field.move_piece(spot)
                self.black.pawn_promote
                #Check for check
                for y in range(7,-1,-1):
                    print(self.field.boardstate[0][y], self.field.boardstate[1][y], self.field.boardstate[2][y], self.field.boardstate[3][y], self.field.boardstate[4][y], self.field.boardstate[5][y], self.field.boardstate[6][y], self.field.boardstate[7][y])
                w_loc = self.white.find_king()
                if self.black.inattackrange(w_loc[0], w_loc[1], self.field):
                    print("White king in check!")
                    w_check = True
                    escape = False
                    for x in range(-1,2):
                        for y in range(-1,2):
                            if x == 0 and y == 0:
                                continue
                            else:
                                if ((w_loc[0]+x) >= 0 and (w_loc[0]+x) <= 7):
                                    if((w_loc[1]+y) >= 0 and (w_loc[1]+y) <= 7):
                                        if not self.white.inattackrange(w_loc[0]+x, w_loc[1]+y, self.field):
                                            escape = True
                                            break
                            if escape:
                                break
                    if not escape:
                        print("Game over! Black wins.")
                        return 0




            #Check if white can move at all
            if not self.white.can_move(self.field):
                print("Game over! White can't move, thus stalemate.")
            drawGameState(self.screen, self.gs.boardstate)
            input("Press Enter to continue...")
            #time.sleep(1)

            drawGameState(self.screen, self.gs.boardstate)
            self.clock.tick(MAX_FPS)
            david.display.flip()
        print("You shouldn't be here.")
        return 0

def main():
    testgame = Game()
    #for i in range(0,8):
        #print(testgame.field.boardstate[i])
    testgame.play_game()


if __name__=="__main__":
    main()
