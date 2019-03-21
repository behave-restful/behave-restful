import bolt
import bolt_flask
import behave_restful.bolt_behave_restful as bbr

bolt.register_module_tasks(bolt_flask)
bolt.register_module_tasks(bbr)

# Bolt has a provided task sleep that is automatically registered

config = {
	'start-flask': {
		'startup-script': 'run_api.py'
	},
	'sleep': {
		'duration': 2
	},
	'behave-restful': {
		'directory': 'features' # path to features folder
		# 'definition': 'yourdefinition',	# if you are using definitions for different environments
	}
}

# Register a task to invoke all that here:

bolt.register_task('test-features', ['start-flask', 'sleep', 'behave-restful'])