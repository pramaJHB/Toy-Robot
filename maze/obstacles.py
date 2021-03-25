import random

obstacles_list = []


def get_obstacles():
    """
    Returns a list of the obstacles starting positions.
    """
    global obstacles_list

    obstacles_list = [(random.randint(-100, 96), random.randint(-200, 196)) \
        for i in range(random.randint(0, 10))]
    return obstacles_list


def is_position_blocked(x, y):
    """
    Checks if robot is going to land on an obstacle.
    Parameters:
            x, y : coordinates of robots destination
    Returns:
            True if obstacle
            False if no obstacle
    """
    global obstacles_list

    for coordinates in obstacles_list:
        obs_x = []
        obs_y = []
        for i in range(0, 5):
            obs_x.append(coordinates[0] + i)
            obs_y.append(coordinates[1] + i)
        if x in obs_x and y in obs_y:
            return True
    return False


def is_path_blocked(x1, y1, x2, y2):
    """
    Checks if there is an obstacle in robots path.
    Parameters:
            x1, y1 : starting coordinates of robot
            x2, y2 : ending coordinates of robot
    Returns:
            True if obstacle in path
            False if no obstacle in path
    """
    global obstacles_list
    
    for coordinates in obstacles_list:
        obs_x = []
        obs_y = []
        for i in range(0, 5):
            obs_x.append(coordinates[0] + i)
            obs_y.append(coordinates[1] + i)
        if x1 in obs_x and x2 in obs_x:
            for y in obs_y:
                if (y1 < y and y2 > y) or (y1 > y and y2 < y):
                    return True
        if y1 in obs_y and y2 in obs_y:
            for x in obs_x:
                if (x1 < x and x2 > x) or (x1 > x and x2 < x):
                    return True
    return False
