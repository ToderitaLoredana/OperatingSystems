# Laboratory Work No. 13 - Semaphores in Your Own Kernel

The installer adds system calls 24-26, copies the kernel implementation and user tests, and updates the xv6 Makefile. It is safe to run again: existing entries are not duplicated, and a different existing `sem.c`, `semtest.c`, or `mix.c` is not overwritten.

## Install into xv6

Run from the OperatingSystems repository and replace `~/xv6-riscv` if your xv6 checkout is elsewhere.

```bash
cd ~/OperatingSystems
python3 labs/lab13/apply_lab13.py ~/xv6-riscv
cd ~/xv6-riscv
git diff -- Makefile kernel user
make clean
make qemu
```

Inside xv6, capture the required evidence:

```text
semtest
mix
mix
mix lock
```

Exit QEMU with `Ctrl-A`, then `X`. Commit the xv6 changes from the host terminal:

```bash
cd ~/xv6-riscv
git status --short
git add Makefile kernel/syscall.h kernel/syscall.c kernel/sem.c user/user.h user/usys.pl user/semtest.c user/mix.c
git commit -m "Add kernel semaphores for Lab 13"
git log -1 --oneline
```

Capture one screenshot of `semtest`, one containing the unlocked and locked `mix` output, and one of the final commit line.
