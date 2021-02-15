from core.models import action, webui
from core import helpers
import subprocess

class _execute(action._action):
	program = str()
	arguments = str()
	timeout = int()

	class _properties(webui._properties):
        def generate(self,classObject):
            formData = []
            formData.append({"type" : "break", "start" : True, "schemaitem": "Execute Options"})
            formData.append({"type" : "input", "schemaitem" : "program", "textbox" : classObject.program, "tooltip" : "The program to execute (e.g. python3)"})
            formData.append({"type" : "input", "schemaitem" : "arguments", "textbox" : classObject.arguments, "tooltip" : "Arguments to pass to the program"})
            formData.append({"type" : "input", "schemaitem" : "timeout", "textbox" : classObject.timeout, "tooltip" : "How long to let the process run before killing it"})
            formData.append({"type" : "break", "start" : False, "schemaitem": "Execute Options"})
            formData.append({"type" : "break", "start" : True, "schemaitem": "Core Options"})
            formData.append({"type" : "input", "schemaitem" : "_id", "textbox" : classObject._id})
            formData.append({"type" : "input", "schemaitem" : "name", "textbox" : classObject.name})
            formData.append({"type" : "checkbox", "schemaitem" : "enabled", "checked" : classObject.enabled})
            formData.append({"type" : "json-input", "schemaitem" : "varDefinitions", "textbox" : classObject.varDefinitions})
            formData.append({"type" : "input", "schemaitem" : "logicString", "textbox" : classObject.logicString})
            formData.append({"type" : "checkbox", "schemaitem" : "log", "checked" : classObject.log})
            formData.append({"type" : "input", "schemaitem" : "comment", "textbox" : classObject.comment})
            return formData

	def run(self,data,persistentData,actionResult):
		program = helpers.evalString(self.program,{"data" : data})
		arguments = helpers.evalString(self.arguments,{"data" : data})

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

