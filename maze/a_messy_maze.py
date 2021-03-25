import random

obstacles_list = []

def get_obstacles():
    """Function to return list of obstacle starting point"""
    global obstacles_list
    maze_additions = []
    type_list = ['top','bottom']
    direction_list = ['right','left']
    
    number_of_obstacles = 280
    for number in range(number_of_obstacles):
        x_cord, y_cord = random.randrange(-95, 96, 10), random.randrange(-195, 196, 10)
        if (x_cord in range(-5,5) or y_cord in range(-5,5)):
            pass
        else:  
            obstacles_list.append((x_cord,y_cord))

    for obstacle in obstacles_list:
        typa = random.choice(type_list)
        direct = random.choice(direction_list)
        if direct == 'right':
            maze_additions.append((obstacle[0] + 4, obstacle[1]))  
            maze_additions.append((obstacle[0] + 8, obstacle[1]))
        else:
            maze_additions.append((obstacle[0] - 4, obstacle[1]))  
            maze_additions.append((obstacle[0] - 8, obstacle[1]))
        if typa == 'top':
            maze_additions.append((obstacle[0], obstacle[1]+4))  
            maze_additions.append((obstacle[0], obstacle[1]+8))
        else:
            maze_additions.append((obstacle[0], obstacle[1]-4))  
            maze_additions.append((obstacle[0], obstacle[1]-8))

    for item in maze_additions:
        obstacles_list.append(item)

    return obstacles_list

def is_position_blocked(x, y):
    """Function to return true if position is blocked"""

    global obstacles_list
    counter = 0
    return_statement = False
    while counter < len(obstacles_list):
        item_f = obstacles_list[counter]
        if x in range(item_f[0], item_f[0]+5) and y in range(item_f[1],item_f[1]+5):
            return_statement = True
            break
        else:
            counter += 1      
    return return_statement

def is_path_blocked(x1,y1, x2, y2):
    """Function to check whether the path is blocked"""
    global obstacles_list

    return_statement = False
    obstacles = obstacles_list
    for obstacle in obstacles:
	    if y1 == y2:
		    for number in range(x1,x2+1):
			    if (number == obstacle[0] or number == obstacle[0]+4) and y1 in range(obstacle[1],obstacle[1]+4):
				    return_statement = True
	    elif x1 == x2:
		    for number in range(y1,y2+1):
			    if (number == obstacle[1] or number == obstacle[1]+4) and x1 in range(obstacle[0],obstacle[0]+4):
				    return_statement = True
    return return_statement