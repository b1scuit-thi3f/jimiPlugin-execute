from core.models import action, webui
from core import helpers
import subprocess

class _execute(action._action):
	program = str()
	arguments = str()
	timeout = int()
	use_program_rc = bool()

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
			if self.timeout > 0:
				try:
					stdout, stderr = process.communicate(timeout=self.timeout)
				except subprocess.TimeoutExpired:
					actionResult["result"] = False
					actionResult["rc"] = -1
					return actionResult
			else:
				stdout, stderr = process.communicate()
			if stdout:
				actionResult["result"] = True
				if self.use_program_rc:
					actionResult["rc"] = process.returncode
				else:
					actionResult["rc"] = 0
				actionResult["data"] = stdout.decode()
			elif stderr:
				actionResult["result"] = False
				if self.use_program_rc:
					actionResult["rc"] = process.returncode
				else:
					actionResult["rc"] = 1
				actionResult["data"] = stderr.decode()
		return actionResult