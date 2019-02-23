import subprocess
import bolt.api as btapi

class StartFlaskServiceTask(btapi.Task):
    
    def __init__(self):
        super(StartFlaskServiceTask, self).__init__()
        self.process = None

    def tear_down(self):
        if self.process:
            self._terminate(self.process)
            
    def _configure(self):
        self.startup_script = self.config.get('startup-script')
        if not self.startup_script: raise StartupScriptNotSpecifiedError()

    def _execute(self):
        args = ['python', self.startup_script]
        self.process = self._popen_script(args)

    def _popen_script(self, args):
        return subprocess.Popen(args)

    def _terminate(self, process):
        process.terminate()
        
        
def register_tasks(registry):
	registry.register_task('start-flask', StartFlaskServiceTask())
        
        
class StartupScriptNotSpecifiedError(btapi.RequiredConfigurationError):
    def __init__(self):
        return super().__init__('startup-script')