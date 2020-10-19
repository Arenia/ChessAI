

import chesstest as ct

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}


        self.whiteToMove = True
        self.moveLog = []
    '''
    Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant
    '''
    def makeMove(self, move):
        print(self)
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log move for history
        self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves() #Don't worry about checks for now

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #range of 2d arrayList length of board ; num of rows
            for c in range(len(self.board[r])):  #Number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)#calls appropriate move functioon based on piece type
        return moves





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
            if c+1 <= 7: #capture to right
                if self.board[r-1][c+1][0] == 'b': #enemy to capture
                    moves.append(Move((r,c), (r-1, c+1), self.board))
        else: #black pawn moves
            if self.board[r+1][c] == "--": #1 square advance
                moves.append(Move( (r,c), (r+1, c), self.board) )
                if r == 1 and self.board[r+2][c] == "--": #2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c-1 >= 0:#capture to left
                if self.board[r+1][c-1][0] == 'w': #enemy piece to capture
                    moves.append(Move((r,c), (r+1, c-1), self.board))
            if c+1 <= 7: #capture to right; should use len because it's better practice... o, well
                if self.board[r+1][c+1][0] == 'w': #enemy to capture
                    moves.append(Move((r,c), (r+1, c+1), self.board))


        #Add pawn promotions later!!!

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
            for m in knightMoves:
                endRow = r + m[0]
                endCol = c + m[1]
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
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




class Move():
    #maps keys to values
    #key : value
    
    ranksToRows = {"1":7, "2":6, "3":5, "4":4,
                   "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3,
                   "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}
    
    
    
    def __init__(self, startSq, endSq, board):
        #Check if valid moves, tyler should do this!
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol #id between 0 and 7777
        print(self.moveID)

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def isWhite(self):
        if self.pieceMoved == "wK":
            return True
        elif self.pieceMoved == "wp":
            return True
        elif self.pieceMoved == "wQ":
            return True
        elif self.pieceMoved == "wR":
            return True
        elif self.pieceMoved == "wN":
            return True
        elif self.pieceMoved == "wB":
            return True
        else:
            return False

    '''
    Overriding equals method
    '''
    def __eq__(self, other): #Compare object to other object
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

