# Panagiotidis Diktampanis Aristeidis, 2323, cs122323
# Zouvgias Giorgos, 2699, cse42699

import sys
import os

# Keywords
PROGRAM = 1
END_PROGRAM = 2
DECLARE = 3
IF = 4
THEN = 5
ELSE = 6
END_IF = 7
DO_WHILE = 8
END_DO_WHILE = 9
WHILE = 10
END_WHILE = 11
LOOP = 12
END_LOOP = 13
EXIT = 14
FORCASE = 15
END_FORCASE = 16
INCASE = 17
END_INCASE = 18
WHEN = 19
END_WHEN = 20
DEFAULT = 21
END_DEFAULT = 22
FUNCTION = 23
END_FUNCTION = 24
RETURN = 25
IN = 26
IN_OUT = 27
IN_AND_OUT = 28
AND = 29
OR = 30
NOT = 31
INPUT = 32
PRINT = 33

# Numerical Operators
PLUS = 34
MINUS = 35
MULTIPLICATION = 36
DIVISION = 37

# Logical Operators
LESS_THAN = 38
GREATER_THAN = 39
EQUALS = 40
LESS_OR_EQUAL = 41
GREATER_OR_EQUAL = 42
DIFFERENT = 43

# Punctuation signs
ASSIGN = 44
SEMICOLON = 45
COMMA = 46
COLON = 47

# Grouping Signs
OPEN_PARENTHESIS = 48
CLOSE_PARENTHESIS = 49
OPEN_BRACKETS = 50
CLOSE_BRACKETS = 51

# Comment signs
OPEN_COMMENT = 52
CLOSE_COMMENT = 53
ONE_LINE_COMMENT = 54

# Alphanumerics
ALNUM = 55
CONSTANT = 56

# Lexical Error ID
ASSIGN_ERR = 1
COMMENT_NOT_STARTED_ERR = 2
COMMENT_NOT_FINISHED_ERR = 3
NESTED_COMMENT_ERR = 4
INVALID_CONSTANT_ERR = 5
OUT_OF_RANGE_ERR = 6
UNKNOWN_CHAR_ERR = 7

# Syntax Error ID
EXPECTED_PROGRAM_DECLARATION_ERR = 1
EXPECTED_ENDPROGRAM_STATEMENT = 2
INVALID_PROGRAM_NAME_ERR = 3
INVALID_VARIABLE_NAME = 4
EXPECTED_END_OF_DECLARE = 5
INVALID_FUNCTION_NAME = 6
EXPECTED_ENDFUNCTION_STATEMENT = 7
EXPECTED_CLOSE_PARENTHESIS = 8
EXPECTED_OPEN_PARENTHESIS = 9
EXPECTED_THEN_STATEMENT = 10
EXPECTED_ENDIF_STATEMENT = 11
EXPECTED_WHILE_STATEMENT = 12
EXPECTED_ENDLOOP_STATEMENT = 13
EXPECTED_COLON_CHARACTER = 14
EXPECTED_WHEN_STATEMENT = 15
EXPECTED_DEFAULT_STATEMENT = 16
EXPECTED_ENDDEFAULT_STATEMENT = 17
EXPECTED_ENDFORCASE_STATEMENT = 18
EXPECTED_ENDINCASE_STATEMENT = 19
EXPECTED_ENDWHILE_STATEMENT = 20
EXPECTED_ALNUM_AS_INPUT = 21
INVALID_RELATIONAL_OPERATOR = 22
EXPECTED_ADD_OPERATOR = 23
EXPECTED_MUL_OPERATOR = 24
EXPECTED_ASSIGNMENT_SIGN = 25
EXPECTED_OPEN_BRACKETS = 26
EXPECTED_CLOSE_BRACKETS = 27
EXPECTED_SEMICOLON = 28
EXPECTED_VARIABLE_NAME_AFTER_COMMA = 29
INVALID_PARAMETER_TYPE = 30

# Lexical & Syntax Analysis Global variables
token_id = 0
token = ""
line = 1

# General Global variables
file = ""
file_position = 0


def main():

	global file

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


def is_num_operator(char) -> bool:

	if char == '+' or char == '-' or char == '*' or char == '/':
		return True
	return False


def is_relational_operator(char) -> bool:
	if char == '>' or char == '<' or char == '=':
		return True
	return False


def is_grouping_sign(char) -> bool:
	if char == '(' or char == ')' or char == '[' or char == ']':
		return True
	return False


def is_punctuation(char) -> bool:
	if char == ';' or char == ',' or char == ':':
		return True
	return False


def is_unknown_character(char) -> bool:
	if char.isspace() or char == "":
		return False
	elif (
		0 <= ord(char) <= 31 or
		33 <= ord(char) <= 39 or
		ord(char) == 46 or ord(char) == 63 or ord(char) == 64 or
		ord(char) == 92 or ord(char) == 95 or ord(char) == 96 or
		123 <= ord(char) <= 255):
		return True
	return False


def lex():

	global file
	global token
	global line
	global file_position

	token = ""
	file_position = file.tell()
	character = file.read(1)

	# Consume white spaces
	while character.isspace():
		if "\n" in character:
			line += 1
		character = file.read(1)

	# Comments
	if character == '/':
		token = token + character
		file_position = file.tell()
		character = file.read(1)
		if character == '*':
			comment_starts_in_line = line
			while True:
				character = file.read(1)
				if character == '/':
					character = file.read(1)
					if character == '*':
						lexical_error(NESTED_COMMENT_ERR, line)
				elif '\n' in character:
					line += 1
				elif character == '*':
					character = file.read(1)
					if character == '/':
						break
				elif not is_unknown_character(character):
					character = file.read(1)
				else:
					lexical_error(COMMENT_NOT_FINISHED_ERR, comment_starts_in_line)
		elif character == '/':
			character = file.readline()
		else:
			word_identifier(token)
			file.seek(file_position)
		return
	elif character == '*':
		token = token + character
		file_position = file.tell()
		character = file.read(1)
		if character == '/':
			lexical_error(COMMENT_NOT_STARTED_ERR, line)
		else:
			word_identifier(token)
			file.seek(file_position)
		return

	# Is unknown character
	if is_unknown_character(character):
		lexical_error(UNKNOWN_CHAR_ERR, line)

	# Alphanumeric starting with letter
	if character.isalpha():
		token = token + character
		file_position = file.tell()
		character = file.read(1)

		while character.isalnum():
			token = token + character
			file_position = file.tell()
			character = file.read(1)

			if is_unknown_character(character):
				lexical_error(UNKNOWN_CHAR_ERR, line)

		if is_unknown_character(character):
			lexical_error(UNKNOWN_CHAR_ERR, line)

		word_identifier(token)
		file.seek(file_position)
		return

	# Constant
	if character.isdigit():
		token = token + character
		file_position = file.tell()
		character = file.read(1)

		while character.isdigit():
			token = token + character
			file_position = file.tell()
			character = file.read(1)

			if is_unknown_character(character):
				lexical_error(UNKNOWN_CHAR_ERR, line)
			elif character.isalpha():
				lexical_error(INVALID_CONSTANT_ERR, line)

		if not -32767 < int(token) < 32767:
			lexical_error(OUT_OF_RANGE_ERR, line)

		word_identifier(token)
		file.seek(file_position)
		return

	# Character is new line.
	if '\n' in character:
		line += 1
		return

	# Character is relational operator
	if is_relational_operator(character):

		if character == '<':
			token = '<'
			file_position = file.tell()
			character = file.read(1)
			if character == '=':
				token = '<='
			elif character == '>':
				token = '<>'
			else:
				file.seek(file_position)
			word_identifier(token)
		elif character == '>':
			token = '>'
			file_position = file.tell()
			character = file.read(1)
			if character == '=':
				token = '>='
			else:
				file.seek(file_position)
			word_identifier(token)
		elif character == '=':
			token = '='
			word_identifier(token)

		return

	# Character is numerical operator
	if is_num_operator(character):
		token = character
		word_identifier(token)
		return

	# Character is grouping sign
	if is_grouping_sign(character):
		token = character
		word_identifier(token)
		return

	# Character is punctuation
	if is_punctuation(character):
		token = character
		word_identifier(token)
		return


def word_identifier(resulting_token):

	global token_id

	if resulting_token == 'program':
		token_id = PROGRAM
	elif resulting_token == 'endprogram':
		token_id = END_PROGRAM
	elif resulting_token == 'declare':
		token_id = DECLARE
	elif resulting_token == 'if':
		token_id = IF
	elif resulting_token == 'then':
		token_id = THEN
	elif resulting_token == 'else':
		token_id = ELSE
	elif resulting_token == 'endif':
		token_id = END_IF
	elif resulting_token == 'dowhile':
		token_id = DO_WHILE
	elif resulting_token == 'enddowhile':
		token_id = END_DO_WHILE
	elif resulting_token == 'while':
		token_id = WHILE
	elif resulting_token == 'endwhile':
		token_id = END_WHILE
	elif resulting_token == 'loop':
		token_id = LOOP
	elif resulting_token == 'endloop':
		token_id = END_LOOP
	elif resulting_token == 'exit':
		token_id = EXIT
	elif resulting_token == 'forcase':
		token_id = FORCASE
	elif resulting_token == 'endforcase':
		token_id = END_FORCASE
	elif resulting_token == 'incase':
		token_id = INCASE
	elif resulting_token == 'endincase':
		token_id == END_INCASE
	elif resulting_token == 'when':
		token_id = WHEN
	elif resulting_token == 'endwhen':
		token_id = END_WHEN
	elif resulting_token == 'default':
		token_id = DEFAULT
	elif resulting_token == 'enddefault':
		token_id = END_DEFAULT
	elif resulting_token == 'function':
		token_id = FUNCTION
	elif resulting_token == 'endfunction':
		token_id = END_FUNCTION
	elif resulting_token == 'return':
		token_id = RETURN
	elif resulting_token == 'in':
		token_id = IN
	elif resulting_token == 'inout':
		token_id = IN_OUT
	elif resulting_token == 'inandout':
		token_id = IN_AND_OUT
	elif resulting_token == 'and':
		token_id = AND
	elif resulting_token == 'or':
		token_id = OR
	elif resulting_token == 'not':
		token_id = NOT
	elif resulting_token == 'input':
		token_id = INPUT
	elif resulting_token == 'print':
		token_id = PRINT
	elif resulting_token == '+':
		token_id = PLUS
	elif resulting_token == '-':
		token_id = MINUS
	elif resulting_token == '*':
		token_id = MULTIPLICATION
	elif resulting_token == '/':
		token_id = DIVISION
	elif resulting_token == '<':
		token_id = LESS_THAN
	elif resulting_token == '>':
		token_id = GREATER_THAN
	elif resulting_token == '=':
		token_id = EQUALS
	elif resulting_token == '<=':
		token_id = LESS_OR_EQUAL
	elif resulting_token == '>=':
		token_id = GREATER_OR_EQUAL
	elif resulting_token == '<>':
		token_id = DIFFERENT
	elif resulting_token == ':=':
		token_id = ASSIGN
	elif resulting_token == ';':
		token_id = SEMICOLON
	elif resulting_token == ',':
		token_id = COMMA
	elif resulting_token == ':':
		token_id = COLON
	elif resulting_token == '(':
		token_id = OPEN_PARENTHESIS
	elif resulting_token == ')':
		token_id = CLOSE_PARENTHESIS
	elif resulting_token == '[':
		token_id = OPEN_BRACKETS
	elif resulting_token == ']':
		token_id = CLOSE_BRACKETS
	elif resulting_token == '/*':
		token_id = OPEN_COMMENT
	elif resulting_token == '*/':
		token_id = CLOSE_COMMENT
	elif resulting_token == '//':
		token_id = ONE_LINE_COMMENT
	else:
		token_id = ALNUM


def lexical_error(err_id, line):
	if err_id == ASSIGN_ERR:
		print("Assignment error. Missing '=' character in line", line)
		exit(0)
	elif err_id == COMMENT_NOT_FINISHED_ERR:
		print("Error in line", line, "| Comment segment is never finished.")
		exit(0)
	elif err_id == COMMENT_NOT_STARTED_ERR:
		print("Error in line", line, "| Comment segment is never declared.")
		exit(0)
	elif err_id == NESTED_COMMENT_ERR:
		print("Error in line", line, "| Nested comment.")
		exit(0)
	elif err_id == INVALID_CONSTANT_ERR:
		print("Error in line", line, "| Invalid constant.")
		exit(0)
	elif err_id == OUT_OF_RANGE_ERR:
		print("Error in line", line, "| Integer value should be greater than -32767 and less than 32767.")
		exit(0)
	elif err_id == UNKNOWN_CHAR_ERR:
		print("Error in line", line, "| Unknown character.")
		exit(0)


def syntax():
	program()


def program():

	lex()		# First token must be 'program'.

	if token_id == PROGRAM:

		lex()		# Next token must be a valid program id (alphanumeric).
		if token_id == ALNUM:
			block()

			lex()		# Next (and final) token must be 'endprogram'.
			if token_id != END_PROGRAM:
				syntax_error(EXPECTED_ENDPROGRAM_STATEMENT, line)

		else:
			syntax_error(INVALID_PROGRAM_NAME_ERR, line)
	else:
		syntax_error(EXPECTED_PROGRAM_DECLARATION_ERR, line)


def block():
	declarations()
	subprograms()
	statements()


def declarations():

	lex()		# Next token may be 'declare', in any case, restore file pointer.

	if token_id == DECLARE:
		variable_list()

		lex()		# Every 'declare' statement must end with semicolon (';').
		if token_id != SEMICOLON:
			syntax_error(EXPECTED_SEMICOLON, line)
		declarations()		# Check for another 'declare' statement.
	else:
		move_file_pointer(-len(token))


def variable_list():

	lex()		# Next token may be variable name (alphanumeric), semicolon or ε.

	if token_id == ALNUM:
		lex()		# Next token may be comma or semicolon.

		if token_id == SEMICOLON:
			move_file_pointer(-len(token))
			return

		elif token_id == COMMA:
			lex()		# Next token must be variable name (alphanumeric).
			if token_id == ALNUM:
				move_file_pointer(-len(token))
				variable_list()
			else:
				syntax_error(EXPECTED_VARIABLE_NAME_AFTER_COMMA, line)

	elif token_id == SEMICOLON:
		move_file_pointer(-len(token))
		return
	else:
		syntax_error(INVALID_VARIABLE_NAME, line)		# Keyword used as a variable name.


def subprograms():
	subprogram()


def subprogram():

	lex()		# Check for function declaration.

	if token_id == FUNCTION:

		lex()		# Next token must be a valid function name.
		if token_id == ALNUM:

			function_body()

			lex()		# Next (and final) token of a function declaration must be 'endfunction'.

			if token_id != END_FUNCTION:
				syntax_error(EXPECTED_ENDFUNCTION_STATEMENT, line)
			subprogram()
	else:
		move_file_pointer(-len(token))


def function_body():
	formal_parameters()
	block()


def formal_parameters():

	lex()		# Next token must be '('.

	if token_id == OPEN_PARENTHESIS:
		formal_parameters_list()

		lex()		# Next token must be ')'.
		if token_id != CLOSE_PARENTHESIS:
			syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)


def formal_parameters_list():

	lex()		# Check what's next.

	if token_id == CLOSE_PARENTHESIS:
		move_file_pointer(-len(token))		# formal_parameters() checks for ')'.
		return
	else:
		move_file_pointer(-len(token))
		formal_parameters_item()
		formal_parameters_list()


def formal_parameters_item():

	lex()		# Next token may be in, inout or inandout.

	if token_id == IN:

		lex()		# Next token must be alphanumeric (variable name).
		if token_id != ALNUM:
			syntax_error(INVALID_VARIABLE_NAME, line)

		lex()		# Next token may be comma (',') or ')'.
		if token_id == COMMA:
			formal_parameters_item()		# Next token must be in, inout or inandout.
		elif token_id == CLOSE_PARENTHESIS:
			move_file_pointer(-len(token))		# formal_parameters() checks for ')'.
			return
		else:
			syntax_error(INVALID_PARAMETER_TYPE, line)

	elif token_id == IN_OUT:

		lex()		# Next token must be alphanumeric (variable name).
		if token_id != ALNUM:
			syntax_error(INVALID_VARIABLE_NAME, line)

		lex()		# Next token may be comma (',') or ')'.
		if token_id == COMMA:
			formal_parameters_item()		# Next token must be in, inout or inandout.
		elif token_id == CLOSE_PARENTHESIS:
			move_file_pointer(-len(token))		# formal_parameters() checks for ')'.
			return
		else:
			syntax_error(INVALID_PARAMETER_TYPE, line)

	elif token_id == IN_AND_OUT:

		lex()		# Next token must be alphanumeric (variable name).
		if token_id != ALNUM:
			syntax_error(INVALID_VARIABLE_NAME, line)

		lex()		# Next token may be comma (',') or ')'.
		if token_id == COMMA:
			formal_parameters_item()		# Next token must be in, inout or inandout.
		elif token_id == CLOSE_PARENTHESIS:
			move_file_pointer(-len(token))		# formal_parameters() checks for ')'.
			return
		else:
			syntax_error(INVALID_PARAMETER_TYPE, line)

	else:
		syntax_error(INVALID_PARAMETER_TYPE, line)


def statements():

	statement()

	lex()
	if token_id == SEMICOLON:
		statements()
	else:
		move_file_pointer(-len(token))


def statement():

	lex()

	if token_id == IF:
		if_statement()
	elif token_id == WHILE:
		while_statement()
	elif token_id == DO_WHILE:
		dowhile_statement()
	elif token_id == LOOP:
		loop_statement()
	elif token_id == EXIT:
		exit_statement()
	elif token_id == FORCASE:
		forcase_statement()
	elif token_id == INCASE:
		incase_statement()
	elif token_id == RETURN:
		return_statement()
	elif token_id == INPUT:
		input_statement()
	elif token_id == PRINT:
		print_statement()
	elif token_id == ALNUM:
		assignment_statement()
	else:
		return		# ε.


def if_statement():

	lex()		# Next token must be '('.

	if token_id == OPEN_PARENTHESIS:
		condition()

		lex()		# Next token must be ')'.
		if token_id != CLOSE_PARENTHESIS:
			syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)

		lex()		# Next token must be 'then'.
		if token_id == THEN:
			statements()
			else_part()
		else:
			syntax_error(EXPECTED_THEN_STATEMENT, line)

		lex()		# Next token must be 'endif'.
		if token_id != END_IF:
			syntax_error(EXPECTED_ENDIF_STATEMENT, line)
	else:
		syntax_error(EXPECTED_OPEN_PARENTHESIS, line)


def else_part():

	lex()		# Next token may be 'else'.

	if token_id == ELSE:
		statements()
	else:
		move_file_pointer(-len(token))


def dowhile_statement():

	statements()

	lex()		# Next token must be 'enddowhile'.

	if token_id == END_DO_WHILE:

		lex()		# Next token must be '('.

		if token_id == OPEN_PARENTHESIS:
			condition()

			lex()		# Next token must be ')'.
			if token_id != CLOSE_PARENTHESIS:
				syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)
		else:
			syntax_error(EXPECTED_OPEN_PARENTHESIS, line)


def while_statement():

	lex()		# Next token must be '('.

	if token_id == OPEN_PARENTHESIS:
		condition()

		lex()		# Next token must be ')'.
		if token_id != CLOSE_PARENTHESIS:
			syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)

		statements()

		lex()		# Next token must be 'endwhile'.
		if token_id != END_WHILE:
			syntax_error(EXPECTED_ENDWHILE_STATEMENT, line)
	else:
		syntax_error(EXPECTED_OPEN_PARENTHESIS, line)


def loop_statement():

	statements()

	lex()		# Next token must be 'endloop'.
	if token_id != END_LOOP:
		syntax_error(EXPECTED_ENDLOOP_STATEMENT, line)


def exit_statement():

	return


def forcase_statement():

	lex()		# Next token may be 'when'.

	if token_id == WHEN:

		lex()		# Next token must be '('.
		if token_id == OPEN_PARENTHESIS:
			condition()

			lex()		# Next token must be ')'.
			if token_id != CLOSE_PARENTHESIS:
				syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)

			lex()		# Next token must be colon (':').
			if token_id == COLON:
				statements()
				forcase_statement()		# Check for another 'when'.
			else:
				syntax_error(EXPECTED_COLON_CHARACTER, line)
		else:
			syntax_error(EXPECTED_OPEN_PARENTHESIS, line)
	else:
		move_file_pointer(-len(token))

	lex()		# Next token must be 'default'.

	if token_id == DEFAULT:

		lex()		# Next token must be colon (':').
		if token_id == COLON:
			statements()
		else:
			syntax_error(EXPECTED_COLON_CHARACTER, line)

		lex()		# Next token must be 'enddefault'.
		if token_id != END_DEFAULT:
			syntax_error(EXPECTED_ENDDEFAULT_STATEMENT, line)
	else:
		syntax_error(EXPECTED_DEFAULT_STATEMENT, line)

	lex()		# Next token must be 'endforcase'.
	if token_id != END_FORCASE:
		syntax_error(EXPECTED_ENDFORCASE_STATEMENT, line)


def incase_statement():

	lex()		# Next token may be 'when'.

	if token_id == WHEN:

		lex()		# Next token must be '('.
		if token_id == OPEN_PARENTHESIS:
			condition()

			lex()		# Next token must be ')'.
			if token_id != CLOSE_PARENTHESIS:
				syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)

			lex()		# Next token must be colon (':').
			if token_id == COLON:
				statements()
				forcase_statement()		# Check for another 'when'.
			else:
				syntax_error(EXPECTED_COLON_CHARACTER, line)
		else:
			syntax_error(EXPECTED_OPEN_PARENTHESIS, line)
	else:
		move_file_pointer(-len(token))

	lex()		# Next token must be 'endincase'.

	if token_id != END_INCASE:
		syntax_error(EXPECTED_ENDINCASE_STATEMENT, line)


def return_statement():

	expression()


def print_statement():

	expression()


def assignment_statement():

	lex()		# Next token must be ':'.

	if token_id == COLON:
		lex()		# Next token must be '='.

		if token_id == EQUALS:

			expression()
		else:
			syntax_error(EXPECTED_ASSIGNMENT_SIGN, line)
	else:
		syntax_error(EXPECTED_ASSIGNMENT_SIGN, line)


def input_statement():

	lex()		# Next token must be alphanumeric.

	if token_id != ALNUM:
		syntax_error(EXPECTED_ALNUM_AS_INPUT, line)


def actual_parameters():

	lex()		# Next token must be '('.

	if token_id == OPEN_PARENTHESIS:
		actual_parameters_list()

		lex()		# Next token must be ')'.

		if token_id != CLOSE_PARENTHESIS:
			syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)
	else:
		syntax_error(EXPECTED_OPEN_PARENTHESIS, line)


def actual_parameters_list():

	lex()		# Check what's next.

	if token_id == CLOSE_PARENTHESIS:
		move_file_pointer(-len(token))		# actual_parameters() checks for ')'.
		return
	else:
		move_file_pointer(-len(token))
		actual_parameters_item()
		actual_parameters_list()


def actual_parameters_item():

	lex()		# Next token may be in, inout or inandout.

	if token_id == IN:

		expression()

		lex()		# Next token may be comma (',') or ')'.

		if token_id == COMMA:
			actual_parameters_item()		# Next token must be in, inout or inandout.
		elif token_id == CLOSE_PARENTHESIS:
			move_file_pointer(-len(token))		# actual_parameters() checks for ')'.
			return
		else:
			syntax_error(INVALID_PARAMETER_TYPE, line)

	elif token_id == IN_OUT:

		lex()		# Next token must be alphanumeric (variable name).
		if token_id != ALNUM:
			syntax_error(INVALID_VARIABLE_NAME, line)

		lex()		# Next token may be comma (',') or ')'.
		if token_id == COMMA:
			actual_parameters_item()		# Next token must be in, inout or inandout.
		elif token_id == CLOSE_PARENTHESIS:
			move_file_pointer(-len(token))		# actual_parameters() checks for ')'.
			return
		else:
			syntax_error(INVALID_PARAMETER_TYPE, line)

	elif token_id == IN_AND_OUT:

		lex()		# Next token must be alphanumeric (variable name).
		if token_id != ALNUM:
			syntax_error(INVALID_VARIABLE_NAME, line)

		lex()		# Next token may be comma (',') or ')'.
		if token_id == COMMA:
			actual_parameters_item()		# Next token must be in, inout or inandout.
		elif token_id == CLOSE_PARENTHESIS:
			move_file_pointer(-len(token))		# actual_parameters() checks for ')'.
			return
		else:
			syntax_error(INVALID_PARAMETER_TYPE, line)

	else:
		syntax_error(INVALID_PARAMETER_TYPE, line)


def condition():

	bool_term()

	lex()		# Next token may be 'or', if not, restore file pointer.

	if token_id == OR:
		condition()
	else:
		move_file_pointer(-len(token))


def bool_term():

	bool_factor()

	lex()		# Next token may be 'and', if not, restore file pointer.

	if token_id == AND:
		bool_term()
	else:
		move_file_pointer(-len(token))


def bool_factor():

	lex()		# Next token may be 'not', '[', or <expression>.

	if token_id == NOT:

		lex()		# Next token must be '['.
		if token_id == OPEN_BRACKETS:
			condition()

			lex()		# Next token must be ']'.
			if token_id != CLOSE_BRACKETS:
				syntax_error(EXPECTED_CLOSE_BRACKETS, line)
		else:
			syntax_error(EXPECTED_OPEN_BRACKETS, line)

	elif token_id == OPEN_BRACKETS:
		condition()

		lex()		# Next token must be ']'.
		if token_id != CLOSE_BRACKETS:
			syntax_error(EXPECTED_CLOSE_BRACKETS, line)

	else:
		move_file_pointer(-len(token))

		expression()
		relational_operator()
		expression()


def expression():

	optional_sign()
	term()

	lex()		# Check what's next.

	while token_id == PLUS or token_id == MINUS:

		move_file_pointer(-len(token))
		add_operator()
		term()

		lex()		# Check for another round.

	move_file_pointer(-len(token))


def term():

	factor()

	lex()		# Check what's next.

	while token_id == MULTIPLICATION or token_id == DIVISION:

		move_file_pointer(-len(token))
		multiplication_operator()
		factor()

		lex()		# Check for another round.

	move_file_pointer(-len(token))


def factor():

	lex()		# Check what's next.

	if token_id == OPEN_PARENTHESIS:

		expression()

		lex()		# Next token must be ')'
		if token_id != CLOSE_PARENTHESIS:
			syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)

	elif token_id == ALNUM:
		id_tail()

	else:		# FIX || Must ensure it's a constant.
		return


def id_tail():

	lex()		# Check for '('. If true, restore file pointer and call actual_parameters.

	if token_id == OPEN_PARENTHESIS:
		move_file_pointer(-len(token))
		actual_parameters()
	else:
		move_file_pointer(-len(token))


def relational_operator():

	lex()		# Next token must be a valid relational operator.

	if (
		token_id != EQUALS and token_id != LESS_OR_EQUAL and
		token_id != GREATER_OR_EQUAL and token_id != LESS_THAN and
		token_id != GREATER_THAN and token_id != DIFFERENT):

		syntax_error(INVALID_RELATIONAL_OPERATOR, line)


def add_operator():

	lex()		# Next token must be '+' or '-'.

	if token_id != PLUS and token_id != MINUS:
		syntax_error(EXPECTED_ADD_OPERATOR, line)


def multiplication_operator():

	lex()		# Next token must be "*" or '/'.

	if token_id != MULTIPLICATION and token_id != DIVISION:
		syntax_error(EXPECTED_MUL_OPERATOR, line)


def optional_sign():

	lex()		# Next token may be '+' or '-'.

	if token_id == PLUS or token_id == MINUS:
		return
	else:
		move_file_pointer(-len(token))


def restore_file_pointer():		# Restores file pointer to the point before latest lex() call.

	global file_position

	file.seek(file_position)


def move_file_pointer(offset):		# Moves file pointer a given amount (offset) forward or backward.

	file.seek(file.tell() + offset, os.SEEK_SET)


def syntax_error(err_id, line):

	if err_id == EXPECTED_PROGRAM_DECLARATION_ERR:
		print("Error in line", line, "| Expected 'program' keyword at the start of every Starlet file.")
	elif err_id == EXPECTED_ENDPROGRAM_STATEMENT:
		print("Error in line", line, "| Expected 'endprogram' keyword at the end of every Starlet file.")
	elif err_id == INVALID_PROGRAM_NAME_ERR:
		print("Error in line", line, "| Invalid program name.")
	elif err_id == INVALID_VARIABLE_NAME:
		print("Error in line", line, "| Invalid variable name.")
	elif err_id == EXPECTED_END_OF_DECLARE:
		print("Error in line", line, "| Expected ';' character at the end of 'declare' statement.")
	elif err_id == INVALID_FUNCTION_NAME:
		print("Error in line", line, "| Invalid function name.")
	elif err_id == EXPECTED_ENDFUNCTION_STATEMENT:
		print("Error in line", line, "| Expected 'endfunction' keyword.")
	elif err_id == EXPECTED_CLOSE_PARENTHESIS:
		print("Error in line", line, "| Expected close parenthesis.")
	elif err_id == EXPECTED_OPEN_PARENTHESIS:
		print("Error in line", line, "| Expected open parenthesis.")
	elif err_id == EXPECTED_THEN_STATEMENT:
		print("Error in line", line, "| Expected 'then' statement.")
	elif err_id == EXPECTED_ENDIF_STATEMENT:
		print("Error in line", line, "| Expected 'endif' statement.")
	elif err_id == EXPECTED_WHILE_STATEMENT:
		print("Error in line", line, "| Expected 'while' statement.")
	elif err_id == EXPECTED_ENDLOOP_STATEMENT:
		print("Error in line", line, "| Expected 'endloop' statement.")
	elif err_id == EXPECTED_COLON_CHARACTER:
		print("Error in line", line, "| Expected ':' character after every 'when' statement.")
	elif err_id == EXPECTED_WHEN_STATEMENT:
		print("Error in line", line, "| Expected 'when' statement.")
	elif err_id == EXPECTED_DEFAULT_STATEMENT:
		print("Error in line", line, "| Expected 'default' statement.")
	elif err_id == EXPECTED_ENDDEFAULT_STATEMENT:
		print("Error in line", line, "| Expected 'enddefault' statement.")
	elif err_id == EXPECTED_ENDFORCASE_STATEMENT:
		print("Error in line", line, "| Expected 'endforcase' statement.")
	elif err_id == EXPECTED_ENDINCASE_STATEMENT:
		print("Error in line", line, "| Expected 'endincase' statement.")
	elif err_id == EXPECTED_ENDWHILE_STATEMENT:
		print("Error in line", line, "| Expected 'endwhile' statement.")
	elif err_id == EXPECTED_ALNUM_AS_INPUT:
		print("Error in line", line, "| Expected alphanumeric value as user input.")
	elif err_id == INVALID_RELATIONAL_OPERATOR:
		print("Error in line", line, "| Expected a valid relational operator.")
	elif err_id == EXPECTED_ADD_OPERATOR:
		print("Error in line", line, "| Expected a valid add operator.")
	elif err_id == EXPECTED_MUL_OPERATOR:
		print("Error in line", line, "| Expected multiplication/division operator.")
	elif err_id == EXPECTED_ASSIGNMENT_SIGN:
		print("Error in line", line, "| Expected assignment sign.")
	elif err_id == EXPECTED_OPEN_BRACKETS:
		print("Error in line", line, "| Expected open brackets.")
	elif err_id == EXPECTED_CLOSE_BRACKETS:
		print("Error in line", line, "| Expected close brackets.")
	elif err_id == EXPECTED_SEMICOLON:
		print("Error in line", line, "| Expected semicolon.")
	elif err_id == EXPECTED_VARIABLE_NAME_AFTER_COMMA:
		print("Error in line", line, "| Expected a variable name after comma.")
	elif err_id == INVALID_PARAMETER_TYPE:
		print("Error in line", line, "| Invalid parameter type. Variables should be passed as in, inout or inandout only.")

	exit(0)


main()
