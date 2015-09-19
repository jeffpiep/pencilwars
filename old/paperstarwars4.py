import math
import pygame

def line2point(x1,y1, x2,y2, x3,y3): # x3,y3 is the point
    px = x2-x1
    py = y2-y1
    something = px*px + py*py
    u = 1
    if something > 0:
        u =  ((x3 - x1) * px + (y3 - y1) * py) / float(something)
        if u > 1:
            u = 1
        elif u < 0:
            u = 0    
    x = x1 + u * px
    y = y1 + u * py
    dx = x - x3
    dy = y - y3
    dist = math.sqrt(dx*dx + dy*dy)
    return dist

pygame.init()

# Define some colors
black = ( 0, 0, 0)
white = ( 255, 255, 255)
green = ( 0, 255, 0)
red = ( 255, 0, 0)
blue = ( 0, 0, 255)
#need player colors
playCol = (blue, red)

# create a screen
size = (800,600)
screen = pygame.display.set_mode(size)

#initialize playing field
numShips = 5
shipAlive = [True] * 2 * numShips
# player 1 ships in first numShips and player 2 in second numShips
shipImage=list()
shipImage.append(pygame.image.load("pencilXWing.png").convert())
shipImage.append(pygame.image.load("pencilTIE.png").convert())
for item in shipImage:
    item.set_colorkey(white)
shipRadius = 20
shipPosX = list()
shipPosY = list()
for iPlay in range(2):
    for iShip in range(numShips):
        shipPosX.append(int(size[0]/6 + iPlay*size[0]/6*4))
        shipPosY.append(int(size[1]/(numShips+1)*(iShip+1)))
flickScale = 30
# obstacles
roidImage = pygame.image.load("pencilAsteroid.png").convert()
roidImage.set_colorkey(white)
roidCol = black
numRoids = 5
roidRadius = 15
roidPosX = list()
roidPosY = list()
roidAlive = [True] * numRoids
for iRoid in range(numRoids):
    x=random.randint(int(size[0]/6) + 2*roidRadius + shipRadius + 1, int(size[0]/6*5) - 2*roidRadius -shipRadius - 1)
    y=random.randint(roidRadius,size[1]-2*roidRadius)
    roidPosX.append(x)
    roidPosY.append(y)

deathImage = pygame.image.load("pencilDeathStar.png").convert()
deathImage.set_colorkey(white)
deathRadius = 60
deathPosX = int(size[0]/2)
deathPosY = int(size[1]/2)
deathAlive = True

#game logic:
#player X
#  chooses ship
#  flicks pencil
#  find if flick collided with other ship
#  if collide
#   destroy other ship
#  else
#   move ship
#player Y's turn


#Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
# gameState state machine variable:
# 0 - user selecting ship
# 1 - flick
#
gameState = 0
playTurn = 0
shipSelected = -1
winner = -1
loseTurn = -1
print("Player " + str(playTurn+1) + "'s turn")
while done == False:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get(): # User did something
        if gameState == 0: #selecting a ship
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pointerPos = event.pos
                    # find the ship
                    for iShip in range(numShips):
                        shipID = playTurn*numShips+iShip
                        if shipAlive[shipID]:
                            testPos=(shipPosX[shipID],shipPosY[shipID])
                            dx = testPos[0]-pointerPos[0];
                            dy = testPos[1]-pointerPos[1];
                            testDist = math.sqrt(dx*dx + dy*dy)
                            if testDist < shipRadius:
                                shipSelected = shipID
                                gameState = 1
        elif gameState == 1: #wait for mouse up
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    gameState = 2
        elif gameState == 2: #wait for flick start
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    flickStartPos = event.pos
                    flickStartTime = pygame.time.get_ticks()
                    gameState = 3
        elif gameState == 3: #wait for flick stop
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    flickStopPos = event.pos
                    flickStopTime = pygame.time.get_ticks()
                    gameState = 4
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop             
    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
    if gameState == 0: #see if there is a winner
        for iPlay in range(2):
            shipsLeft = 0
            for iShip in range(numShips):
                shipID = iPlay*numShips+iShip
                shipsLeft += shipAlive[shipID]
            if shipsLeft == 0:
                winner = (iPlay + 1) % 2
                done = True
    elif gameState == 4:
        #compute mouse speed and direction
        dx = flickStopPos[0] - flickStartPos[0]
        dy = flickStopPos[1] - flickStartPos[1]
        dt = flickStopTime - flickStartTime
        mouseSpeed = math.sqrt(dx*dx + dy*dy)/float(dt)
        mouseDir = math.atan2(dy,dx)
        #determine flick on the screen
        flickDist = mouseSpeed * flickScale
        flickDX = int(flickDist * math.cos(mouseDir))
        flickDY = int(flickDist * math.sin(mouseDir))

        #did it collide with an asteroid or another ship?
        strikeList = list();
        #first check to see if it hit the death star
        dist=line2point(shipPosX[shipSelected],shipPosY[shipSelected],shipPosX[shipSelected]+flickDX,shipPosY[shipSelected]+flickDY,deathPosX,deathPosY)
        if dist < shipRadius + deathRadius: #hit the Death Star!
            strikeList.append((2,0,dist))
        for shipID in range(2*numShips):
            #exclude selected ship
            if shipID != shipSelected and shipAlive[shipID]:
                dist=line2point(shipPosX[shipSelected],shipPosY[shipSelected],shipPosX[shipSelected]+flickDX,shipPosY[shipSelected]+flickDY,shipPosX[shipID],shipPosY[shipID])
                if dist < shipRadius: #ship hit!
                    strikeList.append((0,shipID,dist))
        for iRoid in range(numRoids):
            if roidAlive[iRoid]:
                dist=line2point(shipPosX[shipSelected],shipPosY[shipSelected],shipPosX[shipSelected]+flickDX,shipPosY[shipSelected]+flickDY,roidPosX[iRoid],roidPosY[iRoid])
                if dist < shipRadius + roidRadius: #asteroid hit!
                    strikeList.append((1,iRoid,dist))
        # now act on the list
        moveShip = True
        if strikeList: #check to make sure it's not empty
            victim=sorted(strikeList, key=lambda tup: tup[2])[0]
            if victim[0]==0: #a ship
                shipAlive[victim[1]]=False
                moveShip = False
            elif victim[0]==1: #an asteroid
##                roidAlive[victim[1]] = False
                loseTurn = playTurn
                #truncate move so it stops at asteroid
                dx=shipPosX[shipSelected]-roidPosX[victim[1]]
                dy=shipPosY[shipSelected]-roidPosY[victim[1]]
                distRS=math.sqrt( dx*dx + dy*dy )
                distRT=float(shipRadius+roidRadius+1)
                newDist=distRS*math.sqrt(1-(victim[2]/distRS)**2) - distRT*math.sqrt(1-(victim[2]/distRT)**2)
                flickDX = int(newDist * math.cos(mouseDir))
                flickDY = int(newDist * math.sin(mouseDir))
                print("Player " + str(loseTurn+1) + " loses a turn!")
            elif victim[0]==2: #the death star
##                deathAlive = False
                shipAlive[shipSelected]=False
##                winner = (playTurn + 1) % 2
##                done = True
                print('Player ' + str(playTurn+1) + ' hit the Death Star!')

        # next players turn
        playTurn = (playTurn + 1) % 2
        if playTurn == loseTurn:
            playTurn = (playTurn + 1) % 2
            loseTurn = -1
        print("Player " + str(playTurn+1) + "'s turn")
        if moveShip:
            shipPosX[shipSelected] += flickDX
            shipPosY[shipSelected] += flickDY
        gameState = 0
    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

    # Clear the screen and set the screen background
    screen.fill(white)

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    # draw the death star
    screen.blit(deathImage, (size[0]//2 - deathRadius, size[1]//2 - deathRadius) )
##    pygame.draw.circle(screen, black, (deathPosX, deathPosY), deathRadius, 1)
    # draw the ships
    for iPlay in range(2):
        for iShip in range(numShips):
            shipID = iPlay*numShips+iShip
            if shipAlive[shipID]:
                currPos=(shipPosX[shipID],shipPosY[shipID])
                screen.blit(shipImage[iPlay], (shipPosX[shipID] - shipRadius, shipPosY[shipID] - shipRadius) )
            if shipID == shipSelected and gameState > 0:
                currPos=(shipPosX[shipID],shipPosY[shipID])                    
                pygame.draw.circle(screen, playCol[iPlay], currPos, shipRadius, 1)
                pygame.draw.circle(screen, playCol[iPlay], currPos, shipRadius, 1)
    # draw the asteroids
    for iRoid in range(numRoids):
        if roidAlive[iRoid]:
            currPos=(roidPosX[iRoid],roidPosY[iRoid])
            screen.blit(roidImage, (roidPosX[iRoid] - roidRadius, roidPosY[iRoid] - roidRadius) )
            pygame.draw.circle(screen, roidCol, currPos, roidRadius, 2)
    # draw the flick
    if shipSelected != -1 and gameState == 0:
        flickColor = playCol[(playTurn + 1) % 2]
        if moveShip:
            pygame.draw.line(screen,flickColor,[shipPosX[shipSelected]-flickDX,shipPosY[shipSelected]-flickDY],[shipPosX[shipSelected],shipPosY[shipSelected]],2)
        else:
            pygame.draw.line(screen,playCol[(playTurn + 1) % 2],[shipPosX[shipSelected],shipPosY[shipSelected]],[shipPosX[shipSelected]+flickDX,shipPosY[shipSelected]+flickDY],2)
    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

print("Winner is Player " + str(winner+1))
pygame.quit()

