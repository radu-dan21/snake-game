# Snake
Console-based version of the beloved [game of Snake](https://www.google.com/search?q=play+snake). 
Implemented using Python 3 and object-driven layered architecture.
The program works in the following way:
   - The game area is a `dimension x dimension` matrix of squares that contains the snake and a number of `apple_count` 
   apples. 
   - The snake starts with a head segment (`*`) and two body segments (`+`) and is placed in the middle of the board. 
   -  Each apple is represented using a dot (`.`). 
     Apples are placed randomly, so that two apples cannot be adjacent on the row or column.
     Apples cannot overlap the snake's body.
   `dimension` must be an odd natural number and `apple_count` must be a natural number >= 1.
   - Whenever the snake eats an apple, it gets one new body segment and another apple is added on the board.
   - If the snake bites itself or a wall, the game is over.
   - The values of `dimension` and `apple_count` are read from the settings.properties file.

The list of available commands is:
    
    move [n]
        This moves the snake `n` squares, in the direction it is currently facing. 
        `move` with no parameters moves the snake by `1` square.
        
    up | right | down | left
        This changes the snake's direction accordingly and DOES NOT move the snake at all.
        Trying to change the snake's direction by 180 degrees will result in an error message.
        Entering the direction the snake is currently heading for does nothing (no visible changes).
        
    exit
        This exits the program.
        
Run the application from the module start.py.
        
NOTE: The [texttable](https://github.com/foutaise/texttable) module must be installed in order for the program to work.
    