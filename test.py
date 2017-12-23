import numpy as np
goal = [[1,2,3],
        [4,5,6],
        [7,8,0]]

# adj_matrix = []
# for i in range(3):
#     adj_matrix.append(goal[i][:])

par8 = np.arange(9)
np.random.shuffle(par8)
print par8
mat8 = goal
for i in range(3):
    for j in range(3):
        mat8[i][j] = par8[i*3+j]
print mat8
# print adj_matrix

# res = ''
# for row in range(3):
#     res += ' '.join(map(str, adj_matrix[row])) + '\r\n'

# print res

# def pr(a):
# 	print a,(a/3)%3,a%3,(a/3)

# map(lambda a: pr(a),range(-1,9))








