# Laboratory Work 10

This laboratory adds the `trace` system call to the course xv6-riscv tree.
`src/trace.c` is the user command, `Makefile.uprogs` contains its registration,
and `xv6-trace.patch` contains all user/kernel integration changes described in
the report.

From the root of the course xv6-riscv checkout, apply the patch. It creates
`user/trace.c` and adds every required kernel and user-space integration point:

```bash
git apply /path/to/OperatingSystems/labs/lab10/xv6-trace.patch
make qemu
```

The course tree used for the report already includes `SYS_sync` as call 22;
`SYS_trace` is assigned call 23. If your xv6 course tree has diverged, inspect
any rejected hunk and insert the corresponding change from the patch manually.

Validate inside the xv6 shell:

```text
trace 32 grep hello README
trace 2147483647 grep hello README
trace 2 usertests forkforkfork
trace 65536 echo hi
trace 2129920 grep hello README
```

The masks select `read`, all calls, `fork`, `write`, and `open` plus `close`,
respectively. The fork test verifies that `trace_mask` is copied into child
processes.

The host-side user-program check can be run from the repository root:

```bash
python3 -m unittest labs/lab10/tests/test_trace_program.py -v
```
