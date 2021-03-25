import sys
import world.text.world as world
try:
    if sys.argv[1] == 'text':
        import world.text.world as world
    elif sys.argv[1] == 'turtle':
        import world.turtle.world as world
except:
    import world.text.world as world

#list of valid command names
valid_commands = ['off', 'help', 'replay', 'mazerun', 'forward', 'back',\
     'right', 'left', 'sprint']
move_commands = valid_commands[4:]
mazerun_commands = ['top', 'bottom', 'left', 'right']
#command history
history = []


def get_robot_name():
    """
    Asks the user to name the robot
    return: name of robot as string
    """
    name = input("What do you want to name your robot? ")
    while len(name) == 0:
        name = input("What do you want to name your robot? ")
    return name


def get_command(robot_name):
    """
    Asks the user for a command, and validate it as well
    return: a valid command as string
    """
    prompt = ''+robot_name+': What must I do next? '
    command = input(prompt)
    while len(command) == 0 or not valid_command(command):
        output(robot_name, "Sorry, I did not understand '"+command+"'.")
        command = input(prompt)
    return command.lower()


def split_command_input(command):
    """
    Splits the string at the first space character, to get the actual command,
        as well as the argument(s) for the command
    return: (command, argument)
    """
    args = command.split(' ', 1)
    if len(args) > 1:
        return args[0], args[1]
    return args[0], ''


def is_int(value):
    """
    Tests if the string value is an int or not
    paramameters: value: A string value to test
    return: A boolean indicating if the value is an int or not
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def valid_command(command):
    """
    Checks if the command is valid or not and if the arguments are valid or not
    parameters: command: A string to test
    return: A boolean indicating if the robot can understand the command or not
    """
    (command_name, arg1) = split_command_input(command)
    if command_name.lower() == 'mazerun':
        if len(arg1.strip()) == 0 or arg1.strip() in mazerun_commands:
            return True
    if command_name.lower() == 'replay':
        if len(arg1.strip()) == 0:
            return True
        elif (arg1.lower().find('silent') > -1 or \
            arg1.lower().find('reversed') > -1) and \
            len(arg1.lower().replace('silent', '')\
                .replace('reversed','').strip()) == 0:
            return True
        else:
            rep_range = arg1.replace('silent', '').replace('reversed','')
            if is_int(rep_range):
                return True
            else:
                rep_range = rep_range.split('-')
                return is_int(rep_range[0]) and is_int(rep_range[1]) and \
                    len(rep_range) == 2
    else:
        return command_name.lower() in valid_commands and \
            (len(arg1) == 0 or is_int(arg1))


def output(name, message):
    """
    Prints out a message to the standard output
    paramaters: name: Name of robot as string
                message: The string to be printed out
    """
    print(''+name+": "+message)


def do_help():
    """
    Provides help information to the user
    return: (True, Help text)
    """
    return True, """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
REPLAY - replays all movement commands from history [FORWARD, BACK, RIGHT, LEFT, SPRINT]
MAZERUN - automatically traverse the maze to desired edge, e.g. 'MAZERUN LEFT'
"""


def do_sprint(robot_name, steps):
    """
    Sprints the robot
    i.e. go forward steps + (steps-1) + (steps-2) + .. + 1 number of steps, in iterations
    parameters: robot_name: Name of robot as string
                steps: Number of steps from arguments as int
    return: (True, forward output)
    """
    if steps == 1:
        return world.do_forward(robot_name, 1)
    else:
        (do_next, command_output) = world.do_forward(robot_name, steps)
        print(command_output)
        return do_sprint(robot_name, steps - 1)


def get_commands_history(reverse, relativeStart, relativeEnd):
    """
    Retrieve the commands from history list,
    already breaking them up into (command_name, arguments) tuples
    :param reverse: if True, then reverse the list
    :param relativeStart: the start index relative to the end position of command, 
        e.g. -5 means from index len(commands)-5; None means from beginning
    :param relativeEnd: the start index relative to the end position of command, 
        e.g. -1 means from index len(commands)-1; None means to the end
    :return: return list of (command_name, arguments) tuples
    """
    commands_to_replay = [(name, args) for (name, args) in \
        list(map(lambda command: split_command_input(command), history)) \
            if name in move_commands]
    if reverse:
        commands_to_replay.reverse()
    range_start = len(commands_to_replay) + relativeStart if \
        (relativeStart is not None and \
            (len(commands_to_replay) + relativeStart) >= 0) else 0
    range_end = len(commands_to_replay) + relativeEnd if  \
        (relativeEnd is not None and \
            (len(commands_to_replay) + relativeEnd) >= 0 and \
                relativeEnd > relativeStart) \
                else len(commands_to_replay)
    return commands_to_replay[range_start:range_end]


def do_replay(robot_name, arguments):
    """
    Replays historic commands
    paramameters: robot_name: Name of robot
                  arguments:  a string containing arguments for the replay command
    return: True, output string
    """
    silent = arguments.lower().find('silent') > -1
    reverse = arguments.lower().find('reversed') > -1
    range_args = arguments.lower().replace('silent', '').replace('reversed', '')
    range_start = None
    range_end = None

    if len(range_args.strip()) > 0:
        if is_int(range_args):
            range_start = -int(range_args)
        else:
            range_args = range_args.split('-')
            range_start = -int(range_args[0])
            range_end = -int(range_args[1])

    commands_to_replay = get_commands_history(reverse, range_start, range_end)

    for (command_name, command_arg) in commands_to_replay:
        (do_next, command_output) = call_command(command_name, command_arg, robot_name)
        if not silent:
            print(command_output)
            world.show_position(robot_name)
    return True, ' > '+robot_name+' replayed ' + str(len(commands_to_replay)) + \
        ' commands' + (' in reverse' if reverse else '') + \
            (' silently.' if silent else '.')


def call_command(command_name, command_arg, robot_name):
    """
    Calls the relevant function based on the command_name
    parameters: command_name: The command as string
                command_arg: the command arguments as string
                robot_name: Name of robot as string
    return: (False, None) 
    """
    if command_name == 'help':
        return do_help()
    elif command_name == 'forward':
        return world.do_forward(robot_name, int(command_arg))
    elif command_name == 'back':
        return world.do_back(robot_name, int(command_arg))
    elif command_name == 'right':
        return world.do_right_turn(robot_name)
    elif command_name == 'left':
        return world.do_left_turn(robot_name)
    elif command_name == 'sprint':
        return do_sprint(robot_name, int(command_arg))
    elif command_name == 'replay':
        return do_replay(robot_name, command_arg)
    elif command_name == 'mazerun':
        return world.do_mazerun(robot_name, command_arg)
    return False, None


def handle_command(robot_name, command):
    """
    Handles a command by asking different functions to handle each command.
    :param robot_name: the name given to robot
    :param command: the command entered by user
    :return: `True` if the robot must continue after the command, 
    or else `False` if robot must shutdown
    """
    (command_name, arg) = split_command_input(command)
    if command_name == 'off':
        world.reset_globals()
        return False
    else:
        (do_next, command_output) = call_command(command_name, arg, robot_name)
    print(command_output)
    world.show_position(robot_name)
    add_to_history(command)
    return do_next


def add_to_history(command):
    """
    Adds the command to the history list of commands
    parameters: command: command as string
    """
    history.append(command)


def robot_start():
    """
    This is the entry point for starting my robot
    """
    robot_name = get_robot_name()
    output(robot_name, "Hello kiddo!")
    world.show_obstacles(robot_name)
    world.show_robot(robot_name)

    command = get_command(robot_name)
    while handle_command(robot_name, command):
        command = get_command(robot_name)
    history.clear()
    output(robot_name, "Shutting down..")


if __name__ == "__main__":
    robot_start()
