from PIL import ImageGrab
from copy import copy
from move import Move
import sys
import serial, time, pyautogui
from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)

waiting = False

startingX = 8130
startingY = 1260
step = 345
board = []
#green, orange, cyan, purple, red, yellow, blue
activeNames = ["S", "L", "I", "T", "Z", "O", "J"]
activeMoveLeft = [[-3,-4], [-3,-4,-3,-3], [-3,-5], [-3,-4,-3,-3], [-3,-4], [-4], [-3,-4,-3,-3]]
activeMoveRight = [[4,4], [4,4,4,3], [3,4], [4,4,4,5], [4,4], [4], [4,4,4,5]]
activeShape = [
        [
            [[0,0],[1,0],[-1,1],[0,1]],
            [[0,0],[1,0],[1,1],[1,2]]
        ],
        [
            [[0,0],[-2,1],[-1,1],[0,1]],
            [[-1,0],[-1,1],[-1,2],[0,2]],
            [[-2,2],[-2,1],[-1,1],[0,1]],
            [[-2,0],[-1,0],[-1,1],[-1,2]]
        ],
        [
            [[0,0],[1,0],[2,0],[3,0]],
            [[2,-1],[2,0],[2,1],[2,2]]
        ],
        [
            [[0,0],[-1,1],[0,1],[1,1]],
            [[0,0],[0,1],[0,2],[1,1]],
            [[-1,1],[0,1],[1,1],[0,2]],
            [[0,0],[-1,1],[0,1],[0,2]]
        ],
        [
            [[0,0],[1,0],[1,1],[2,1]],
            [[2,0],[2,1],[1,1],[1,2]]
        ],
        [
            [[0,0],[1,0],[0,1],[1,1]],
        ],
        [
            [[0,0],[0,1],[1,1],[2,1]],
            [[1,0],[2,0],[1,1],[1,2]],
            [[0,1],[1,1],[2,1],[2,2]],
            [[1,0],[1,1],[1,2],[0,2]]
        ]
    ]

activeList = [[84, 209, 4], [243, 95, 8], [0,201,232], [167, 42, 243], [247, 39, 54], [238, 191, 3], [39, 31, 245]]
ghostList = [[14, 57, 13], [63, 23, 12], [11, 51, 56], [41, 21, 63], [65, 21, 17], [56, 48, 13], [14, 20, 69]]
tolerance = 4
brickTolerance = 4
colorSampleDistance = 11
negativeColor = [16, 16, 16]
ser = None


def getgamestate():
    board.clear()
    px = getRectAsImage((0,0,1920,1080))
    activeIndex = None
    activeX = None
    activeY = None
    gridY = 0
    #px.save("C:\Gamedev\screencapture_256_256.png", format='png')
    for y in range(startingY, startingY + step*20, step):
        #print("grid = {}, {}".format(gridY, y))
        gridX = 0
        row = []
        for x in range(startingX, startingX + step*10, step):
            colorFound = False
            if(gridY>=18 or gridY < 3):
                tolerance = 10
            else:
                tolerance = 4
            for i in range(-colorSampleDistance, colorSampleDistance):
                color = px.getpixel((int(x/10), int(y/10) + i))
                isEmpty = abs(color[0] - negativeColor[0]) < tolerance and abs(color[1] - negativeColor[1]) < tolerance and abs(color[2] - negativeColor[2]) < tolerance
                isGhost = False
                isActive = False
                if(not isEmpty): #there is some block here
                    for ghostColor in ghostList:
                        isGhost = abs(color[0] - ghostColor[0]) < brickTolerance and abs(color[1] - ghostColor[1]) < brickTolerance and abs(color[2] - ghostColor[2]) < brickTolerance
                        if(isGhost):
                            break
                    for i in range(0, len(activeList)):
                        activeColor = activeList[i]
                        isActive = abs(color[0] - activeColor[0]) < brickTolerance and abs(color[1] - activeColor[1]) < brickTolerance and abs(color[2] - activeColor[2]) < brickTolerance
                        if(isActive and activeIndex == None):
                            activeIndex = i
                            activeX = gridX
                            activeY = gridY
                            break
                        elif(isActive):
                            break
                colorWithinRange = isEmpty or isGhost or isActive
                if(not colorFound and colorWithinRange):
                    row.append(False)
                    #print("- ", end='')
                    colorFound = True
            if(not colorFound):
                row.append(True)
                #print('+ ', end='')
            gridX+=1
        gridY+=1
        board.append(row)
        #print("")
        #print_board(board)
    #print(" ")
    if(activeIndex != None):
        analyze_move(activeIndex, activeX, activeY)

def analyze_move(activeIndex, activeX, activeY): #x, y, index of color of first found active block
    heuristicList = []
    moveList = []
    print("Board height is {} and the active piece is at [{}, {}]".format(len(board), activeX, activeY))
    print("The {} block is currently active!".format(activeNames[activeIndex]))
    for j in range(0, 1): #rotation
        for i in range(activeMoveLeft[activeIndex][j], activeMoveRight[activeIndex][j] - 1):
            #print("i = {}, j = {}".format(i, j))
            drop_distance = len(board)
            for block in activeShape[activeIndex][j]:
                x = activeX + block[0] + i
                y = activeY + block[1]
                print("checking {},{}".format(x,y))
                distance = len(board) - y
                for k in range(y, len(board) - 1):
                    if(board[k][x]):
                        distance = k - y
                        break
                if(distance < drop_distance):
                    drop_distance = distance
            activeX_temp = activeX + i
            activeY_temp = activeY + drop_distance - 1
            heuristic = get_heuristic(activeIndex, activeX_temp, activeY_temp, j, drop_distance)
            #print("heuristic = {}".format(heuristic))
            heuristicList.append(heuristic)
            moveList.append((i, j))

    bestMove = 0
    for i in range(0, len(moveList)):
        if(heuristicList[i] <= heuristicList[bestMove]):
            bestMove = i
    print("Best is {}".format(heuristicList[bestMove]))
    make_move(moveList[bestMove])

def get_heuristic(activeIndex, activeX, activeY, rotation, drop_distance):
    temp_board = [row[:] for row in board]
    for block in activeShape[activeIndex][rotation]:
        blockX = activeX + block[0]
        blockY = activeY + block[1]
        temp_board[blockY][blockX] = True
    #height = get_aggregate_height(temp_board)
    #completed = get_complete_lines(temp_board)
    #bumpiness = get_bumpiness(temp_board)
    holes = get_holes(temp_board)
    #print_board(temp_board)
    #print("aggregate = {}, completed = {}, bumpiness = {}, holes = {}, dropdistance = {}".format(height, completed, bumpiness, holes, drop_distance))
    #heuristic = -0.2*height + 10*completed + -4*holes + -.2*bumpiness + .2*drop_distance
    heuristic = holes
    print("drop distance = {}, heuristic = {}".format(drop_distance, heuristic))
    return heuristic

def get_aggregate_height(temp_board):
    aggregate = 0
    for x in range(0, len(temp_board[0])):
        height = 0
        for y in range(0, len(temp_board)):
            if(temp_board[y][x]):
                height = len(temp_board) - y
                break
        aggregate += height
    return aggregate

def get_complete_lines(temp_board):
    completed = 0
    for row in temp_board:
        if(not False in row):
            completed += 1
    return completed

def get_bumpiness(temp_board):
    bumpiness = 0
    last_height = 0
    for x in range(0, len(temp_board[0])):
        height = 0
        for y in range(0, len(temp_board)):
            if(temp_board[y][x]):
                height = len(temp_board) - y
                break
        if(x > 0):
            bumpiness += abs(height-last_height)
        last_height = height
    return bumpiness

def get_holes(temp_board):
    print_board(temp_board)
    aggregate_holes = 0
    for x in range(0, 10):
        hitBlock = False
        for y in range(0, 20):
            if(temp_board[y][x]):
                hitBlock = True
            elif(hitBlock):
                aggregate_holes+=1
    return aggregate_holes


def make_move(x):
    global waiting
    print("Writing to serial: {}".format(x))
    waiting = True
    ser.write("{}{}".format(x[0], x[1]).encode('ascii'))
    pass

def print_board(temp_board):
    print("|||||||||||||||||||||||||||||||||||||||")
    for y in range(0, len(temp_board)):
        for x in range(0, len(temp_board[0])):
            if(temp_board[y][x]):
                print("+ ", end="")
            else:
                print("- ", end="")
        print(" ")

# DO THINGS
ser = serial.Serial('COM3', 9600)
connected = False
waiting = False
while(True):
    if(not connected or waiting):
        connected = True
        waiting = False
        print("Waiting for serial.")
        try:
            val = ser.readline()
        except KeyboardInterrupt:
            # quit
            print("Quitting.")
            sys.exit()
        print("Serial sent {}, continuing program.".format(val))
    getgamestate()