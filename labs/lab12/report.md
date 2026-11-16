# Laboratory Work No. 12 - Observe Answers

## Part 1 - Producer and consumer

1. `sem_wait(&empty)` stops the producer when the buffer has no free slot, so the count cannot exceed 4.
2. The consumer waits at the start because `full` is initialized to 0. It blocks in `sem_wait(&full)` until the producer inserts an item and posts `full`.
3. If the producer locks the mutex before waiting on `empty`, a full buffer causes a deadlock. The producer sleeps while still holding `lock`; the consumer can pass `sem_wait(&full)` but cannot lock the mutex to remove an item and post `empty`.

## Part 2 - Condition variable

1. The ordinary integer variable `ready` remembers whether the message has been written.
2. Replacing `while` with `if` normally still works in this small program because there is one reader and one writer, and the writer makes `ready` true before signaling.
3. A condition wait may return because of a spurious wakeup, or another awakened thread may consume/change the shared state first. Rechecking in a `while` loop guarantees that the required predicate is actually true.

## Part 3 - Readers and writers

1. The first reader executes `if (++readers == 1) sem_wait(&room);`, excluding writers. The last reader executes `if (--readers == 0) sem_post(&room);`, admitting a writer only after all readers leave.
2. `rlock` makes changes to the reader count atomic. Without it, simultaneous readers could lose increments/decrements, two readers could both believe they are first or last, and `room` could be acquired or released incorrectly while readers are still inside.
3. A continuous stream of readers can keep `room` occupied indefinitely, so writer 2 may never run. This is writer starvation.

## Part 4 - Deadlock

1. Thread one holds A and waits for B, while thread two holds B and waits for A. The wait-for circle is `one -> B -> two -> A -> one`.
2. Without the sleeps the original program does not necessarily hang on every run, because one thread may acquire both locks before the other gets its first lock. This is worse operationally because the deadlock becomes intermittent and timing-dependent, making it harder to reproduce and diagnose.
3. A common lock order prevents deadlock because it removes circular wait: no thread may hold the later lock while waiting for the earlier one.
