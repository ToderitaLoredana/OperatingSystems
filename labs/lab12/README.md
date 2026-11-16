# Laboratory Work No. 12 - Producer, Consumer and the Other Tools

Run on Linux. `deadlock_original.c` preserves the required stuck experiment; `deadlock.c` is the fixed hand-in version.

## Build

```bash
cd ~/OperatingSystems/labs/lab12
mkdir -p bin
gcc -Wall -pthread -o bin/prodcons src/prodcons.c
gcc -Wall -pthread -o bin/condvar src/condvar.c
gcc -Wall -pthread -o bin/readers src/readers.c
gcc -Wall -pthread -o bin/deadlock-original src/deadlock_original.c
gcc -Wall -pthread -o bin/deadlock src/deadlock.c
```

## Evidence commands

```bash
./bin/prodcons
./bin/condvar
./bin/readers
timeout 5 ./bin/deadlock-original; echo "exit code: $?"
timeout 5 ./bin/deadlock; echo "exit code: $?"
```

Capture one screenshot for each of the first three programs and one screenshot containing both deadlock runs and their exit codes.
