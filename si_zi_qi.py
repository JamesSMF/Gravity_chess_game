from colorama import Fore, init  # for color print
import os, sys
init(autoreset=True)

'''
check_win:
   Check if there is a winner. If yes, return the winner, else return 'n'.
   Use double-pointer to perform a run-and-catch style algorithm.

Params:
   mat: the input matrix
   size: board size
'''
def check_win(mat, size):
   for row in range(size):
      i = j = count = 0
      for i in range(size):
         while(i<size and mat[row][i]==' '):
            i += 1
         j = i
         while(j<size and mat[row][i]==mat[row][j]):
            j += 1
         count = max(count, j-i)
         if(count>=4):
            return mat[row][i]
         i = j

   return 'n'

'''
diag_check:
   Check if a player wins by scoring diagnally. Use dynamic programming.

Params:
   mat: the input matrix
   dp: the DP tensor
      for each entry (a,b), a stands for the longest left diagnal, and b
      stands for the longest right diagnal.
   size: board size
'''
def diag_check(mat, size):
   dp = [[[1,1] for col in range(size)] for row in range(size)]
   for r in range(size):
      for c in range(size):
         if(r==0 or mat[r][c]==' '):
            continue
         if(c==0):
            if(mat[r][c]==mat[r-1][c+1]):
               dp[r][c][1] = dp[r-1][c+1][1] + 1
         elif(c==6):
            if(mat[r][c]==mat[r-1][c-1]):
               dp[r][c][0] = dp[r-1][c-1][0] + 1
         else:
            if(mat[r][c]==mat[r-1][c-1]):
               dp[r][c][0] = dp[r-1][c-1][0] + 1
            if(mat[r][c]==mat[r-1][c+1]):
               dp[r][c][1] = dp[r-1][c+1][1] + 1

         if(max(dp[r][c])>=4):
            return mat[r][c]

   return 'n'


'''
print_board:
   Print out the chessboard

Params:
   mat: the chessboard
   size: board size
'''
def print_board(mat, size):
   print()
   for r in range(size-1,-1,-1):
      print(end=' ')
      for c in range(size):
         if(mat[r][c]=='x'):
            print(Fore.BLUE + mat[r][c], end='  ')
         elif(mat[r][c]=='o'):
            print(Fore.RED + mat[r][c], end='  ')
         else:
            print(Fore.YELLOW + mat[r][c], end='  ')
      print()

   print(end=' ')
   for i in range(size):
      print(i+1, end='  ')
   print()

'''
grid_board:
   print out the chessboard with grids

Params:
   mat: the chessboard
   size: board size
'''
def grid_board(mat, size):
   for i in range(size):
      print('----', end='')
   print()
   for r in range(size-1,-1,-1):
      print(end='| ')
      for c in range(size):
         if(mat[r][c]=='x'):
            print(Fore.BLUE + mat[r][c], end=' | ')
         elif(mat[r][c]=='o'):
            print(Fore.RED + mat[r][c], end=' | ')
         else:
            print(Fore.YELLOW + mat[r][c], end=' | ')
      print()
      for i in range(size):
         print('----', end='')
      print()

   print(end='  ')
   for i in range(size):
      print(i+1, end='   ')
   print()

def x_wins():
   print()
   print('   XXX   XXX    WWW     WW      WWW  IIIIII  NNN     NN   SSSSS')
   print('    XXX XXX     WWW    WW WW    WWW    II    NN NN   NN  SS')
   print('      XXX        WWW  WW   WW  WWW     II    NN  NN  NN   SSSSSS')
   print('    XXX XXX      WWW WW     WW WWW     II    NN   NN NN        SS')
   print('   XXX   XXX      WWW        WWW     IIIIII  NN     NNN   SSSSSS')
   print()

def o_wins():
   print()
   print('     OOO        WWW     WW      WWW  IIIIII  NNN     NN   SSSSS')
   print('   OO   OO      WWW    WW WW    WWW    II    NN NN   NN  SS')
   print('  OOO   OOO      WWW  WW   WW  WWW     II    NN  NN  NN   SSSSSS')
   print('   OO   OO       WWW WW     WW WWW     II    NN   NN NN        SS')
   print('     OOO          WWW        WWW     IIIIII  NN     NNN   SSSSSS')
   print()

size = 7
grid = False
if('-s' in sys.argv):
   size = int(sys.argv[sys.argv.index('-s') + 1])
   assert(str(size).isdigit())
   assert(size>3)
if('-grid' in sys.argv or '--grid' in sys.argv):
   grid = True

board = [[' ' for col in range(size)] for row in range(size)]
height = {i:0 for i in range(size)}
rd = 1
rd_num = 0

while(True):
   if(rd_num==48):
      print('Checkmate!')
      break

   if(rd==1):
      print('Round for x')
   else:
      print('Round for o')

   col = input("Select a column to place a chess: (enter number) ")

   # If that motherfucker regrets
   if(rd_num!=0 and col=='regret'):
      rd = -rd
      rd_num -= 1
      board[record[0]][record[1]] = ' '
      height[record[1]] -= 1
      os.system('clear')
      if(grid):
         grid_board(board, size)
      elif(len(sys.argv)==1):
         print_board(board, size)
      col = input("OK, you regretted. Enter the column number:  ")

   while(not col.isnumeric() or int(col)>size or int(col)<1 or height[int(col)-1]>=size):
      if(not col.isnumeric() or int(col)>size or int(col)<1):
         col = input("Please enter number 1 -"+str(size)+':')
      elif(height[int(col)-1]>=size):
         col = input("This column is full. Choose another column: ")

   col = int(col) - 1
   os.system('clear')

   if(rd==1):
      board[height[col]][col] = 'x'
   else:
      board[height[col]][col] = 'o'

   record = [height[col], col]

   rd = -rd
   height[col] += 1

   winner = check_win(board, size)
   if(winner=='n'):
      winner = check_win(list(zip(*board)), size)
      if(winner=='n'):
         winner = diag_check(board, size)

   if(grid):
      grid_board(board, size)
   else:
      print_board(board, size)
   if(winner!='n'):
      x_wins() if winner=='x' else o_wins()
      break

   rd_num += 1
