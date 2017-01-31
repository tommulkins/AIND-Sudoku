# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: When a row or column has a naked twin we know that those "twins" values are locked.  We use constraint propagation to iterate over each of the naked twins boxes found after using eliminate() and only_choice() strategies until the puzzle can no longer be reduced using all those strategies.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: A box located in a main diagonal (A1->I9 || A9<-I1) has that diagonal as a peer in addition to the peers of a conventional Soduku.  Include the diagonal peer to isolate a unique value from 1 thru 9.  *Important Note: A box located within a main diagonal only has the diagonal, such as top left to bottom right, as its peer and not the opposite diagonal.  The lone exception is box E5 which is the center point of the Soduku.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.