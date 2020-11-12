'''
Thnking use this for user input as well as the board>?? idk.
'''

import pygame as p
#from ChessAI import DavidChessEngine
import DavidChessEngine
import random

p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8 #8x8
SQ_SIZE = HEIGHT //DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionary of images. this will be call exacly once in main
'''
def loadImages():
    #IMAGES['wp'] = p.image.load("Images/P.png") #from folder images / 'the picture to use for that piece.'
    #IMAGES['bp'] = p.image.load("Images/bP.png")
    pieces = ['wp','wR','wN','wB','wK','wQ', 'bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images2/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
'''
Main driver for code. Handle user Input and updating the graphics :)

'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = DavidChessEngine.GameState()#calling my ChessEngine for the state of the board

    validMoves = gs.getValidMoves()  # Don't regenerate this until a valide move is made
    moveMade = False  # flag for when move is made

    animate = False #flag variable for when we should animate a move

    print(gs.board)
    loadImages() #only do this once before the while loop :)
    running = True
    sqSelected = () #no square selected initially, keep track of last click of user (tuple: (row,col))
    playerClicks = [] #keep track of player clicks (two tuples: [(6, 4), (4,4)]

    gameOver = False


    while running:
        if gs.whiteToMove == True:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
            #Mouse handler
                elif e.type == p.MOUSEBUTTONDOWN:
                    #if not gameOver:
                        location = p.mouse.get_pos()  # (x,y) location of mouse
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE

                        if sqSelected == (row,col): #User clicked the same square twice
                            print("Cancelling selection")
                            sqSelected = () #deselect :)
                            playerClicks = [] #clear player clicks
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                        if len(playerClicks) == 2: #After 2nd click
                            # Call DavidChessEngine for log and moving
                            move = DavidChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    print(move.getChessNotation())
                                    gs.makeMove(validMoves[i])
                                    moveMade = True

                                    sqSelected = () #reset user Clicks :)
                                    playerClicks = []
                                else:
                                    #print("Not your turn!!!! >:(")
                                    sqSelected = ()  # reset user Clicks :)
                                    playerClicks = []
            #Key handlers while playing white
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_r: #reset the board when 'r' is pressed
                        gs = DavidChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                if moveMade:
                    animateMoves(gs.moveLog[-1], screen, gs.board, clock)
                    validMoves = gs.getValidMoves()
                    moveMade = False




#Blacks turn/ AI TURN!!!
        else:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False

                if not gs.checkMate and not gs.whiteToMove:
                    movelist = gs.getValidMoves()
                    random.shuffle(movelist)
                    gs.makeMove(movelist[0])
                    moveMade = True
                #This is needed so that the AI doesn't choose how white moves at all
                if moveMade:
                    animateMoves(gs.moveLog[-1], screen, gs.board, clock)
                    validMoves = gs.getValidMoves()
                    moveMade = False







        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()






'''
Responsible for all graphics in game
'''
def drawGameState(screen, gs, validMoves, sqSelected): #this draws the squares on the board
    drawBoard(screen)
    #add piece highlighting or move suggestions (later?)
    drawPieces(screen, gs.board)#draw pieces on the squares
    highlightSquares(screen, gs, validMoves, sqSelected)#Could put this after the drawGameState call in the main loop
'''
Draw squares on board
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            #Don't draw pieces here just incase we want to implement highlighting
            #Extra loop isn't that expensive
'''
Draw pieces on board using current GameState.board
'''
def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty squares
                screen.blit( IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE) ) #Puts the piece in for us




'''
Highlight square selected and moves fro piece selected
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is piece that can be moved
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #Transperancy value -> 0 transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
			#highlight moves from that square to moves
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
					#Now lets put this in draw game state
	


def animateMoves(move, screen, board, clock): #Not the best algorithm to do this but hey, it works
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
		#draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Green"))
    screen.blit(textObject, textLocation.move(2,2))


if __name__ == "__main__": #Recommended way by Python
    main()
