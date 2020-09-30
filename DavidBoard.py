


'''
Thnking use this for user input as well as the board>?? idk. 
'''

import pygame as p
#from ChessAI import DavidChessEngine
import DavidChessEngine

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
    #IMAGES['wp'] = p.image.load("Images/wp.png") #from folder images / 'the picture to use for that piece.'
    #IMAGES['bp'] = p.image.load("Images/bp.png")
    pieces = ['wp','wR','wN','wB','wK','wQ', 'bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

'''
Main driver for code. Handle user Input and updating the graphics :)

'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = DavidChessEngine.GameState()#calling my ChessEngine for the state of the board
    #print(gs.board)
    loadImages() #only do this once before the while loop :)
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Responsible for all graphics in game
'''
def drawGameState(screen, gs): #this draws the squares on the board
    drawBoard(screen)
    #add piece highlighting or move suggestions (later?)
    drawPieces(screen, gs.board)#draw pieces on the squares

'''
Draw squares on board
'''
def drawBoard(screen):
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




if __name__ == "__main__": #Recommended way by Python
    main()



