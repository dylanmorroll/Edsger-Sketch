#Importing necessary modules
import pygame, sys, os, text_input, perform_dijkstras
from pygame.locals import *
from math import log10, floor
#Centring pygame window
os.environ['SDL_VIDEO_CENTERED'] = '1'
#Initialising pygame
pygame.init()
#Creating the display (resolution, flags, bits)
screen = pygame.display.set_mode((1280, 720), 0, 0)
#Setting title for the program
pygame.display.set_caption('Edsger-Sketch')
#Setting a background image
bg_pic = "background.jpg"
#Convert background image for use in program
background = pygame.image.load(bg_pic).convert()

#Declaring variables for RGB values of colours:
black = (0, 0, 0)
light_grey = (200, 200, 200)
grey = (125, 125, 125)
white = (255, 255, 255)
light_red = (255, 125, 125)
red = (255, 0, 0)
light_green = (100, 238, 161)
green = (67, 205, 128)
brown = (139, 69, 39)
light_blue = (0, 125, 200)

#Dictionary of global variables that holds the current settings of the program
options = {'show_options':False, 'size_of_grid':[10, 7], 'selected_colour':white, 'size_of_square':66, 'show_solve_button':False, 'solve':False, 'show_options_arrow':True, 'function':2, 'start_of_line':True, 'lines':False}
#Since this options dictionary is a global variable, it means any function can access it, so it serves as a way for the program to communicate with itself. When a value is changed, such as the size of the grid, the part of the program which changes that value will change the corresponding value in the dictionary. Then when running a function that displays and updates pygame window, that function will retrieve the necessary information from this dictionary. So for example when running the function which displays the grid, to find out the how many cells it needs to display, it will retrieve that information from this dictionary.

#Declaring empty global lists for use in the program:
grid_references = []
list_of_lines = []
line_coordinates = []
list_of_circles = []

#The first screen of the program
def main_menu():
    #Standard use of the box class to create text boxes or buttons on screen with text in them:
	#blit the background image onto the screen of the program
    screen.blit(background,(0,0))
	#Assigning variable to instance of the class 'box'. The box has default values for each variable, so if a variable isn't declared it will use the standard ones
    start_button = box()

	#Setting the size of the box (x, y)
    start_button.size = (300, 125)
	#Setting the location for the top left of the box (x, y)
    start_button.location = (490, 250)
	#Declaring the size of the font for the text
    start_button.font_size = 22
	#The size, in pixels, of the black outline for the box.
    start_button.size_outline = 2
	#The text to be featured in the box, which is in this case the start button
    start_button.text_input = "Start"
	#Necessary modules called to create the box. Draw box displays the box with it's outline on screen, prep creates the font and initialises it. This is separate module in case I need to create a box without text. Centralise text centralises the text in both the x and y directions. Display text displays the text on top of the box, this is a separate module since sometimes I won't want to centralise the text.
    start_button.draw_box(), start_button.prep(), start_button.centralise_text(), start_button.display_text()
	#Getting the coordinates in the format (Start x coordinate (left), end x coordinate (right), start y coordinate (top), end y coordinate (bottom). These are used to detect which button has been clicked, if any, when the mouse button is pressed
    sb_co = start_button.get_coords()

	#Infinite loop - needs to be infinite to constantly update the pygame window
    while True:
		#Get the x and y coordinates of the mouse relative to the pygame window
        x,y = pygame.mouse.get_pos()
		#Loops through the events that have backlogged since the last time it ran through this loop - events are actions such as the mouse button being pressed or a key on the keyboard being pressed etc.
        for event in pygame.event.get():

			#If the event type is QUIT, meaning the X button has been pressed at the top right of the window, or the escape button is pressed:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				#Quit pygame
                pygame.quit()
				#Also exit the system to make sure there isn't an empty shell of a pygame window left running
                sys.exit()

			#If the event is the mouse button being released - Pushing back up after being pressed down
            if event.type == MOUSEBUTTONUP:
				#If the coordinates of the mouse when the mouse button was released are within the coordinates sb_co (The start button)
                if (x >= sb_co[0] and x <= sb_co[1]) and (y >= sb_co[2] and y <= sb_co[3]):
					#Then perform the choose_function function - Displays the next screen
                    choose_function()

		#Update the pygame window with any changes. Needs to be called otherwise the screen will never change.
        pygame.display.update()

#Choose which function of the program the user wants to perform.
def choose_function():
	#Display background
    screen.blit(background,(0,0))

    #Defining variables for instance of box class - same routine as when creating the start box:
    text_box1 = box()
    #This runs the default_text_box module, which changes some of the default values for variables which are more suited to a text box.
    text_box1.default_text_box()
    text_box1.text_location = (0, 465)
    text_box1.text_input = "Hover over a button for a more detailed description."
    #Here I only centralise the text in the x direction since I want the text to sit at the top of the box since it's a text box not a button
    text_box1.draw_box(), text_box1.prep(), text_box1.centralise_x() ,text_box1.display_text()

    #Defining variables for a button instance of box class:
    button1 = box()
    #This runs the default_button module, which changes some of the default values for variables which are more suited to a button.
    button1.default_button()

    button1.location = (400, 200)
    button1.text_input = "Grid"
    button1.draw_box(), button1.prep(), button1.centralise_text(), button1.display_text()
    b1co = button1.get_coords()

    #Defining variables for another button:
    button2 = box()
    button2.default_button()
    button2.location = (730, 200)
    button2.text_input = "Vertices"
    button2.draw_box(), button2.prep(), button2.centralise_text(), button2.display_text()
    b2co = button2.get_coords()

	#Infinite loop
    while True:
		#Mouse coordinates
        x, y = pygame.mouse.get_pos()
		#Event handling loop
        for event in pygame.event.get():

            #Quitting the program
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #Check if button 1 has been pressed
            if (x >= b1co[0] and x <= b1co[1]) and (y >= b1co[2] and y <= b1co[3]):
				#When hovering over a button, without pressing it, change the text of the text box to this
                text_box1.text_input = "All cells are available. Choose the type of terrain for each cell and it will find the shortest route."

                if event.type == MOUSEBUTTONUP:
					#Set function part of options to 1, so after the options screen it knows which function to perform
                    options['function'] = 1
					#Perform options_screen function - Display the options screen
                    options_screen()

            #Check if button 2 has been pressed
            elif (x >= b2co[0] and x <= b2co[1]) and (y >= b2co[2] and y <= b2co[3]):
                #When hovering over a button, without pressing it, change the text of the text box to this
                text_box1.text_input = "Only selected cells are available. More standard Dijkstra's Algorithm operations with weighted vertices."

                if event.type == MOUSEBUTTONUP:
					#Set function part of options to 1, so after the options screen it knows which function to perform
                    options['function'] = 2
					#Perform options_screen function - Display the options screen
                    options_screen()

            else:
                #If no buttons are currently being hovered over, change the text of the text box to this
                text_box1.text_input = "Hover over a button for a more detailed description."

            #Re draw the text box to erase the old text and display the updated text.
            text_box1.draw_box(), text_box1.prep(), text_box1.centralise_x() ,text_box1.display_text()

        pygame.display.update()

#Options screen before accessing the main program.
def display_options():
	#Declaring empty coordinates list to append the coordinates of each button to later
    coordinates = []
	#Blit background
    screen.blit(background,(0,0))

    #Creating all the text boxes and buttons necessary:
    options_area = box()
    options_area.location = (440, 200)
    options_area.size = (400, 200)
    options_area.font_size = 18
    options_area.text_location = (450, 210)
    options_area.text_input = "Options:"
    options_area.draw_box(), options_area.prep(), options_area.display_text()

	#Here I am assigning a font to a variable for use later on
    font = pygame.font.SysFont("calibri", 18)
	#I am using the font to display the text "Size of Grid:" on screen
    screen.blit(font.render("Size of Grid:", 1, black), (520, 275))
    size_of_grid = box()
    size_of_grid.default_options_buttons()
    size_of_grid.location = (640, 270)
    size_of_grid.size = (35, 25)
    #The text for this box is the current x value for the size of the grid - This is so it automatically updates when the user enters a value
    size_of_grid.text_input = str(options['size_of_grid'][0])

    size_of_grid.font_size = 16
    size_of_grid.draw_box(), size_of_grid.prep(), size_of_grid.centralise_text(), size_of_grid.display_text()
	#Appending the coordinates of the this button to the list
    coordinates.append(size_of_grid.get_coords())

    screen.blit(font.render("x", 1, black), (690, 275))
    size_of_grid2 = box()
    size_of_grid2.default_options_buttons()
    size_of_grid2.location = (715, 270)
    size_of_grid2.size = (35, 25)
    size_of_grid2.text_input = str(options['size_of_grid'][1])
    size_of_grid2.font_size = 16
    size_of_grid2.draw_box(), size_of_grid2.prep(), size_of_grid2.centralise_text(), size_of_grid2.display_text()
    coordinates.append(size_of_grid2.get_coords())

	#Assigning text options to a variable
    font = pygame.font.SysFont("calibri", 16)
	#Assigning text to a variable
    max_size1 = font.render("Max Size of Grid:", 1, black)
	#Displaying text on screen
    screen.blit(max_size1, (520, 310))

	#If running the first function
    if options['function'] == 1:
		#The max x value is 40
        max_size2 = font.render("40", 1, black)
	#If running the second function
    elif options['function'] == 2:
		#The max x value is 14
        max_size2 = font.render("14", 1, black)
	#Displaying the max x value
    screen.blit(max_size2, (650, 310))

	#Assigning text and options together in a variable
    max_size3 = pygame.font.SysFont("calibri", 20).render("x", 1, black)
	#Displaying text max_size3 on screen
    screen.blit(max_size3, (690, 307))

	#If running the first function
    if options['function'] == 1:
		#The max y value is 30
        max_size4 = font.render("30", 1, black)
	#If running the second function
    elif options['function'] == 2:
		#The max y value is 10
        max_size4 = font.render("10", 1, black)
	#Display the max y value
    screen.blit(max_size4, (725, 310))

    finished = box()
    finished.location = (750, 365)
    finished.size = (80, 25)
    finished.font_size = 18
    finished.text_input = "Finished"
    finished.draw_box(), finished.prep(), finished.centralise_text(), finished.display_text()
    coordinates.append(finished.get_coords())
	#Return the coordinate list, containing the coordinates of any buttons necessary for use
    return coordinates

def options_screen():
	#Display all the text boxes and buttons in the display_options function, and assign the coordinates list to a variable
    coordinates = display_options()
	#First size of grid box is the first set of coordinates in the list
    sog_co = coordinates[0]
	#Second size of grid box is the second set of coordinates
    sog2_co = coordinates[1]
	#Third set of coordinates is the finish button
    fin_co = coordinates[2]

	#Infinite loop
    while True:
        x, y = pygame.mouse.get_pos()
		#Event handling loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				#Exiting program
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONUP:
				#If the mouse is inside the first size of grid box during the MOUSEBUTTONUP event:
                if (x >= sog_co[0] and x <= sog_co[1]) and (y >= sog_co[2] and y <= sog_co[3]):
					#Coordinates of the first size of grid box - the x value (startx, starty, endx, endy)
                    coords = (640, 270, 675, 295)
					#Size of the box (x, y)
                    size = (35, 25)

                    #Call the text_input_display function from the text_input imported file to allow the user to type on screen in the size of grid text input
                    size_of_grid_input = text_input.text_input_display(screen, coords, size)
					#Assigning the full text input to a variable
                    width_value = size_of_grid_input.completed_text

					#If the length of the text doesn't equal 0 (they have actually input something)
                    if len(width_value) != 0:
						#Turn the input to an integer - If they didn't input anything it would return an error so this comes after checking the length of the input - Validation to check if the input is a number is inside the text_input file
                        width_value = int(width_value)

						#If the value is less than 0
                        if width_value <= 0:
							#Change it to the lowest accepted value, which is 1
                            width_value = 1

						#If function 1 is running, the max x value is 40, so if it is greater than that
                        elif options['function'] == 1 and width_value > 40:
							#Change the value to the highest accepted value, which is 40
                            width_value = 40

						#If function 2 is running, the max x value is 14, so if it is greater than that
                        elif options['function'] == 2 and width_value > 14:
							#Change the value to the highest accepted value, which is 14
                            width_value = 14

						#Once the validation is complete, update the size of grid value in the options dictionary to reflect the change
                        options['size_of_grid'][0] = width_value

				#This is the same as above, but this time for the second size of grid box, which holds the y value
                elif (x >= sog2_co[0] and x <= sog2_co[1]) and (y >= sog2_co[2] and y <= sog2_co[3]):
                    coords = (715, 270, 750, 295)
                    size = (35, 25)
                    size_of_grid2_input = text_input.text_input_display(screen, coords, size)
                    height_value = size_of_grid2_input.completed_text
                    if len(height_value) != 0:
                        height_value = int(height_value)
                        if height_value <= 0:
                            height_value = 1
                        elif options['function'] == 1 and height_value > 30:
                            height_value = 30
                        elif options['function'] == 2 and height_value > 10:
                            height_value = 10
                        options['size_of_grid'][1] = height_value

				#If the mouse is over the finish button during the MOUSEBUTTONUP event:
                elif (x >= fin_co[0] and x <= fin_co[1]) and (y >= fin_co[2] and y <= fin_co[3]):
					#Run the set_square_value function, to find the size of the square, commented further down:
                    set_square_value()

                    #Detects which function is currently selected from the options dictionary and runs the appropriate function (the next page):
                    if options['function'] == 1:
                        function1()
                    elif options['function'] == 2:
                        function2()

		#This runs through the display options function again to update any value that have changed, for example the size of the grid
        display_options()
		#Update the pygame display
        pygame.display.update()

def set_square_value():
	#Since the maximum number of pixels the width of the grid can take up is 950, I divide this to get what would be the number of pixels for each square, rounded down. For example if I had 10 cells along the x axis, each cell would be 95 pixels wide (however this would be changed to 66 since that is the maximum pixel number for a cell)
    temp_square_value = 950/options['size_of_grid'][0]
	#The same process but now for the number of rows (number of cells going down/ on the y axis)
    temp_square_value2 = 660/options['size_of_grid'][1]

    #This finds out which of the two pixel sizes for the cells is smaller:
    if temp_square_value <= temp_square_value2:
        square_value = temp_square_value
    elif temp_square_value2 <= temp_square_value:
        square_value = temp_square_value2

    #The maximum number of pixels for a cell is 66, so if it is greater than this it changes it back to 66
    if square_value > 66:
        square_value = 66

	#Sets the size of the square to the now validated value
    options['size_of_square'] = square_value

#Function 1 - Grid function
def function1():
	#Setting the function to use the global variable "grid_references" instead of creating a new local one
    global grid_references
	#Blit background
    screen.blit(background,(0,0))

    #Assigns an instance of the function1_screen class to window, this is because certain coordinates are needed before the first update
    window = function1_screen()
	#Running the module draw_initial_screen
    window.draw_initial_screen()

    #It fetches these coordinates first since they can be pressed before the screen is updated for the first time
    coordinate_list = window.coordinate_list
    arrow_co = window.arrow_box_coordinates
    home_co = window.home_button_coordinates

	#Infinite loop
    while True:
        x, y = pygame.mouse.get_pos()
		#Event handling loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				#Quit program
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONUP:
                #This checks if the mouse is within the arrow that can be seen in the top right corner of the program
                if (x >= arrow_co[0] and x <= arrow_co[1]) and (y >= arrow_co[2] and y <= arrow_co[3]) and options['show_options_arrow'] == True:
                    #If the options screen isn't showing already then display it:
                    if options['show_options'] == False:
                        window = function1_screen()
                        window.draw_options_screen()
						#Retrieving necessary coordinates
                        coordinate_list = window.coordinate_list
						#Changing options dictionary to show that the options screen is currently displaying
                        options['show_options'] = True

                    #If the options screen is showing then hide it:
                    elif options['show_options'] == True:
                        window = function1_screen()
                        window.draw_no_options_screen()
                        coordinate_list = window.coordinate_list
                        options['show_options'] = False

                #If the options are showing, then the cells can be edited:
                if options['show_options'] == True:
                    #Assigning each set of coordinates to a variable
                    grid_co = coordinate_list[0]   #grid co-ordinates
                    sog_co = coordinate_list[1]    #size of grid co-ordinates
                    sog2_co = coordinate_list[2]   #size of grid 2nd box co-ordinates
                    sp_co = coordinate_list[3]     #starting position co-ordinates
                    pt_co = coordinate_list[4]     #passable terrain co-ordinates
                    it_co = coordinate_list[5]     #impassable terrain co-ordinates
                    dp_co = coordinate_list[6]     #destination position co-ordinates
                    st_co = coordinate_list[7]     #slow terrain co-ordinates

                    #If the size of grid box has been clicked, retrieve and display the input text and update option dictionary to reflect these changes
                    if (x >= sog_co[0] and x <= sog_co[1]) and (y >= sog_co[2] and y <= sog_co[3]):
                        coords = (1150, 95, 1180, 115)
                        size = (30, 20)
                        size_of_grid_input = text_input.text_input_display(screen, coords, size)
                        width_value = size_of_grid_input.completed_text
                        if len(width_value) != 0:
                            width_value = int(width_value)
                            if width_value <= 0:
                                width_value = 1
                            elif width_value > 40:
                                width_value = 40
                            options['size_of_grid'][0] = width_value
                        set_square_value()

                    #If the size of grid box has been clicked, retrieve and display the input text and update option dictionary to reflect these changes
                    elif (x >= sog2_co[0] and x <= sog2_co[1]) and (y >= sog2_co[2] and y <= sog2_co[3]):
                        coords = (1210, 95, 1240, 115)
                        size = (30, 20)
                        size_of_grid2_input = text_input.text_input_display(screen, coords, size)
                        height_value = size_of_grid2_input.completed_text
                        if len(height_value) != 0:
                            height_value = int(height_value)
                            if height_value <= 0:
                                height_value = 1
                            elif height_value > 30:
                                height_value = 30
                            options['size_of_grid'][1] = height_value
                        set_square_value()

                    #If one of the options has been clicked, it updates the currently selected colour in the options dictionary
                    elif (x >= sp_co[0] and x <= sp_co[1]) and (y >= sp_co[2] and y <= sp_co[3]):
                        options['selected_colour'] = red
                    elif (x >= pt_co[0] and x <= pt_co[1]) and (y >= pt_co[2] and y <= pt_co[3]):
                        options['selected_colour'] = white
                    elif (x >= st_co[0] and x <= st_co[1]) and (y >= st_co[2] and y <= st_co[3]):
                        options['selected_colour'] = brown
                    elif (x >= it_co[0] and x <= it_co[1]) and (y >= it_co[2] and y <= it_co[3]):
                        options['selected_colour'] = grey
                    elif (x >= dp_co[0] and x <= dp_co[1]) and (y >= dp_co[2] and y <= dp_co[3]):
                        options['selected_colour'] = green

                    #When the mouse is clicked within the grid it takes the selected colour/ property and applies it to the cell that was clicked
                    elif (x >= grid_co[0] and x <= grid_co[1]) and (y >= grid_co[2] and y <= grid_co[3]):
						#Retrieving the number of pixels in each cell from the options
                        size_of_square = options['size_of_square']
						#This takes the x and y value of the mouse and subtracts 30 from it, since the start of the grid, the top left of the grid, is 30 pixels away from the edge of the pygame in both axes. In other words the grid starts at (30, 30) so it find the mouse position relative to the start of the grid
                        temp_x, temp_y = x - 30, y - 30

						#Takes the pixel coordinates of the mouse and divides them by the pixel size of each cell to find which cell it's in
                        row = temp_x / size_of_square
                        column = temp_y / size_of_square

						#This checks if the mouse is on the line in between the cells or actually on a cell, if it's on the line it doesn't process it
                        if (temp_x % size_of_square) != 0 and (temp_y % size_of_square) != 0:

                            #If the selected colour is green or red
                            if options['selected_colour'] == green or options['selected_colour'] == red:
								#Loop through the grid
                                for i in range(options['size_of_grid'][0]):
                                    for j in range(options['size_of_grid'][1]):
										#If the selected colour is green and it finds another green cell within the grid
                                        if grid_references[i][j][2] == green and options['selected_colour'] == green:
											#Change the old green cell to white, since there can only be one start cell
                                            grid_references[i][j][2] = white
										#The same but with the destination cell/ red colour
                                        elif grid_references[i][j][2] == red and options['selected_colour'] == red:
                                            grid_references[i][j][2] = white

                            #Applies the colour to the appropriate cell
                            grid_references[row][column][2] = options['selected_colour']
                            #It updates the grid_references since when the grid updates it will retrieve the colour of the cell from the grid_references

                    #Updates the screen, using the module that includes the options screen
                    window = function1_screen()
                    window.draw_options_screen()
                    coordinate_list = window.coordinate_list

                #If the options screen isn't showing: (When the options screen isn't up the solve and home buttons are available)
                elif options['show_options'] == False:
                    #If the home button is pressed
                    if (x >= home_co[0] and x <= home_co[1]) and (y >= home_co[2] and y <= home_co[3]):
						#Erase grid references to stop cells carrying over to a new grid
                        grid_references = []
                        options['solve'] = False
                        options['show_options_arrow'] = True
						#Return to the coose_function screen
                        choose_function()

                    #If the solve button is showing (basic validation checking if the start and destination coordinates are on the grid)
                    elif options['show_solve_button'] == True:
						#Solve button co-ordinates - the coordinates list is different for the screen without options
                        sb_co = coordinate_list[1]

                        #If the solve button is pressed
                        if (x >= sb_co[0] and x <= sb_co[1]) and (y >= sb_co[2] and y <= sb_co[3]):

                            #If the graph isn't currently solved
                            if options['solve'] == False:
								#Changing options to show the graph is solved
                                options['solve'] = True
								#Removes the options arrow while the graph is solved
                                options['show_options_arrow'] = False

                            #If the graph isn't solved the text is now "Return" and it removes the solution from the screen
                            elif options['solve'] == True:
                                options['solve'] = False
                                options['show_options_arrow'] = True

                        #Updates screen
                        window.draw_no_options_screen()
                        coordinate_list = window.coordinate_list

        pygame.display.update()

#Function 2
def function2():
    #These variables are globalised, since they need to be set to empty lists when the home button is pressed and if it isn't globalised it tries to create new local variables
    global grid_references, list_of_lines, list_of_circles, line_coordinates, final_route

    #Resetting the Solve button to False, in case they came from a solved function
    options['show_solve_button'] = False

	#Blit background
    screen.blit(background,(0,0))
	#Assigning variable
    initial_screen = function1_screen()
	#Displaying the screen
    initial_screen.draw_initial_screen()

    #Assigning coordinates to variables
    coordinate_list = initial_screen.coordinate_list
    arrow_co = initial_screen.arrow_box_coordinates
    home_co = initial_screen.home_button_coordinates

	#These are the start and end cells when retrieved by a line. If a line is drawn and it starts or ends at either the start of destination position these variables will be filled in. It provides a simple form a validation.
    start_cell, end_cell = "", ""

	#This is a variable that holds the coordinates of the start cell of a line if a line is being drawn
    start_grid = ""

	#Infinite loop
    while True:
        x, y = pygame.mouse.get_pos()
		#Event handling loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				#Quit program
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONUP:
				#Displaying/ hiding options
                if (x >= arrow_co[0] and x <= arrow_co[1]) and (y >= arrow_co[2] and y <= arrow_co[3]) and options['show_options_arrow'] == True:
                    if options['show_options'] == False:
                        options_screen = function1_screen()
                        options_screen.draw_options_screen()
                        coordinate_list = options_screen.coordinate_list
                        options['show_options'] = True

                    elif options['show_options'] == True:
                        options['start_of_line'] = True
                        if start_grid != "":
                            grid_references[start_grid[0]][start_grid[1]][2] = start_colour
                        no_options_screen = function1_screen()
                        no_options_screen.draw_no_options_screen()
                        coordinate_list = no_options_screen.coordinate_list
                        options['show_options'] = False

				#If options are displayed, enable ability to edit grid
                if options['show_options'] == True:
					#Assigning coordinates of each button to a variable
                    grid_co = coordinate_list[0]   #grid co-ordinates
                    sog_co = coordinate_list[1]    #size of grid co-ordinates
                    sog2_co = coordinate_list[2]   #size of grid 2nd box co-ordinates
                    sp_co = coordinate_list[3]     #starting position co-ordinates
                    pt_co = coordinate_list[4]     #passable terrain co-ordinates
                    it_co = coordinate_list[5]     #impassable terrain co-ordinates
                    dp_co = coordinate_list[6]     #destination position co-ordinates
                    dl_co = coordinate_list[7]     #draw lines button co-ordinates
					#If there are lines on screen then assign the clear lines button coordinates, if there are no lines this button isn't displayed
                    if len(list_of_lines) != 0:
                        cl_co = coordinate_list[8]  #clear lines button co-ordinates

					#Whilst there aren't any lines on the screen - Since options are disabled when a line has been drawn
                    if len(list_of_lines) == 0:
						#Retrieve and display number of columns input
                        if (x >= sog_co[0] and x <= sog_co[1]) and (y >= sog_co[2] and y <= sog_co[3]):
                            coords = (1150, 95, 1180, 115)
                            size = (30, 20)
                            size_of_grid_input = text_input.text_input_display(screen, coords, size)
                            width_value = size_of_grid_input.completed_text
                            if len(width_value) != 0:
                                width_value = int(width_value)
                                if width_value <= 0:
                                    width_value = 1
                                elif width_value > 14:
                                    width_value = 14
                                options['size_of_grid'][0] = width_value
                            set_square_value()

						#Retrieve and display number of rows input
                        elif (x >= sog2_co[0] and x <= sog2_co[1]) and (y >= sog2_co[2] and y <= sog2_co[3]):
                            coords = (1210, 95, 1240, 115)
                            size = (30, 20)
                            size_of_grid2_input = text_input.text_input_display(screen, coords, size)
                            height_value = size_of_grid2_input.completed_text
                            if len(height_value) != 0:
                                height_value = int(height_value)
                                if height_value <= 0:
                                    height_value = 1
                                elif height_value > 10:
                                    height_value = 10
                                options['size_of_grid'][1] = height_value
                            set_square_value()

						#Detect and update currently selected colour
                        elif (x >= sp_co[0] and x <= sp_co[1]) and (y >= sp_co[2] and y <= sp_co[3]):
                            options['selected_colour'] = red
                        elif (x >= pt_co[0] and x <= pt_co[1]) and (y >= pt_co[2] and y <= pt_co[3]):
                            options['selected_colour'] = white
                        elif (x >= it_co[0] and x <= it_co[1]) and (y >= it_co[2] and y <= it_co[3]):
                            options['selected_colour'] = grey
                        elif (x >= dp_co[0] and x <= dp_co[1]) and (y >= dp_co[2] and y <= dp_co[3]):
                            options['selected_colour'] = green
                        elif (x >= dl_co[0] and x <= dl_co[1]) and (y >= dl_co[2] and y <= dl_co[3]):
                            options['selected_colour'] = black

					#If there are lines on the screen, clear lines button is displayed, and this button is clicked:
                    if len(list_of_lines) != 0 and (x >= cl_co[0] and x <= cl_co[1]) and (y >= cl_co[2] and y <= cl_co[3]):
						#Reset variables holding characteristics of lines, lines are cleared from the screen
                        list_of_lines = []
                        list_of_circles = []
                        line_coordinates = []
                        options['lines'] = False
                        start_cell, end_cell = "", ""

					#If a location within the grid has been clicked
                    if (x >= grid_co[0] and x <= grid_co[1]) and (y >= grid_co[2] and y <= grid_co[3]):
						#Retrieve the size of each cell in pixels
                        size_of_square = options['size_of_square']
						#x, y position relative to the start of the grid
                        temp_x, temp_y = x - 30, y - 30

						#If the click wasn't on the border of a cell (was within a a cell)
                        if (temp_x % size_of_square) != 0 and (temp_y % size_of_square) != 0:
							#Find the column and row that the click was registered in
                            column = temp_x / size_of_square
                            row = temp_y / size_of_square
							#A list of all the 8 cells surrounding the cell clicked, starting from the right and going clockwise
                            surrounding_cells = [[column+1, row], [column+1, row+1], [column, row+1], [column-1, row+1], [column-1, row], [column-1, row-1], [column, row-1], [column+1, row-1]]

							#If the current colour/ property to be assigned to a cell is passable terrain
                            if options['selected_colour'] == green or options['selected_colour'] == red or options['selected_colour'] == white:
								#Turn all the cells around the cell clicked grey (since two passable terrain cells can't be adjacent)
                                for i in surrounding_cells:
									#Checks that cell isn't outside the grid so an error doesn't occur
                                    if (i[0] >= 0 and i[0] < options['size_of_grid'][0]) and (i[1] >= 0 and i[1] < options['size_of_grid'][1]):
                                        grid_references[i[0]][i[1]][2] = grey

								#If the current colour/ property is the start or destination cell then remove the old start/ destination cell from the grid
                                if options['selected_colour'] == green or options['selected_colour'] == red:
                                    for i in range(options['size_of_grid'][0]):
                                        for j in range(options['size_of_grid'][1]):
                                            if grid_references[i][j][2] == green and options['selected_colour'] == green:
                                                grid_references[i][j][2] = grey
                                            elif grid_references[i][j][2] == red and options['selected_colour'] == red:
                                                grid_references[i][j][2] = grey

							#If the selected colour is black - A line is being drawn
                            elif options['selected_colour'] == black:
								#If the cell being clicked is passable terrain - Validates you aren't trying to draw a line to an impassable terrain cell
                                if grid_references[column][row][2] == green or grid_references[column][row][2] == red or grid_references[column][row][2] == white:
									#If the click is the start of a line
                                    if options['start_of_line'] == True:
										#Assign the column and row of the first cell of the line to a variable
                                        start_grid = [column, row]
										#Assign the colour/ property of a cell to a variable so it can be restored later
                                        start_colour = grid_references[column][row][2]

										#If the start colour is red, shade the cell light red to show it is the start of a line
                                        if start_colour == red:
											#Start cell is filled in as validation
                                            start_cell = [column, row]
                                            grid_references[column][row][2] = light_red
										#If the start colour is red, shade the cell light red to show it is the start of a line
                                        elif start_colour == green:
											#End cell is filled in as validation
                                            end_cell = [column, row]
                                            grid_references[column][row][2] = light_green
										#If the cell is white, shade it light grey
                                        else:
                                            grid_references[column][row][2] = light_grey

										#Note the start of the line for drawing it
                                        start_of_line = grid_references[column][row]
										#Get the coordinates of the top left of the cell
                                        startx, starty = start_of_line[0], start_of_line[1]
										#Get the coordinates of the centre of the cell, relative to the screen
                                        startx += 29 + (options['size_of_square']/2)
                                        starty += 29 + (options['size_of_square']/2)
										#Start of line is now false, so that the next click draws the line
                                        options['start_of_line'] = False

									#If selecting the end coordinate of the line
                                    elif options['start_of_line'] == False:
										#Validation
                                        if grid_references[column][row][2] == red:
                                            start_cell = [column, row]
                                        elif grid_references[column][row][2] == green:
                                            end_cell = [column, row]

										#Returning the starting cell back to it's original colour
                                        grid_references[start_grid[0]][start_grid[1]][2] = start_colour
										#Assigning appropriate coordinates of the end cell to variables
                                        end_of_line = grid_references[column][row]
                                        endx, endy = end_of_line[0], end_of_line[1]
                                        endx += 29 + (options['size_of_square']/2)
                                        endy += 29 + (options['size_of_square']/2)

										#If a line has been drawn
                                        if len(list_of_lines) != 0:
											#The coordinates of the line being drawn - Take the start co-ordinates of this line as A and end coordinates as B, so line is AB [startx, starty, endx, endy]
                                            line1 = [start_grid[0], start_grid[1], column, row]
											#The reverse of a line so [endx, endy, startx, starty]
                                            reverse_line1 = [line1[2], line1[3], line1[0], line1[1]]
											#Validation check
                                            intersect = False

											#Loop through all the lines and check if they intersect with the line being drawn
                                            for i in line_coordinates:
												#Validation variables for each line
                                                intersect1, intersect2 = False, False
												#Assigning the coordinates of each line in line coordinates to a variable that is easier to understand - Take the start co-ordinates of this line as C and end coordinates as D, so line is CD
                                                line2 = i

												#Initial validation - Checking the line being drawn isn't the same line, or the same line being drawn the other way, as a line already on the grid - Removing duplicate lines
                                                if line1 == line2 or reverse_line1 == line2:
													#Intersect variable for validation is True, the line won't be drawn
                                                    intersect = True

												#With the line being drawn as AB and each line in the list of lines being CD, we can use the following formula to check if they intersect - Ax would be the x value for A, Ay would be the y coordinate
                                                else:
													#(Dx - Cx)(Ay - Dy) - (Dy - Cy)(Ax - Dx)
                                                    x = (line2[2] - line2[0])*(line1[1] - line2[3]) - (line2[3] - line2[1])*(line1[0] - line2[2])
													#(Dx - Cx)(By - Fy) - (Dy - Cy)(Bx - Dx)
                                                    y = (line2[2] - line2[0])*(line1[3] - line2[3]) - (line2[3] - line2[1])*(line1[2] - line2[2])

													#If x and y are opposite signs, one is positive and one is negative, then one coordinate of the line being drawn is within the boundary of another line - We then perform the check with another coordinate
                                                    if x > 0 and y < 0:
                                                        intersect1 = True
                                                    elif x < 0 and y > 0:
                                                        intersect1 = True

													#(Bx - Ax)(Cy - By) - (By - Ay)(Cx - Bx)
                                                    a = (line1[2] - line1[0])*(line2[1] - line1[3]) - (line1[3] - line1[1])*(line2[0] - line1[2])
													#(Bx - Ax)(Dy - By) - (By - Ay)(Dx - Bx)
                                                    b = (line1[2] - line1[0])*(line2[3] - line1[3]) - (line1[3] - line1[1])*(line2[2] - line1[2])

													#Checking if the other coordinate of the line being drawn is within the boundary of another line
                                                    if a > 0 and b < 0:
                                                        intersect2 = True
                                                    elif a < 0 and b > 0:
                                                        intersect2 = True

													#If both coordinates are within the boundaries of another line, that means it intersects
                                                    if intersect1 == True and intersect2 == True:
														#The intersect variable is assigned to True, so the line will not be drawn
                                                        intersect = True

										#If this is the first line being drawn (can't intersect with another line) or if it isn't the first line but is valid, then draw the line
                                        if len(list_of_lines) == 0 or intersect == False:
											#Finding the length of the line [dx, dy]
                                            size = [endx-startx, endy-starty]
											#Getting the coordinates of the middle of the line, then taking away half the size of the box that contains the number for the length of the line - So the box is drawn in the centre
                                            middlex = startx + (size[0]/2)
                                            middlex -= 13
                                            middley = starty + (size[1]/2)
                                            middley -= 13
											#Use the Pythagoras theorem to work out the distance between the two lines
                                            pythag = ((column-start_grid[0])**2 + (row-start_grid[1])**2)**0.5
											#Rounding the weight of the line to two significant figures
                                            weight = round(pythag, 2-int(floor(log10(pythag)))-1)

											#If the line ends in .0
                                            if str(weight-int(weight))[1:] == ".0":
												#Remove the .0 so that it just displays the number
                                                weight = int(weight)

											#Append the coordinates of start and end coordinates of the line to the list, along with the coordinates where the box will be drawn and the weight - The box is drawn later with the line - This is used to draw the lines
                                            list_of_lines.append([startx, starty, endx, endy, middlex, middley, weight])
											#Append the start and end cell reference, instead of the pixel coordinate, to a separate list - This is used for performing Dijkstra's Algorithm
                                            line_coordinates.append([start_grid[0], start_grid[1], column, row, weight])

											#If either the start or the end of a line is on a cell that hasn't had a line drawn to it yet, append it to the list of circles, since these are drawn before the lines so that they always appear below them
                                            if [startx, starty] not in list_of_circles:
                                                list_of_circles.append([startx, starty])
                                            if [endx, endy] not in list_of_circles:
                                                list_of_circles.append([endx, endy])

										#Once a has been drawn, or failed to be drawn, the start of line option is now True again so the next click starts another line
                                        options['start_of_line'] = True
										#Option to show lines have been drawn - Recolours options to show they are disabled
                                        options['lines'] = True

							#If the selected colour isn't a line - Then update the cell with the colour selected
                            if options['selected_colour'] != black:
                                grid_references[column][row][2] = options['selected_colour']

					#If the user clicks outside the grid, the start of the line is reset
                    else:
                        options['start_of_line'] = True
                        if start_grid != "":
                            grid_references[start_grid[0]][start_grid[1]][2] = start_colour

					#Redraw the options screen with any changes
                    options_screen = function1_screen()
                    options_screen.draw_options_screen()
                    coordinate_list = options_screen.coordinate_list

				#If the user clicks and the options aren't displayed, other buttons are available
                elif options['show_options'] == False:
					#If the user clicks the home button
                    if (x >= home_co[0] and x <= home_co[1]) and (y >= home_co[2] and y <= home_co[3]):
						#Erase all variables associated with the grid, so that not of it carries over if the user decides to start a new grid
                        grid_references = []
                        list_of_lines = []
                        list_of_circles = []
                        line_coordinates = []
                        options['lines'] = False
                        options['solve'] = False
                        options['show_options_arrow'] = True
						#Returns the user to the choose function page again
                        choose_function()

					#If either the start or destination cell doesn't have a line attached to it then the solve button shouldn't be displayed
                    if start_cell == "" or end_cell == "":
                        options['show_solve_button'] = False
                    else:
                        options['show_solve_button'] = True

					#If the solve button is available, validation has checked it should be displayed
                    if options['show_solve_button'] == True:
						#Retrieve the solve button co-ordinates, this is retrieved now so the user cannot click the button when it isn't displayed
                        sb_co = coordinate_list[1]
						#If the user clicks the solve button
                        if (x >= sb_co[0] and x <= sb_co[1]) and (y >= sb_co[2] and y <= sb_co[3]):
                            #If solve is False, then the graph is ready to be solved
                            if options['solve'] == False:
								#Solve option turns true
                                options['solve'] = True
								#Remove options arrow when the graph is solved
                                options['show_options_arrow'] = False
								#Run function2 of the perform_dijkstras file, to retrieve the final route - Is displayed in another class
                                final_route = perform_dijkstras.function2(line_coordinates, start_cell, end_cell)
                                print final_route

                            #If solve is true, then the graph has been solved, so clicking this button again returns the user back to the editing screen
                            elif options['solve'] == True:
                                options['solve'] = False
                                options['show_options_arrow'] = True

					#Redraw the screen to reflect any changes made
                    no_options_screen = function1_screen()
                    no_options_screen.draw_no_options_screen()
                    coordinate_list = no_options_screen.coordinate_list

		#Update the display
        pygame.display.update()

#Creating a class for creation of buttons and text boxes
class box(object):
	#This runs automatically, the default place holder variables that are then changed by a module or by editing the instance
    def __init__(self):
		#Fill colour of the box
        self.fill_colour = white
		#Location, in pixels, from the top left of the screen to the top left of the box
        self.location = (0, 0)
		#Size of box in pixels
        self.size = (0, 0)
		#Colour of the outline of the box
        self.outline_colour = black
		#Size of the outline of the box
        self.size_outline = 1
		#Font size of text within the box
        self.font_size = 18
		#Text input, if any
        self.text_input = ""
		#Location of the text within the box, usually defined by a module but can be custom defined
        self.text_location = (0, 0)
		#If the text is bold
        self.bold = False

	#Module for the standard button used in throughout the menu
    def default_button(self):
        self.size = (150, 100)
        self.font_size = 20

	#Module for standard text box, used in the main menu
    def default_text_box(self):
        self.location = (200, 450)
        self.size = (880, 150)
        self.font_size = 16

	#Module for standard button featured on the options screen at the side of the grid
    def default_options_buttons(self):
        self.size = (20, 20)
        self.font_size = 16
        self.size_outline = 2

	#Module that draws the box on screen once the size and location has been defined
    def draw_box(self):
		#The outline of the box is created by drawing a larger box behind the first
        outline_location = (self.location[0] - self.size_outline, self.location[1] - self.size_outline)
        outline_size = (self.size[0] + (self.size_outline*2), self.size[1] + (self.size_outline*2))

		#Drawing first the outline box, then the actual box on top to create the button/ text box
        screen.lock()
        pygame.draw.rect(screen, self.outline_colour, (outline_location, outline_size))
        pygame.draw.rect(screen, self.fill_colour, (self.location, self.size))
        screen.unlock()

	#Preparing the necessary variables for displaying text on screen, this is separate in case the text needs to be centralised before displayed
    def prep(self):
        self.x_position, self.y_position = self.text_location
        self.font = pygame.font.SysFont("calibri", self.font_size, self.bold)
        self.text = self.font.render(self.text_input, 1, black)    #rendering the text on to the screen

	#Getting the start and end coordinates of the box
    def get_coords(self):
        x1 = self.location[0]
        x2 = self.location[0] + self.size[0]
        y1 = self.location[1]
        y2 = self.location[1] + self.size[1]
        return x1, x2, y1, y2

	#Runs two modules to centralise the text in both axes
    def centralise_text(self):
        self.centralise_x(), self.centralise_y()

	#Centralises the text in the x axis
    def centralise_x(self):
		#Gets the middle coordinate of the box
        self.x_position = self.location[0] + (self.size[0]/2)
		#Subtracts half the width of the text
        self.x_position -= ((self.text.get_width()+1)/2)

	#Centralises the text in the y axis
    def centralise_y(self):
        self.y_position = self.location[1] + (self.size[1]/2)
        self.y_position  -= (((self.text.get_height()+1)*(3/4.))/2)

	#Display the final text on the screen
    def display_text(self):
        screen.blit(self.text, (self.x_position, self.y_position))

#Class containing the necessary modules to display the main function screen of the program
class function1_screen(object):
	#Displays the workspace area using the box class, the white box that the grid and options are displayed on top of
    def __init__(self):
        workspace = box()
        workspace.location = (10, 10)
        workspace.size = (1260, 700)
        workspace.draw_box()
		#Resets coordinate list each time, since it is used for both functions
        self.coordinate_list = []

	#Displays the home button using the box class
    def home_button(self):
        home = box()
        home.default_button()
        home.location = (1090, 90)
        home.size = (150, 30)
        home.font_size = 20 #1240, 65
        home.text_input = "Main Menu"
        home.draw_box(), home.prep(), home.centralise_text(), home.display_text()
        self.home_button_coordinates = home.get_coords()

	#Creates all the buttons necessary for the options bar at the side of the screen during the main program
    def options_box_create(self):
		#Creating the options bar
        options_box = box()
        options_box.location = (1000, 30)
        options_box.size = (250, 660)
        options_box.size_outline = 2
        options_box.draw_box()

		#Displaying options text at top of options bar
        font = pygame.font.SysFont("calibri", 18)
        screen.blit(font.render("Options:", 1, black), (1010, 45))

		#Creating inverted options arrow to close the options bar
        self.arrow_box_create()
        pygame.draw.polygon(screen, black, [(1220, 45), (1221, 45), (1233, 52), (1233, 53), (1221, 60), (1220, 60)])

		#Displays the first size of grid input along with the text "Size of Grid:"
        screen.blit(pygame.font.SysFont("calibri", 16).render("Size of Grid:", 1, black), (1010, 100))
        size_of_grid = box()
        size_of_grid.default_options_buttons()
        size_of_grid.location = (1150, 95)
        size_of_grid.size = (30, 20)
        size_of_grid.text_input = str(options['size_of_grid'][0])
        if options['lines'] == True:
            size_of_grid.fill_colour = light_grey
        size_of_grid.draw_box(), size_of_grid.prep(), size_of_grid.centralise_text(), size_of_grid.display_text()
        sog_coords = size_of_grid.get_coords()

		#Displays the second size of grid input along with the "x" in between the two inputs
        screen.blit(pygame.font.SysFont("calibri", 16).render("x", 1, black), (1190, 100))
        size_of_grid2 = box()
        size_of_grid2.default_options_buttons()
        size_of_grid2.location = (1210, 95)
        size_of_grid2.size = (30, 20)
        size_of_grid2.text_input = str(options['size_of_grid'][1])
        if options['lines'] == True:
            size_of_grid2.fill_colour = light_grey
        size_of_grid2.draw_box(), size_of_grid2.prep(), size_of_grid2.centralise_text(), size_of_grid2.display_text()
        sog2_coords = size_of_grid2.get_coords()

		#Displays the text "Max Size of Grid: a x b" depending on the function (40 x 30 for Grid function, 14 x 10 for Vertices function)
        font = pygame.font.SysFont("calibri", 14)
        max_size1 = font.render("Max Size of Grid:", 1, black)
        screen.blit(max_size1, (1010, 125))
        if options['function'] == 1:
            max_size2 = font.render("40", 1, black)
        elif options['function'] == 2:
            max_size2 = font.render("14", 1, black)
        screen.blit(max_size2, (1157, 125))
        max_size3 = font.render("x", 1, black)
        screen.blit(max_size3, (1190, 125))
        if options['function'] == 1:
            max_size4 = font.render("30", 1, black)
        elif options['function'] == 2:
            max_size4 = font.render("10", 1, black)
        screen.blit(max_size4, (1217, 125))

		#Creates the start position option box
        start_position = box()
        start_position.default_options_buttons()
        start_position.location = (1220, 160)
        start_position.text_location = (1010, 165)
        start_position.text_input = "Start Position:"
        if options['lines'] == False:
            start_position.fill_colour = red
        else:
			#For when the options are disabled
            start_position.fill_colour = light_grey
        start_position.draw_box(), start_position.prep(), start_position.display_text()
        sp_coords = start_position.get_coords()

		#Creates the passable terrain option
        passable_terrain = box()
        passable_terrain.default_options_buttons()
        passable_terrain.location = (1220, 200)
        passable_terrain.text_location = (1010, 205)
        passable_terrain.text_input = "Passable Terrain:"
        if options['lines'] == True:
            passable_terrain.fill_colour = light_grey
        passable_terrain.draw_box(), passable_terrain.prep(), passable_terrain.display_text()
        pt_coords = passable_terrain.get_coords()

		#If the Grid function is working then there is a slow terrain option
        if options['function'] == 1:
            slow_terrain = box()
            slow_terrain.default_options_buttons()
            slow_terrain.location = (1220, 240)
            slow_terrain.text_location = (1010, 245)
            slow_terrain.text_input = "Slow Terrain:"
            if options['lines'] == False:
                slow_terrain.fill_colour = brown
            else:
                slow_terrain.fill_colour = light_grey
            slow_terrain.draw_box(), slow_terrain.prep(), slow_terrain.display_text()
            st_coords = slow_terrain.get_coords()

		#Impassable terrain option
        impassable_terrain = box()
        impassable_terrain.default_options_buttons()
        impassable_terrain.location = (1220, 280)
        impassable_terrain.text_location = (1010, 285)
        if options['function'] == 2:
			#Since there is no slow terrain all other options have to be moved up
            impassable_terrain.location = (1220, 240)
            impassable_terrain.text_location = (1010, 245)
        impassable_terrain.text_input = "Impassable Terrain:"
        if options['lines'] == False:
            impassable_terrain.fill_colour = grey
        else:
            impassable_terrain.fill_colour = light_grey
        impassable_terrain.draw_box(), impassable_terrain.prep(), impassable_terrain.display_text()
        it_coords = impassable_terrain.get_coords()

		#Destination position option
        destination_position = box()
        destination_position.default_options_buttons()
        destination_position.location = (1220, 320)
        destination_position.text_location = (1010, 325)
        if options['function'] == 2:
            destination_position.location = (1220, 280)
            destination_position.text_location = (1010, 285)
        destination_position.text_input = "Destination Position:"
        if options['lines'] == False:
            destination_position.fill_colour = green
        else:
            destination_position.fill_colour = light_grey
        destination_position.draw_box(), destination_position.prep(), destination_position.display_text()
        dp_coords = destination_position.get_coords()

		#If the Vertices function is running then the draw lines option is displayed at the bottom of the options
        if options['function'] == 2:
            draw_line = box()
            draw_line.default_options_buttons()
            draw_line.location = (1220, 320)
            draw_line.text_location = (1010, 325)
            draw_line.text_input = "Draw Line"
            draw_line.fill_colour = black
            draw_line.draw_box(), draw_line.prep(), draw_line.display_text()
            dl_coords = draw_line.get_coords()

		#Displays the currently selected colour so teh user knows what property they will assign to a cell if they click one
        selected_colour = box()
        selected_colour.default_options_buttons()
        selected_colour.location = (1220, 370)
        selected_colour.text_location = (1010, 375)
        selected_colour.text_input = "Selected Colour:"
        selected_colour.font_size = 16
        selected_colour.bold = True
        if options['lines'] == False:
            selected_colour.fill_colour = options['selected_colour']
        else:
            selected_colour.fill_colour = black
        selected_colour.draw_box(), selected_colour.prep(), selected_colour.display_text()

		#If the Vertices function is running and a line has been drawn on the screen then the Clear Lines button needs to be displayed
        if options['function'] == 2 and len(list_of_lines) != 0:
            clear_lines = box()
            clear_lines.location = (1050, 600)
            clear_lines.size = (150, 40)
            clear_lines.text_input = "Clear current lines"
            clear_lines.font_size = 18
            clear_lines.draw_box(), clear_lines.prep(), clear_lines.centralise_text(), clear_lines.display_text()
            cl_coords = clear_lines.get_coords()

		#Adds the coordinates of each button the coordinate list (extend is the same as append but for multiple items
        self.coordinate_list.extend([sog_coords, sog2_coords, sp_coords, pt_coords, it_coords, dp_coords])
		#If the Grid function is running it appends the slow terrain coordinates at the end
        if options['function'] == 1:
            self.coordinate_list.append(st_coords)
		#If the Vertices function is running it appends the draw line coordinates at the end along with the clear lines if there are lines drawn
        elif options['function'] == 2:
            self.coordinate_list.append(dl_coords)
            if len(list_of_lines) != 0:
                self.coordinate_list.append(cl_coords)

	#Displays the arrow in the top right corner to open/ close the option bar
    def arrow_box_create(self):
        arrow_box = box()
        arrow_box.location = (1215, 40)
        arrow_box.size = (25, 25)
        arrow_box.draw_box()
        self.arrow_box_coordinates = arrow_box.get_coords()

	#Creates the solve button
    def solve_box_create(self):
        solve_button = box()
        solve_button.default_button()
        solve_button.location = (1025, 600)
        solve_button.size = (200, 50)
        solve_button.font_size = 20
        if options['solve'] == False:
            solve_button.text_input = "Solve"
		#If the graph is solved the button returns the user to the editing screen, so the text is changed
        elif options['solve'] == True:
            solve_button.text_input = "Return"
        solve_button.draw_box(), solve_button.prep(), solve_button.centralise_text(), solve_button.display_text()
        self.solve_button_coordinates = solve_button.get_coords()

	#This module performs a basic validation check, if the grid contains the start and destination cells required to solve the grid
    def grid_validity(self):
        green_valid, red_valid = False, False
		#Loops through all the cells in the grid
        for i in range(options['size_of_grid'][0]):
            for j in range(options['size_of_grid'][1]):
				#If the end cell is present updates the variable to show it is
                if grid_references[i][j][2] == green:
                    green_valid = True
				#If the start cell is present updates the variable to show it is
                elif grid_references[i][j][2] == red:
                    red_valid = True

		#If the Grid function is running then validate the grid (the Vertices function requires extra validation to detect if there are lines drawn to/ from the start and destination coordinates)
        if options['function'] == 1:
			#If both the start and destination cells are present, the Solve button is displayed
            if green_valid == True and red_valid == True:
                options['show_solve_button'] = True
            else:
                options['show_solve_button'] = False

	#Module that runs other modules necessary to create the main program screen (such as creating the grid references)
    def draw_initial_screen(self):
		#Instance of the display_grid class below
        grid = display_grid()
		#Initialises the grid - Creates lists and draws the grid
        grid.initialise_grid()

		#Runs the arrow_box_create module to display the arrow box
        self.arrow_box_create()
		#Draws the initial arrow
        pygame.draw.polygon(screen, black, [(1235, 45), (1234, 45), (1222, 52), (1222, 53), (1234, 60), (1235, 60)])

		#Appends the coordinates of the outline of the grid to the coordinate list
        self.coordinate_list.append(grid.grid_coordinates)
		#Check if the grid is valid
        self.grid_validity()

		#If the grid is valid and the solve button can be pressed then display the solve button and append the coordinates
        if options['show_solve_button'] == True:
            self.solve_box_create()
            self.coordinate_list.append(self.solve_button_coordinates)

		#Create the home button
        self.home_button()
        self.coordinate_list.append(self.home_button_coordinates)

	#Draw the screen with the options bar displayed
    def draw_options_screen(self):
		#Instance of display_grid class
        grid = display_grid()
		#Update the grid - Separate from initialise grid since it doesn't have to create the grid coordinates from scratch
        grid.update_grid()
		#Append the coordinates to the list
        self.coordinate_list.append(grid.grid_coordinates)
		#Run the options_box_create module
        self.options_box_create()

	#Draw the screen without the options bar displayed
    def draw_no_options_screen(self):
		#Displaying grid and home button
        grid = display_grid()
        grid.update_grid()
        self.coordinate_list.append(grid.grid_coordinates)
        self.grid_validity()
        self.home_button()

		#If the options arrow should be displayed then display it
        if options['show_options_arrow'] == True:
            self.arrow_box_create()
            pygame.draw.polygon(screen, black, [(1235, 45), (1234, 45), (1222, 52), (1222, 53), (1234, 60), (1235, 60)])

		#If the solve button should be displayed then display it
        if options['show_solve_button'] == True:
            self.solve_box_create()
            self.coordinate_list.append(self.solve_button_coordinates)

		#If the graph has selected to be solved
        if options['solve'] == True:
			#If it Grid function
            if options['function'] == 1:
				#Retrieve the shortest route by running the main function of the perform_dijkstras file
                finished_route = perform_dijkstras.main(options['size_of_grid'], grid_references)
				#Run the draw_shortest_route module of the grid class to display the shortest route
                grid.draw_shortest_route(finished_route)

		#Display the home button
        self.home_button()
        self.coordinate_list.append(self.home_button_coordinates)

#Class for everything to do with displaying the grid
class display_grid(object):
	#Runs every time this class is called
    def __init__(self):
		#Using the global grid_references variable instead of creating a new one
        global grid_references
		#Retrieving necessary information from options dictionary
        self.size_of_grid = options['size_of_grid']
        self.size_of_square = options['size_of_square']

		#Creating the outline of the grid
        grid_outline = box()
        grid_outline.location = (30, 30)
        grid_outline.size = ((self.size_of_grid[0]*self.size_of_square) + 1, (self.size_of_grid[1]*self.size_of_square) + 1)
        grid_outline.size_outline = 1
        grid_outline.fill_colour = black
        grid_outline.draw_box()
        self.grid_coordinates = grid_outline.get_coords()

	#Module to create and draw the grid
    def initialise_grid(self):
        self.create_grid_references()
        self.draw_grid()

	#Module to create list of all grid references
    def create_grid_references(self):
        global grid_references
		#Loops through the number of columns that should be displayed
        for i in range(self.size_of_grid[0]):
			#The x coordinate, in pixels, of the start of each cell in that column
            self.x = (i * self.size_of_square) + 1
			#Append an empty list to the grid_references to hold all of the rows in that column
            grid_references.append([])

			#Loops through all the rows in that column
            for j in range(self.size_of_grid[1]):
				#Creates the y coordinate of each cell in that column
                self.y = (j * self.size_of_square) + 1
				#If the Grid function is running then all the cells are default white/ passable terrain
                if options['function'] == 1:
                    grid_references[i].append([self.x, self.y, white])
				#If the Vertices function is running then all the cells are default grey/ impassable terrain
                elif options['function'] == 2:
                    grid_references[i].append([self.x, self.y, grey])

		#Assign the top left cell to be the start cell and the bottom right cell to be the destination cell as default placeholders
        grid_references[0][0][2], grid_references[self.size_of_grid[0]-1][self.size_of_grid[1]-1][2] = red, green

	#Draw the grid from the grid references
    def draw_grid(self):
        global grid_references#
		#Loops through all the cells
        for i in range(self.size_of_grid[0]):
            for j in range(self.size_of_grid[1]):
				#Assigns the x and y coordinate of the top left of each cell to variables
                x_coordinate = grid_references[i][j][0]
                y_coordinate = grid_references[i][j][1]
				#Retrieves the colour of the cell from the grid references to be displayed
                colour_of_cell = grid_references[i][j][2]
				#Draw each cell on the grid (Where it's being drawn, colour, ((x coordinate of start of cell, y coordinate of start of cell), (size of each cell))
                pygame.draw.rect(screen, colour_of_cell, ((x_coordinate + 30, y_coordinate + 30), ((self.size_of_square-1), (self.size_of_square-1))))

		#If the Vertices function is running
        if options['function'] == 2:
            finished_route_circles = [] #--

            for i in list_of_lines:
                if i[:2] in list_of_circles and i[:2] not in finished_route_circles:
                    finished_route_circles.append(i[:2])
                if i[2:4] in list_of_circles and i[2:4] not in finished_route_circles:
                    finished_route_circles.append(i[2:4])

			#Draw a circle for each circle in the list - To show the start and end of each line more clearly
            for i in list_of_circles:
                if i not in finished_route_circles:
                    pygame.draw.circle(screen, light_blue, (i[0], i[1]), 7)

			#Variables for drawing the lines on screen
            count = 0
            finished_route = []

			#Loops through each line drawn on screen
            for i in list_of_lines:
                if options['solve'] == True:
                    print options['solve'], line_coordinates[count], final_route, i
				#If the graph has been solved and that line is in the final route retrieved from the perform_dijkstras file, then another list is created with the x and y coordinates or each line, instead of the column and row number
                if options['solve'] == True and line_coordinates[count] in final_route:
                    finished_route.append(i)

				#If the line is not in the finished route then draw the line, including the text box in the middle displaying the weight of the line
                else:
                    pygame.draw.line(screen, black, (i[0]-1, i[1]-1), (i[2]-1, i[3]-1), 2)
                    pygame.draw.rect(screen, black, ((i[4]-1, i[5]-1), (27, 27)))
                    pygame.draw.rect(screen, white, ((i[4], i[5]), (25, 25)))
                    font = pygame.font.SysFont("calibri", 16)
                    text = font.render(str(i[6]), 1, black)
                    middlex = i[4] + 12
                    middlex -= ((text.get_width()+1)/2)
                    middley = i[5] + 12
                    middley -= (((text.get_height()+1)*(3/4.))/2)
                    screen.blit(text, (middlex, middley))

				#Count variable for looping through the line_coordinates
                count += 1

            for i in finished_route_circles:    #--
                pygame.draw.circle(screen, light_blue, (i[0], i[1]), 7)

			#For each line in the finished route, draw the line but in blue - This happens after so that the finished route is always displayed on top of other lines
            for i in finished_route:
                pygame.draw.line(screen, light_blue, (i[0]-1, i[1]-1), (i[2]-1, i[3]-1), 3)
                pygame.draw.rect(screen, light_blue, ((i[4]-1, i[5]-1), (27, 27)))
                pygame.draw.rect(screen, white, ((i[4], i[5]), (25, 25)))
                font = pygame.font.SysFont("calibri", 16)
                text = font.render(str(i[6]), 1, black)
                middlex = i[4] + 12
                middlex -= ((text.get_width()+1)/2)
                middley = i[5] + 12
                middley -= (((text.get_height()+1)*(3/4.))/2)
                screen.blit(text, (middlex, middley))

	#Module for updating the grid - Since the grid references don't need to be created again
    def update_grid(self):
        global grid_references
		#Store the original grid references and grid size before any changes
        old_grid_references = grid_references
        old_size_of_grid = [len(old_grid_references), len(old_grid_references[0])]
		#Retrieve the new size of the grid from the options
        new_size_of_grid = options['size_of_grid']

		#If the grid size has been changed, then it recreates the grid references, but keeping any old cells
        if old_size_of_grid != new_size_of_grid:
            grid_references = []
			#Loops through all the cells
            for i in range(new_size_of_grid[0]):
                x = (i * self.size_of_square) + 1
                grid_references.append([])
                for j in range (new_size_of_grid[1]):
                    y = (j * self.size_of_square) + 1
					#This is where it's different, if the cell is within the size of the old grid
                    if i < old_size_of_grid[0] and j < old_size_of_grid[1]:
						#It retrieves the property of that cell from the old grid_references
                        colour = old_grid_references[i][j][2]

					#Otherwise it fills the cell in with it's default property depending on the function
                    else:
                        if options['function'] == 1:
                            colour = white
                        elif options['function'] == 2:
                            colour = grey

					#Updating the new grid references with the coordinate and colour of each cell
                    grid_references[i].append([x, y, colour])

		#Draw the updated grid
        self.draw_grid()

	#Module for drawing the shortest route - For the Grid function
    def draw_shortest_route(self, finished_route):
		#For each cell in the finished route
        for i in range(len(finished_route)):
			#Retrieve the coordinate of the cell and find the middle of the cell
            current_cell = grid_references[finished_route[i][0]][finished_route[i][1]]
            x = current_cell[0]
            y = current_cell[1]
            x += 29 + (self.size_of_square/2)
            y += 29 + (self.size_of_square/2)

			#Replace the column/ row number with the x and y coordinate of the centre of each cell in the finished route
            finished_route[i] = (x, y)

		#Loops through the finished route and draws a line from the centre of each cell to the next
        for i in range(len(finished_route)-1):
            pygame.draw.line(screen, black, finished_route[i], finished_route[i+1], 2)

#If the program is being run by itself, not through another file, then perform the main_menu function
if __name__ == "__main__":
    main_menu()