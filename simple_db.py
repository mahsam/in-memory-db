#!/usr/bin/python
import fileinput
import sys

# InMemoryDB class builds the database and provides its functionalities
# It also supports transactions

class InMemoryDB(object):
	
	# define the commands for in memory database
	commands = ['end', 'get', 'set', 'unset', 'numequalto', 'begin', 'commit', 'rollback'];
	
	def __init__(self):
		self.data = {}
		self.data_counts = {}
		self.txn_stack = []

	def end_db(self):
		sys.exit()

	def get_name(self, name):
		if name is not None and name in self.data:
			if not self.data[name] is None:
				return self.data[name]
			else:
				return 'NULL'
		else:
			return 'NULL'

	def set_name(self, name, value, push_to_txn_stack = True):
		if name is not None:
			old_value = self.data[name] if name in self.data else None
			self.update_data_counts(value, old_value)
			self.data[name] = value
			if len(self.txn_stack) > 0 and push_to_txn_stack:
				self.txn_stack.append([name, value, old_value])
		
	def unset_name(self, name):
		self.set_name(name, None)

	def numequalto_value(self, value):
		if value is not None and value in self.data_counts:
			return self.data_counts[value]
		else:
			return 0

	def begin_tx(self):
		self.txn_stack.append([self.commands[5]])

	def commit_tx(self):
		self.txn_stack_pop(False)

	def rollback_tx(self):
		self.txn_stack_pop(True)

	def txn_stack_pop(self, is_rollback):
		if len(self.txn_stack) == 0 or (is_rollback and len(self.txn_stack) == 1):
			print("NO TRANSACTION")

		i = len(self.txn_stack) - 1
		committed_names = {}
		while i > -1 and self.txn_stack[i][0] != self.commands[5]:
			name = self.txn_stack[i][0]
			if is_rollback:
				self.set_name(name, None, False)
				self.set_name(name, self.txn_stack[i][2], False)
			else:
				committed_names[name] = True

			self.txn_stack.pop(i)
			i -= 1

		if i > -1:
			self.txn_stack.pop()

		if not is_rollback and len(self.txn_stack) > 0:
			for j in range(0, len(committed_names)):
				for k in range(0, len(self.txn_stack)):
					if self.txn_stack[k][0] != self.commands[5] and committed_names[self.txn_stack[k][0]]:
						self.txn_stack.pop(k)


	def update_data_counts(self, new_value, old_value):
		if new_value is not None:
			if new_value in self.data_counts:
				self.data_counts[new_value] += 1
			else:
				self.data_counts[new_value] = 1

		if old_value is not None and old_value in self.data_counts:
			if self.data_counts[old_value] > 1:
				self.data_counts[old_value] -= 1
			else:
				del self.data_counts[old_value]

	def parse_command(self, command_line):
		parsed_command = command_line.split()
		
		try:
			if parsed_command[0] != '':
				command = parsed_command[0].lower()
				
				try:
					self.commands.index(command)
				except ValueError:
					print('Please type a valid command')

				if command == 'end':
					self.end_db()
				elif command == 'get' and len(parsed_command) > 1:
					print self.get_name(parsed_command[1])
				elif command == 'set' and len(parsed_command) > 2:
					self.set_name(parsed_command[1], parsed_command[2])
				elif command == 'unset' and len(parsed_command) > 1:
					self.unset_name(parsed_command[1])
				elif command == 'numequalto' and len(parsed_command) > 1:
					print self.numequalto_value(parsed_command[1])
				elif command == 'begin':
					self.begin_tx()
				elif command == 'commit':
					self.commit_tx()
				elif command == 'rollback':
					self.rollback_tx()
				else:
					print('Please type a valid command')

		except IndexError:
			print('Please type a valid command')


if __name__ == '__main__':
	inramdb = InMemoryDB()
	try:
		if len(sys.argv) != 1:
			for line in fileinput.input():
				inramdb.parse_command(line)
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
else:
	print "Imported simple_db"

