
from global_variables import *
from main import *


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