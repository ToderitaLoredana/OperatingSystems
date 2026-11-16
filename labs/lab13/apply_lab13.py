#!/usr/bin/env python3
"""Install the Lab 13 semaphore implementation into an xv6-riscv tree."""

import re
import sys
from pathlib import Path


LAB = Path(__file__).resolve().parent


def add_after(text: str, anchor: str, addition: str, label: str) -> str:
    if addition.strip() in text:
        return text
    if anchor not in text:
        raise SystemExit(f"Cannot find the {label} anchor: {anchor!r}")
    return text.replace(anchor, anchor + addition, 1)


def add_after_pattern(text: str, pattern: str, addition: str, label: str) -> str:
    if addition.strip() in text:
        return text
    match = re.search(pattern, text, flags=re.MULTILINE)
    if match is None:
        raise SystemExit(f"Cannot find the {label} anchor matching: {pattern!r}")
    return text[:match.end()] + addition + text[match.end():]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} PATH_TO_XV6_RISCV")
    root = Path(sys.argv[1]).expanduser().resolve()
    required = [
        root / "Makefile",
        root / "kernel/syscall.h",
        root / "kernel/syscall.c",
        root / "user/user.h",
        root / "user/usys.pl",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Not an xv6 tree; missing: " + ", ".join(missing))

    updates = {}
    path = root / "kernel/syscall.h"
    updates[path] = add_after_pattern(
        path.read_text(),
        r"^#define[ \t]+SYS_sync[ \t]+22[ \t]*\n",
        "#define SYS_sem_init 24\n#define SYS_sem_down 25\n#define SYS_sem_up 26\n",
        "system-call number",
    )

    path = root / "user/user.h"
    updates[path] = add_after(
        path.read_text(),
        "int sync(void);\n",
        "int sem_init(int, int);\nint sem_down(int);\nint sem_up(int);\n",
        "user declaration",
    )

    path = root / "user/usys.pl"
    updates[path] = add_after(
        path.read_text(),
        'entry("sync");\n',
        'entry("sem_init");\nentry("sem_down");\nentry("sem_up");\n',
        "user stub",
    )

    path = root / "kernel/syscall.c"
    syscall_c = add_after(
        path.read_text(),
        "extern uint64 sys_sync(void);\n",
        "extern uint64 sys_sem_init(void);\nextern uint64 sys_sem_down(void);\nextern uint64 sys_sem_up(void);\n",
        "kernel declaration",
    )
    syscall_c = add_after_pattern(
        syscall_c,
        r"^[ \t]*\[SYS_sync\][ \t]*=[ \t]*sys_sync,[ \t]*\n",
        "[SYS_sem_init] = sys_sem_init,\n[SYS_sem_down] = sys_sem_down,\n[SYS_sem_up] = sys_sem_up,\n",
        "dispatch table",
    )
    updates[path] = syscall_c

    path = root / "Makefile"
    makefile = add_after(
        path.read_text(),
        "  $K/sysproc.o \\\n",
        "  $K/sem.o \\\n",
        "kernel object",
    )
    makefile = add_after(
        makefile,
        "\t$U/_zombie\\\n",
        "\t$U/_semtest\\\n\t$U/_mix\\\n",
        "user programs",
    )
    updates[path] = makefile

    templates = {
        root / "kernel/sem.c": LAB / "kernel/sem.c",
        root / "user/semtest.c": LAB / "user/semtest.c",
        root / "user/mix.c": LAB / "user/mix.c",
    }
    for destination, source in templates.items():
        content = source.read_text()
        if destination.exists() and destination.read_text() != content:
            raise SystemExit(f"Refusing to overwrite different existing file: {destination}")
        updates[destination] = content

    for destination, content in updates.items():
        destination.write_text(content)
    print(f"Lab 13 installed in {root}")


if __name__ == "__main__":
    main()
