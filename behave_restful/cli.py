"""
Exposes functions to provide a command line interface to Behave Restful.
"""
import sys

import behave_restful.app as app

def behave_restful_init():
    try:
        target_dir = sys.argv[1] if len(sys.argv) > 1 else None
        application = app.BrInitApp()
        application.init_project(target_dir)
    except app.ProjectInitError as err:
        print(err.reason)
        sys.exit(2)
    except Exception as err:
        msg = 'Error creating project {e}'.format(e=err)
        print(msg)
        sys.exit(1)
