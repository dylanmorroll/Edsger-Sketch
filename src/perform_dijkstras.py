#Importing necessary modules
from math import log10, floor

#Assigning RGB values to variables
black = (0, 0, 0)
grey = (125, 125, 125)
white = (255, 255, 255)
red = (255, 0, 0)
green = (67, 205, 128)
brown = (139, 69, 39)

#The initial function for the Grid function
def main(size_of_grid, grid_references):
    #Creating an empty list to hold properties for each cell
    weight_list =[]

    #Loop through all the cell
    for i in range(size_of_grid[0]):
        weight_list.append([])
        for j in range(size_of_grid[1]):
            #Retrieve the colour of the cell and get the weight
            colour_of_cell = grid_references[i][j][2]
            weight_of_cell = get_weight(colour_of_cell)
            #Append an list for each cell containing the weight of the cell, then 3 empty strings to be replaced with permanent value, working cumulative weight and the permanent cumulative weight respectively
            weight_list[i].append([weight_of_cell, "", "", ""])

            #Assign the start and destination cell reference to variables
            if grid_references[i][j][2] == green:
                start_position = [i, j]
            elif grid_references[i][j][2] == red:
                end_position = [i, j]
                #Assigning weight of destination cell to 1
                weight_list[i][j][0] = 1

    #Use the assign values function to get fill in the missing properties (permanent value, working cumulative weight and the permanent cumulative weight)
    updated_weight_list = assign_values(size_of_grid, weight_list, start_position, end_position)

    #Use the updated weight list, with complete properties, to find the shortest route
    finished_route = find_route(size_of_grid, updated_weight_list, start_position, end_position)

    #Return the shortest route so it is assigned to a variable
    return finished_route

#Get the weight of each cell from it's colour
def get_weight(colour_of_cell):
    #Grey cells are 0 - They are impassable
    if colour_of_cell == grey:
        weight = 0

    #White/ passable terrain cells are 1, normal weight
    elif colour_of_cell == white:
        weight = 1

    #Brown/ slow terrain cells are 2, they take twice as long to pass through
    elif colour_of_cell == brown:
        weight = 2

    #This forms part of the validation
    else:
        weight = ""
    return weight

#Assigning the missing properties to the weight list
def assign_values(size_of_grid, cells, start, end):
    #Assigning the properties of the start cell to 0
    cells[start[0]][start[1]] = [0, 0, 0, 0]
    #When calling the cells list it follows this formula:
    #cells[X Position/ Column][Y Position/ Row][0= weight || 1= permanent value (count) || 2= working cumulative weight || 3= permanent cumulative weight]

    #Assigning start as the current cell and some place holder variables
    current_cell = start
    finish = False

    #Once all the permanent weights have been filled in, this looks at the remaining weights and checks which has the lowest working weight and then assigns all the cells with the lowest working weight into this list
    smallest_values = []

    #Until all cells are filled in
    while finish != True:
        #The options are right, down, left and above the current cell, these check if the cell is accessible
        option1, option2, option3, option4 = False, False, False, False

        #These are the the [column, row] positions of each option
        right = [current_cell[0] +1, current_cell[1]]
        down = [current_cell[0], current_cell[1] +1]
        left = [current_cell[0] -1, current_cell[1]]
        up = [current_cell[0], current_cell[1] -1]

        #Checks to see if each cell is valid or not
        #If the option is not outside the grid, the cell hasn't already been assigned a PERMANENT value and the cell isn't impassable terrain
        if right[0] < size_of_grid[0] and cells[right[0]][right[1]][0] != 0 and cells[right[0]][right[1]][1] == "":
            #Then that option is True - The cell can be accessed
            option1 = True
        #This continues for all the options
        if down[1] < size_of_grid[1] and cells[down[0]][down[1]][0] != 0 and cells[down[0]][down[1]][1] == "":
            option2 = True
        if left[0] >= 0 and cells[left[0]][left[1]][0] != 0 and cells[left[0]][left[1]][1] == "":
            option3 = True
        if up[1] >= 0 and cells[up[0]][up[1]][0] != 0 and cells[up[0]][up[1]][1] == "":
            option4 = True

        #Here I assign each of the options, if they are valid, certain properties:
        #If the cell is valid
        if option1 == True:
            #If the working weight (the current permanent weight of the cell, plus the distance to the next cell, is less than working weight of the next cell
            if cells[current_cell[0]][current_cell[1]][3] + cells[right[0]][right[1]][0] < cells[right[0]][right[1]][2]:
                #Replace the working weight with the new, lower working weight
                cells[right[0]][right[1]][2] = cells[right[0]][right[1]][0] + cells[current_cell[0]][current_cell[1]][3]
                #Also the permanent value of that cell is the permanent value of the current cell plus one - This shows which cell is the next cell from it
                cells[right[0]][right[1]][1] = cells[current_cell[0]][current_cell[1]][1] + 1
        #This continues for each available option
        if option2 == True:
            if cells[current_cell[0]][current_cell[1]][3] + cells[down[0]][down[1]][0] < cells[down[0]][down[1]][2]:
                cells[down[0]][down[1]][2] = cells[down[0]][down[1]][0] + cells[current_cell[0]][current_cell[1]][3]
                cells[down[0]][down[1]][1] = cells[current_cell[0]][current_cell[1]][1] + 1
        if option3 == True:
            if cells[current_cell[0]][current_cell[1]][3] + cells[left[0]][left[1]][0] < cells[left[0]][left[1]][2]:
                cells[left[0]][left[1]][2] = cells[left[0]][left[1]][0] + cells[current_cell[0]][current_cell[1]][3]
                cells[left[0]][left[1]][1] = cells[current_cell[0]][current_cell[1]][1] + 1
        if option4 == True:
            if cells[current_cell[0]][current_cell[1]][3] + cells[up[0]][up[1]][0] < cells[up[0]][up[1]][2]:
                cells[up[0]][up[1]][2] = cells[up[0]][up[1]][0] + cells[current_cell[0]][current_cell[1]][3]
                cells[up[0]][up[1]][1] = cells[current_cell[0]][current_cell[1]][1] + 1

        #If there are no items in the smallest_values list - All the permanent weights have been filled in
        if len(smallest_values) == 0:
            #Assigns infinity to a variable to check which is the lowest number
            smallest_working_value = float('inf')
            #Loop through all the cells in the grid
            for i in range(size_of_grid[0]):
                for j in range(size_of_grid[1]):
                    #If the weight of a cell is smaller than the smallest_working_value, it changes the smallest_working_value to the lowest weight - This finds the lowest working weight out of any of the cells which don't have a permanent weight
                    if cells[i][j][2] < smallest_working_value and cells[i][j][3] == "":
                        smallest_working_value = cells[i][j][2]

            #Loops through all the cells and assigns those with the smallest working weight to a list
            for i in range(size_of_grid[0]):
                for j in range(size_of_grid[1]):
                    if cells[i][j][2] == smallest_working_value:
                        smallest_values.append([i, j])

        #If there are no more smallest values and none of the options are available function ends - This is either when we reach the destination cell or there is no route to the destination cell and it hits a dead end
        if option1 == False and option2 == False and option3 == False and option4 == False and len(smallest_values) == 0:
            finish = True

        #Whilst finish isn't True - there are still cells available
        if finish != True:
            #Assigns the current cell to the next value in the list of smallest values
            current_cell = smallest_values[0]
            #Removes the current cell from the list - Since we are going to check this now it is no longer going to have no permanent weight
            smallest_values.remove(current_cell)
            #The permanent weight of this cell is the smallest working value
            cells[current_cell[0]][current_cell[1]][3] = smallest_working_value

    #Return the cells with all properties assigned
    return cells

#Using the completed weight list with all properties assigned, find the route
def find_route(size_of_grid, cells, start_position, destination_position):
    #Creating place holder variables
    finished_route = []
    #The first cell in the final route must be the destination cell (working from destination to start)
    finished_route.append(destination_position)
    finish = False
    count = 0

    while finish != True:
        #Current cell is the next cell in the final route
        current_cell = finished_route[count]
        count += 1

        #Assigns cells adjacent to the current cell to variables
        option1, option2, option3, option4 = False, False, False, False
        right = [current_cell[0] +1, current_cell[1]]
        down = [current_cell[0], current_cell[1] +1]
        left = [current_cell[0] -1, current_cell[1]]
        up = [current_cell[0], current_cell[1] -1]

        #Here we check not only that the option is within the grid and valid, but also that the permanent value of the current cell subtract the permanent value of the cell we are looking at is 1 - This checks that it was directly connected to it as part of the route
        if right[0] < size_of_grid[0] and cells[right[0]][right[1]][1] != "" and cells[current_cell[0]][current_cell[1]][1] - cells[right[0]][right[1]][1] == 1:
            #The second part of this check, checks that the permanent weight of the current cell subtract the permanent weight of the cell we are looking at, is the distance between the two cells - Part of Dijkstra's algorithm
            if cells[current_cell[0]][current_cell[1]][3] - cells[right[0]][right[1]][3] == cells[current_cell[0]][current_cell[1]][0]:
                option1 = True

        if down[1] < size_of_grid[1] and cells[down[0]][down[1]][1] != "" and cells[current_cell[0]][current_cell[1]][1] - cells[down[0]][down[1]][1] == 1:
            if cells[current_cell[0]][current_cell[1]][3] - cells[down[0]][down[1]][3] == cells[current_cell[0]][current_cell[1]][0]:
                option2 = True

        if left[0] >= 0 and cells[left[0]][left[1]][1] != "" and cells[current_cell[0]][current_cell[1]][1] - cells[left[0]][left[1]][1] == 1:
            if cells[current_cell[0]][current_cell[1]][3] - cells[left[0]][left[1]][3] == cells[current_cell[0]][current_cell[1]][0]:
                option3 = True

        if up[1] >= 0 and cells[up[0]][up[1]][1] != "" and cells[current_cell[0]][current_cell[1]][1] - cells[up[0]][up[1]][1] == 1:
            if cells[current_cell[0]][current_cell[1]][3] - cells[up[0]][up[1]][3] == cells[current_cell[0]][current_cell[1]][0]:
                option4 = True

        #Once we have done this for each of the options, only one of them is valid, so we append that to the final route
        if option1 == True:
            finished_route.append(right)
        elif option2 == True:
            finished_route.append(down)
        elif option3 == True:
            finished_route.append(left)
        elif option4 == True:
            finished_route.append(up)

        #If they are all invalid, that means we have reached the starting cell and the final route is complete
        if option1 == False and option2 == False and option3 == False and option4 == False:
            finish = True

    #We reverse the final route, so that it goes from start to finish and return it back
    finished_route.reverse()
    return finished_route

#This is the function that handles the Vertices function of our program
def function2(line_coordinates, start_cell, end_cell):
    #Creating place holder variables
    #Cells is a list of all the cells that are used in the lines - Not to be mistaken with the line coordinates
    cells = []
    current_perm_value = 0
    finish = False
    valid = True

    #Multiply the weight of each line by 10 to avoid floating point arithmetic errors
    for i in range(len(line_coordinates)):
        line_coordinates[i][4] = line_coordinates[i][4] * 10

    #Creating a list of all the cells used in the program, with place holder properties
    for i in line_coordinates:
        #Here we use the formula cells[column][row][0= x co-ordinate || 1= y co-ordinate || 2= permanent value || 3= permanent cumulative weight || 4= working cumulative weight] for retrieving data
        if [i[0], i[1], "", "", ""] not in cells:
            cells.append([i[0], i[1], "", "", ""])
        if [i[2], i[3], "", "", ""] not in cells:
            cells.append([i[2], i[3], "", "", ""])

    #Loop through all the cells
    for i in range(len(cells)):
        #Assign the start cell with a working cumulative weight of 0
        if cells[i][:2] == start_cell:
            cells[i][4] = 0
        #Retrieve the coordinates of the end cell
        elif cells[i][:2] == end_cell:
            end_cell_pos = i

    while finish != True:
        finish = ""
        current_perm_value += 1

        #Finding which cell has the lowest working cumulative weight which hasn't been assigned a permanent value
        x = float('inf')
        current_cell = []
        for i in cells:
            if i[2] == "" and i[3] == "" and i[4] < x:
                x = i[4]
                current_cell = i

        #If there are no cells which are valid
        if current_cell == []:
            #The loop ends, but valid is set to False since there is no route from the start to the end cell
            finish = True
            valid = False

        #Otherwise if there are valid cells
        else:
            #The current cell is given a permanent value and permanent cumulative weight
            position = cells.index(current_cell)
            cells[position][2] = current_perm_value
            cells[position][3] = x
            #Update the current cell with new properties
            current_cell = cells[position]

            #Amy lines branching off the current cell are appended to the vertex options list
            vertex_options = []
            for i in line_coordinates:
                if i[:2] == current_cell[:2]:
                    vertex_options.append(i)
                elif i[2:4] == current_cell[:2]:
                    vertex_options.append(i)

            #Loops through vertex options
            for i in vertex_options:
                #Calculates the weight to that next cell by adding the cell's permanent weight to the next
                working_weight = i[4]+current_cell[3]
                #This works out the cell which isn't the cell we're currently looking at, out of the two in the line co-ordinates
                if i[:2] == current_cell[:2]:
                    working_cell = i[2:4]
                elif i[2:4] == current_cell[:2]:
                    working_cell = i[:2]

                #Finds the other location of the working cell in the cells list
                for i in cells:
                    if i[:2] == working_cell:
                        working_cell_position = cells.index(i)

                #If the cell doesn't have a working weight or the current working weight is less the working weight the next cell it has
                if cells[working_cell_position][4] == "" or working_weight < cells[working_cell_position][4]:
                    #The working weight of the next cell is replaced by the current working weight
                    cells[working_cell_position][4] = working_weight

            #If any cells do not have a permanent cumulative weight, then it doesn't finish
            for i in range(len(cells)):
                for j in cells[i]:
                    if j == "":
                        finish = False

            #Otherwise the loop is exited - All cells have a permanent cumulative weight ready to be solved
            if finish == "":
                finish = True

    #Here I run the second part of the function - Using the weights of each cell to find the final route
    final_route = find_route_function2(cells, line_coordinates, start_cell, end_cell_pos, valid)

    #Return the final route
    return final_route

#I split it up into two separate functions to make it easier to follow
def find_route_function2(cells, line_coordinates, start_cell, end_cell_pos, valid):
    #Here we create some place holder variables - This time we start with the end cell and work backwards
    current_cell = cells[end_cell_pos]
    final_route = []
    finish = False

    #If the initial route was valid - If it is invalid the final_route is left as [] so nothing is drawn for the solution
    if valid != False:
        while finish != True:
            line_options = []

            #Looks through the line coordinates to find which lines involve the current cell and appends any lines connect to the current cell to a list
            for i in line_coordinates:
                if i[:2] == current_cell[:2]:
                    line_options.append(i)
                elif i[2:4] == current_cell[:2]:
                    line_options.append(i)

            #Loop through line options list
            for i in line_options:
                #Loop through all the cells
                for j in cells:
                    #Finds the other coordinate of the line (the one which isn't the current cell) and finds the cell properties
                    if i[:2] != current_cell[:2] and i[:2] == j[:2]:
                        #If the current cell cell permanent weight, subtract the weight of the next cell is equal to the weight of the line
                        if current_cell[3] - j[3] == i[4]:
                            #Then this cell must be part of the final route - The current cell is now assigned to this cell and it repeats
                            final_route.append(i)
                            current_cell = j

                    #Same as before but if the first coordinate is the current cell
                    if i[2:4] != current_cell[:2] and i[2:4] == j[:2]:
                        if current_cell[3] - j[3] == i[4]:
                            final_route.append(i)
                            current_cell = j

            #Once the current cell is the start cell the loop ends
            if current_cell[:2] == start_cell:
                finish = True

            #Otherwise it continues unless there are no more line options - Then the final route is set to [] so nothing is drawn for the solution
            elif line_options == []:
                finish = True
                final_route = []

    #Divides the weight of all the values by 10 to avoid any errors when running the function twice and the weight being multiplied again and rounds them to two significant figures
    for i in range(len(line_coordinates)):
        weight = line_coordinates[i][4] / 10.
        weight = round(weight, 2-int(floor(log10(weight)))-1)
        line_coordinates[i][4] = weight

    #Return final route
    return final_route