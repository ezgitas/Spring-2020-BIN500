import numpy as np
import sys
import random
from random import shuffle

def friends(alist,blist):						# Turns friends to a symmetric 1-0 matrix. Matrix diagonal is zero since a person cannot be friends with herself.

	limit = int(alist[0])

	friend_list = np.zeros([limit,limit])

	for i in range(1,len(alist)):

		x = int(alist[i])

		y = int(blist[i])

		friend_list[x,y] = 1
		friend_list[y,x] = 1

	return friend_list

def intercept(x,y):								# Finds number of mutual friends.

	i = np.logical_and(x,y)

	i.astype(np.int)

	return sum(i)

def union(x,y):									# Finds total number of people two person knows.

	u = np.logical_or(x,y)

	u.astype(np.int)

	return sum(u)
	
def Jaccard(x,y):								# Jaccard Similarity Function

	return intercept(x,y)/union(x,y)

def CommonNeighbors(x,y):						# Common Neighbors Similarity Function

	return intercept(x,y)

def PreferentialAttachment(x,y):				# Preferential Attachment Similarity Function

	return sum(x)*sum(y)

def similarity(func,alist,blist,x):				# Suggest friend(s) to the person according to selected similarity function. 

	similarity = 0

	equal_sim = []

	limit = int(alist[0])

	if func == 'Jaccard':
		fun = Jaccard

	elif func == 'Common Neighbors':
		fun = CommonNeighbors

	elif func == 'Preferential Attachment':
		fun = PreferentialAttachment

	for i in range(limit):

		sim = fun(friends(alist,blist)[x],friends(alist,blist)[i])

		if sim > similarity and i!=x and friends(alist,blist)[x][i]!=1:

			similarity = sim

			equal_sim = [i]

		elif sim == similarity and i!=x and friends(alist,blist)[x][i]!=1:

			equal_sim.append(i)

	return equal_sim


def conditions(filename,alist,blist,func):		# Applies desired print statements as output.

	for i in range(len(alist)):

		alist[i] = int(alist[i])

		blist[i] = int(blist[i])

	n_max = max(alist+blist)
	n_min = min(alist+blist)

	while True:

		try:

			r = int(input('Enter an integer in the range %d to %d: ' %(n_min,n_max-1)))

			if min(alist) <= r <= max(alist)-1:

				print(('The suggested friend(s) for %d is(are) ' %(r)), end =" ") 
				print(*similarity(func,alist,blist,r), sep = ", ")

				answ = input('\nDo you want to continue (yes/no)? ')

				no_list = ['no', 'No', 'nO', 'NO']

				yes_list = ['yes', 'Yes', 'yEs', 'yeS', 'YEs', 'YeS', 'yES', 'YES']

				if answ in no_list:
	
					sys.exit()

				while (answ not in yes_list) and (answ not in no_list):

					answ = input('Do you want to continue (yes/no)? ')

					if answ in no_list:
						
						sys.exit()

			elif min(alist) > r or r > max(alist)-1:

				print('Error: input must be an int between %d and %d' %(n_min,n_max-1))

		except ValueError:

			print('Error: input must be an int between %d and %d' %(n_min,n_max-1))

def Part1():
	list1 = []
	list2 = []

	print('Facebook friend recommendation.\n')

	function_list = ['Jaccard', 'Common Neighbors', 'Preferential Attachment']

	func = input('Enter the name of similarity function : ')

	while func not in function_list:

		print('Similarity function should be Jaccard, Common Neighbors or Preferential Attachment.')

		func = input('Enter the name of similarity function : ')	

	print()

	while True:

		try:

			filename = input('Enter a file name: ')				# Asks for a file
			thefile = open(filename,"r")
			print()

			for line in thefile:								# Splits file into 2 lists

				prop = line.split()
				list1.append(prop[0])
				list2.append(prop[-1])

			conditions(thefile, list1, list2, func)				# Applies desired conditions to the lists

		except SystemExit:

			break

		except(FileNotFoundError,NameError) as e:				# Checks possible errors in file name.
			
			print('Error in file name.')


def Part2():

	def friend_shuffle(alist, blist):			# Creates a dictionary to encode people in lists.
		d = {}

		limit = int(alist[0])

		alist_key = np.linspace(0,int(alist[0])-1,num=int(alist[0])).astype(int).astype(str)

		alist_value = np.copy(alist_key) 

		shuffle(alist_value)

		d = dict(zip(alist_key, alist_value))

	
		for i in range(1,len(alist)):

			alist[i] = d[alist[i]]
			blist[i] = d[blist[i]]

		return alist, blist

	list1 = []
	list2 = []

	print('\n\nFacebook friend recommendation with shuffle.\n')

	function_list = ['Jaccard', 'Common Neighbors', 'Preferential Attachment']

	func = input('Enter the name of similarity function : ')

	while func not in function_list:

		print('Similarity function should be Jaccard, Common Neighbors or Preferential Attachment.')

		func = input('Enter the name of similarity function : ')	

	print()


	while True:

		try:

			filename = input('Enter a file name: ')
			thefile = open(filename,"r")
			print()

			for line in thefile:

				prop = line.split()
				list1.append(prop[0])
				list2.append(prop[-1])

			list1,list2 = friend_shuffle(list1,list2)

			conditions(thefile, list1, list2, func)

		except SystemExit:

			break

		except(FileNotFoundError,NameError) as e:
			
			print('File does not exist.')


def Part3():

	def twitter_network(population):					# Creates a non-symmetrical 1-0 matrix for people.
														# If person x followes person y, twitter_network(population)[x][y] = 1. 
														# Person y does not have to follow person x. 
														# Matrix diagonal is zero since following yourself is not possible.

		follower_list = np.zeros([population,population])

		for i in range(population):

			for j in range(population):

				if i == j:

					follower_list[i,j] = 0

				else:

					follower_list[i,j] = random.randint(0,1)

		return follower_list

	def twitter_similarity(func,population,x):				# Applies similarity functions to twitter network and suggests new people to follow.
															# Similarity functions were shown in tools.py file.

		similarity = 0

		limit = population

		if func == 'Jaccard':
			fun = Jaccard

		elif func == 'Common Neighbors':
			fun = CommonNeighbors

		elif func == 'Preferential Attachment':
			fun = PreferentialAttachment

		else:
			print('Similarity function should be Jaccard, Common Neighbors or Preferential Attachment.')

		for i in range(limit):

			sim = fun(twitter_network(population)[x],twitter_network(population)[i])

			if sim > similarity and i!=x and twitter_network(population)[x][i]!=1:

				similarity = sim

				equal_sim = [i]

			elif sim == similarity and i!=x and twitter_network(population)[x][i]!=1:

				equal_sim.append(i)

		return equal_sim

	def twitter_conditions(population,func):				# Applies desired print statements as output.

		while True:

			try:

				r = int(input('Enter an integer in the range 0 to %d: ' %(population-1)))

				if 0 <= r <= population-1:

					print(('%d can follow' %(r)), end=" ")
					print(*twitter_similarity(func,population,r), sep=",")

					answ = input('\nDo you want to continue (yes/no)? ')

					no_list = ['no', 'No', 'nO', 'NO']

					yes_list = ['yes', 'Yes', 'yEs', 'yeS', 'YEs', 'YeS', 'yES', 'YES']

					if answ in no_list:
		
						sys.exit()

					while answ not in yes_list and no_list:

						answ = input('Do you want to continue (yes/no)? ')

						while answ in no_list:
							
							sys.exit()

				elif 0 > r or r > population-1:

					print('Error: input must be an int between 0 and %d' %(population-1))

			except ValueError:

				print('Error: input must be an int between 0 and %d' %(population-1))


	print('\n\nTwitter follow recommendation.\n')

	function_list = ['Jaccard', 'Common Neighbors', 'Preferential Attachment']

	func = input('Enter the name of similarity function : ')

	while func not in function_list:

		print('Similarity function should be Jaccard, Common Neighbors or Preferential Attachment.')

		func = input('Enter the name of similarity function : ')	

	print()

	twitter_conditions(250, func)

def main():

	Part1()
	Part2()
	Part3()

if __name__ == "__main__":
	main()