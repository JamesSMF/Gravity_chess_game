from colorama import Fore, init  # for color print
import os, sys, pickle, random
from time import sleep
import os.path
import numpy as np
import math
import matplotlib.pyplot as plt

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
      while(i<size):
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
         elif(c==size-1):
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
      if(i<9):
         print(i+1, end='  ')
      elif(i>=9):
         print(i+1, end=' ')
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
      if(i<9):
         print(i+1, end='   ')
      elif(i>=9):
         print(i+1, end='  ')
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

'''
This function is irrelevant to the game itself. It is used to generate
a state status for reinforcement learning.
'''
def encode(board, height):
   out_code = 0
   for col in range(7):
      if(height[col]==0):     # no chess on this col
         out_code += 0
         out_code *= 255
         continue
      base = 2**height[col]-1
      code = list()
      #  print(height[col]+1)
      for row in range(height[col]):
         code.append('1') if board[row][col] == 'x' else code.append('0')

      bin_str = ''.join(code[::-1])
      dec = int(bin_str, base=10)
      out_code += (dec + base)
      out_code *= 255
   return out_code

def decode(code):
	height_ls = list()
	for i in range(7):
		height_ls.append(code % 255)
		code //= 255

	return height_ls[::-1]

def code_to_board(code):
   board = [[' ' for col in range(7)] for row in range(7)]
   col_count = 0
   for col_code in code:
      base = int(math.log(col_code, 2)) if col_code!=0 else 0
      col_code -= 2**base
      bin_str = bin(col_code)[2:]
      while(len(bin_str)<base):
         bin_str = '0' + bin_str

      # 我是傻逼，前面翻转了，现在又要翻转回来
      bin_str = bin_str[::-1]

      for r in range(base):
         board[r][col_count] = bin_str[r]

      col_count += 1

   return board

'''
This function checks if the opponent is about to win the game.
If so, it returns the corresponding column number, otherwise -1.
'''
def check_opp_win(board, height, rd):
   opp_col = -1
   for c in range(7):
      if(height[c]>=7 or height[c]<3):
         continue

      three = True
      opp_three = True
      for chess in range(height[c]-1, height[c]-4, -1):
         if(board[chess][c]!=rd):
            three = False
         else:
            opp_three = False

      if(three):  # current player is about to win
         return [c, 1]

      if(opp_three):    # opponent about to win
         opp_col = c

   if(opp_col!=-1):
      return [opp_col, -1]
   else:
      return [-1, 0]

def plot_rd_num(rd_num_ls):
   plt.plot(range(1,500001), rd_num_ls)
   plt.xlabel('epochs')
   plt.ylabel('rounds')
   plt.show()

def iterate_helper(board, height, rd, consec, rd_same):
   for row in range(7):
      i = j = count = 0
      while(i<7):
         while(i<7 and board[row][i]==' '):
            i += 1
         j = i
         while(j<7 and board[row][i]==board[row][j]):
            j += 1

         if(j<7 and board[row][i] != rd):
            i = j
            continue

         # two or three chesses in a row
         if(j - i == consec):
            if(i > 0 and height[i-1]==row):
               #  print("Block 1")
               return [i-1, 1]
            elif(j < 7 and height[j]==row):
               #  print("Block 2")
               return [j, 1]

         i = j

   if(not rd_same and consec==3):
      for row in range(7):
         i = j = count = 0
         while(i<7):
            while(i<7 and board[row][i]==' '):
               i += 1
            j = i
            while(j<7 and board[row][i]==board[row][j]):
               j += 1

            if(j<7 and board[row][i] != rd):
               i = j
               continue

            # two or three chesses in a row
            if(j - i == consec):
               if(i > 0 and height[i-1]==row-1):
                  #  print("Block 3")
                  return [i-1, 2]
               elif(j < 7 and height[j]==row-1):
                  #  print("Block 4")
                  return [j, 2]

            i = j

   return [-1, 0]

def check_horizontal(board, height, rd):
   # 优先级排行：
   # 自己的3连
   # 对手的3连
   # 对手的2连
   # 自己的2连

   col, sign = iterate_helper(board, height, rd, 3, True)
   if(sign!=0):
      #  print("self 3")
      return [col, sign]

   if(rd=='x'):
      col,sign = iterate_helper(board, height, 'o', 3, False)
   else:
      col,sign = iterate_helper(board, height, 'x', 3, False)
   if(sign!=0):
      #  print("opp 3")
      return [col, sign]

   if(rd=='x'):
      col,sign = iterate_helper(board, height, 'o', 2, False)
   else:
      col,sign = iterate_helper(board, height, 'x', 2, False)
   if(sign!=0):
      #  print("opp 2")
      return [col, sign]

   col, sign = iterate_helper(board, height, rd, 2, True)
   if(sign!=0):
      #  print("self 2")
      return [col, sign]

   return [-1, 0]


def calc_reward(code, flag):
   board = code_to_board(decode(code))
   winner = check_win(board, 7)
   if(winner=='n'):
      winner = check_win(list(zip(*board)), 7)
      if(winner=='n'):
         winner = diag_check(board, 7)

   reward = 0

   if(flag==1):
      if(winner=='x'):
         reward = 100
      elif(winner=='o'):
         reward = -50
   else:
      if(winner=='o'):
         reward = 100
      elif(winner=='x'):
         reward = -50

   if(winner=='n'):
      reward = -1

   return reward

def normalize(ls):
   floor = min(ls)
   if(floor<0):
      ls = list(map(lambda x: x-floor, ls))

   ls = list(map(lambda x: x/sum(ls), ls))
   return ls

def playerVScomputer(q_table):
   board = [[' ' for col in range(7)] for row in range(7)]
   height = {i:0 for i in range(7)}
   rd = 1
   rd_num = 0

   last_move = list()

   while(True):
      if(rd_num==48):
         print('Checkmate!')
         break

      if(rd==1):
         print('Round for x')
         current_code = encode(board, height)

         if(current_code not in q_table):
            q_table[current_code] = np.random.uniform(size=7)
            print("Not in q_table")
         else:
            print("In q_table")

         #  print(q_table[current_code])
         # Check if current player is about to win or its opponent is about to win
         col, sign = check_opp_win(board, height, 'x')
         if(sign!=0):
            for i in range(7):
               q_table[current_code][i] = -100000
            q_table[current_code][col] += 200000

         col, sign = check_horizontal(board, height, 'x')
         if(sign==1):
            q_table[current_code][col] += 5
         elif(sign==2):
            q_table[current_code][col] -= 2

         next_move = np.argmax(q_table[current_code])
         prob_ls = normalize(q_table[current_code])
         print('preference of each column:')
         for i in range(7):
            print('column ' + str(i+1) + ': ' + str(round(prob_ls[i], 4)))

         k = 6
         while(height[next_move]>=7):
            next_move = np.where(np.argsort(q_table[current_code])==k)[0][0]
            k -= 1

         last_move.append([current_code, next_move])   # save as historical move
         if(len(last_move)>6):
            last_move.pop(0)

         board[height[next_move]][next_move] = 'x'
         height[next_move] += 1

      else:
         # Player's Round

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

         record = [height[col], col]
         board[height[col]][col] = 'o'
         height[col] += 1

      rd = -rd

      winner = check_win(board, 7)
      if(winner=='n'):
         winner = check_win(list(zip(*board)), 7)
         if(winner=='n'):
            winner = diag_check(board, 7)

      if(grid):
         grid_board(board, 7)
      else:
         print_board(board, 7)

      # Hyper-params
      alpha = 0.2

      if(winner!='n'):
         if(winner=='x'):
            for index in range(len(last_move)):
               old_value = q_table[last_move[index][0]][last_move[index][1]]
               new_value = (1 - alpha) * old_value + ((index+1)/2) * alpha * 60
               q_table[last_move[index][0]][last_move[index][1]] = new_value
            x_wins()
         else:
            for index in range(len(last_move)):
               old_value = q_table[last_move[index][0]][last_move[index][1]]
               new_value = (1 - alpha) * old_value - ((index+1)/2) * alpha * 30
               q_table[last_move[index][0]][last_move[index][1]] = new_value
            q_table[current_code][col] += 2
            o_wins()
         break

      rd_num += 1

   return q_table

def finetune(q_table, opp_table, board, height):

   loser_count = 0
   loser = False

   for i in range(50000):
      print('epoch', i+1, '     Q table size:', len(q_table))
      board = [[' ' for col in range(7)] for row in range(7)]
      height = {i:0 for i in range(7)}
      rd = 1
      rd_num = 0

      last_move = list()
      if(not loser):
         last_seq = list()

      while(True):
         if(rd_num==48):
            break

         if(rd==1):
            current_code = encode(board, height)

            if(current_code not in q_table):
               q_table[current_code] = np.random.uniform(size=7)

            #  print(q_table[current_code])
            # Check if current player is about to win or its opponent is about to win
            col, sign = check_opp_win(board, height, 'x')
            if(sign!=0):
               for i in range(7):
                  q_table[current_code][i] = -100000
               q_table[current_code][col] += 200000

            col, sign = check_horizontal(board, height, 'x')
            if(sign==1):
               q_table[current_code][col] += 5
            elif(sign==2):
               q_table[current_code][col] -= 2

            next_move = np.argmax(q_table[current_code])

            k = 6
            while(height[next_move]>=7):
               next_move = np.where(np.argsort(q_table[current_code])==k)[0][0]
               k -= 1

            last_move.append([current_code, next_move])   # save as historical move
            if(len(last_move)>6):
               last_move.pop(0)

            board[height[next_move]][next_move] = 'x'
            height[next_move] += 1

         else:
            if(loser and rd_num//2 < len(last_seq)):
               next_move = last_seq[rd_num//2]
               while(height[next_move]>=7):
                  next_move = np.random.randint(0,7)

            else:
               next_move = np.random.randint(0,7)
               while(height[next_move]>=7):
                  next_move = np.random.randint(0,7)
               last_seq.append(next_move)


            board[height[next_move]][next_move] = 'o'
            height[next_move] += 1

         rd = -rd

         winner = check_win(board, 7)
         if(winner=='n'):
            winner = check_win(list(zip(*board)), 7)
            if(winner=='n'):
               winner = diag_check(board, 7)


         # Hyper-params
         alpha = 0.2

         if(winner!='n'):
            if(winner=='x'):
               for index in range(len(last_move)):
                  old_value = q_table[last_move[index][0]][last_move[index][1]]
                  new_value = (1 - alpha) * old_value + ((index+1)/2) * alpha * 60
                  q_table[last_move[index][0]][last_move[index][1]] = new_value
               loser = False
            else:
               for index in range(len(last_move)):
                  old_value = q_table[last_move[index][0]][last_move[index][1]]
                  new_value = (1 - alpha) * old_value - ((index+1)/2) * alpha * 30
                  q_table[last_move[index][0]][last_move[index][1]] = new_value
               q_table[current_code][next_move] += 2
               loser = True
               loser_count += 1
            break

         rd_num += 1

   print("Failed Games Count:", loser_count)
   return q_table


size = 7
grid = False

if('-grid' in sys.argv or '--grid' in sys.argv):
   grid = True

# Player v.s. Computer
# Computer v.s. Computer
if('-rl' in sys.argv):
   # If the player decides to play with the computer
   # enter reinforcement learning mode.

   # Well if you do this, python will allocate more than 3 EiB memory space
   # Note: 1 EiB = 1024 PiB = 1024*1024 TiB = 1024^3 GiB
   # Only Google can afford this ...

   #  if(os.path.isfile('Q_table.npy')):
      #  q_table = np.load('Q_table.npy')
   #  else:
      #  q_table = np.random.uniform(size=(70110209207109375, 7))

   # Solution: By observing the state space, it is not hard to find that most
   # states are unreachable. Therefore, we only need to create q tables for those
   # confronted states.

   print('Loading AI data...')
   if(os.path.isfile('Q_table.pkl')):
      with open('Q_table.pkl', 'rb') as f:
         q_table = pickle.load(f)
   else:
      # initial state
      q_table = {0: np.random.uniform(size=7)}

   if(os.path.isfile('Opp_table.pkl')):
      with open('Opp_table.pkl', 'rb') as f:
         opp_table = pickle.load(f)
   else:
      opp_table = dict()

   # if the agent is in training mode
   if('-train' in sys.argv):
      x_win_c = 0
      o_win_c = 0
      epoch = 0

      rd_num_ls = list()
      for i in range(500000):
         epoch += 1

         print('epoch', epoch, '     Q table size:', len(q_table), '     Opp table size:', len(opp_table))
         board = [[' ' for col in range(7)] for row in range(7)]
         height = {i:0 for i in range(7)}
         rd = 1
         rd_num = 0
         last_move = list()
         opp_last_move = list()

         # Hyper-params
         alpha = 0.2
         gamma = 0.6
         ep = 0.1

         # One game (epoch)
         while(rd_num<48):

            if(rd==1):
               # Computer's Round
               #  print('Round for x')

               # get the code for the current board status
               current_code = encode(board, height)
               if(current_code not in q_table):
                  q_table[current_code] = np.random.uniform(size=7)

               # Check if current player is about to win or its opponent is about to win
               col, sign = check_opp_win(board, height, 'x')
               if(sign!=0):
                  q_table[current_code][col] += 100000

               col, sign = check_horizontal(board, height, 'x')
               if(sign==1):
                  q_table[current_code][col] += 5
               elif(sign==2):
                  q_table[current_code][col] -= 2

               next_move = 0
               new_code = 0
               #  sleep(0.1)

               epsilon = random.uniform(0, 1)

               # random move
               if(epsilon<ep):
                  next_move = random.randint(0, 6)

               # move according to the max q_table entry
               else:
                  next_move = np.argmax(q_table[current_code])

               last_move.append([current_code, next_move])   # save as historical move
               if(len(last_move)>4):
                  last_move.pop(0)

               #  print("Computer placed at column", next_move+1)

               k = 6
               while(height[next_move]>=7):
                  next_move = np.where(np.argsort(q_table[current_code])==k)[0][0]
                  k -= 1

               board[height[next_move]][next_move] = 'x'
               height[next_move] += 1
               new_code = encode(board, height)
               reward = calc_reward(new_code, 1)
               old_value = q_table[current_code][next_move]

               if(new_code not in opp_table):
                  opp_table[new_code] = np.random.uniform(size=7)

               # 这里应该是从对手视角最优决策
               opp_next_move = np.argmax(opp_table[new_code])
               k = 6
               while(height[opp_next_move]>=7):
                  opp_next_move = np.where(np.argsort(opp_table[new_code])==k)[0][0]
                  k -= 1

               board[height[opp_next_move]][opp_next_move] = 'o'
               height[opp_next_move] += 1

               # 假设对手走了最牛逼的一步，咱们应该怎么应对？
               # aka Mini Max
               new_code = encode(board, height)
               if(new_code not in q_table):
                  q_table[new_code] = np.random.uniform(size=7)

               # Check if current player is about to win or its opponent is about to win
               col, sign = check_opp_win(board, height, 'x')
               if(sign!=0):
                  q_table[new_code][col] += 10

               col, sign = check_horizontal(board, height, 'x')
               if(sign==1):
                  q_table[new_code][col] += 5
               elif(sign==2):
                  q_table[new_code][col] -= 2

               next_max = np.max(q_table[new_code])

               # 刚刚只是假想，现在还原棋盘
               height[opp_next_move] -= 1
               board[height[opp_next_move]][opp_next_move] = ' '

               # Update q_table
               new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
               q_table[current_code][next_move] = new_value

            else:
               #  print('Round for o')

               current_code = encode(board, height)
               if(current_code not in opp_table):
                  opp_table[current_code] = np.random.uniform(size=7)

               # Check if current player is about to win or its opponent is about to win
               col, sign = check_opp_win(board, height, 'o')
               if(sign==1 or sign==-1):
                  opp_table[current_code][col] += 100000

               col, sign = check_horizontal(board, height, 'o')
               if(sign==1):
                  opp_table[current_code][col] += 5
               elif(sign==2):
                  opp_table[current_code][col] -= 2

               next_move = 0
               new_code = 0
               #  sleep(0.1)

               epsilon = random.uniform(0, 1)

               # random move
               if(epsilon<ep):
                  next_move = random.randint(0, 6)

               # move according to the max q_table entry
               else:
                  next_move = np.argmax(opp_table[current_code])

               opp_last_move.append([current_code, next_move])
               if(len(opp_last_move)>4):
                  opp_last_move.pop(0)

               #  print("Computer placed at column", next_move+1)

               k = 6
               while(height[next_move]>=7):
                  next_move = np.where(np.argsort(opp_table[current_code])==k)[0][0]
                  k -= 1
               board[height[next_move]][next_move] = 'o'
               height[next_move] += 1
               new_code = encode(board, height)
               reward = calc_reward(new_code, 0)
               old_value = opp_table[current_code][next_move]

               if(new_code not in q_table):
                  q_table[new_code] = np.random.uniform(size=7)

               q_next_move = np.argmax(q_table[new_code])
               k = 6
               while(height[q_next_move]>=7):
                  q_next_move = np.where(np.argsort(q_table[new_code])==k)[0][0]
                  k -= 1

               board[height[q_next_move]][q_next_move] = 'x'
               height[q_next_move] += 1

               # 假设对手走了最牛逼的一步，咱们应该怎么应对？
               # aka Mini Max
               new_code = encode(board, height)
               if(new_code not in opp_table):
                  opp_table[new_code] = np.random.uniform(size=7)

               # Check if current player is about to win or its opponent is about to win
               col, sign = check_opp_win(board, height, 'o')
               if(sign!=0):
                  opp_table[new_code][col] += 10

               col, sign = check_horizontal(board, height, 'o')
               if(sign==1):
                  opp_table[new_code][col] += 10
               elif(sign==2):
                  opp_table[new_code][col] -= 5

               next_max = np.max(opp_table[new_code])

               # 刚刚只是假想，现在还原棋盘
               height[q_next_move] -= 1
               board[height[q_next_move]][q_next_move] = ' '

               # Update q_table
               new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
               opp_table[current_code][next_move] = new_value

            rd = -rd

            winner = check_win(board, 7)
            if(winner=='n'):
               winner = check_win(list(zip(*board)), 7)
               if(winner=='n'):
                  winner = diag_check(board, 7)

            #  if(grid):
               #  grid_board(board, 7)
            #  else:
               #  print_board(board, 7)
            if(winner!='n'):
               if(winner=='x'):
                  #  x_wins()
                  x_win_c += 1

                  for index in range(len(last_move)):
                     old_value = q_table[last_move[index][0]][last_move[index][1]]
                     new_value = (1 - alpha) * old_value + ((index+1)/2) * alpha * 50
                     q_table[last_move[index][0]][last_move[index][1]] = new_value

                  for index in range(len(opp_last_move)):
                     old_value = opp_table[opp_last_move[index][0]][opp_last_move[index][1]]
                     new_value = (1 - alpha) * old_value - ((index+1)/2) * alpha * 25
                     opp_table[opp_last_move[index][0]][opp_last_move[index][1]] = new_value
               else:
                  #  o_wins()
                  o_win_c += 1
                  for index in range(len(opp_last_move)):
                     old_value = opp_table[opp_last_move[index][0]][opp_last_move[index][1]]
                     new_value = (1 - alpha) * old_value + ((index+1)/2) * alpha * 50
                     opp_table[opp_last_move[index][0]][opp_last_move[index][1]] = new_value

                  for index in range(len(last_move)):
                     old_value = q_table[last_move[index][0]][last_move[index][1]]
                     new_value = (1 - alpha) * old_value - ((index+1)/2) * alpha * 25
                     q_table[last_move[index][0]][last_move[index][1]] = new_value

               break

            rd_num += 1

         print('round counts:', rd_num)
         rd_num_ls.append(rd_num)

      print('x wins:', x_win_c)
      print('o wins:', o_win_c)
      #  plot_rd_num(rd_num_ls)
   elif('-finetune' in sys.argv):
      board = [[' ' for col in range(7)] for row in range(7)]
      height = {i:0 for i in range(7)}
      q_table = finetune(q_table, opp_table, board, height)
   else:
      for i in range(10):
         q_table = playerVScomputer(q_table)

   print('Saving AI data...')
   # Save the partial Q-table as a dict
   with open('Q_table.pkl', 'wb') as f:
      pickle.dump(q_table, f)

   if('-train' in sys.argv):
      with open('Opp_table.pkl', 'wb') as f:
         pickle.dump(opp_table, f)


# Player v.s. Player
else:
   if('-s' in sys.argv):
      size = int(sys.argv[sys.argv.index('-s') + 1])
      assert(str(size).isdigit())
      assert(size>3 and size<20)

   board = [[' ' for col in range(size)] for row in range(size)]
   height = {i:0 for i in range(size)}
   rd = 1
   rd_num = 0

   while(True):
      if(rd_num==size**2-1):
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

      print(encode(board, height))
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
