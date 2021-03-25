# Toy Robot

* You can run the program using the instructions in *To Run* below.
* You can test technical correctness by running the unit tests as in the section *To Test* below.

### To Run

* `python3 robot.py <text/turtle> <maze>`

* add 'text' as command line argument for text based Toy Robot, 
* add 'turtle' as command line argument for turtle graphics based Toy Robot,
* leaving blank will default to text.

* add name of maze from Toy-Robot/maze/ package to deploy specific maze, eg. 'crazy_maze',
* leaving blank will default to 'obstacles' maze.

* follow the input prompts to get the desired output

### To Test

* To run all the unittests: `python3 -m unittest tests/test_main.py`
* To run a specific step's unittest, e.g step *1*: `python3 -m unittest tests.test_main.MyTestCase.test_step1`
