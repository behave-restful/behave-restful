"""
Contains hooks to test project creation
"""
import os
import shutil


def before_feature(context, feature):
    if feature.name == 'Project Creation':
        context.initial_working_directory = os.getcwd()
        context.sandbox_dir = os.path.join(context.initial_working_directory, 'sandbox')
        context.project_src_dir = os.path.join(context.test_dir, '..', 'behave_restful', '_project')
        existent_dir = os.path.join(context.sandbox_dir, 'existent')
        os.makedirs(existent_dir)
        os.chdir(context.sandbox_dir)
        


def after_feature(context, feature):
    if feature.name == 'Project Creation':
        os.chdir(context.initial_working_directory)
        shutil.rmtree(context.sandbox_dir)

