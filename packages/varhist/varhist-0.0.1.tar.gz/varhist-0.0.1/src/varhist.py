import traceback
class varhist:

	HIST = {}
	checking = []

	line = 0

	@classmethod
	def trace(self, frame, event, arg):
		line = self.line
		self.line = frame.f_lineno #traceback.format_stack()[-2].split(',')[1].strip(' ').split(' ')[1]
		dictionary = frame.f_locals
		# dictionary.update(frame.f_globals)
		# dictionary.update(frame.f_builtins)
		for name in self.checking:
			if name[0] in dictionary:
				val = dictionary[name[0]]
				try:
					for sub in name[1:]:
						val = getattr(val, sub)

				except AttributeError:
					continue

				if '.'.join(name) in self.HIST:
					if val != self.HIST['.'.join(name)][-1][0]:
						self.HIST['.'.join(name)].append([val, line, frame.f_code.co_name])

				else:
					self.HIST['.'.join(name)] = [[val, line, frame.f_code.co_name]]

		# for name,val in dictionary.items():
		# 	if name in self.checking:
		# 		if name in self.HIST:
		# 			if val != self.HIST[name][-1][0]:
		# 				self.HIST[name].append([val, line, frame.f_code.co_name])

		# 		else:
		# 			self.HIST[name] = [[val, line, frame.f_code.co_name]]
		return self.trace




	@classmethod
	def track(self, var_name):
		self.checking.append(var_name.split('.'))

	@classmethod
	def history(self, var_name):
		if var_name not in self.HIST and var_name.split('.') not in self.checking:
			raise ValueError(f'Variable is not being tracked. Use VarHist.track({var_name}).')

		elif var_name.split('.') in self.checking and var_name not in self.HIST:
			print(f'Variable \'{var_name}\' was never created.')
		else:
			print(f'----------Start of History for \'{var_name}\'----------')
			for value in self.HIST[var_name]:
				print(f"Variable '{var_name}' changed to '{value[0]}' on line '{value[1]}' in function '{value[2]}'")

			print(f'----------End of History for \'{var_name}\'----------')





