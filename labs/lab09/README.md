# Laboratory Work 9

This laboratory observes Linux system calls with `strace`. The program in
`src/syscalls.c` creates `note.txt`, writes `hello, kernel\n`, reopens the file,
and reads the same 14 bytes back.

Build and run the direct system-call experiment:

```bash
cc -std=c11 -Wall -Wextra -Werror -o syscalls src/syscalls.c
./syscalls
strace -e trace=openat,write,read,close ./syscalls
```

Trace a familiar command and count the selected calls:

```bash
strace -f -e trace=openat,read,write,close -o ls.strace ls -l
grep -Eo '(openat|read|write|close)\(' ls.strace | sort | uniq -c
```

Run the automated behavior check from the repository root:

```bash
python3 -m unittest labs/lab09/tests/test_syscalls.py -v
```
