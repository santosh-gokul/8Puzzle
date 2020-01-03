import numpy as np
import heapq

class Eight_Puzzle:

    def __init__(self,magic_square):
        self.solution = [[1,2,3],[4,5,6],[7,8,0]]
        magic_square1 = magic_square
        magic_square = list(magic_square)
        magic_square2 = []
        for i in magic_square:
            magic_square2.append(list(i))

        magic_square = magic_square2

        
        root_h_value = self.calc_inv(magic_square)

        if((root_h_value%2)==1):
            print("Not solvable...")
            return
        print("The calc_inv value is:")
        print(root_h_value)

        root_h_value = self.calc_heu(magic_square)
        print("The heuristics value of the root table is: ")
        print(root_h_value)
        self.q_board_out_list ={}
        self.q_board = {root_h_value: [magic_square]}
        self.h_values = []
        self.h_values.append(root_h_value)
        heapq.heapify(self.h_values)
        self.parent = {magic_square1:magic_square}
        self.solve()

    def calc_heu(self,magic_square):
        diff = 0

        for i in range(1,9):
            index_solution = tuple()
            index_square = tuple()
            index_solution = self.findindex(self.solution,i)
            index_square = self.findindex(magic_square,i)
            diff+= abs(index_square[0]-index_solution[0])
            diff+=abs(index_square[1]-index_solution[1])
        return(diff)


    def findindex(self,solution,i1):

        index_i = 0
        index_j = 0

        for i in solution:
            for j in i:
                if (i1==j):
                    index_i = solution.index(i)
                    index_j = i.index(j)
        return(index_i,index_j)
    def calc_inv(self,magic_square):

        magic_square1 = np.asarray(magic_square)
        magic_square1 = magic_square1.ravel()
        inv = 0
        for i in range(len(magic_square1)):
            for j in range(i+1,len(magic_square1)):
                if(magic_square1[i]>magic_square1[j] and magic_square1[i]!=0 and magic_square1[j]!=0):
                    inv+=1

        return(inv)

    def solve(self):

        min_h =  heapq.heappop(self.h_values)
        

        if(min_h==0):
            print ("Solved")
            print("The solution is:  ")
            self.final_solution(self.q_board[0][0])
            return

        if self.q_board[min_h]:
            temp_list = self.q_board[min_h]
            root_board = temp_list[0]
            if(not(min_h in self.q_board_out_list)):
                self.q_board_out_list[min_h] = []
            self.q_board_out_list[min_h].append(temp_list[0])
            temp_list.remove(temp_list[0])
        
            child_board = self.possible_squares(root_board)

            for i in child_board:
            
                if(self.in_q_board(i) or self.in_q_board_out_list(i)):
                    continue
                else:

                    temp_h_value = self.calc_heu(i)
                
                    if (not(temp_h_value in self.q_board)):
                        self.q_board[temp_h_value] = []
                    
                    self.q_board[temp_h_value].append(i)
                    if(not self.h_values):
                        self.h_values.append(temp_h_value)
                        heapq.heapify(self.h_values)
                    else:
                        heapq.heappush(self.h_values,temp_h_value)
                    i1 = []

                    for j in i:
                        j = tuple(j)
                        i1.append(j)

                    i1 = tuple(i1)
                    self.parent[i1] = root_board

        self.solve()
 
    def possible_squares(self,root_board):

        for i in root_board:
            for j in i:
                if(j==0):
                    index_i = root_board.index(i)
                    index_j = i.index(j)
        list_child = []
        
        if((index_i+1)<3):
            magic_square1 = list(map(list,root_board))
            temp = magic_square1[index_i+1][index_j]
            magic_square1[index_i+1][index_j] = 0
            magic_square1[index_i][index_j] = temp
            list_child.append(magic_square1)
            #root_board[index_i][index_j] = 0
            #root_board[index_i+1][index_j] = temp
        if((index_i-1)>-1):
            magic_square2 = list(map(list,root_board))
            temp = magic_square2[index_i-1][index_j]
            magic_square2[index_i-1][index_j] = 0
            magic_square2[index_i][index_j] = temp
            list_child.append(magic_square2)
            #root_board[index_i][index_j] = 0
            #root_board[index_i-1][index_j] = temp
        if((index_j+1)<3):
            magic_square3 = list(map(list,root_board))
            temp = magic_square3[index_i][index_j+1]
            magic_square3[index_i][index_j+1] = 0
            magic_square3[index_i][index_j] = temp
            list_child.append(magic_square3)
            #root_board[index_i][index_j] = 0
            #root_board[index_i][index_j+1] = temp
        if((index_j-1)>-1):
            magic_square4 = list(map(list,root_board))
            temp = magic_square4[index_i][index_j-1]
            magic_square4[index_i][index_j-1] = 0
            magic_square4[index_i][index_j] = temp
            list_child.append(magic_square4)
            #root_board[index_i][index_j] = 0
            #root_board[index_i][index_j-1] = temp


        list_child = tuple(list_child)

        return(list_child)

    def in_q_board(self,i):

        h_i = self.calc_heu(i)

        if(not (h_i in self.q_board)):
            return (0)

        else:

            list_board = self.q_board[h_i]

            for j in list_board:
                if(i==j):
                    return(1)

            return(0)
    def in_q_board_out_list(self,i):

        h_i = self.calc_heu(i)

        if(not(h_i in self.q_board_out_list)):
            return(0)

        else:

            list_board = self.q_board_out_list[h_i]

            for j in list_board:
                if(i==j):
                    return(1)

            return(0)

    def final_solution(self,root_board):

        root_board1 = []
        for i in root_board:
            root_board1.append(tuple(i))

        root_board1 = tuple(root_board1)
        if(self.parent[root_board1]==root_board):
            
            for i in root_board:
                str1 = " ".join(str(e) for e in i)
                print(str1)
            print("-->")

            return
        self.final_solution(self.parent[root_board1])
        for i in root_board:
            str1 = " ".join(str(e) for e in i)
            print(str1)
        
        print("-->")

        return



eightpuzzle = Eight_Puzzle(((3,1,2),(4,5,6),(7,8,0)))
