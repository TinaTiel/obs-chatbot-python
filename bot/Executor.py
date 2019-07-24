from bot.Result import *
from collections import deque
from importlib import import_module

class ExecutorBase():
	def __init__(self, parent=None, lvl=0, **kwargs):
		self.parent = parent
		self.lvl = lvl
		self._validate(**kwargs)
		self._build(**kwargs)

	def __repr__(self):
		res = "{}{}[\n".format("\t"*(self.lvl), self.__class__.__name__)
		for action in self.actions:
			res += "{}\n".format(action)
		res += "{}]\n".format("\t"*(self.lvl))
		return res

	def _validate(self, **kwargs):
		args = kwargs.get('args', None)
		if(args is None):
			raise ValueError("Executor must have 'args'. Conf: {}".format(kwargs))

		actions = args.get("actions", None)
		if(actions is None):
			raise ValueError("Executor args must have 'actions'. Conf: {}".format(kwargs))

	def _build(self, **kwargs):
		self.actions = []
		for conf in kwargs['args']['actions']:
			# Get the action type
			if(conf['type'] is None):
				raise ValueError("Missing 'type' for specified Action or Executor. Conf: {}".format(conf['type']))

			# determine the corresponding class
			try:
				_class = self._get_class("Action", conf['type'] )
			except Exception:
				try:
					_class = self._get_class("Executor", conf['type'] )
				except Exception as e:
					raise ValueError("Specified action/executor '{}' does not exist. Error: {}".format(conf['type'], e))

			# instantiate it
			_obj = _class(self, self.lvl+1, **conf)
			self.actions.append(_obj)

	def _get_class(self, module_name, class_name):
		try:
			module_ = import_module("bot." + module_name)
			class_ = getattr(module_, class_name)
			return class_
		except Exception as e:
			raise ValueError("Could not load specified {} type '{}': {}".format(module_name, class_name, e))

	def execute(self, user, args_list):
		pass

class ExecuteAll(ExecutorBase):

	def execute(self, user, args_list):
		results = []
		for action in self.actions:
			result = action.execute(user, args_list)
			results.append(result)

			# If an action failed, exit early
			if(result.state == State.FAILURE):
				return Result(State.FAILURE, results)

		# Return success
		return Result(State.SUCCESS, results)

class ExecuteGated(ExecutorBase):
	def __init__(self, parent=None, lvl=0, **kwargs):
		super().__init__(parent, lvl, **kwargs)
		self.executed = list()
		self.actions = deque(self.actions)

	def execute(self, user, args_list):
		# If this was initialized with no actions at all, do nothing
		if(len(self.actions) == 0 and len(self.executed) == 0):
			return Result(State.SUCCESS)

		# Otherwise if just the actions are empty, then re-initialize them
		if(len(self.actions) == 0):
			while(len(self.executed) > 0):
				self.actions.appendleft(self.executed.pop())

		# process the first item in the queue
		# if it executes successfully then added it to the executed queue
		# else put it back in the queue
		selected = self.actions.popleft()
		result = selected.execute(user, args_list)
		
		# If it has executed successfully then don't execute it again unless it has more actions to execute
		if(result.state == State.SUCCESS):
			# If it was an Action, then take it out of the queue
			if(not hasattr(selected, 'actions')): # not an Executor; just an Action
				self.executed.append(selected)
			# Otherwise it's an executor
			else:
				# If it has more actions then put it back in the queue
				if(len(selected.actions) > 0):
					self.actions.appendleft(selected)
				# Otherwise take it out of the queue
				else:
					self.executed.append(selected)
			return Result(State.SUCCESS, [result])
		# If the action didn't execute, put it back in the queue
		else:
			self.actions.appendleft(selected)
			return Result(State.FAILURE, [result])

# class ExecuteRandom(Executor):
# 	def __init__(self, **kwargs):
# 		actions = kwargs.get("actions", None)
# 		max_picked = kwargs.get("max_picked": 2)
# 		if(actions is None):
# 			raise ValueError("Executor must have 'actions'.")
# 		self.executed = list()
# 		self.actions = deque(actions)