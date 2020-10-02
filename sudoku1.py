#Function to display the sudoku in desired format
def display(rows, cols, sudoku):
	for i in range(rows):
		if i/int(rows**0.5) == i//int(rows**0.5):
			print()
		for j in range(cols):
			if j/int(cols**0.5) == j//int(cols**0.5):
				print(end=" ")
			print(sudoku[i][j],end=" ")
		print()

#Function to remove a value from a row, a column and a quadrant
def remov(row, col, values, element, rows, cols):
	values[row][col] = [0]*rows
	for block in range(rows): #Remove element from a row
		values[row][block][element-1] = 0
	for block in range(cols): #Reamove element from a column
		values[block][col][element-1] = 0
	row = int(rows**0.5)*(row//int(rows**0.5))
	col = int(cols**0.5)*(col//int(cols**0.5))
	for i in range(row, row + int(rows**0.5)):
		for j in range(col, col + int(cols**0.5)):
			values[i][j][element-1] = 0

#Function to initialize the 'values' array, which holds the possible values(1 to 9) in any block
def init(rows, cols):
	values = []
	for row in range(rows):
		values.append([])
		for col in range(cols):
			values[-1].append([x for x in range(1, cols+1)])
	return values

#Function to call remov function for all pre-printed values
def init1(rows, cols, values, sudoku):
	for row in range(rows):
		for col in range(cols):
			if sudoku[row][col]:
			  values[row][col] = [0]*rows
			  remov(row, col, values, sudoku[row][col], rows, cols)
	return values

#Function to check if there is any block in sudoku where only one value(1 to 9) is possible
def single(rows, cols, values, sudoku):
	flag = 0
	for i in range(rows):
		for j in range(cols):
			count = 0
			for k in range(rows):
				if values[i][j][k]:
					count += 1
					value = values[i][j][k]
			if count == 1:
				sudoku[i][j] = value
				remov(i, j, values, value, rows, cols)
				flag = 1
	return flag

#Function to check if any number(1 to 9) occurs only once in a row
def row_check(rows, cols, values, sudoku):
	flag = 0
	for i in range(rows):
		count = [0]*rows
		pos = [-1]*rows
		for j in range(cols):
			for k in range(rows):
				if values[i][j][k]:
					count[values[i][j][k]-1] += 1
					pos[values[i][j][k]-1] = j
		for j in range(rows):
			if count[j] == 1:
				sudoku[i][pos[j]] = j+1
				remov(i, pos[j], values, j+1, rows, cols)
				flag = 1
	return flag

#Function to check if any number(1 to 9) occurs only once in a column
def col_check(rows, cols, values, sudoku):
	flag = 0
	for j in range(cols):
		count = [0]*rows
		pos = [-1]*rows
		for i in range(rows):
			for k in range(rows):
				if values[i][j][k]:
					count[values[i][j][k]-1] += 1
					pos[values[i][j][k]-1] = i
		for i in range(rows):
			if count[i] == 1:
				sudoku[pos[i]][j] = i+1
				remov(pos[i], j, values, i+1, rows, cols)
				flag = 1
	return flag

#Function to check if any number(1 to 9) occurs only once in a quadrant
def quad_check(rows, cols, values, sudoku):
	flag = 0
	for i in range(rows):
		st_row = int(rows**0.5)*(i//int(rows**0.5))
		st_col = (i-st_row)*int(rows**0.5)
		count = [0]*rows
		pos = [-1]*rows
		for j in range(st_row, st_row+int(rows**0.5)):
			for k in range(st_col, st_col+int(rows**0.5)):
				for l in range(rows):
					if values[j][k][l]:
						count[values[j][k][l]-1] += 1
						pos[values[j][k][l]-1] = [j, k]
		for j in range(rows):
			if count[j] == 1:
				sudoku[pos[j][0]][pos[j][1]] = j+1
				remov(pos[j][0], pos[j][1], values, j+1, rows, cols)
				flag = 1
	return flag
	
#Function to check if the given sudoku is valid or not
def check_valid_sudoku(rows, cols, values, sudoku):
	flag = 0
	for i in range(rows):
		st_col = (i-st_row)*int(rows**0.5)
		count = [0]*rows
		pos = [-1]*rows
		st_row = int(rows**0.5)*(i//int(rows**0.5))
		for j in range(st_row, st_row+int(rows**0.5)):
			for k in range(st_col, st_col+int(rows**0.5)):
				for l in range(rows):
					if values[j][k][l]:
						count[values[j][k][l]-1] += 1
						pos[values[j][k][l]-1] = [j, k]
						flag = 1
		for j in range(rows):
			if count[j] == 1:
                count[values[j][k][l]-1] += 1 
				sudoku[pos[j][0]][pos[j][1]] = j+1
				remov(pos[j][0], pos[j][1], values, j+1, rows, cols)
				flag = 1
	    for j in range(rows):
			if count[j] == 1:
				sudoku[pos[j][0]][pos[j][1]] = j+1
				count[values[j][k][l]-1] += 1
				remov(pos[j][0], pos[j][1], values, j+1, rows, cols)
				flag = 1
		for l in range(rows):
			if values[j][k][l]:
				count[values[j][k][l]-1] += 1
				pos[values[j][k][l]-1] = [j, k]
				flag = 1
	return flag
	

#Function to find numbers(1 to 9) which share common blocks in a row or a column based on typ(0 for row and 1 for column) and remove all other numbers in those blocks if possible
def special2(rows, values, pos, i, typ):
    flag = 0
    for j in range(rows):
        count = 1
        array = [j]
        for k in range(j+1, rows):
            if pos[j] == pos[k]:
                count += 1
                array.append(k)
        if count == len(pos[j]):
            for k in range(count):
               for l in range(rows):
                 if typ:
                   row = pos[j][k]
                   if values[row][i][l] and values[row][i][l]-1 not in array:
                       flag = 1
                       values[row][i][l] = 0
                 else:
                   col = pos[j][k]
                   if values[i][col][l] and values[i][col][l]-1 not in array:
                       flag = 1
                       values[i][col][l] = 0
    return flag

#Function to:
#  i. Find numbers(1 to 9) which share common blocks in a quadrant and remove all other numbers in those blocks if possible
#  ii.Find numbers(1 to 9) which occur only in a row or a column of a quadrant and remove that number from other blocks in that row or column
def special(rows, values, sudoku):
    flag = 0
    for i in range(rows):
        st_row = int(rows**0.5)*(i//int(rows**0.5))
        st_col = (i-st_row)*int(rows**0.5)
        pos = []
        for l in range(rows):
            pos.append([])
            for j in range(st_row, st_row+int(rows**0.5)):
                for k in range(st_col, st_col+int(rows**0.5)):
                    if values[j][k][l]:
                        pos[-1].append([j,k])
        #First part
        for j in range(rows):
            count = 1 
            array = [j]
            for k in range(j+1, rows):
                if pos[j] == pos[k]:
                    count += 1
                    array.append(k)
            if count == len(pos[j]):
               for k in range(count):
                   for l in range(rows):
                       row = pos[j][k][0]
                       col = pos[j][k][1]
                       if values[row][col][l] and values[row][col][l]-1 not in array:
                            flag = 1
                            values[row][col][l] = 0
        #Second part
        for j in range(rows):
            if len(pos[j]) == 3:
                if pos[j][0][0] == pos[j][1][0] == pos[j][2][0]:
                    for k in range(rows):
                        if k not in [x for x in range(st_col, st_col+int(rows**0.5))]:
                            if values[pos[j][0][0]][k][j]:
                                flag = 1
                                values[pos[j][0][0]][k][j] = 0
                if pos[j][0][1] == pos[j][1][1] == pos[j][2][1]:
                    for k in range(rows):
                        if k not in [x for x in range(st_row, st_row+int(rows**0.5))]:
                            if values[k][pos[j][0][1]][j]:
                                flag = 1
                                values[k][pos[j][0][1]][j] = 0
            elif len(pos[j]) == 2:
                if pos[j][0][0] == pos[j][1][0]:
                    for k in range(rows):
                        if k not in [x for x in range(st_col, st_col+int(rows**0.5))]:
                            if values[pos[j][0][0]][k][j]:
                                flag = 1
                                values[pos[j][0][0]][k][j] = 0
                if pos[j][0][1] == pos[j][1][1]:
                    for k in range(rows):
                        if k not in [x for x in range(st_row, st_row+int(rows**0.5))]:
                            if values[k][pos[j][0][1]][j]:
                                flag = 1
                                values[k][pos[j][0][1]][j] = 0
    return flag

#Function to invoke special2 function and to check if a number in a row occurs in only one quadrant and if so then remove that number from all other blocks of that quadrant
def row_check1(rows, values, sudoku):
    flag = 0
    for i in range(rows):
        pos = []
        for j in range(rows):
            pos.append([])
            for k in range(rows):
                if values[i][k][j]:
                    pos[-1].append(k)
        flag = special2(rows, values, pos, i, 0)
        for j in range(rows):
            quad = []
            for k in range(len(pos[j])):
                block = pos[j][k]//int(rows**0.5)
                if block not in quad:
                    quad.append(block)
            if len(quad) == 1:
                block = quad[0]
                st_row = int(rows**0.5)*(i//int(rows**0.5))
                st_col = int(rows**0.5)*block
                for k in range(st_row, st_row+int(rows**0.5)):
                    for l in range(st_col, st_col+int(rows**0.5)):
                        if k == i:
                            continue
                        if values[k][l][j]:
                            flag = 1
                            values[k][l][j] = 0
    return flag

#Function to invoke special2 function and to check if a number in a column occurs in only one quadrant and if so then remove that number from all other blocks of that quadrant
def col_check1(rows, values, sudoku):
	flag = 0
	for i in range(rows):
		pos = []
		for j in range(rows):
			pos.append([])
			for k in range(rows):
				if values[k][i][j]:
					pos[-1].append(k)
		flag = special2(rows, values, pos, i, 1)
		for j in range(rows):
			quad = []
			for k in range(len(pos[j])):
				block = pos[j][k]//int(rows**0.5)
				if block not in quad:
					quad.append(block)
			if len(quad) == 1:
				block = quad[0]
				st_col = int(rows**0.5)*(i//int(rows**0.5))
				st_row = int(rows**0.5)*block
				for k in range(st_row, st_row+int(rows**0.5)):
					for l in range(st_col, st_col+int(rows**0.5)):
						if l == i:
							continue
						if values[k][l][j]:
							flag = 1
							values[k][l][j] = 0
	return flag

#Function to check if the sudoku is filled. If yes it returns 0 else it return the block with the minimum numbers of possible values(1 to 9)
def check(rows, cols, sudoku, values):
    flag = 0
    mini = [-1, -1, 10]
    for i in range(rows):
        for j in range(cols):
            if not sudoku[i][j] and rows-values[i][j].count(0) < mini[2]:
                mini = [i, j, rows-values[i][j].count(0)]
                flag = 1
    if not flag:
        return 0
    else:
        return mini[:2]

#Function to apply the recursive logic and for the backtracking part
def rec_logic(rows, cols, values, sudoku):
    first = single(rows, cols, values, sudoku)
    second = row_check(rows, cols, values, sudoku)
    third = col_check(rows, cols, values, sudoku)
    fourth = quad_check(rows, cols, values, sudoku)
    fifth = special(rows, values, sudoku)
    sixth = row_check1(rows, values, sudoku)
    seventh = col_check1(rows, values, sudoku)
    if first or second or third or fourth or fifth or sixth or seventh:
        return rec_logic(rows, cols, values, sudoku)
    else:
        emptycols = check(rows, cols, sudoku, values)
        if emptycols:  #Backtracking part
            row = emptycols[0]
            col = emptycols[1]
            for i in range(rows):
                if values[row][col][i]:
                    sudoku1, values1 = [], []
                    for j in range(cols):
                        sudoku1.append([])
                        values1.append([])
                        for k in range(rows):
                            sudoku1[-1].append(sudoku[j][k])
                            values1[-1].append([])
                            for l in range(rows):
                                values1[-1][-1].append(values[j][k][l])
                    sudoku1[row][col] = values[row][col][i]
                    values1[row][col] = [0]*rows
                    remov(row, col, values1, sudoku1[row][col], rows, cols)
                    retvalue = rec_logic(rows, cols, values1, sudoku1)
                    if not check(rows, cols, sudoku1, values1) or retvalue:
                        return 1
            return 0
        else:
            display(rows, cols, sudoku)
            return 1
    return 0

#Main function for invoking all other functions
def main(sudoku):
    rows = len(sudoku)
    cols = rows
    values = init(rows, cols)
    values = init1(rows, cols, values, sudoku)
    retvalue = rec_logic(rows, cols, values, sudoku)

#Sudokus
sudoku1 =          [[9,0,0, 0,1,0, 0,0,3],
		   [7,0,0, 9,0,0, 8,6,0],
		   [0,5,3, 0,0,0, 0,0,0],

		   [1,0,0, 6,0,0, 0,0,0],
		   [0,8,6, 0,0,0, 4,3,0],
		   [0,0,0, 0,0,8, 0,0,1],
		  
		   [0,0,0, 0,0,0, 1,8,0],
		   [0,4,9, 0,0,3, 0,0,2],
		   [6,0,0, 0,5,0, 0,0,9]]

#Hardest Sudoku ever created
sudoku2 =          [[8,0,0, 0,0,0, 0,0,0],
		   [0,0,3, 6,0,0, 0,0,0],
                   [0,7,0, 0,9,0, 2,0,0],

		   [0,5,0, 0,0,7, 0,0,0],
		   [0,0,0, 0,4,5, 7,0,0],
		   [0,0,0, 1,0,0, 0,3,0],
		  
		   [0,0,1, 0,0,0, 0,6,8],
		   [0,0,8, 5,0,0, 0,1,0],
		   [0,9,0, 0,0,0, 4,0,0]]
		  
sudoku = [[7,0,0, 0,0,3, 0,0,1],
          [0,0,0, 9,0,0, 7,0,0],
          [0,0,0, 8,0,0, 0,4,6],
          
          [0,6,0, 0,9,0, 0,7,0],
          [0,2,0, 3,0,5, 0,9,0],
          [0,3,0, 0,8,0, 0,2,0],
          
          [3,5,0, 0,0,1, 0,0,0],
          [0,0,9, 0,0,8, 0,0,0],
          [1,0,0, 2,0,0, 0,0,5]]

#Invoking the main function    
main(sudoku1)
