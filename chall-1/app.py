#!/usr/bin/env python3
import builtins
import sys
import numpy as np
import sys

FLAG = "CTF{numpy_breakfree_ftw}"

allowed_builtins={
        'globals','locals','print','type','__build_class'
}

for builtin in list(builtins.__dict__.keys()):
    if builtin not in allowed_builtins:
        del builtins.__dict__[builtin]
sys.modules.clear()
sys.modules['numpy']=np
sys.modules['builtins']=builtins

blacklist = {'load', 'loads', 'loadtxt', 'save', 'savetxt', 'savez', 
    'fromfile', 'fromstring', 'frombuffer', 'source', 'ctypes',
    'import', 'eval', 'exec', 'system', 'popen', 'os', 'sys',
    'subprocess', 'file', 'open', 'read', 'write', '__code__',
    '__globals__', '__closure__', 'globals'
}


class RestrictedNumpy:
    def __init__(self):
        for attr in dir(np):
            if not attr.startswith('_') and attr not in blacklist:
                setattr(self, attr, getattr(np, attr))

np = RestrictedNumpy()

def check_input(code):
    """Check if input contains forbidden patterns"""
    forbidden = ['__', 'exec', 'eval', 'import', 'os', 'sys', 'subprocess', 
                'read', 'write', 'file', 'open', 'code', 'builtins']

    return not any(bad in code.lower() for bad in forbidden)

def main():
    print("PyJail Challenge V2")
    while True:
        try:
            code=input(">>>> ")
            if check_input(code):
                exec(code,{"np":np,"print": print})
            else:
                print("Forbidden input detected!")
        except Exception as e:
            print(f"Error:{e}")

if __name__ == "__main__":
    main()
