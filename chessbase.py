# Initial Board Version

class ChessPiece:
    #Basic methods for all pieces.
    def __init__(self, xcod, ycod, worth):
        self.xpos = xcod
        self.ypos = ycod
        self.value = worth

    def act_move(self, tar_xpos, tar_ypos):
        self.ypos = tar_ypos
        self.xpos = tar_xpos

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
        else:
            return false

    def occupation(tar_x, tar_y, team):
        if self.boardstate[tar_x][tar_y] == "":
            #empty spaces are unoccupied
            return false
        elif self.boardstate[tar_x][tar_y].isupper != team:
            #Check if opossing team
            return true
        else:
            return false

    def move_piece(self, spot):
        #Moves a piece from the coordinates given in a turn. Overwrites the target location, piece removal handled by Player classes.
        self.boardstate[spot[1][0]][spot[1][1]] = self.boardstate[spot[0][0]][spot[0][1]]
        self.boardstate[spot[0][0]][spot[0][1]] = ""

    def find_piece(self, identifier):
        collection = []
        for x in range(0,8):
            for y in range(0,8):
                if self.boardstate[x,y] == identifier:
                    collection.append([x,y])
        return collection

class King(ChessPiece):
    #Class and methods for Kings.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        #Value is set exceptionally high to disregard other attack attempts
        self.value = 999999
        if side:
            self.name = "K"
        else:
            self.name = "k"

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                x_dis = abs(tar_xpos - a)
                y_dis = abs(tar_ypos - b)
                if (x_dis == 0 and y_dis == 1) or (y_dis == 0 and x_dis == 1) or (y_dis == 1 and x_dis == 1):
                    if (field[tar_xpos][tar_ypos].isupper() != self.name.isupper()):
                        targets.append([a, b])
        return targets

    def move_attempt(self, tar_xpos, tar_ypos, field):
        x_dis = abs(self.xpos - tar_xpos)
        y_dis = abs(self.ypos - tar_ypos)
        if (x_dis == 0 and y_dis == 1) or (y_dis == 0 and x_dis == 1) or (y_dis == 1 and x_dis == 1):
            if (field[tar_xpos][tar_ypos].isupper() != self.name.isupper()):
                return true
            else:
                return false
        else:
            return false

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if move_attempt(a, b, field):
                    targets.append([a, b])
        return targets

class Rook(ChessPiece):
    #Classes and methods for Rooks.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        self.value = 5
        if side:
            self.name = "R"
        else:
            self.name = "r"

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                x_dis = tar_xpos - a
                y_dis = tar_ypos - b
                if (x_dis == 0 and y_dis != 0):
                    block = false
                    if (y_dis > 0):
                        #Aim down
                        for y in range(0,y_dis):
                            if (len(field[tar_xpos][(y-tar_pos)]) != 0):
                                block = true
                        if not block:
                            targets.append([a,b])
                    else:
                        #Aim up
                        for y in range(0,abs(y_dis)):
                            if (len(field[tar_xpos][(tar_ypos-y)]) != 0):
                                block = true
                        if not block:
                            targets.append([a,b])
                elif (y_dis == 0 and x_dis != 0):
                    block = false
                    if (x_dis > 0):
                        for x in range(0,x_dis):
                            if (len(field[(x-tar_xpos)][tar_ypos]) != 0):
                                block = true
                        if not block:
                            targets.append([a,b])
                    else:
                        #Aim up
                        for x in range(0,abs(x_dis)):
                            if (len(field[(x-tar_xpos)][tar_ypos]) != 0):
                                block = true
                        if not block:
                            targets.append([a,b])
        return targets

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

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if move_attempt(a, b, field):
                    targets.append([a, b])
        return targets

class Knight(ChessPiece):
    #Class and methods for knights.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        self.value = 3
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

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if move_attempt(a, b, field):
                    targets.append([a, b])
        return targets

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                x_dis = abs(tar_xpos - a)
                y_dis = abs(tar_ypos - b)
                if (x_dis == 1 and y_dis == 2) or (x_dis == 2 and y_dis == 1):
                    targets.append([a, b])

class Bishop(ChessPiece):
    #Class and methods for bishops.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        self.value = 3
        if side:
            self.name = "B"
        else:
            self.name = "b"

    def move_attempt(self, tar_xpos, tar_ypos, field):
        x_dis = self.xpos - tar_xpos
        y_dis = self.ypos - tar_ypos
        if (abs(x_dis) == abs(y_dis)):
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

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                x_dis = tar_xpos - a
                y_dis = tar_ypos - b
                if (abs(x_dis) == abs(y_dis)):
                    block = false
                    #Either x or y works, both funcion
                    if (x_dis > 0):
                        for x in range(0,x_dis):
                            if (len(field[(x-tar_xpos)][x-tar_ypos]) != 0):
                                block = true
                        if not block:
                            targets.append([a, b])
                    else:
                        for x in range(0,abs(x_dis)):
                            if (len(field[(tar_xpos-x)][tar_ypos-x]) != 0):
                                block = true
                        if not block:
                            targets.append([a, b])
        return targets

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if move_attempt(a, b, field):
                    targets.append([a, b])
        return targets

class Queen(ChessPiece):
    #Class and method for queens. Uses the methods from rook and bishop for simplicity's sake.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        self.value = 9
        if side:
            self.name = "Q"
        else:
            self.name = "q"

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
        elif (x_dis == y_dis):
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

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if move_attempt(a, b, field):
                    targets.append([a, b])
        return targets

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                x_dis = tar_xpos - a
                y_dis = tar_ypos - b
                if (x_dis == 0 and y_dis != 0):
                    block = false
                    if (y_dis > 0):
                        #Aim down
                        for y in range(0,y_dis):
                            if (len(field[tar_xpos][(y-tar_ypos)]) != 0):
                                block = true
                        if not block:
                            targets.append([a, b])
                    else:
                        #Aim up
                        for y in range(0,abs(y_dis)):
                            if (len(field[tar_xpos][(tar_ypos-y)]) != 0):
                                block = true
                        if not block:
                            targets.append([a, b])
                elif (y_dis == 0 and x_dis != 0):
                    block = false
                    if (x_dis > 0):
                        for x in range(0,x_dis):
                            if (len(field[(x-tar_xpos)][tar_ypos]) != 0):
                                block = true
                        if not block:
                            targets.append([a, b])
                    else:
                        #Aim up
                        for x in range(0,abs(x_dis)):
                            if (len(field[(x-tar_xpos)][tar_ypos]) != 0):
                                block = true
                        if not block:
                            return false
                elif (x_dis == y_dis):
                    block = false
                    #Either x or y works, both funcion
                    if (x_dis > 0):
                        for x in range(0,x_dis):
                            if (len(field[(x-tar_xpos)][x-tar_ypos]) != 0):
                                block = true
                        if not block:
                            targets.append([a, b])
                    else:
                        for x in range(0,abs(x_dis)):
                            if (len(field[(tar_xpos-x)][tar_ypos-x]) != 0):
                                block = true
                        if not block:
                            targets.append([a, b])
        return targets

class BlackPawn(ChessPiece):
    #Class and methods for black pawns. Separated due to movement checks being different between color.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        self.value = 1
        if side:
            self.name = "P"
        else:
            self.name = "p"


    def move_attempt(self, tar_xpos, tar_ypos, field):
        if (self.ypos == tar_ypos-1):
            if (self.xpos == tar_xpos) and (len(field[tar_xpos][tar_ypos]) == 0):
                return true
            elif (((self.xpos == tar_xpos+1) or (self.xpos == tar_xpos-1)) and (len(field[tar_xpos][tar_ypos]) != 0)):
                return true
            else:
                return false
        else:
            return false

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if (tar_ypos == b-1):
                    if (tar_xpos == a) and (len(field[a][b]) == 0):
                        targets.append([a, b])
                    elif (((tar_xpos == a+1) or (tar_xpos == a-1)) and (len(field[a][b]) != 0)):
                        targets.append([a, b])
        return targets

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for x in range(-1,2):
            if move_attempt(self.xpos+x, self.ypos-1, field):
                targets.append([self.xpos+x, self.ypos-1])
        return targets

class WhitePawn(ChessPiece):
    #Class and methods for white pawns. Separated due to movement checks being different between color.

    def __init__(self, xcod, ycod, side):
        ChessPiece.init(xcod, ycod)
        self.value = 1
        if side:
            self.name = "P"
        else:
            self.name = "p"

    def move_attempt(self, tar_xpos, tar_ypos, field):
        if (self.ypos == tar_ypos+1):
            if (self.xpos == tar_xpos) and (len(field[tar_xpos][tar_ypos]) == 0):
                return true
            elif (((self.xpos == tar_xpos+1) or (self.xpos == tar_xpos-1)) and (len(field[tar_xpos][tar_ypos]) != 0)):
                return true
            else:
                return false
        else:
            return false

    def distant_range(self, tar_xpos, tar_ypos, field):
        #use passed target as the location of the piece
        #returns a list of indicies that can attack a given square next turn (two turns to reach)
        targets = []
        for a in range(0,8):
            for b in range(0,8):
                if (tar_ypos == b+1):
                    if (tar_xpos == a) and (len(field[a][b]) == 0):
                        targets.append([a, b])
                    elif (((tar_xpos == a+1) or (tar_xpos == a-1)) and (len(field[a][b]) != 0)):
                        targets.append([a, b])
        return targets

    def arange(self, field):
        #Returns an array containing each set of indices it can attack.
        targets = []
        for x in range(-1,2):
            if move_attempt(self.xpos+x, self.ypos+1, field):
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
            self.pieces.append(BlackPawn(x, 6, false))

        #Initialize Bishops
        self.pieces.append(Bishop(2,7, false))
        self.pieces.append(Bishop(5,7, false))

        #Initialize Knights
        self.pieces.append(Knight(1,7, false))
        self.pieces.append(Knight(6,7, false))

        #Initialize Rooks
        self.pieces.append(Rook(0,7, false))
        self.pieces.append(Rook(7,7, false))

        #Initialize Queen
        self.pieces.append(Queen(3,7, false))

        #Initialize King
        self.pieces.append(King(4,7, false))



    def find_king(self):
        for piece in self.pieces:
            if piece.name.lower() == "k":
                target = [piece.xpos, piece[x].ypos]
                return target

    def remove_piece(self, ind):
        self.pieces.remove(ind)
        self.pieceCount = self.pieceCount-1

    def canattack(self, tar_x, tar_y, field):
        #Checks what pieces can attack the spot
        result = []
        for x in range(self.pieces):
            #Assume space to attack is owned for the sake of check
            if self.pieces[x].move_attempt(x,y,field):
                result.append(x)
                break
        return result

    def inattackrange(self, tar_x, tar_y, field):
        #check for checkmate
        result = false
        for piece in self.pieces:
            if piece.move_attempt(tar_x,tar_y,field):
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

    def can_move(self, field):
        arange = self.attackrange(field)
        count = 0
        for x in range(8):
            for y in range(8):
                if arange[x][y]:
                    count += 1
        if count > range(self.pieces):
            return true
        #if condition falls through
        return false

    def turn(self, field):
        #Search for highest value piece to take. If can't take, aim at highest in range next turn. If none in range, random move.
        #Don't need to check if king can be attacked, assumed not if game is going
        #Check for queen
        target = field.find_piece("Q")
        if target:
            if inattackrange(target[0][0], target[0][1], field):
                attack_list = canattack(target[0], target[1], field)
                #Piece to use, random from the available attackers
                ptu = random.choice(attack_list)
                coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos], [target[0][0], target[0][1]]]
                print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({target[0][0]}, {target[0][1]}).')
                self.pieces[ptu].act_move(tar_x, tar_y)
                return coordinates
        #Queen out of range, try to attack rook
        target = field.find_piece("R")
        if target:
            #Shuffle target to randomize target
            target = random.shuffle(target)
            #Check each piece through the list
            for x in range(target):
                if inattackrange(target[x][0], target[x][1], field):
                    attack_list = canattack(target[x][0], target[x][1], field)
                    #Piece to use, random from the available attackers
                    ptu = random.choice(attack_list)
                    coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos], [target[x][0], target[x][1]]]
                    print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({target[0][0]}, {target[0][1]}).')
                    self.pieces[ptu].act_move(target[x][0], target[x][1])
                    return coordinates
        #No rooks, sample both bishops and knights at the same time
        target = field.find_piece("B")
        target.extend(find_piece("N"))
        if target:
            #Shuffle target to randomize target
            target = random.shuffle(target)
            #Check each piece through the list
            for x in range(target):
                if inattackrange(target[x][0], target[x][1], field):
                    attack_list = canattack(target[x][0], target[x][1], field)
                    #Piece to use, random from the available attackers
                    ptu = random.choice(attack_list)
                    coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos], [target[x][0], target[x][1]]]
                    print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({target[0][0]}, {target[0][1]}).')
                    self.pieces[ptu].act_move(target[x][0], target[x][1])
                    return coordinates
        #No knights or bishops, pawns
        target = field.find_piece("P")
        if target:
            #Shuffle target to randomize target
            target = random.shuffle(target)
            #Check each piece through the list
            for x in range(target):
                if inattackrange(target[x][0], target[x][1], field):
                    attack_list = canattack(target[x][0], target[x][1], field)
                    #Piece to use, random from the available attackers
                    ptu = random.choice(attack_list)
                    coordinates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos], [target[x][0], target[x][1]]]
                    print(f'Moving {self.pieces[ptu].name} from ({self.pieces[ptu].xpos}, {self.pieces[ptu].ypos}) to ({target[0][0]}, {target[0][1]}).')
                    self.pieces[ptu].act_move(target[x][0], target[x][1])
                    return coordinates
        #No pawns, try and check king
        #use piece's attack range from king's position?
        target = field.find_piece("K")
        #Iterates through pieces, lower value first
        for i in range(self.pieces):
            #farside returns a two layer array containing the indicies that can attack target
            #nearside returns a two layer array containing the indicies that the piece can reach now
            #nearside and farside locations must match for a valid move
            #Use target as location to evaluate for
            farside = self.pieces[i].distant_range(target[0][0],target[0][1],field)
            nearside = self.pieces[i].arange(field)
            #Valid location if piece.arange == piece.distant_range
            for x in range(farside):
                if not breakout:
                    for y in range(nearside):
                        if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                            #farside and nearside match, valid move
                            coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                            self.pieces[i].act_move(farside[x][0], farside[x][1])
                            print(f'Moving {self.pieces[ptu].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[0][0]}, {farside[0][1]}).')
                            return coordinates
        #Falling through loop assumes unable to check king, check queen
        target = field.find_piece("Q")
        #Iterates through pieces, lower value first
        for i in range(self.pieces):
            #farside returns a two layer array containing the indicies that can attack target
            #nearside returns a two layer array containing the indicies that the piece can reach now
            #nearside and farside locations must match for a valid move
            #Use target as location to evaluate for
            farside = self.pieces[i].distant_range(target[0][0],target[0][1],field)
            nearside = self.pieces[i].arange(field)
            #Valid location if piece.arange == piece.distant_range
            for x in range(farside):
                if not breakout:
                    for y in range(nearside):
                        if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                            #farside and nearside match, valid move
                            coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                            print(f'Moving {self.pieces[ptu].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[0][0]}, {farside[0][1]}).')
                            self.pieces[i].act_move(farside[x][0], farside[x][1])
                            return coordinates
        #Queen not checked, check rook?
        target = field.find_piece("R")
        #Iterates through pieces, lower value first
        for i in range(self.pieces):
            #farside returns a two layer array containing the indicies that can attack target
            #nearside returns a two layer array containing the indicies that the piece can reach now
            #nearside and farside locations must match for a valid move
            #Use target as location to evaluate for
            farside = self.pieces[i].distant_range(target[0][0],target[0][1],field)
            nearside = self.pieces[i].arange(field)
            #Valid location if piece.arange == piece.distant_range
            for x in range(farside):
                if not breakout:
                    for y in range(nearside):
                        if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                            #farside and nearside match, valid move
                            coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                            print(f'Moving {self.pieces[ptu].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[0][0]}, {farside[0][1]}).')
                            self.pieces[i].act_move(farside[x][0], farside[x][1])
                            return coordinates
        #No rook, check bishop/knight?
        target = field.find_piece("B")
        target.extend(find_piece("N"))
        #Iterates through pieces, lower value first
        for i in range(self.pieces):
            #farside returns a two layer array containing the indicies that can attack target
            #nearside returns a two layer array containing the indicies that the piece can reach now
            #nearside and farside locations must match for a valid move
            #Use target as location to evaluate for
            farside = self.pieces[i].distant_range(target[0][0],target[0][1],field)
            nearside = self.pieces[i].arange(field)
            #Valid location if piece.arange == piece.distant_range
            for x in range(farside):
                if not breakout:
                    for y in range(nearside):
                        if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                            #farside and nearside match, valid move
                            coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                            print(f'Moving {self.pieces[ptu].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[0][0]}, {farside[0][1]}).')
                            self.pieces[i].act_move(farside[x][0], farside[x][1])
                            return coordinates
        #No bishop/knight, pawns?
        target = field.find_piece("P")
        #Iterates through pieces, lower value first
        for i in range(self.pieces):
            #farside returns a two layer array containing the indicies that can attack target
            #nearside returns a two layer array containing the indicies that the piece can reach now
            #nearside and farside locations must match for a valid move
            #Use target as location to evaluate for
            farside = self.pieces[i].distant_range(target[0][0],target[0][1],field)
            nearside = self.pieces[i].arange(field)
            #Valid location if piece.arange == piece.distant_range
            for x in range(farside):
                if not breakout:
                    for y in range(nearside):
                        if farside[x][0] == nearside[y][0] and farside[x][1] == nearside[y][1]:
                            #farside and nearside match, valid move
                            coordinates = [[self.pieces[i].xpos, self.pieces[i].ypos], [farside[x][0], farside[x][1]]]
                            print(f'Moving {self.pieces[ptu].name} from ({self.pieces[i].xpos}, {self.pieces[i].ypos}) to ({farside[0][0]}, {farside[0][1]}).')
                            self.pieces[i].act_move(farside[x][0], farside[x][1])
                            return coordinates

        #Unable to check any piece, take a random move
        ptu = random.choice(range(self.pieces))
        attacklist = self.pieces[ptu].arange(field)
        random.shuffle(attacklist)
        coordiates = [[self.pieces[ptu].xpos, self.pieces[ptu].ypos],[attacklist[0][0], attacklist[0][1]]]
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

        #When initalizing pieces, true implies white
        #Initialize pawns
        for x in range(0,8):
            pieces.append(WhitePawn(x, 1, true))

        #Initialize Bishops
        pieces.append(Bishop(2,0, true))
        pieces.append(Bishop(5,0, true))

        #Initialize Knights
        pieces.append(Knight(1,0, true))
        pieces.append(Knight(6,0, true))

        #Initialize Rooks
        pieces.append(Rook(0,0, true))
        pieces.append(Rook(7,0, true))

        #Initialize Queen
        pieces.append(Queen(3,0, true))

        #Initialize King
        pieces.append(King(4,0, true))


    def remove_piece(self, ind):
        #Value to be used later
        #self.value -= self.pieces[ind].value
        self.pieces.remove(ind)
        self.pieces.pieceCount = self.pieces.pieceCount-1

    def find_king(self):
        target = [0,0]
        for piece in self.pieces:
            if piece.name.lower() == "k":
                target = [piece.xpos, piece[x].ypos]
                return target

    def inattackrange(self, tar_x, tar_y, field):
        #check for checkmate
        result = false
        for piece in self.pieces:
            #Assume space to attack is owned for the sake of check
            if piece.move_attempt(tar_x,tar_y,field):
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
                if arange[x][y]:
                    continue
                else:
                    for piece in self.pieces:
                        if piece.move_attempt(x,y,field):
                            arange[x][y] = true
                            break
        return arange

    def can_move(self, field):
        arange = self.attackrange(field)
        count = 0
        for x in range(8):
            for y in range(8):
                if arange[x][y]:
                    count += 1
        if count > range(self.pieces):
            return true
        #if condition falls through
        return false


    def turn(self, field):
        #Set as full user control, can be adjusted on a later date
        while true:
            sel_x = input("Input the x coordinate of your piece to move: ")
            sel_y = input("Input the y coordinate of your piece to move: ")
            sel_index = -1
            for x in range(self.pieces.size):
                if sel_x == self.pieces[x].xpos and sel_y == self.pieces[x].ypos:
                    sel_index = x
                    break
            if sel_index != -1:
                tar_x = input("Input the x coordinate to move to: ")
                tar_y = input("Input the y coordinate to move to: ")
                if move_attempt(tar_x, tar_y, field):
                    coordinates = [[sel_x, sel_y], [tar_x, tar_y]]
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
        #Note: Factor a stalemate
        while true:
            #Engage Player turn
            spot = self.white.turn(self.field)
            #Check for piece taken
            for ind in range(self.black.pieces):
                if (self.black.pieces[ind].xpos == spot[1][0] and self.black.pieces[ind].ypos == spot[1][1]):
                    self.black.remove_piece(ind)
                    break
            self.field.move_piece(spot)
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
            #Check if black can move at all
            if not self.black.can_move(self.field):
                print("Game over! Black can't move, thus stalemate.")
            #Engage Opponent turn
            spot = self.black.turn(self.field)
            #Check for piece taken
            for ind in range(self.white.pieces):
                if (self.white.pieces[ind].xpos == spot[1][0] and self.white.pieces[ind].ypos == spot[1][1]):
                    self.white.remove_piece(ind)
                    break
            self.field.move_piece(spot)
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
            #Check if white can move at all
            if not self.whte.can_move(self.field):
                print("Game over! White can't move, thus stalemate.")
        print("You shouldn't be here.")
        return 0

def main():
    print("Compiles and runs.")

if __name__=="__main__":
    main()
