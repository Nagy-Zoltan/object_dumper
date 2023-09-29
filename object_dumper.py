import keyword
import inspect
import os
import pickle
import re
import time
import traceback


def dump_obj(*, obj: object, obj_name: str = None, folder_path: str = None, run_id: str = None):
    _locals = locals()
    if obj_name is None:
        stack = inspect.stack()
        func_name = stack[0].function
        code_context = stack[1].code_context
        
        first_kwarg_name, second_kwarg_name = [*_locals][0:2]
   
        args = re.search(f'{func_name}(\(.+?\))', code_context[0])
        if args is None:
            raise RuntimeError(
                f'Please call the function like this: "{func_name}({first_kwarg_name}=<val>, ...)"'
                f' or provide "{second_kwarg_name}"'
            )
        args = args.group(1)
            
        first_kwarg_value = re.search(f'{first_kwarg_name}\s*=\s*(.+?)[, )]', args)
        if first_kwarg_value is None:
            raise RuntimeError(
                f'Please call the function like this: "{func_name}({first_kwarg_name}=<val>, ...)"'
                f' or provide "{second_kwarg_name}"'
            )
        first_kwarg_value = first_kwarg_value.group(1)
        
        if not first_kwarg_value.isidentifier() or first_kwarg_value in keyword.kwlist:
            raise RuntimeError(
                f'Please provide "{first_kwarg_name}" parameter with an identifier or provide "{second_kwarg_name}"'
            )
            
        obj_name = first_kwarg_value
    
    if folder_path is None:
        folder_path = os.getcwd()
        
    if run_id is None:
        run_id = str(time.time()).replace('.', '')
        
    file_name = f'{obj_name}_{run_id}.p'
    file_path = os.sep.join([folder_path, file_name])
    
    print(f'Dumping object: {obj}, with name "{obj_name}" to {file_path}')
    
    try:
        with open(file_path, 'wb') as dump_file:
            pickle.dump(obj=obj, file=dump_file)
    except Exception as e:
        print(f'Failed to pickle {obj} for the following reason: {e}')
        traceback.format_stack()
        os.remove(file_path)
