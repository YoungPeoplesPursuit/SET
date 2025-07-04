# Install Pygame
import pygame
import random

pygame.init()

# set up screen
screen = pygame.display.set_mode((1200,800),pygame.RESIZABLE) #screen dimensions and it is resizable
pygame.display.set_caption("Set")


#game running loop stuff
running = True

# make 3x4 interface grid

def drawGrid():
    for i in range(3):
        for j in range(4):
            pygame.draw.rect(screen, 'white', pygame.Rect(290*j + 40, 250*i + 50, 250, 200)) #draw 12 rectangles

# rectangle parameters: upper left coordinates, width, height

# Cards class:
class Card:
    # 4 properties to draw: number, color, shading, and shape
    def __init__(self, number, color, shading, shape):
        self.number = number
        self.color = color
        self.shading = shading
        self.shape = shape
        self.onGrid = False #is card displayed on gird right now
        self.clicked = False #is card clicked

    def toList(self): #convert card to a list for easier manipulation
        list = []
        list.append(self.number)
        list.append(self.color)
        list.append(self.shading)
        list.append(self.shape)
        return list

    # function for drawing the corresponding card on a card in the interface with coordinates of top left card corner
    def draw(self, x, y):

        for i in range(self.number+1):
            if self.shading == 'Light': #shading configs
                width = 5 #draw a line border
                if self.color == 'red':
                    shade = 'crimson'
                elif self.color == 'green':
                    shade = 'green'
                else:
                    shade = 'darkslateblue'
            else:
                width = 0
                if self.shading == 'Mid': #light color fill for mid shading
                    if self.color == 'red':
                        shade = 'lightcoral'
                    elif self.color == 'green':
                        shade = 'lightgreen'
                    else:
                        shade = 'lightslateblue'
                else: #dark colors for dark filling
                    if self.color == 'red':
                        shade = 'crimson'
                    elif self.color == 'green':
                        shade = 'green'
                    else:
                        shade = 'darkslateblue'
            if self.shape == 'Oval':
                pygame.draw.ellipse(screen, shade, (x+25+70*i, y+50, 60, 100), width)
            elif self.shape == 'Diamond':
                pygame.draw.polygon(screen, shade, [[x+55+70*i, y+50], [x+85+70*i, y+100],[x+55+70*i, y+150], [x+25+70*i, y+100]], width)
            else:
                pygame.draw.polygon(screen,shade,[[x+25+70*i,y+50],[x+85+70*i,y+50],[x+55+70*i,y+80],[x+85+70*i,y+100],[x+85+70*i,y+150],[x+25+70*i,y+150],[x+55+70*i,y+120],[x+25+70*i,y+100]],width)



# each property has 3 different variants


#Deck of total cards
deck = []
colors = ['red', 'green', 'purple']
shadings = ['Light', 'Mid', 'Dark']
shapes = ['Diamond', 'Oval', 'Squiggle']
#generate 81 unique cards for the deck
for i in range(3):
    for color in colors:
        for shading in shadings:
            for shape in shapes:
                deck.append(Card(i,color,shading,shape))

random.shuffle(deck) #shuffle the deck
cards_on_grid_location = [] # cards and rectangles stored where are the rectangles of these cards
cards_clicked = [] #check for sets and know which cards are clicked
#dealDeck function
def dealDeck(deck,cards_on_grid_location):
    # passing in the cards on grid list
   # Clear any existing cards from the grid list
    cards_on_grid_location.clear()
    # Ensure we have enough cards to deal
    if len(deck) < 12: #edge case when it runs out of cards in deck
        print('Not enough cards in the deck to deal 12.')
        return

    for count in range(12):
        # Take the top card from the shuffled deck
        selected_card = deck.pop(0)  # get and remove the first card

        j = count % 4  # find the remainder (column)
        i = count // 4  # find the quotient (row)

        # Don't draw here, draw in the main loop
        selected_card.onGrid = True
        card_rect = pygame.Rect(290*j + 40, 250*i + 50, 250, 200)
        cards_on_grid_location.append((selected_card, card_rect)) #add rectangle location of card to grid


# randomly generate 12 cards from deck to put on the interface
#user can click shuffle for an entirely new board

#replaceCard function
'''
old replace card function that didn't work
def replaceCard(cardlist):
    global deck, cards_on_grid_location
    # Find the positions (Rects) of the cards to be removed
    # and replace them with new cards from the deck
    for card in cardlist:
        index = cards_on_grid_location.index(card)
        card.onGrid = False
        card.used = True
        if len(deck) > 0:  # Ensure there are cards left in the deck
            newcard = deck.pop(0)
            newcard.onGrid = True
            rect = (cards_on_grid_location[index])[1] #get 2nd entry of tuples in cards on grid location
            cards_on_grid_location.pop(index)
            cards_on_grid_location.insert(index, (newcard, rect))
        else:
            print('No cards in the deck')

'''


def replaceCard(cards_clicked, deck, cards_on_grid_location):

    # Create a list of the indexes to update
    indices_to_replace = []

    # the indexes of all cards in the cards clicked list within cards_on_grid_location
    for card_in_set in cards_clicked:  # Iterate through the 3 cards that formed the set
        for i, (card_on_grid, rect) in enumerate(cards_on_grid_location):
            if card_on_grid is card_in_set:
                indices_to_replace.append(i)
                break  # Break inner loop once this specific card is found

    # loop through indexes to replace
    for index in indices_to_replace:
        old_card_at_index = cards_on_grid_location[index][0]
        old_card_at_index.onGrid = False  # Mark the old card as no longer on the grid

        if len(deck) > 0:  # Ensure there are cards left in the deck
            newcard = deck.pop(0)
            newcard.onGrid = True
            newcard.clicked = False  # Ensure new card is not clicked

            # Get the existing rectangle for this position
            rect = cards_on_grid_location[index][1]

            # Replace the old (Card, Rect) tuple with the new (Card, Rect) tuple at this index
            cards_on_grid_location[index] = (newcard, rect)
        else:
            print('No cards in the deck, replacing with empty slot.')
            # If deck is empty, replace the slot with None
            cards_on_grid_location[index] = (None, cards_on_grid_location[index][1])


#isSet function
def isSet(cardlist):
    card1 = cardlist[0]
    card2 = cardlist[1]
    card3 = cardlist[2]

    list1 = card1.toList()
    list2 = card2.toList()
    list3 = card3.toList()
    # the 3 cards picked are a set if for each of their properties, the variants are either all the same or all different
    allTrue = False
    setcount = 0
    for i in range(4):
        if list1[i] == list2[i] and list1[i] == list3[i]: #attributes all same
            setcount += 1
        elif not list1[i] == list2[i] and not list1[i] == list3[i] and not list2[i] == list3[i]: #attributes all different
            setcount += 1

    if setcount == 4: # if these 3 cards make a set
        allTrue = True

    return allTrue

#initialize score to 0
score = 0
current_game_message = ''

# Game loop
game_started = False
# set background color to our window
screen.fill('black')
# Create font
font = pygame.font.Font('freesansbold.ttf', 32)
# keep game running till running is true
while running:

    # Check for event if user has pushed any event in queue
    for event in pygame.event.get():

        # if event is of type quit then set running bool to false
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # else if the user clicks something

            #get the x and y of the mouse
            click_pos = event.pos
            for card, rect in cards_on_grid_location:
                #if it clicks a card
                if rect.collidepoint(click_pos):
                    if len(cards_clicked) == 3 and not isSet(cards_clicked): #conditional to clear cards that aren't in a set
                        for c in cards_clicked:
                            if c: c.clicked = False
                        cards_clicked.clear()
                    if card.clicked == True:
                # if card clicked before:
                        card.clicked = False
                        cards_clicked.remove(card)
                    # card clicked = false
                    # remove card from cards_clicked
                    else:
                        if len(cards_clicked) < 3: #don't check for set
                            card.clicked = True
                            cards_clicked.append(card)
                            #add card to cards.clicked and mark clicked as true
                    if len(cards_clicked) == 3:
                        current_game_message = ""
                        message_display_end_time = 0
                        if isSet(cards_clicked):
                            if len(deck) > 0:
                                replaceCard(cards_clicked, deck, cards_on_grid_location)
                            score += 3
                            print(score)
                            print(len(deck), 'cards remaining')
                            for card in cards_clicked:
                                card.clicked = False
                            cards_clicked = []
                        else:
                            current_game_message = "Press the space bar for new cards. Press backspace to try again"
                            smallfont = pygame.font.Font('freesansbold.ttf', 24)
                            current_message_font = smallfont
                            current_message_rect_center = (700, 25)


        elif event.type == pygame.KEYDOWN:
            current_game_message = ''
            message_display_end_time = 0 #reset message timer
            if len(cards_clicked) == 3 and not isSet(cards_clicked):
                if event.key == pygame.K_SPACE:
                    if len(deck) > 0:
                        replaceCard(cards_clicked, deck, cards_on_grid_location)

            for card in cards_clicked:
                card.clicked = False
            cards_clicked.clear() # Clear the list after action


    drawGrid()

    # Score text to be displayed
    scorestring = 'Score:' + str(score)
    score_text = font.render(scorestring, True, 'white', 'black')
    # rectangle around text
    textRect = score_text.get_rect()
    # set the center of the rectangular object.
    textRect.center = (100, 25)
    screen.blit(score_text, textRect)  # draw text for score

    #display messages
    if current_game_message:
        message_surface = current_message_font.render(current_game_message, True, 'white', 'black')
        message_rect = message_surface.get_rect(center=current_message_rect_center)
        screen.blit(message_surface, message_rect)

    #deal the deck once game starts
    if not game_started:
        dealDeck(deck, cards_on_grid_location)
        game_started = True
    # Draw the cards that are currently on the grid
    if len(cards_on_grid_location) > 0:
        for count, cardrect in enumerate(cards_on_grid_location):
            j = count % 4
            i = count // 4
            card = cardrect[0]
            card.draw(290*j + 40, 250*i + 50)  # draw the card on the correct rectangle
            if card.clicked:
                # cards turn gold when user clicks. User can click again to undo
                pygame.draw.rect(screen, 'gold', pygame.Rect(290*j + 40, 250*i + 50, 250, 200),5)


    #update everything in main loop per run
    pygame.display.flip()


pygame.quit()
print(score)

