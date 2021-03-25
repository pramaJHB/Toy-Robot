import random

obstacles_list = []


def get_obstacles():
    """
    Returns a list of randomly generated obstacle coordinates.
    """
    global obstacles_list
    invalid_obs = [-5, 0]

    for i in range(random.randint(500, 500)):
        x = random.randrange(-100, 100, 5)
        y = random.randrange(-200, 200, 5)
        if x in invalid_obs and y in invalid_obs:
            continue
        else:
            obstacles_list.append((x, y))
    
    #obstacles_list = obstacles_list.sort()
    return obstacles_list.sort(key = lambda x: x[1], reverse=True)


def is_position_blocked(x, y):
    """
    Checks if there is an obstacle at the robots destination.
    Parameters:
            x, y : the coordinates of robots destination
    Returns:
            True if obstacle
            False if no obstacle
    """
    global obstacles_list

    for c in obstacles_list:
        if (x >= c[0] and x <= c[0] + 4) and (y >= c[1] and y <= c[1] + 4):
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
                if (y1 < y < y2) or (y1 > y > y2):
                    return True
        if y1 in obs_y and y2 in obs_y:
            for x in obs_x:
                if (x1 < x < x2) or (x1 > x > x2):
                    return True
    return False
