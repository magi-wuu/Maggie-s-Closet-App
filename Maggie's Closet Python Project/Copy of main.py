"""
SUMMATIVE: part 2, program
MAGGIE'S CLOSET: outfit matching and making program using pygame
ICS3U-02
Maggie Wu
History:
April 30, 2024: Program Creation
June 1, 2024: completed program, added finishing touches
"""

#SETUP: ============================================================================================
import pygame
import sys

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 55)

# game window
screen_width = 600
screen_height = 550

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MAGGIE'S CLOSET!")

# Load background music
pygame.mixer.music.load("background_music.mp3")

#LOAD IMAGES: ============================================================================================

#opening images:
opening_screen = pygame.image.load("opening_screen.png").convert_alpha()
intro = pygame.image.load("instructions.png").convert_alpha()
game_page = pygame.image.load("game_page.png").convert_alpha()
character = pygame.image.load("model.png").convert_alpha()

#menu:
menuBG = pygame.image.load("Menu.png").convert_alpha()

#score:
scoreBG = pygame.image.load("YourScore.png").convert_alpha()
score_ani = [pygame.image.load(f"score_ani/Scoring{i + 1}.png").convert_alpha() for i in range(4)]
score_good = pygame.image.load("score_good.png").convert_alpha()
score_perfect = pygame.image.load("score_perfect.png").convert_alpha()
score_ok = pygame.image.load("score_ok.png").convert_alpha()
exit = pygame.image.load("Exit.png").convert_alpha()

#view/ save location:
viewBG = pygame.image.load("ViewBG.png").convert_alpha()
view_layer = pygame.image.load("View_layer.png").convert_alpha()
background_rect = view_layer.get_rect()

#button images
score = pygame.image.load("scoreButton.png").convert_alpha()
arrow = pygame.image.load("arrowButton.png").convert_alpha()
arrow_flipped = pygame.image.load("arrowButton - Copy.png").convert_alpha()
view = pygame.image.load("viewButton.png").convert_alpha()
start = pygame.image.load("start.png").convert_alpha()

menu_but = pygame.image.load("Menu button.png").convert_alpha()
outfit_but = pygame.image.load("Outfit button.png").convert_alpha()
save_but = pygame.image.load("Save button.png").convert_alpha()
home_but = pygame.image.load("Home button.png").convert_alpha()
view_outfit_but = pygame.image.load("View button.png").convert_alpha()

#LISTS AND VARIABLES
topsIndex = 0
bottomsIndex = 0
hairIndex = 0
shoesIndex = 0
white = (255, 255, 255)
scale_factor = 1.165
points = 0
numOutfit = 0

# Initial positions of the two background images
background_y1 = 0
background_y2 = -550

# Scroll speed
scroll_speed = 5

# Animation:
frame_count = len(score_ani)
current_frame = 0
fps = 2
clock = pygame.time.Clock()
counter =0

# list to save the current outfit for viewing
cur_outfit = [0, 0, 0, 0]  # Stores indices instead of surfaces

# Define positions for each item in the outfit
positions = [(-303, 13), (-300, -9), (-265, 25), (-300, 0)]
catalog = []

# item databases (loads in images from file path)
tops = [pygame.image.load(f"tops/top({i + 1}).png") for i in range(7)]
bottoms = [pygame.image.load(f"bottoms/bottom({i + 1}).png").convert_alpha() for i in range(7)]
hair = [pygame.image.load(f"hair/hair({i + 1}).png").convert_alpha() for i in range(3)]
shoes = [pygame.image.load(f"shoes/shoes({i + 1}).png").convert_alpha() for i in range(3)]

# FUNCTIONS AND CLASSES:  ============================================================================================
# Changes position of an item in a 1x2 gallery
def top_position(num, background_y):
    """
    Changes the position of a clothing item (tops) in a 1x2 gallery.

    Args:
        num (int): The index of the outfit item.
        background_y (int): The vertical position of the background.

    Returns:
        tuple: A tuple containing the x and y coordinates of the outfit item.
    """
    topx = -245 if num % 2 == 0 else 0  # Alternate between -220 and 0 (based on the outfit displayed)
    topy = 15+(num // 2) * 550 + background_y  # Images 1 screen below if 2 outfits have been drawn in a row
    return topx, topy

def bot_position(num, background_y):
    """
    Changes the position of a clothing item (bottoms) in a 1x2 gallery.

    Args:
        num (int): The index of the outfit item.
        background_y (int): The vertical position of the background.

    Returns:
        tuple: A tuple containing the x and y coordinates of the outfit item.
    """
    botx = -245 if num % 2 == 0 else 0
    boty = 10 + (num // 2) * 550 + background_y
    return botx, boty

def hair_position(num, background_y):
    """
    Changes the position of a clothing item (hair) in a 1x2 gallery.

    Args:
        num (int): The index of the outfit item.
        background_y (int): The vertical position of the background.

    Returns:
        tuple: A tuple containing the x and y coordinates of the outfit item.
    """
    hairx = -245 if num % 2 == 0 else 0
    hairy = 50 + (num // 2) * 550 + background_y
    return hairx, hairy

def shoes_position(num, background_y):
    """
    Changes the position of a clothing item (shoes) in a 1x2 gallery.

    Args:
        num (int): The index of the outfit item.
        background_y (int): The vertical position of the background.

    Returns:
        tuple: A tuple containing the x and y coordinates of the outfit item.
    """
    shoesx = -245 if num % 2 == 0 else 0
    shoesy = 30 + (num // 2) * 550 + background_y
    return shoesx, shoesy

# Saving outfits:
def save(outfit):
    """
    Saves an outfit to the catalog.

    Args:
        outfit (list): A list containing the indices of clothing items.

    Returns:
        None
    """
    global catalog
    catalog.append(list(outfit))

# scoring outfit
def score_outfit(outfit):
    """
    score_rules dictionary is a nested dictionary that organizes the scoring rules based on the index of the top.
    Each top index has its own dictionary which contains the scoring rules for bottoms, hair, and shoes.
    Initializes points, extracts indices from the outfit list, and then adds points based on the rules defined in score_rules.

    Args:
        outfit (list): A list containing the indices of clothing items.

    Returns:
        int: The score of the outfit.
    """
    global points
    points = 0
    # Scoring rules
    score_rules = {
        0: {
            "bottoms": {5: 1, 6: 2, "default": 3},    #For each type of clothing (bottoms, hair, shoes), the function looks up the dictionary for the current top index.
            "hair": {1: 1, "default": 2},           # It checks if there's a specific rule for the current index of the item, it uses that score, otherwise it uses the "default" score.
            "shoes": {1: 1, "default": 3}
        },
        1: {
            "bottoms": {0: 1, 1: 1, "default": 3},
            "shoes": {3: 1, "default": 3},
            "hair": {1: 3, "default": 2}
        },
        2: {
            "bottoms": {0: 1, 6: 1, "default": 3},
            "shoes": {1: 1, "default": 3},
            "hair": {"default": 2}
        },
        3: {
            "bottoms": {1: 1, 5: 1, "default": 3},
            "shoes": {1: 1, "default": 3},
            "hair": {"default": 2}
        },
        4: {
            "bottoms": {1: 1, 2: 1, "default": 3},
            "shoes": {1: 1, "default": 3},
            "hair": {1: 1, "default": 2}
        },
        5: {
            "bottoms": {1: 1, 2: 1, "default": 3},
            "shoes": {1: 1, "default": 3},
            "hair": {1: 1, "default": 2}
        },
        6: {
            "bottoms": {1: 1, 5: 1, "default": 3},
            "shoes": {1: 1, "default": 3},
            "hair": {"default": 2}
        }
    }

    top_index = outfit[0]
    bottom_index = outfit[1]
    hair_index = outfit[2]
    shoes_index = outfit[3]

    # Score bottoms
    points += score_rules[top_index]["bottoms"].get(bottom_index, score_rules[top_index]["bottoms"]["default"])

    # Score hair
    points += score_rules[top_index]["hair"].get(hair_index, score_rules[top_index]["hair"]["default"])

    # Score shoes
    points += score_rules[top_index]["shoes"].get(shoes_index, score_rules[top_index]["shoes"]["default"])

    return points

# switch items
def switch_item(item):
    """
    Switches to the next item in a category.

    Args:
        item (str): The category of the item to switch (e.g., "tops", "bottoms", "hair", "shoes").

    Returns:
        int: The index of the selected item.
    """
    global topsIndex, bottomsIndex, hairIndex, shoesIndex
    # move 1 image in the list
    if item == "tops":
        if topsIndex < len(tops) - 1:  # if it's not at the last item in the list
            topsIndex += 1
        else:
            topsIndex = 0  # reset to the first item in the list
        return topsIndex

    elif item == "bottoms":
        if bottomsIndex < len(bottoms) - 1:
            bottomsIndex += 1
        else:
            bottomsIndex = 0
        return bottomsIndex

    elif item == "hair":
        if hairIndex < len(hair) - 1:
            hairIndex += 1
        else:
            hairIndex = 0
        return hairIndex

    elif item == "shoes":
        if shoesIndex < len(shoes) - 1:
            shoesIndex += 1
        else:
            shoesIndex = 0
        return shoesIndex

def switch_item_backward(item):
    """
    Switches to the previous item in a category.

    Args:
        item (str): The category of the item to switch (e.g., "tops", "bottoms", "hair", "shoes").

    Returns:
        int: The index of the selected item.
    """
    global topsIndex, bottomsIndex, hairIndex, shoesIndex
    # move 1 image back in the list
    if item == "tops":
        if topsIndex > 0:  # if it's not at the first item in the list
            topsIndex -= 1
        else:
            topsIndex = len(tops) - 1  # set to the last item in the list
        return topsIndex

    elif item == "bottoms":
        if bottomsIndex > 0:
            bottomsIndex -= 1
        else:
            bottomsIndex = len(bottoms) - 1
        return bottomsIndex

    elif item == "hair":
        if hairIndex > 0:
            hairIndex -= 1
        else:
            hairIndex = len(hair) - 1
        return hairIndex

    elif item == "shoes":
        if shoesIndex > 0:
            shoesIndex -= 1
        else:
            shoesIndex = len(shoes) - 1
        return shoesIndex

# button class:
class Button:
    def __init__(self, surface, x, y, image, width, height, toggle=False):
        """
        Initializes a Button object.

        Args:
            surface: The surface on which the button is drawn.
            x (int): The x-coordinate of the button's top-left corner.
            y (int): The y-coordinate of the button's top-left corner.
            image: The image used for the button.
            width (int): The width of the button.
            height (int): The height of the button.
            toggle (bool, optional): If True, the button toggles its state when clicked. Defaults to False.
        """
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.image_hover = pygame.transform.scale(image, (int(width * 1.1), int(height * 1.1)))  # Expanded image when hovered
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.toggle = toggle
        self.toggle_state = False  # To track the toggle state

    def draw(self):
        """
        Draws the button on the screen and handles user interaction.

        Returns:
            bool: True if the button is clicked (or toggled on if toggle is True), False otherwise.
        """
        action = False
        pos = pygame.mouse.get_pos()

        # Check if hovered
        if self.rect.collidepoint(pos):
            # If hovered, draw the expanded image
            expanded_rect = self.image_hover.get_rect(center=self.rect.center)
            self.surface.blit(self.image_hover, expanded_rect.topleft)
        else:
            # Draw the normal button
            self.surface.blit(self.image, (self.rect.x, self.rect.y))

        # Check if clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                if self.toggle:
                    self.toggle_state = not self.toggle_state
                    action = self.toggle_state
                else:
                    action = True
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False

        # Maintain action state if toggle is on
        if self.toggle and self.toggle_state:
            action = True

        # Reset action for momentary buttons when the mouse button is released
        if not self.toggle and pygame.mouse.get_pressed()[0] == 0:
            action = False
            self.clicked = False

        return action


# CLASS INSTANCES: ============================================================================================
# start_button = Button(screen, 338, 507, , 184, 45, toggle=True)
viewButton = Button(screen, 338, 507, view, 184, 45, toggle=True)
scoreButton = Button(screen,38 , 506, score, 184, 45, toggle=False)
saveButton = Button(screen, 190,130, save_but, 184,45, toggle=False)

# Create the forward and backward buttons
topsButtonF = Button(screen, 540, 180, arrow, 55, 59, toggle=False)
topsButtonB = Button(screen, 270, 180, arrow_flipped, 55, 59, toggle=False)
botsButtonF = Button(screen, 540, 330, arrow, 55, 59, toggle=False)
botsButtonB = Button(screen, 270, 330, arrow_flipped, 55, 59, toggle=False)
hairButtonF = Button(screen, 540, 65, arrow, 55, 59, toggle=False)
hairButtonB = Button(screen, 270, 65, arrow_flipped, 55, 59, toggle=False)
shoeButtonF = Button(screen, 540, 450, arrow, 55, 59, toggle=False)
shoeButtonB = Button(screen, 270, 450, arrow_flipped, 55, 59, toggle=False)

menuButton = Button(screen, 5,5, menu_but, 50,45, toggle=True)
exitButton = Button(screen, 110,85, exit, 52,52, toggle=False)
homeButton = Button(screen, 8,200, home_but, 44,44, toggle=False)
outfitButton = Button(screen, 8,70, outfit_but, 44,44, toggle=False)
viewSavedButton = Button(screen, 8,140, view_outfit_but, 44,44, toggle=False)
start_button = Button(screen, 75,425, start, 261,85, toggle=False)

# MAIN GAME LOOP: ============================================================================================
run = True
# Start playing background music (set -1 to loop indefinitely)
pygame.mixer.music.play(-1)

# draw initial background:
location = "opening screen"

while run:
    clock.tick(60)
    if location == "opening screen":
        screen.blit(opening_screen, (0,0))
        if start_button.draw():
            location = "home"
            screen.fill(white)

    if location == 'home':
        screen.blit(intro,(0,0))
        if menuButton.draw():
            screen.blit(menuBG, (5,5))

            if menuButton.draw(): #if clicked again
                location = 'home' # go back to home program

            if viewSavedButton.draw():
                screen.fill(white) # screen clear
                location = 'saved outfits' # go to outfit gallery
                numOutfit = 0

            if outfitButton.draw():
                screen.fill(white) # screen clear
                location = 'main game' # go to main game

    if location == 'main game':
        screen.fill(white)
        screen.blit(game_page, (0, 0))
        screen.blit(character, (0, 0))
        screen.blit(tops[topsIndex], (2, -11))
        screen.blit(bottoms[bottomsIndex], (0, -8))
        screen.blit(hair[hairIndex], (0, 10))
        screen.blit(shoes[shoesIndex], (0, 0))

        #switching items, clicking between items
        # Check for button presses
        if topsButtonF.draw():
            switch_item("tops")
        if topsButtonB.draw():
            switch_item_backward("tops")

        if botsButtonF.draw():
            switch_item("bottoms")
        if botsButtonB.draw():
            switch_item_backward("bottoms")

        if hairButtonF.draw():
            switch_item("hair")
        if hairButtonB.draw():
            switch_item_backward("hair")

        if shoeButtonF.draw():
            switch_item("shoes")
        if shoeButtonB.draw():
            switch_item_backward("shoes")

         #viewing the outfit on model
        if viewButton.draw():
            cur_outfit[0] = topsIndex # Current outfit = [top,bottom,hair,shoes], first index top becomes the file path in topsIndex
            cur_outfit[1] = bottomsIndex
            cur_outfit[2] = hairIndex
            cur_outfit[3] = shoesIndex

            for i, item in enumerate(cur_outfit):
                    if i == 0:
                        screen.blit(tops[item], positions[i])
                    elif i == 1:
                        screen.blit(bottoms[item], positions[i])
                    elif i == 2:
                        screen.blit(hair[item], positions[i])
                    elif i == 3:
                        screen.blit(shoes[item], positions[i])

        if menuButton.draw():
            screen.blit(menuBG, (5,5))
            if menuButton.draw(): #if clicked again
                location = 'main game' # go back to main game program

            if viewSavedButton.draw():
                screen.fill(white) # screen clear
                location = 'saved outfits' # go back to outfit gallery
                numOutfit = 0

            if homeButton.draw():
                screen.fill(white) # screen clear
                location = 'home'

        #scoring the outfit
        if scoreButton.draw():
            grade = score_outfit(cur_outfit)
            print(points)
            counter = 0
            location = 'scoring'

    if location == 'scoring':
        #reset counter for animation:
        while counter != 8:
                # Draw the current frame
            screen.blit(score_ani[current_frame], (0, 0))
                # Update the display
            pygame.display.flip()
                # Wait for the next frame
            clock.tick(fps)
            counter += 1
                # Move to the next frame
            current_frame = (current_frame + 1) % frame_count

        #render text score ontop later!!
        screen.blit(scoreBG, (0,0))
        if points >= 7:
            screen.blit(score_perfect, (75,0))
        elif points >= 5:
            screen.blit(score_good, (75,0))
        else:
            screen.blit(score_ok, (75,0))

        # Render the text
        points_text = font.render(str(points), True, white)
        screen.blit(points_text, (415, 90))

        if saveButton.draw():
            save(cur_outfit)
            location = 'main game'
        if exitButton.draw():
            location = 'main game'

    if location == 'saved outfits':
        # Get the state of all keyboard buttons
        keys = pygame.key.get_pressed()

        # Scroll the background down
        if keys[pygame.K_DOWN]:
            background_y1 += scroll_speed
            background_y2 += scroll_speed

        # Scroll the background up
        if keys[pygame.K_UP]:
            background_y1 -= scroll_speed
            background_y2 -= scroll_speed

        # Check if the background images are out of view and reset their positions
        if background_y1 >= screen_height:
            background_y1 = background_y2 - background_rect.height
        if background_y2 >= screen_height:
            background_y2 = background_y1 - background_rect.height
        if background_y1 <= -background_rect.height:
            background_y1 = background_y2 + background_rect.height
        if background_y2 <= -background_rect.height:
            background_y2 = background_y1 + background_rect.height

        # Redraw the backgrounds
        screen.blit(view_layer, (0, background_y1))
        screen.blit(view_layer, (0, background_y2))

        # Control the frame rate
        pygame.time.Clock().tick(30)

        # DRAWING THE OUTFITS:
        for numOutfit, outfit in enumerate(catalog):  # Access an outfit from list of outfits
            topPos = top_position(numOutfit, background_y1)
            botPos = bot_position(numOutfit, background_y1)
            hairPos = hair_position(numOutfit, background_y1)
            shoesPos = shoes_position(numOutfit, background_y1)

            for i, item in enumerate(outfit):  # Draws an outfit
                if i == 0:
                    screen.blit(tops[item], topPos)
                elif i == 1:
                    screen.blit(bottoms[item], botPos)
                elif i == 2:
                    screen.blit(hair[item], hairPos)
                elif i == 3:
                    screen.blit(shoes[item], shoesPos)
        screen.blit(viewBG, (0, 0))  # Draw intro image on top

        # Update the display
        pygame.display.flip()

        if menuButton.draw():
            screen.blit(menuBG, (5, 5))
            if menuButton.draw():  # if clicked again
                location = 'saved outfits'  # go back to current location program

            if outfitButton.draw():
                location = 'main game'  # go to main game

            if homeButton.draw():
                screen.fill(white) # screen clear
                location = 'home'

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
