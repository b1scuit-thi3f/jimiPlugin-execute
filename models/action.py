from core.models import action
import subprocess

class _execute(action._action):
	options = dict()
	timeout = int()

	def run(self,data,persistentData,actionResult):
		actionResult["result"] = False
		actionResult["rc"] = 1
		if "program" in self.options:
			command = [self.options['program']]
			if "arguments" in self.options:
				command.extend([str(x) for x in self.options['arguments']])
			process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			if self.timeout:
				try:
					stdout, stderr = process.communicate(timeout=self.timeout)
				except subprocess.TimeoutExpired:
					actionResult["result"] = False
					actionResult["rc"] = -999
					return actionResult
			else:
				stdout, stderr = process.communicate()
			if stdout:
				actionResult["result"] = True
				actionResult["rc"] = 0
			if stderr:
				actionResult["result"] = False
				actionResult["rc"] = 1
		return actionResult

