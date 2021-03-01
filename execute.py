from core import plugin, model

class _execute(plugin._plugin):
    version = 1.5

    def install(self):
        # Register models
        model.registerModel("execute","_execute","_action","plugins.execute.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("execute","_execute","_action","plugins.execute.models.action")
        return True
    