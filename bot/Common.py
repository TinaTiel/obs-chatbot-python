from importlib import import_module

def get_class(module_name, class_name):
	try:
		module_ = import_module("bot." + module_name)
		class_ = getattr(module_, class_name)
		return class_
	except Exception as e:
		raise ValueError("Could not load specified {} type '{}': {}".format(module_name, class_name, e))