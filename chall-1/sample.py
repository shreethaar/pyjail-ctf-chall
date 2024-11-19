from sys import modules
modules.clear()
del modules

_raw_input = input("Enter input:")
_eval = eval
ident = ''.join((chr(i) for i in range(256)))

#TIL: the interactive interpreter freaks if 'True' gets undefined,
#and 'None' is actually a keyword pretending to be a variable.
__builtins__.__dict__.clear()
__builtins__ = None

print('Get a shell. The flag is NOT in ./key, ./flag, etc.')

while 1:
  try:
    inp = _raw_input()
    if not inp: continue
    inp = inp.split()[0][:1900]
    #Dick move: you also have to only use the characters that my solution did.
    inp = inp.translate(ident, '!"#$&*+-/0123456789;=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\\^abcdefghijklmnopqrstuvwxyz|')
    a = None
    exec('a=' + _eval(inp, {}), {})
    print('Return Value:', a)
  except ().__class__.__bases__[0].__subclasses__()[42].__subclasses__()[0] as e: #42 is base exception.
    if e.__str__().startswith('EOF'): raise e
    else: print('Exception:', e)

