# from inspect import currentframe, getframeinfo

# dtype = int


# class VarHist:
# 	def __init__(self, data, dtype):
# 		class Obj(dtype):
# 			def __init__(self, data: any):
# 				self.data: dtype = data
# 				# self


# 			def __setattr__(self, name, value):
# 				frame_info = getframeinfo(currentframe()).filename + ':' + str(getframeinfo(currentframe()).lineno)
# 				print(f"{frame_info}: Attribute \'{name}\' changed to {value}")
# 				super().__setattr__(name, value)



# 		self.object = Obj(data);

# data = VarHist(1, dtype).object

# print(type(data))

import sys
from varhist import varhist as VarHist

VarHist.track('Obj.x.vadl')
 
sys.settrace(VarHist.trace)
 
def main():
	class Bob:
		def __init__(self, val):
			self.val = val
	class John:
		x = Bob(4)

	Obj = John
	Obj.x.val = 2
	Obj.x.vadl = 3
	Obj.x.val -=21

	assert VarHist.HIST == [[3, 42]]
	# a = 10
	# a = [20]
 
	# for i in range(5):
	# 	c = i

# main()
# VarHist.history('Obj.x.vadl')