from colorama import Fore, init  # for color print
import os
init(autoreset=True)

'''
check_win:
   Check if there is a winner. If yes, return the winner, else return 'n'.
   Use double-pointer to perform a run-and-catch style algorithm.

Params:
   mat: the input matrix
'''
def check_win(mat):
   for row in range(7):
      i = j = count = 0
      for i in range(7):
         while(i<7 and mat[row][i]==' '):
            i += 1
         j = i
         while(j<7 and mat[row][i]==mat[row][j]):
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
'''
def diag_check(mat):
   dp = [[[1,1] for col in range(7)] for row in range(7)]
   for r in range(7):
      for c in range(7):
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
'''
def print_board(mat):
   print()
   for r in range(6,-1,-1):
      print(end=' ')
      for c in range(7):
         if(mat[r][c]=='x'):
            print(Fore.BLUE + mat[r][c], end='  ')
         elif(mat[r][c]=='o'):
            print(Fore.RED + mat[r][c], end='  ')
         else:
            print(Fore.YELLOW + mat[r][c], end='  ')
      print()
   print(' 1  2  3  4  5  6  7\n')

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

board = [[' ' for col in range(7)] for row in range(7)]
height = {i:0 for i in range(7)}
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
      board[record[0]][record[1]] = ' '
      height[record[1]] -= 1
      os.system('clear')
      print_board(board)
      col = input("OK, you regretted. Enter the column number:  ")

   while(not col.isnumeric() or int(col)>7 or int(col)<1 or height[int(col)-1]>=7):
      if(not col.isnumeric() or int(col)>7 or int(col)<1):
         col = input("Please enter number 1 - 7:  ")
      elif(height[int(col)-1]>=7):
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

   winner = check_win(board)
   if(winner=='n'):
      winner = check_win(list(zip(*board)))
      if(winner=='n'):
         winner = diag_check(board)

   print_board(board)
   if(winner!='n'):
      x_wins() if winner=='x' else o_wins()
      break

   rd_num += 1
