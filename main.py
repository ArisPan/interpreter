
from syntax import *
import sys


def main():

	if len(sys.argv) < 2:
		print("Too few arguments in function main. A Starlet script should be passed as an argument.")
		exit(0)
	elif len(sys.argv) > 2:
		print("Too many arguments in function main. A Starlet script should be passed as an argument.")
		exit(0)

	try:
		file = open(sys.argv[1], "r")
	except (FileNotFoundError, IOError):
		sys.exit("Error opening file " + sys.argv[1] + ". Please, check input file and try again.")
		exit(0)

	syntax()


main()
