# Lab 2 observations

## Part 2 — Use xv6 as Unix

1. xv6 includes programs such as `cat`, `echo`, `wc`, `ls`, `grep`, `sh`,
   `kill`, `mkdir`, `ln`, `rm`, and `usertests`.
2. A pipeline needs process management so the shell can create concurrent
   processes, and kernel-supported inter-process communication so one process's
   standard output can feed another process's standard input.
3. The xv6 shell supports basic command execution, redirection, and pipelines,
   but omits most Bash conveniences such as job control and scripting features.

## Part 3 — Read the source

1. `user/cat.c` uses `read` to receive bytes from a file descriptor, `write` to
   send bytes to standard output, and `exit` to terminate on errors or success.
2. `sys_read` and `sys_write` are implemented in `kernel/sysfile.c`.
3. Code under `kernel/` runs with privilege and manages shared resources. Code
   under `user/` is unprivileged and requests kernel services through system
   calls.

The course tree exposes `pause(int)` rather than the traditional `sleep(int)`
system-call name, so the submitted program checks `user/user.h` and calls
`pause(atoi(argv[1]))`.
