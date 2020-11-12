#Identify where Tyler needs to put his AI logic (BareBones AI)
#randomShuffle => random.shuffle(  arrasy/List giving  )
    #Shuffles in place no need to seed



#class AI():
	# All THIS
	# Get all pieces and give values



#class ComputerPlayer():
	#Best



class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "wB", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "wQ", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        #value of piece; this could be used for making the AI Tyler
        self.valOfPiece = {'p': 1, 'R': 2, 'N': 3,
                              'B': 4, 'Q': 5, 'K': 6}

        self.whiteToMove = True
        self.moveLog = []
        #The following two are for checking checks..
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () #cordinates for square where en passant capture is possible
        self.currentCastleingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastleingRights.wks, self.currentCastleingRights.bks,
                                             self.currentCastleingRights.wqs, self.currentCastleingRights.bqs)]

    '''
    Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant
    '''
    def makeMove(self, move):
        #print(self)
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log move for history
        self.whiteToMove = not self.whiteToMove
        #update kings locations
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawnPromotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' #capturing pawn

        #update enpassantPoss var
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #only 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.endCol)#integer divsision; hints '//'
        else:
            self.enpassantPossible = ()


        #Castle Move
        if move.isCastleMove:#checking squares already done
            if move.endCol - move.startCol ==2: #kingside castle move
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #mooves the rook
                self.board[move.endRow][move.endCol+1] = '--'
            else: #queenside castle
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] #moves rook
                self.board[move.endRow][move.endCol-2] = '--'
        #update castling rights - whenver a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastleingRights.wks, self.currentCastleingRights.bks,
                                                 self.currentCastleingRights.wqs, self.currentCastleingRights.bqs))

#######################################################################################################     BoardStateUpdateChecks

    def updateCastleRights(self,move):
        if move.pieceMoved == 'wK':
            self.currentCastleingRights.wks = False
            self.currentCastleingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastleingRights.bks = False
            self.currentCastleingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastleingRights.wqs = False
                elif move.startCol ==7: #right rook
                    self.currentCastleingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastleingRights.bqs = False
                elif move.startCol ==7: #right rook
                    self.currentCastleingRights.bks = False

    def getValidMoves(self):
        #for log in self.castleRightsLog:
            #print(log.wks, log.wqs, log.bks, log.bqs, end=", ")
        #print()



        tempEnpassantPossible = self.enpassantPossible #save value for switching back and forth; This algorithm is bad
        tempCasleRights = CastleRights(self.currentCastleingRights.wks, self.currentCastleingRights.bks,
                                       self.currentCastleingRights.wqs, self.currentCastleingRights.bqs) #Copy current rights
        '''
        This algorithm definitely has issues.
        1) generate all possible moves
        2) for each move, make move
        3) generate all opponenet's moves
        4) for each of your opponent's mvoes, see if they attack your king
        5) if they do attack your king, not a valid move
        '''
        #return self.getAllPossibleMoves() #Don't worry about checks for now
        moves = self.getAllPossibleMoves()#1 done

        # fixes recursion issue
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        for i in range (len(moves)-1, -1, -1): #when removing from a list go backwards through list
            self.makeMove(moves[i])
            #3 and 4 finished using inCheck()
            self.whiteToMove = not self.whiteToMove #Thinks that it's opp turn

            if self.inCheck():
                moves.remove(moves[i]) #5
            self.whiteToMove = not self.whiteToMove
            self.undoMove()#automatically undo if invalid basically; comment this out to see it place all the pieces of where it can be moves to basically.  It's really weird
        if len(moves) == 0:
            if self.inCheck():
                print("CheckMate")
                self.checkMate = True
            else:
                print("StaleMate")
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastleingRights = tempCasleRights
        return moves

    '''
    Determine if current player is in check
    '''
#Decoupling :)
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    '''
    Determine if enemy can attack the square r,c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for moves in oppMoves:
            if moves.endRow == r and moves.endCol == c: #square is under attack
                #self.whiteToMove = not self.whiteToMove #switch turns back
                return True #square is under attack
        return False

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns back
            #update king's position if needed
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            #undo en pass
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            #undo a 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
            #undo castling rights
            self.castleRightsLog.pop() #rid new castle rights from move undoing
            self.currentCastleingRights = self.castleRightsLog[-1] #set current castle rights to last one on list
            #undo castle Move
            if move.isCastleMove:
                if move.endCol - move.startCol ==2: #kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol -1] = '--'
                else:
                    self.board[move.endRow][move.endCol +-2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol +1] = '--'

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #range of 2d arrayList length of board ; num of rows
            for c in range(len(self.board[r])):  #Number of cols in given row
                turn = self.board[r][c][0] # index string assuming
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)#calls appropriate move functioon based on piece type
        return moves


#######################################################################################################     MOVEMENT

    '''
    Get all pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #1 square advance
                moves.append(Move( (r,c), (r-1, c), self.board) )
                if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c-1 >= 0:#capture to left
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r,c), (r-1, c-1), self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))
            if c+1 <= 7: #capture to right
                if self.board[r-1][c+1][0] == 'b': #enemy to capture
                    moves.append(Move((r,c), (r-1, c+1), self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))
        else: #black pawn moves
            if self.board[r+1][c] == "--": #1 square advance
                moves.append(Move( (r,c), (r+1, c), self.board) )
                if r == 1 and self.board[r+2][c] == "--": #2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c-1 >= 0:#capture to left
                if self.board[r+1][c-1][0] == 'w': #enemy piece to capture
                    moves.append(Move((r,c), (r+1, c-1), self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            if c+1 <= 7: #capture to right; should use len because it's better practice... o, well
                if self.board[r+1][c+1][0] == 'w': #enemy to capture
                    moves.append(Move((r,c), (r+1, c+1), self.board))
                elif (r+1,c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))
    '''
    Get all Rook moves for the pawn located at row, col and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        #break
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))

    '''
    Generate all valid castle moves fro the king at (r,c) and add them to the list of moves
    '''
    def getCastleMoves(self, r,c,moves):
        if self.squareUnderAttack(r,c):
            return #can't castle while we are in check
        if (self.whiteToMove and self.currentCastleingRights.wks) or (not self.whiteToMove and self.currentCastleingRights.bks):
            self.getKingsideCastleMoves(r,c,moves)
        if (self.whiteToMove and self.currentCastleingRights.wqs) or (not self.whiteToMove and self.currentCastleingRights.bqs):
            self.getQueensideCastleMoves(r,c,moves)

    def getKingsideCastleMoves(self,r,c,moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c), (r,c+2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self,r,c,moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3]:
            if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r,c), (r,c-2), self.board, isCastleMove=True))

class Move():
    #maps keys to values
    #key : value

    ranksToRows = {"1":7, "2":6, "3":5, "4":4,
                   "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3,
                   "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False): #enpassantPossible is a optional variable!@!!!
        #Check if valid moves, tyler should do this!
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol #id between 0 and 7777
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7) # same thing as if statement
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        #CastleMove
        self.isCastleMove = isCastleMove
        #print(self.moveID)

    def getChessNotation(self):#This can be used to translate to the ARM
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    '''
    Overriding equals method
        using the moveID
    '''
    def __eq__(self, other): #Compare object to other object
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
