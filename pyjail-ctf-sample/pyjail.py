#!/usr/bin/env python3
import sys
from typing import Any

class RestrictedSession:
    def __init__(self):
        # Allowed builtins
        self.allowed_builtins = {
            'int': int,
            'str': str,
            'len': len,
            'print': print
        }
        
        # Blocked words/characters
        self.blacklist = [
            'import',
            'eval',
            'exec',
            'open',
            'read',
            'system',
            'subprocess',
            'os',
            'sys',
            'builtins',
            'globals',
            'locals',
            'getattr',
            'setattr',
            '__',
            'class',
            'base',
            'code',
            'flag',
            'break',
            '\\'
        ]
        
        # Create restricted globals
        self.restricted_globals = {
            '__builtins__': self.allowed_builtins
        }

    def check_input(self, user_input: str) -> bool:
        """Check if input contains any blacklisted terms"""
        return not any(bad in user_input.lower() for bad in self.blacklist)

    def execute(self, code: str) -> Any:
        """Execute the provided code in the restricted environment"""
        if not self.check_input(code):
            print("Nice try! But that's not allowed!")
            return None
        
        try:
            # Execute in restricted environment
            code_object = compile(code, '<stdin>', 'eval')
            result = eval(code_object, self.restricted_globals, {})
            return result
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

def main():
    # Create the flag file
    with open('flag.txt', 'w') as f:
        f.write('CTF{Py7h0n_J41L_Br34k0u7}')
    
    print("Welcome to the Python Jail!")
    print("Try to break out and read the flag from 'flag.txt'!")
    print("Only basic operations are allowed. Type 'exit' to quit.")
    print("=========================================")
    
    session = RestrictedSession()
    
    while True:
        try:
            user_input = input(">>> ").strip()
            
            if user_input.lower() == 'exit':
                break
                
            if user_input:
                result = session.execute(user_input)
                if result is not None:
                    print(result)
                    
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
