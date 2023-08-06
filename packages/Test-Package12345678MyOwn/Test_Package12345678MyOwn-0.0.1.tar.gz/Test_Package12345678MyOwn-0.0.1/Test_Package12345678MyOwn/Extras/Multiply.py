def multiply(*args):
	r = args[0]
	for i in args[1:]:
		r *= i
	return r