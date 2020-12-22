import angr
import claripy

success_addr = 0x00401527 # address of puts("Thou shall  not pass! Or shall you? ")
fail_addr = 0x00401535    # address of puts("Thou shall pass! Or maybe not?")

flag_len = 30 # 31 buffer, but last is a null byte

proj = angr.Project("./thou_shall_pass_patched")
# thank you googleCTF 2020
inp = [claripy.BVS('flag_%d' %i, 8) for i in range(flag_len)]
flag = claripy.Concat(*inp + [claripy.BVV(b'\n')])

st = proj.factory.full_init_state(args=["./thou_shall_pass_patched"], stdin=flag)
for k in inp:
    # limit to special characters/letters/numbers
    st.solver.add(k < 0x7f)
    st.solver.add(k > 0x20)

sm = proj.factory.simulation_manager(st)
sm.explore(find=success_addr,avoid=fail_addr)
if len(sm.found) > 0:
    for found in sm.found: # print what worked
        print(found.posix.dumps(0))
