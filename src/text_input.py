#Importing modules
import pygame, sys
#RGB value for black
black = (0, 0, 0)

#Class containing the code for the retrieving inputs and displaying them on screen
class text_input_display():
    def __init__(self, screen, co_ords, size):
		#Assigning the start and end coordinates of the box it is being displayed in
        x, y, endx, endy = co_ords
		#Place holder variables
        empty_string = ""
        self.completed_text = ""
        current_list = []
        done = False
		
		#Whilst done doesn't equal False, run through loop. done = False until stated otherwise in the code
        while done == False:
			#Coordinates of mouse
            mousex, mousey = pygame.mouse.get_pos()
			#Loops through all events in the event loop (button clicks, entered keyboard characters etc.)
            for event in pygame.event.get():
				#If the current event is QUIT (the X in the top right of the window)
                if event.type == pygame.QUIT:
					#Quits the program
                    pygame.quit()
                    sys.exit()
					
				#If the mouse is clicked and it's outside the input box:	
                elif (event.type == pygame.MOUSEBUTTONUP) and ((mousex < x or mousex > endx) or (mousey < y or mousey > endy)):
					#Append each of the character of the list to the variable "completed_text"
                    self.completed_text = self.completed_text.join(current_list)
					#done = True, so the while loop closes and moves onto the code after it (exiting the program)
                    done = True
					
				#If the current event is a keyboard button being pressed down
                elif event.type == pygame.KEYDOWN:
					#If the key of the current event is the backspace being pressed down
                    if event.key == pygame.K_BACKSPACE:
						#The current list is now 1 less in length of what it was before (removes the last character of the list)
                        current_list = current_list[0:-1]
					#If the current key is the enter key
					
                    elif event.key == 13 or event.key == 271:
						#Append each character of the list to the variable "completed_text"
                        self.completed_text = self.completed_text.join(current_list)
						#Done is now True, so the loop ends
                        done = True
						
					#If the current key is a number being pressed down and the length of the current list is less than 2, there is room for another character, then convert it to a number
                    elif ((event.key >= 48 and event.key <= 57) or (event.key >= 256 and event.key <= 265)) and len(current_list) < 2:
						#This changes numbers entered on the number pad to be the same as the ones at the top of the keyboard, so I can easily convert them
                        if event.key >= 256:
                            key = event.key - 208
                        else:
                            key = event.key
							
						#Convert the key into a character and append it to the list
                        current_list.append(chr(key))
						
			#Append the current characters to a string to be displayed on screen
            text = empty_string.join(current_list)
			#Run the displaytext module to display the text on screen
            self.displaytext(screen, x, y, size, text)

    def displaytext(self, screen, x, y, size, text):
		#Assigning font properties to a variable
        font = pygame.font.SysFont("calibri", 16)
        text = font.render(text, 1, black)

		#Getting the coordinates of where the text should start - Middle of the input box
        middlex = x + (size[0]/2)
        middlex -= ((text.get_width()+1)/2)
        middley = y + (size[1]/2)
        middley -= (((text.get_height()+1)*(3/4.))/2)

		#Display the text on screen
        pygame.draw.rect(screen, (200, 200, 200), ((x, y), size))
        screen.blit(text, (middlex, middley))
        pygame.display.update()