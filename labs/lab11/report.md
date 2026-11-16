# Laboratory Work No. 11 - Observe Answers

## Part 1 - See the race

1. `counter++` consists of three operations: load the current value from memory into a register, add one in the register, and store the result back to memory.
2. Both threads can load the same value, for example 10. Each adds one and obtains 11, then both store 11. Two additions were attempted but the counter increased only once, so one update was lost.
3. Thread scheduling, interrupts, and the exact instruction interleaving vary from run to run. Therefore, the number of overlapping load/add/store sequences and lost updates also varies.

## Part 2 - Mutex and semaphore

1. Yes. The mutex version and the semaphore initialized to 1 both produce 2,000,000 in every run because only one thread can execute the critical section at a time.
2. With `sem_init(&s, 0, 2)`, two threads may pass `sem_wait` simultaneously. Because there are exactly two worker threads, the counter is effectively unprotected and updates can again be lost. A counting semaphore with value 2 is not a mutual-exclusion lock.
3. The protected versions perform synchronization around every increment. Lock acquisition and release add instructions, atomic memory operations, cache-coherence traffic, and sometimes blocking or context-switch overhead.

## Part 3 - Semaphore as a signal

1. With an initial value of 1, B does not block. It can read before A writes and therefore prints an empty string because the global `message` array is initially filled with zero bytes.
2. A semaphore initialized to 0 means no operation may pass `sem_wait` until another thread posts a signal with `sem_post`.

## Part 4 - Semaphore as a counter

1. The largest observed value of `inside` is 3. The `sem_wait(&places)` call occurs before `inside++`, so a car cannot enter unless it obtains one of the three available permits.
2. With `PLACES` equal to 1, the counting semaphore becomes a binary semaphore and acts like a mutex: only one car may be inside at a time.
