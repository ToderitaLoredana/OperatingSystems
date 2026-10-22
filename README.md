# Operating Systems Laboratory Works 1–8

This repository contains the task sheets, implementation files, and reports for
Laboratory Works 1 through 8 from the Operating Systems course (FCIM/FAF, UTM).

Student: **Tacu Loredana**

Group: **FAF-242**

## Repository layout

| Lab | Topic | Task and implementation | Report |
| --- | --- | --- | --- |
| 1 | The OS as a Resource Manager | [`labs/lab01`](labs/lab01) | [`reports/lab01`](reports/lab01) |
| 2 | Meet the OS You Will Build (xv6) | [`labs/lab02`](labs/lab02) | [`reports/lab02`](reports/lab02) |
| 3 | Command Line Shell, Pipes, and Text Filters | [`labs/lab03`](labs/lab03) | [`reports/labs03-04`](reports/labs03-04) |
| 4 | The xv6 Shell from the Outside | [`labs/lab04`](labs/lab04) | [`reports/labs03-04`](reports/labs03-04) |
| 5 | The File System with Your Own Hands (Linux) | [`labs/lab05`](labs/lab05) | [`reports/labs05-06`](reports/labs05-06) |
| 6 | Inside the xv6 File System | [`labs/lab06`](labs/lab06) | [`reports/labs05-06`](reports/labs05-06) |
| 7 | Three Small Programs: Processes, Redirection, and a Pipe | [`labs/lab07`](labs/lab07) | [`reports/labs07-08`](reports/labs07-08) |
| 8 | The Same Calls Inside xv6 | [`labs/lab08`](labs/lab08) | [`reports/labs07-08`](reports/labs07-08) |

Combined reports are stored once and linked from both relevant laboratory rows.
Editable DOCX and final PDF versions are included where available.

## Quick verification

Lab 6 includes host-side structural and syntax checks for the xv6 programs:

```bash
python3 -m unittest labs/lab06/tests/test_xv6_sources.py -v
```

Lab 7 programs can be checked with a normal C compiler:

```bash
cc -std=c11 -Wall -Wextra -Werror -fsyntax-only labs/lab07/src/*.c
```

The xv6 sources in Labs 2, 4, 6, and 8 are intended to be copied into the
`user/` directory of an xv6-riscv checkout and registered using the accompanying
`Makefile.uprogs` fragment.
