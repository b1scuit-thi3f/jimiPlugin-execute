from core.models import action, webui
from core import helpers
import subprocess

class _execute(action._action):
	program = str()
	arguments = str()
	timeout = int()

	def run(self,data,persistentData,actionResult):
		program = helpers.evalString(self.program,{"data" : data})
		arguments = helpers.evalString(self.arguments,{"data" : data})

		actionResult["result"] = False
		actionResult["rc"] = 1
		if program != "":
			command = [program]
			if len(arguments) > 0:
				command.extend([str(x) for x in arguments.split(" ")])
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