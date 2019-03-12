
from global_variables import *
from lex import *
import os


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
