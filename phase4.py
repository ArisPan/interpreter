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

# -----------------------------------
# 		Symbol Table Classes
# -----------------------------------


# Class "quad" contains attributes of each quad plus methods for editing respective attributes.
class quad:

	def __init__(self, label, op, x, y, z):

		self.label = label
		self.op = op
		self.x = x
		self.y = y
		self.z = z

	def get_label(self):
		return self.label

	def get_op(self):
		return self.op

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_z(self):
		return self.z

	def get_quad(self):
		return self.label + '{} {} {} {}'.format(self.op, self.x, self.y, self.z)

	def print_quad(self):
		print(str(self.label) + " " + str(self.op) + " " + str(self.x) + " " + str(self.y) + " " + str(self.z))

	def set_op(self, op):
		self.op = op

	def set_x(self, x):
		self.x = x

	def set_y(self, y):
		self.y = y

	def set_z(self, z):
		self.z = z


class scope:

	def __init__(self, nesting_level, entity_list=list(), next_offset=12, next_scope=None):
		self.nesting_level = nesting_level
		self.entity_list = entity_list
		self.next_offset = next_offset
		self.next_scope = next_scope

	def set_next(self, new_scope):
		self.next_scope = new_scope

	def get_next(self):
		return self.next_scope

	def get_next_offset(self) -> int:
		return self.next_offset

	def increase_next_offset(self):
		self.next_offset += 4

	def get_frame_length(self) -> int:
		return self.next_offset - 4

	def get_nesting_level(self) -> int:
		return self.nesting_level

	def get_all_entities(self):
		return self.entity_list

	def add_entity(self, new_entity):
		self.entity_list.append(new_entity)

	def get_latest_entity(self):
		return self.entity_list[len(self.entity_list) - 1]

	def delete_scope(self, main_scope):

		temp_scope = main_scope
		while temp_scope.get_nesting_level() != (self.nesting_level - 1):
			temp_scope = temp_scope.get_next()

			if temp_scope is None:
				break

		if temp_scope is not None:
			temp_scope.set_next(None)

		return temp_scope


# Class "argument" contains attributes for every argument. "Mode" may be CV, REF, CP. "Type" may be INT.
class argument:

	def __init__(self, mode, _type):		# _type because "type" is a python function.
		self.mode = mode
		self.type = _type

	def get_mode(self):
		return self.mode

	def get_type(self):
		return self._type


# Class "entity" contains attributes for every entity (variable, constant, function, argument, temporary variable).
class entity:

	def __init__(self, name, _type, offset, frame_length, nesting_level):
		self.name = name
		self._type = _type
		self.offset = offset
		self.frame_length = frame_length
		self.nesting_level = nesting_level

	def get_name(self):
		return self.name

	def get_type(self):
		return self._type

	def get_offset(self):
		return self.offset

	def get_frame_length(self):
		return self.frame_length

	def get_nesting_level(self):
		return self.nesting_level

	@staticmethod
	def set_arguments(func, new_argument_list):

		existing_argument_list = func.get_arguments()

		for x in range(len(new_argument_list)):

			existing_argument_list.append(new_argument_list[x])


# Class "variable" inherits from "entity". Includes an extra attribute, "var_type".
class variable(entity):

	def __init__(self, name, var_type, offset, frame_length, nesting_level):
		self.name = name
		self.var_type = var_type
		self.offset = offset
		self.frame_length = frame_length
		self.nesting_level = nesting_level
		self._type = "Variable"		# Updates _type variable of base class "entity".

	def get_variable_type(self):
		return self.var_type


# Class "parameter" inherits from "entity". Includes two extra attributes, "par_type" & "par_mode".
class parameter(entity):

	def __init__(self, name, par_type, par_mode, offset, frame_length, nesting_level):
		self.name = name
		self.par_type = par_type
		self.par_mode = par_mode
		self.offset = offset
		self.frame_length = frame_length
		self.nesting_level = nesting_level
		self._type = "Parameter"		# Updates _type variable of base class "entity".

	def get_parameter_type(self):
		return self.par_type

	def get_parameter_mode(self):		# CV, REF, CP
		return self.par_mode


# Class "temp" inherits from "entity".
class temp(entity):

	def __init__(self, name, offset, frame_length, nesting_level):
		self.name = name
		self.offset = offset
		self.frame_length = frame_length
		self.nesting_level = nesting_level
		self._type = "Temporary Variable"		# Updates _type variable of base class "entity".


# Class "function" inherits from "entity". Includes three extra attributes, "return_type", "parameters" & "start_quad".
class function(entity):

	def __init__(self, name, return_type, start_quad, frame_length, nesting_level, parameters=list()):
		self.name = name
		self.return_type = return_type
		self.parameters = parameters
		self.start_quad = start_quad
		self.frame_length = frame_length
		self.nesting_level = nesting_level
		self._type = "Function"

	def get_start_quad(self):
		return self.start_quad

	def set_start_quad(self, new_start_quad):
		self.start_quad = new_start_quad

	def get_arguments(self):
		return self.parameters


# Intermediate code global variables.
quad_list = []		# A list containing all quads.
quad_label = 0		# Base label/index of quads. With every new quad, quad_label will be increased by 1.
temp_index = 0		# Number of temporary variable (T_1, T_2 etc).

# Symbol table Global variables.
main_scope = scope(0)
tail_scope = main_scope
number_of_parameters = 0
program_name = ""
block_level = 1		# Block nesting level (program block is 1). With every new block, increase by 1.

# -----------------------------------
# Intermediate Code Utility Functions
# -----------------------------------


def find_entity(entity_name):

	global main_scope

	new_scope = main_scope
	new_entity_list = list()
	target_entity = None		# If the entity we are looking for exists, store it here and return.

	while new_scope is not None:
		new_entity_list = new_scope.get_all_entities()

		for x in new_entity_list:
			if x.get_name() == entity_name:
				target_entity = x

		new_scope = new_scope.get_next()

	if target_entity is None:
		print("Entity " + str(entity_name) + " not found.\n")
		exit(0)

	return target_entity


def print_scope():

	main_scope.print()


def next_quad() -> int:

	global quad_list

	return len(quad_list)		# Returns the index of next quad to be created.


def gen_quad(op, x, y, z):

	global quad_list
	global quad_label

	quad_list.append(quad(quad_label, op, x, y, z))
	quad_label += 1


def new_temp():

	global temp_index
	global tail_scope

	temp_index += 1

	entity_temporary_list = tail_scope.get_all_entities()
	new_temp_nesting_level = entity_temporary_list[len(entity_temporary_list) - 1].get_nesting_level()

	tail_scope.add_entity(temp("T_" + str(temp_index), tail_scope.get_next_offset(), tail_scope.get_next_offset(), new_temp_nesting_level))
	tail_scope.increase_next_offset()

	return "T_" + str(temp_index)


def empty_list():		# Returns a new, empty list of quad labels.

	return list()


def make_list(new_label):		# Returns a new list of quad labels with "new_label" added to it.

	new_list = list()
	new_list.append(new_label)

	return new_list


def merge(list_1, list_2):		# Returns a new list of quad labels by merging "list_1" & "list_2".

	if(len(list_1) == 0):
		return list_2
	elif (len(list_2) == 0):
		return list_1

	list_3 = list()

	for x in list_1:
		list_3.append(x)

	for x in list_2:
		list_3.append(x)

	return list_3


def backpatch(list_full_of_holes, z):

	if(len(list_full_of_holes) == 0):
		return

	for x in range(len(list_full_of_holes)):		# "list_full_of_holes" contains labels (int) of quads with a blank z.

		quad_list[list_full_of_holes[x]].set_z(z)


def copy_list(list1, list2):		# Copies list1 to list2.

	list2.clear()

	for x in list1:
		list2.append(x)

# -----------------------------------
# 		Final Code Functions
# -----------------------------------


def gnlvcode(variable):		# Transfer the address of a non-local variable to $t0.

	global tail_scope

	new_entity = find_entity(variable)
	current_scope_level = tail_scope.get_nesting_level()
	new_entity_scope_level = new_entity.get_nesting_level()

	while current_scope_level != new_entity_scope_level:
		print("lw $t0, -4($t0)")
		new_entity_scope_level += 1

	print("add $t0, $t0 -", new_entity.get_offset())


def loadvr(v, r):		# Data transfer to register r.

	global tail_scope

	new_entity = find_entity(v)
	current_scope_level = tail_scope.get_nesting_level()
	new_entity_scope_level = new_entity.get_nesting_level()

	if v.isdigit():
		print("li $t", r, ", ", v)
		return

	if new_entity_scope_level == 0:
		print("lw $t", r, ", -", new_entity.get_offset(), "($s0)")

	elif current_scope_level == new_entity_scope_level:

		if new_entity.get_type() == "Parameter":
			if new_entity.get_parameter_mode() == "CV":
				print("lw $t", r, ", -", new_entity.get_offset(), "($sp)")

			elif new_entity.get_parameter_mode() == "REF":
				print("lw $t0, -", new_entity.get_offset(), "($sp)")
				print("lw $t", r, ", ($t0)")

		elif new_entity.get_type() == "Variable" or new_entity.get_type() == "Temp":
			print("lw $t", r, ", -", new_entity.get_offset(), "($sp)")

	elif new_entity_scope_level < current_scope_level:

		if new_entity.get_type() == "Parameter":
			if new_entity.get_parameter_mode() == "CV":
				gnlvcode(v)
				print("lw $t", r, ", ($t0)")

			elif new_entity.get_parameter_mode() == "REF":
				gnlvcode(v)
				print("lw $t0, ($t0)")
				print("lw $t", r, ", ($t0)")

		elif new_entity.get_type() == "Variable":
			gnlvcode(v)
			print("lw $t", r, ", ($t0)")


def storerv(r, v):		# Data transfer from register r to memory (variable v).

	global tail_scope

	new_entity = find_entity(v)
	current_scope_level = tail_scope.get_nesting_level()
	new_entity_scope_level = new_entity.get_nesting_level()

	if v.isdigit():
		print("li $t", r, ", ", v)
		return

	if new_entity_scope_level == 0:
		print("sw $t", r, ", -", new_entity.get_offset(), "($s0)")

	elif current_scope_level == new_entity_scope_level:

		if new_entity.get_type() == "Parameter":
			if new_entity.get_parameter_mode() == "CV":
				print("sw $t", r, ", -", new_entity.get_offset(), "($sp)")

			elif new_entity.get_parameter_mode == "REF":
				print("lw $t0, -", new_entity.get_offset(), "($sp)")
				print("sw $t", r, ", ($t0)")

		elif new_entity.get_type() == "variable" or new_entity.get_type() == "Temp":
			print("sw $t", r, ", -", new_entity.get_offset(), "($sp)")

	elif new_entity_scope_level < current_scope_level:

		if new_entity.get_type() == "Parameter":
			if new_entity.get_parameter_mode() == "CV":
				gnlvcode(v)
				print("sw $t", r, ", ($t0)")

			elif new_entity.get_parameter_mode() == "REF":
				gnlvcode(v)
				print("lw $t0, ($t0)")
				print("sw $t", r, ", ($t0)")

		elif new_entity.get_type() == "Variable":
			gnlvcode(v)
			print("sw $t", r, ", ($t0)")


def relop(operation, x, y, z):

	loadvr(x, 1)
	loadvr(y, 2)

	if operation == "=":
		branch = "beq"
	elif operation == "<":
		branch = "blt"
	elif operation == ">":
		branch = "bgt"
	elif operation == "<=":
		branch = "ble"
	elif operation == ">=":
		branch = "bge"
	elif operation == "<>":
		branch = "bne"

	print(branch + "$t1, $t2," + z)


def oper(operation, x, y, z):

	loadvr(x, 1)
	loadvr(y, 2)

	if operation == "+":
		mips_operation = "add"
	elif operation == "-":
		mips_operation = "sub"
	elif operation == "*":
		mips_operation = "mul"
	elif operation == "/":
		mips_operation = "div"

	print(mips_operation + "$t1, $t1, $t2")

	storerv(1, z)


def parameters(quad):

	global tail_scope
	global number_of_parameters

	number_of_parameters += 1

	print("add $fp, $sp,", tail_scope.get_frame_length())

	if quad.get_y() == "CV":
		loadvr(quad.get_x(), 0)
		print("sw $t0, -(12 + 4", number_of_parameters, ")($fp)")

	elif quad.get_y == "REF":

		new_entity = find_entity(quad.get_x())
		current_scope_level = tail_scope.get_nesting_level()
		new_entity_scope_level = new_entity.get_nesting_level()

		if new_entity_scope_level == current_scope_level:

			if new_entity.get_type() == "Parameter":
				if new_entity.get_parameter_mode == "CV":
					print("add $t0, $sp, -", new_entity.get_offset())
					print("sw $t0, -(12 + 4", number_of_parameters, ")($fp)")

				elif new_entity.get_parameter_mode == "REF":
					print("lw $t0, -", new_entity.get_offset(), "($sp)")
					print("sw $t0, -(12 + 4", number_of_parameters, ")($fp)")

			elif new_entity.get_type() == "Variable":
				print("add $t0, $sp, -", new_entity.get_offset())
				print("sw $t0, -(12 + 4", number_of_parameters, ")($fp)")

		else:
			if new_entity.get_type() == "Parameter":
				if new_entity.get_parameter_mode == "CV":
					gnlvcode(quad.get_x)
					print("sw $t0, -(12 + 4", number_of_parameters, ")($fp)")

				elif new_entity.get_parameter_mode == "REF":
					gnlvcode(quad.get_x)
					print("lw $t0, ($t0)")
					print("sw $t0, -(12 + 4", number_of_parameters, ")($fp)")

				elif new_entity.get_type() == "Variable":
					gnlvcode(quad.get_x)
					print("sw $t0, -(12 + 4", number_of_parameters, ")($fp)")

	elif quad.get_y == "RET":

		new_entity = find_entity(quad.get_x())

		print("add $t0, $sp, -", new_entity.get_offset())
		print("sw $t0, -8($fp)")


def function_call(quad):

	global tail_scope

	new_entity = find_entity(quad.get_x())
	current_scope_level = tail_scope.get_nesting_level()		# Caller
	new_entity_scope_level = new_entity.get_nesting_level()		# Callee

	if new_entity.get_type() == "Function":

		print("sw $ra, ($sp)")

		if current_scope_level == new_entity_scope_level:
			print("lw $t0, -4($sp)")
			print("sw $t0, -4($fp)")

		else:
			print("sw $sp, -4($fp)")

		print("add $sp, $sp,", tail_scope.get_frame_length())
		print("jal ", new_entity.get_start_quad())				# FIX || Unsure. Check PDF 7, page 32.
		print("lw $ra, ($sp)")
		print("jr $ra")
		print("add $sp, $sp, -", tail_scope.get_frame_length())


def generate_final_code(quad):		# FIX || Missing stuff. Check PDF 7, page 34.

	global program_name

	operation = quad.get_op()

	if operation == "Begin Block" and quad.get_x() == program_name:
		print("L0:")

	if operation == "Begin Block" and quad.get_x() != program_name:
		print("L", quad.get_label(), ":")

	if operation != "Begin Block" and quad.get_x() != program_name:
		print("L", quad.get_label(), ":")

	if operation == "jump":
		print("j L", quad.get_z())

	elif operation == "=" or operation == "<>" or operation == "<" or operation == ">" or operation == "<=" or operation == ">=":
		relop(quad.get_op(), quad.get_x(), quad.get_y(), quad.get_z())

	elif operation == ":=":
		loadvr(quad.get_x(), 1)
		storerv(1, quad.get_z())

	elif operation == "+" or operation == "-" or operation == "*" or operation == "/":
		oper(quad.get_op(), quad.get_x(), quad.get_y(), quad.get_z())

	elif operation == "out":
		print("li $v0, 1")
		print("li $a0," + quad.get_x())
		print("syscall")

	elif operation == "in":
		print("li $v0, 5")
		print("syscall")

	elif operation == "retv":
		loadvr(quad.get_x(), 1)
		print("lw $t0, -8($sp)")
		print("sw $t1, ($t0)")

	elif operation == "par":
		parameters(quad)

	elif operation == "call":
		function_call(quad)

# -----------------------------------
# 				main()
# -----------------------------------


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

	for x in range(len(quad_list)):
		quad_list[x].print_quad()

	for x in range(len(quad_list)):
		generate_final_code(quad_list[x])
		quad_list.remove(quad_list[x])

# -----------------------------------
# 				lex()
# -----------------------------------


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

# -----------------------------------
# 			  syntax()
# -----------------------------------


def syntax():
	program()


def program():

	global program_name
	global quad_list

	lex()		# First token must be 'program'.

	if token_id == PROGRAM:

		lex()		# Next token must be a valid program id (alphanumeric).
		if token_id == ALNUM:

			program_name = token

			print("j Lmain")

			block(token, 1)

			lex()		# Next (and final) token must be 'endprogram'.
			if token_id == END_PROGRAM:

				gen_quad("Halt", "_", "_", "_")

		# 		for x in range(len(quad_list)):
		# 			generate_final_code(quad_list[0])
		# 			quad_list.remove(quad_list[0])
		# 	else:
		# 		syntax_error(EXPECTED_ENDPROGRAM_STATEMENT, line)

		else:
			syntax_error(INVALID_PROGRAM_NAME_ERR, line)
	else:
		syntax_error(EXPECTED_PROGRAM_DECLARATION_ERR, line)


def block(block_name, new_block_level):

	global main_scope
	global tail_scope
	global block_level
	global quad_list

	declarations()

	gen_quad("Begin Block", block_name, "_", "_")

	subprograms()
	statements()

	gen_quad("End Block", block_name, "_", "_")

	if new_block_level > 1:		# Every other block, except program block.

		start_quad = quad_list[new_block_level].get_label()
		new_entity = find_entity(block_name)
		new_entity.set_start_quad(start_quad)

		temp_scope = main_scope
		while temp_scope.get_nesting_level() != (tail_scope.get_nesting_level() - 1):
			temp_scope = temp_scope.get_next()

		tail_scope = tail_scope.delete_scope(main_scope)

		block_level -= 1


def declarations():

	lex()		# Next token may be 'declare', if not, restore file pointer.

	if token_id == DECLARE:
		variable_list()

		lex()		# Every 'declare' statement must end with semicolon (';').
		if token_id != SEMICOLON:
			syntax_error(EXPECTED_SEMICOLON, line)
		declarations()		# Check for another 'declare' statement.
	else:
		move_file_pointer(-len(token))


def variable_list():

	global tail_scope
	global token

	lex()		# Next token may be variable name (alphanumeric), semicolon or ε.

	if token_id == ALNUM:

		tail_scope.add_entity(variable(token, "int", tail_scope.get_next_offset(), tail_scope.get_next_offset(), tail_scope.get_nesting_level()))
		tail_scope.increase_next_offset()

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

	function_name = ""

	lex()		# Check for function declaration.

	if token_id == FUNCTION:

		lex()		# Next token must be a valid function name.

		if token_id == ALNUM:

			function_name = token
			tail_scope.add_entity(function(function_name, "int", next_quad(), tail_scope.get_next_offset(), tail_scope.get_nesting_level() + 1))
			function_body(function_name)

			lex()		# Next (and final) token of a function declaration must be 'endfunction'.

	# 		if token_id != END_FUNCTION:
	# 			syntax_error(EXPECTED_ENDFUNCTION_STATEMENT, line)
			subprogram()
	else:
		move_file_pointer(-len(token))


def function_body(function_name):

	global block_level
	block_level += 1

	formal_parameters()
	block(function_name, block_level)


def formal_parameters():

	global tail_scope

	lex()		# Next token must be '('.

	if token_id == OPEN_PARENTHESIS:

		argument_list = list()
		temp_scope1 = tail_scope
		temp_scope2 = scope(tail_scope.get_nesting_level() + 1)
		tail_scope.set_next(temp_scope2)
		tail_scope = temp_scope2

		formal_parameters_list(argument_list)

		lex()		# Next token must be ')'.
		if token_id != CLOSE_PARENTHESIS:
			syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)

		func = temp_scope1.get_latest_entity()
		# temp_scope1.get_latest_entity().set_arguments(func, argument_list)		# FIX || "temp_scope1.get_latest_entity()" returns type parameter. Needs casting to function.


def formal_parameters_list(argument_list):

	lex()		# Check what's next.

	if token_id == CLOSE_PARENTHESIS:
		move_file_pointer(-len(token))		# formal_parameters() checks for ')'.
		return
	else:
		move_file_pointer(-len(token))
		formal_parameters_item(argument_list)
		formal_parameters_list(argument_list)


def formal_parameters_item(argument_list):

	global tail_scope

	lex()		# Next token may be in, inout or inandout.

	if token_id == IN:

		argument_list.append(argument("CV", "int"))

		lex()		# Next token must be alphanumeric (variable name).
		if token_id != ALNUM:
			syntax_error(INVALID_VARIABLE_NAME, line)

		tail_scope.add_entity(parameter(token, "int", "CV", tail_scope.get_next_offset(), tail_scope.get_next_offset(), tail_scope.get_nesting_level()))
		tail_scope.increase_next_offset()

		lex()		# Next token may be comma (',') or ')'.
		if token_id == COMMA:
			formal_parameters_item(argument_list)		# Next token must be in, inout or inandout.
		elif token_id == CLOSE_PARENTHESIS:
			move_file_pointer(-len(token))		# formal_parameters() checks for ')'.
			return
		else:
			syntax_error(INVALID_PARAMETER_TYPE, line)

	elif token_id == IN_OUT:

		argument_list.append(argument("REF", "int"))

		lex()		# Next token must be alphanumeric (variable name).
		if token_id != ALNUM:
			syntax_error(INVALID_VARIABLE_NAME, line)

		tail_scope.add_entity(parameter(token, "int", "REF", tail_scope.get_next_offset(), tail_scope.get_next_offset(), tail_scope.get_nesting_level()))
		tail_scope.increase_next_offset()

		lex()		# Next token may be comma (',') or ')'.
		if token_id == COMMA:
			formal_parameters_item(argument_list)		# Next token must be in, inout or inandout.
		elif token_id == CLOSE_PARENTHESIS:
			move_file_pointer(-len(token))		# formal_parameters() checks for ')'.
			return
		else:
			syntax_error(INVALID_PARAMETER_TYPE, line)

	elif token_id == IN_AND_OUT:

		argument_list.append(argument("CP", "int"))

		lex()		# Next token must be alphanumeric (variable name).
		if token_id != ALNUM:
			syntax_error(INVALID_VARIABLE_NAME, line)

		tail_scope.add_entity(parameter(token, "int", "CP", tail_scope.get_next_offset(), tail_scope.get_next_offset(), tail_scope.get_nesting_level()))
		tail_scope.increase_next_offset()

		lex()		# Next token may be comma (',') or ')'.
		if token_id == COMMA:
			formal_parameters_item(argument_list)		# Next token must be in, inout or inandout.
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

	# global token

	Btrue = empty_list()
	Bfalse = empty_list()

	lex()		# Next token must be '('.

	if token_id == OPEN_PARENTHESIS:
		condition(Btrue, Bfalse)

		lex()		# Next token must be ')'.

		if token_id != CLOSE_PARENTHESIS:
			syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)

		lex()		# Next token must be 'then'.

		if token_id == THEN:
			statements()

			if_list = empty_list()
			if_list = make_list(next_quad())
			gen_quad("jump", "_", "_", "_")
			backpatch(Bfalse, next_quad())

			else_part(if_list)
		else:
			syntax_error(EXPECTED_THEN_STATEMENT, line)

		lex()		# Next token must be 'endif'.

	# 	if token_id != END_IF:
	# 		syntax_error(EXPECTED_ENDIF_STATEMENT, line)
	else:
		syntax_error(EXPECTED_OPEN_PARENTHESIS, line)


def else_part(if_list):

	lex()		# Next token may be 'else'.

	if token_id == ELSE:
		statements()
	else:
		move_file_pointer(-len(token))

	backpatch(if_list, next_quad())


def dowhile_statement():

	Btrue = empty_list()
	Bfalse = empty_list()
	start_quad = next_quad()

	statements()

	lex()		# Next token must be 'enddowhile'.

	if token_id == END_DO_WHILE:

		lex()		# Next token must be '('.

		if token_id == OPEN_PARENTHESIS:
			condition(Btrue, Bfalse)

			lex()		# Next token must be ')'.
			if token_id == CLOSE_PARENTHESIS:
				backpatch(Btrue, start_quad)
			else:
				syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)
		else:
			syntax_error(EXPECTED_OPEN_PARENTHESIS, line)


def while_statement():

	Btrue = empty_list()
	Bfalse = empty_list()
	jump_at = 0

	lex()		# Next token must be '('.

	if token_id == OPEN_PARENTHESIS:

		jump_at = next_quad()
		condition(Btrue, Bfalse)

		lex()		# Next token must be ')'.
		if token_id != CLOSE_PARENTHESIS:
			syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)

		statements()
		gen_quad("jump", "_", "_", jump_at)
		backpatch(Bfalse, next_quad())

		lex()		# Next token must be 'endwhile'.
		if token_id != END_WHILE:
			syntax_error(EXPECTED_ENDWHILE_STATEMENT, line)
	else:
		syntax_error(EXPECTED_OPEN_PARENTHESIS, line)


def loop_statement():

	jump_at = next_quad()

	statements()
	gen_quad("jump", "_", "_", jump_at)

	lex()		# Next token must be 'endloop'.
	if token_id != END_LOOP:
		syntax_error(EXPECTED_ENDLOOP_STATEMENT, line)


def exit_statement():

	return


def forcase_statement():

	Btrue = empty_list()
	Bfalse = empty_list()
	starting_point = next_quad()

	lex()		# Next token may be 'when'.

	if token_id == WHEN:

		lex()		# Next token must be '('.
		if token_id == OPEN_PARENTHESIS:
			condition(Btrue, Bfalse)

			lex()		# Next token must be ')'.
			if token_id != CLOSE_PARENTHESIS:
				syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)

			lex()		# Next token must be colon (':').
			if token_id == COLON:

				backpatch(Btrue, next_quad())

				statements()

				gen_quad("jump", "_", "_", starting_point)
				backpatch(Bfalse, next_quad())

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

	Btrue = empty_list()
	Bfalse = empty_list()
	starting_point = next_quad()
	temp = new_temp()
	gen_quad(":=", "1", "_", temp)

	lex()		# Next token may be 'when'.

	if token_id == WHEN:

		lex()		# Next token must be '('.
		if token_id == OPEN_PARENTHESIS:
			condition(Btrue, Bfalse)

			lex()		# Next token must be ')'.
			if token_id != CLOSE_PARENTHESIS:
				syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)

			lex()		# Next token must be colon (':').
			if token_id == COLON:

				backpatch(Btrue, next_quad())

				statements()

				gen_quad(":=", "0", "_", temp)
				backpatch(Bfalse, next_quad())

				incase_statement()		# Check for another 'when'.
			else:
				syntax_error(EXPECTED_COLON_CHARACTER, line)
		else:
			syntax_error(EXPECTED_OPEN_PARENTHESIS, line)
	else:
		move_file_pointer(-len(token))

	gen_quad(":=", temp, "0", starting_point)

	lex()		# Next token must be 'endincase'.

	if token_id != END_INCASE:
		syntax_error(EXPECTED_ENDINCASE_STATEMENT, line)


def return_statement():

	expression_return_value = empty_list()

	expression(expression_return_value)
	gen_quad("retv", expression_return_value[0], "_", "_")


def print_statement():

	expression_return_value = empty_list()

	expression(expression_return_value)
	gen_quad("out", expression_return_value[0], "_", "_")


def assignment_statement():

	assign_to = token
	expression_return_value = empty_list()

	lex()		# Next token must be ':'.

	if token_id == COLON:
		lex()		# Next token must be '='.

		if token_id == EQUALS:

			expression(expression_return_value)
			if(len(expression_return_value) == 0):
				expression_return_value.append("_")
			gen_quad(":=", expression_return_value[0], "_", assign_to)
		else:
			syntax_error(EXPECTED_ASSIGNMENT_SIGN, line)
	else:
		syntax_error(EXPECTED_ASSIGNMENT_SIGN, line)


def input_statement():

	lex()		# Next token must be alphanumeric.

	if token_id != ALNUM:
		syntax_error(EXPECTED_ALNUM_AS_INPUT, line)

	gen_quad("inp", token, "_", "_")


def actual_parameters():

	parameters_list = empty_list()

	lex()		# Next token must be '('.

	if token_id == OPEN_PARENTHESIS:
		actual_parameters_list(parameters_list)

		lex()		# Next token must be ')'.

		if token_id != CLOSE_PARENTHESIS:
			syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)
	else:
		syntax_error(EXPECTED_OPEN_PARENTHESIS, line)

	for i in range(len(parameters_list)):
		gen_quad("pars", parameters_list[i], "CV", "_")


def actual_parameters_list(parameters_list):

	lex()		# Check what's next.

	if token_id == CLOSE_PARENTHESIS:
		move_file_pointer(-len(token))		# actual_parameters() checks for ')'.
		return
	else:
		move_file_pointer(-len(token))
		actual_parameters_item(parameters_list)
		actual_parameters_list(parameters_list)


def actual_parameters_item(parameters_list):

	lex()		# Next token may be in, inout or inandout.

	if token_id == IN:

		exp = empty_list()

		expression(exp)
		parameters_list.append(exp[0])

		lex()		# Next token may be comma (',') or ')'.

		if token_id == COMMA:
			actual_parameters_item(parameters_list)		# Next token must be in, inout or inandout.
		elif token_id == CLOSE_PARENTHESIS:
			move_file_pointer(-len(token))		# actual_parameters() checks for ')'.
			return
		else:
			syntax_error(INVALID_PARAMETER_TYPE, line)

	elif token_id == IN_OUT:

		lex()		# Next token must be alphanumeric (variable name).
		if token_id != ALNUM:
			syntax_error(INVALID_VARIABLE_NAME, line)

		gen_quad("par", token, "REF", "_")

		lex()		# Next token may be comma (',') or ')'.
		if token_id == COMMA:
			actual_parameters_item(parameters_list)		# Next token must be in, inout or inandout.
		elif token_id == CLOSE_PARENTHESIS:
			move_file_pointer(-len(token))		# actual_parameters() checks for ')'.
			return
		else:
			syntax_error(INVALID_PARAMETER_TYPE, line)

	elif token_id == IN_AND_OUT:

		lex()		# Next token must be alphanumeric (variable name).
		if token_id != ALNUM:
			syntax_error(INVALID_VARIABLE_NAME, line)

		gen_quad("par", token, "CP", "_")

		lex()		# Next token may be comma (',') or ')'.
		if token_id == COMMA:
			actual_parameters_item(parameters_list)		# Next token must be in, inout or inandout.
		elif token_id == CLOSE_PARENTHESIS:
			move_file_pointer(-len(token))		# actual_parameters() checks for ')'.
			return
		else:
			syntax_error(INVALID_PARAMETER_TYPE, line)

	else:
		syntax_error(INVALID_PARAMETER_TYPE, line)


def condition(Btrue, Bfalse):

	Qtrue = empty_list()
	Qfalse = empty_list()

	bool_term(Qtrue, Qfalse)

	copy_list(Qtrue, Btrue)		# Copy Qtrue to Btrue
	copy_list(Qfalse, Bfalse)		# Copy Qfalse to Bfalse

	lex()		# Next token may be 'or', if not, restore file pointer.

	if token_id == OR:

		backpatch(Bfalse, next_quad())

		condition(Qtrue, Qfalse)

		Btrue = merge(Btrue, Qtrue)
		Bfalse = Qfalse
	else:
		move_file_pointer(-len(token))


def bool_term(Qtrue, Qfalse):

	Rtrue = empty_list()
	Rfalse = empty_list()

	bool_factor(Rtrue, Rfalse)

	copy_list(Rtrue, Qtrue)		# Copy Rtrue to Qtrue.
	copy_list(Rfalse, Qfalse)

	lex()		# Next token may be 'and', if not, restore file pointer.

	if token_id == AND:

		backpatch(Qtrue, next_quad())

		bool_term(Rtrue, Rfalse)

		Qfalse = merge(Qfalse, Rfalse)
		Qtrue = Rtrue
	else:
		move_file_pointer(-len(token))


def bool_factor(Rtrue, Rfalse):

	Qtrue = empty_list()
	Qfalse = empty_list()
	operation = ""

	lex()		# Next token may be 'not', '[', or <expression>.

	if token_id == NOT:

		lex()		# Next token must be '['.
		if token_id == OPEN_BRACKETS:
			condition(Qfalse, Qtrue)

			lex()		# Next token must be ']'.
			if token_id != CLOSE_BRACKETS:
				syntax_error(EXPECTED_CLOSE_BRACKETS, line)

			copy_list(Qtrue, Rtrue)
			copy_list(Qfalse, Rfalse)
		else:
			syntax_error(EXPECTED_OPEN_BRACKETS, line)

	elif token_id == OPEN_BRACKETS:
		condition(Qtrue, Qfalse)

		lex()		# Next token must be ']'.
		if token_id != CLOSE_BRACKETS:
			syntax_error(EXPECTED_CLOSE_BRACKETS, line)

		copy_list(Qtrue, Rtrue)
		copy_list(Qfalse, Rfalse)
	else:
		move_file_pointer(-len(token))

		exp1 = empty_list()
		exp2 = empty_list()

		expression(exp1)
		relational_operator()
		operation = token
		expression(exp2)

		Qtrue = make_list(next_quad())
		gen_quad(operation, exp1, exp2, "_")
		Qfalse = make_list(next_quad())
		gen_quad("jump", "_", "_", "_")

		copy_list(Qtrue, Rtrue)
		copy_list(Qfalse, Rfalse)


def expression(return_value):

	term1 = empty_list()		# Using lists 'cause of mutability.
	term2 = empty_list()
	sign = empty_list()
	temp = ""

	optional_sign()

	if token_id == MINUS:
		sign.append(token)
	else:
		sign.append("")

	term(term1)

	term1[0] = sign[0] + term1[0]

	lex()		# Check what's next.

	while token_id == PLUS or token_id == MINUS:

		move_file_pointer(-len(token))
		add_operator()

		operation = token

		lex()		# Check for another round.

		term2.append(token)
		term(term2)

		temp = new_temp()
		gen_quad(operation, term1[0], term2[0], temp)
		term1[0] = temp

	if len(return_value) == 0:
		copy_list(term1, return_value)
	else:
		return_value.append(return_value[0] + term1[0])

	move_file_pointer(-len(token))


def term(term):

	term1 = empty_list()
	sign = empty_list()
	temp = ""

	factor(term)

	lex()		# Check what's next.

	while token_id == MULTIPLICATION or token_id == DIVISION:

		move_file_pointer(-len(token))
		multiplication_operator()

		sign.append(token)

		lex()		# Check for another round.

		term1.append(token)

		factor(term1)

		temp = new_temp()
		gen_quad(sign[0], term[0], term1[0], temp)
		term[0] = temp

	move_file_pointer(-len(token))


def factor(term):

	lex()		# Check what's next.

	if token_id == OPEN_PARENTHESIS:

		expression(term)

		lex()		# Next token must be ')'
		if token_id != CLOSE_PARENTHESIS:
			syntax_error(EXPECTED_CLOSE_PARENTHESIS, line)

	elif token_id == ALNUM:

		if token.isdigit():
			term.append(token)

		elif token.isalpha():
			term.append(token)
			id_tail(token, term)
	else:
		return


def id_tail(func_name, term):

	lex()		# Check for '('. If true, restore file pointer and call actual_parameters.

	if token_id == OPEN_PARENTHESIS:
		move_file_pointer(-len(token))
		actual_parameters()

		temp = new_temp()

		gen_quad("par", temp, "RET", "_")
		gen_quad("call", func_name, "_", "_")

		term.append(temp)
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
	print("Last token: " + token)
	exit(0)

# -----------------------------------
# 	  File Navigation Functions
# -----------------------------------


def restore_file_pointer():		# Restores file pointer to the point before latest lex() call.

	global file_position

	file.seek(file_position)


def move_file_pointer(offset):		# Moves file pointer a given amount (offset) forward or backward.

	file.seek(file.tell() + offset, os.SEEK_SET)


main()
