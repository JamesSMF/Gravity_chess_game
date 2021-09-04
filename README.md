# Gravity Chess Game

重力四子棋。工作摸鱼写的，打发时间好伴侣。不多说了，老板来了。

## Introduction
This is a novel chess game coded up by James Li. I also built a simple AI agent using Q-learning algorithm. This algorithm is coded up from scratch using numpy only. Have fun with this project :)

![Playing with a well-trained AI agent](sample_play.gif)

## Rules
In a traditional tic-tac-toe game, two players put `x` or `o` on the chessboard by turns. If one of the players got 3 chesses of the same kind on the same row, or the same column, or the same diagnal, this player wins the game.

Gravity chess game is similar, except that you have to got 4 chesses of the same kind on the same row, or the same column, or the same diagnal. However, someone sets the chessboard up, and you have to play the "tic-tac-toe-plus-plus" vertically. In other words, you cannot choose which row to place a chess, and you one have controls on column choices. Whenever you put a chess at a certain column, the chess falls down to the bottom.

## Dependencies
+ numpy
+ colorama
+ pickle

## Running the program
+ Run `python3 si_zi_qi.py` for default game setting (7x7 chessboard, player v.s. player)
+ Add `-grid` for grid style chessboard
+ Add `-size <size>` to custom chessboard size (maximum 19x19)
+ Add `-rl` for player v.s. computer mode (note that size is fixed to 7x7 in this mode, and the original model is untrained, which means the AI agent is stupid at this stage. You need to train it first.)
+ Add `-rl -train` to train the model (default 500000 epochs)
