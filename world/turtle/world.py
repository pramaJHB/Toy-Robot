import turtle
import import_helper
import robot
obstacles = import_helper.dynamic_import()
# variables tracking position and direction
position_x = 0
position_y = 0
directions = ['forward', 'right', 'back', 'left']
current_direction_index = 0
# area limit vars
min_y, max_y = -200, 200
min_x, max_x = -100, 100
# robot vars
rob = turtle.Turtle()
rob.hideturtle()
rob.seth(90)


def show_robot(robot_name):
    """
    Initialiases the robot on turtle screen.
    parameters: robot_name: Name of robot as string
    """
    global rob, position_x, position_y
    robot_shape = ((-4, -4), (-4, -2), (-5, -2), (-5, 2), (-4, 2), (-4, 4),\
        (-3, 4), (-3, 5), (-1, 5), (-1, 4), (1, 4), (1, 5), (3, 5), (3, 4),\
            (4, 4), (4, 2), (5, 2), (5, -2), (4, -2), (4, -4))
    turtle.register_shape('robot', robot_shape)
    rob.pen(fillcolor=None, speed=1)
    rob.up()
    rob.shape('robot')
    rob.color('black', 'dim gray')
    rob.shapesize(1, 1, 0.5)
    rob.goto(position_x, position_y)
    rob.showturtle()
    rob.speed(10)


def show_obstacles(robot_name):
    """
    Draws the obstacles on turtle screen.
    parameters: robot_name: Name of robot as string
    """
    turtle.title('Toy Robot - ' + robot_name)
    print('{}: Loaded {}.'.format(robot_name, \
        import_helper.name.replace('maze.', '').replace('_', ' ')))
    obstacles_list = obstacles.get_obstacles()
    maze_block = ((-2,-2), (2, -2), (2, 2), (-2, 2))
    turtle.register_shape('block', maze_block)
    o = turtle.Turtle()
    o.shape('block')
    o.shapesize(2.5, 2.5, 1)
    o.hideturtle()
    o.pen(pencolor='gainsboro', fillcolor='peru', pensize=1, speed=0)
    o.up()
    turtle.tracer(1, 0)
    for coordinates in obstacles_list:
        o.goto(coordinates[0] + 2, coordinates[1] + 2)
        o.stamp()
    turtle.update()
    turtle.tracer(1, 5)


def show_position(robot_name):
    """
    Moves the robot to its new position.
    parameters: robot_name: name of robot as string
    """
    global rob, position_x, position_y
    rob.goto(position_x, position_y)


def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    """
    if obstacles.is_position_blocked(new_x, new_y) or \
        obstacles.is_path_blocked(position_x, position_y, new_x, new_y):
        return False
    return min_x <= new_x <= max_x and min_y <= new_y <= max_y


def update_position(steps):
    """
    Update the current x and y positions given the current direction, 
    and specific number of steps
    :param steps: number of steps int
    :return: True if the position is allowed, 'blocked' if obstacle in the way, else False
    """
    global position_x, position_y, current_direction_index, directions
    new_x = position_x
    new_y = position_y

    if directions[current_direction_index] == 'forward':
        new_y = new_y + steps
    elif directions[current_direction_index] == 'right':
        new_x = new_x + steps
    elif directions[current_direction_index] == 'back':
        new_y = new_y - steps
    elif directions[current_direction_index] == 'left':
        new_x = new_x - steps

    if obstacles.is_position_blocked(new_x, new_y) or \
        obstacles.is_path_blocked(position_x, position_y, new_x, new_y):
        return 'blocked'

    if is_position_allowed(new_x, new_y):
        position_x = new_x
        position_y = new_y
        return True
    return False


def do_forward(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name: name of robot
    :param steps: number of steps int
    :return: (True, forward output text)
    """
    if update_position(steps) == True:
        return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.'
    elif update_position(steps) == 'blocked':
        return True, ''+robot_name+': Sorry, there is an obstacle in the way.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_back(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name: name of robot
    :param steps: number of steps int
    :return: (True, forward output text)
    """
    if update_position(-steps) == True:
        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.'
    elif update_position(-steps) == 'blocked':
        return True, ''+robot_name+': Sorry, there is an obstacle in the way.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_right_turn(robot_name):
    """
    Do a 90 degree turn to the right
    :param robot_name: name of robot
    :return: (True, right turn output text)
    """
    global current_direction_index, rob

    rob.right(90)
    current_direction_index += 1
    if current_direction_index > 3:
        current_direction_index = 0
    return True, ' > '+robot_name+' turned right.'


def do_left_turn(robot_name):
    """
    Do a 90 degree turn to the left
    :param robot_name: name of robot
    :return: (True, left turn output text)
    """
    global current_direction_index, rob

    rob.left(90)
    current_direction_index -= 1
    if current_direction_index < 0:
        current_direction_index = 3
    return True, ' > '+robot_name+' turned left.'


def do_mazerun(robot_name, edge):
    """
    Automatically traverse the maze.
    Parameters:
            robot_name: Name of robot
            egde: Which edge of the map the robot must go to
    Returns: True, mazerun output text
    """
    global position_x, position_y
    print('> ' + robot_name + ' starting maze run..')
    if edge == '' or edge == 'top':
        edge = 'top'
    elif edge == 'left':
        robot.handle_command(robot_name, 'left')
    elif edge == 'right':
        robot.handle_command(robot_name, 'right')
    elif edge == 'bottom':
        robot.handle_command(robot_name, 'left')
        robot.handle_command(robot_name, 'left')
    
    while not reached_edge(edge):
        if current_direction_index == 0:
            if is_position_allowed(position_x, position_y + 4) and \
               is_position_allowed(position_x - 4, position_y) and \
               is_position_allowed(position_x + 4, position_y):
                robot.handle_command(robot_name, 'forward 4')
            elif is_position_allowed(position_x - 4, position_y):
                robot.handle_command(robot_name, 'left')
                robot.handle_command(robot_name, 'forward 4')
            elif is_position_allowed(position_x, position_y + 4):
                robot.handle_command(robot_name, 'forward 4')
            else:
                robot.handle_command(robot_name, 'right')
        
        elif current_direction_index == 1:
            if is_position_allowed(position_x + 4, position_y) and \
               is_position_allowed(position_x, position_y + 4) and \
               is_position_allowed(position_x, position_y - 4):
                robot.handle_command(robot_name, 'forward 4')
            elif is_position_allowed(position_x, position_y + 4):
                robot.handle_command(robot_name, 'left')
                robot.handle_command(robot_name, 'forward 4')
            elif is_position_allowed(position_x + 4, position_y):
                robot.handle_command(robot_name, 'forward 4')
            else:
                robot.handle_command(robot_name, 'right')
        
        elif current_direction_index == 2:
            if is_position_allowed(position_x, position_y - 4) and \
               is_position_allowed(position_x + 4, position_y) and \
               is_position_allowed(position_x - 4, position_y):
                robot.handle_command(robot_name, 'forward 4')
            elif is_position_allowed(position_x + 4, position_y):
                robot.handle_command(robot_name, 'left')
                robot.handle_command(robot_name, 'forward 4')
            elif is_position_allowed(position_x, position_y - 4):
                robot.handle_command(robot_name, 'forward 4')
            else:
                robot.handle_command(robot_name, 'right')

        elif current_direction_index == 3:
            if is_position_allowed(position_x - 4, position_y) and \
               is_position_allowed(position_x, position_y - 4) and \
               is_position_allowed(position_x, position_y + 4):
                robot.handle_command(robot_name, 'forward 4')
            elif is_position_allowed(position_x, position_y - 4):
                robot.handle_command(robot_name, 'left')
                robot.handle_command(robot_name, 'forward 4')
            elif is_position_allowed(position_x - 4, position_y):
                robot.handle_command(robot_name, 'forward 4')
            else:
                robot.handle_command(robot_name, 'right')

    return True, robot_name + ': I am at the '+ edge + ' edge.'


def reached_edge(edge):
    """
    Checks if the robot has reached the relevant edge of the map
    parameters: edge: The edge to which needs to be checked as string
    return: True if the robot has reached the relevant edge
            False if robot has not reached relevant edge
    """
    global position_x, position_y, min_x, min_y, max_x, max_y

    if (edge == 'top' or edge == '') and (position_y == max_y):
        return True
    elif edge == 'bottom' and (position_y == min_y):
        return True
    elif edge == 'right' and (position_x == max_x):
        return True
    elif edge == 'left' and (position_x == min_x):
        return True
    return False


def reset_globals():
    """
    Resets the global variables to default values
    """
    global position_x, position_y, current_direction_index
    position_x = 0
    position_y = 0
    current_direction_index = 0