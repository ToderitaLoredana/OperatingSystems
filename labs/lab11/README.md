# Laboratory Work No. 11 - The Race and the Semaphore

Required source files are in `src/`; the optional atomic implementation is included as well. Run the commands on Linux because macOS does not implement unnamed POSIX semaphores.

## Build

```bash
cd ~/OperatingSystems/labs/lab11
mkdir -p bin
gcc -Wall -pthread -o bin/race src/race.c
gcc -Wall -pthread -o bin/mutex src/mutex.c
gcc -Wall -pthread -o bin/sem src/sem.c
gcc -Wall -pthread -o bin/order src/order.c
gcc -Wall -pthread -o bin/parking src/parking.c
gcc -Wall -pthread -o bin/atomic src/atomic.c
```

## Evidence commands

```bash
./bin/race; ./bin/race; ./bin/race
./bin/mutex; ./bin/mutex; ./bin/mutex
./bin/sem; ./bin/sem; ./bin/sem
time ./bin/race
time ./bin/mutex
time ./bin/sem
./bin/order
./bin/parking
time ./bin/atomic
```

Capture one screenshot for the three race runs, one for mutex/semaphore plus timing, one for `order`, and one for `parking` plus `atomic`.
