import importlib.util
import argparse

import os

"""
取得參數
"""
parser = argparse.ArgumentParser()
parser.add_argument('--task', help='Specify the task name')

args, extra_args = parser.parse_known_args()
extra_args = dict(zip(extra_args[0::2], extra_args[1::2]))

task_name = args.task


"""
取得 Class
"""
module_path = os.path.join("post_process_scripts", f"{task_name}.py")

module_name = task_name
spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

task_name = task_name
post_processing_class = getattr(module, task_name)

"""
執行 class
"""
instance = post_processing_class(extra_args)
instance.run()