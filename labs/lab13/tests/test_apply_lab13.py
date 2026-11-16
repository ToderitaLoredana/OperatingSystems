import subprocess
import tempfile
import unittest
from pathlib import Path


LAB = Path(__file__).resolve().parents[1]


class Lab13InstallerTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> None:
        (root / "kernel").mkdir()
        (root / "user").mkdir()
        (root / "kernel" / "syscall.h").write_text("#define SYS_sync   22\n")
        (root / "user" / "user.h").write_text("int sync(void);\n")
        (root / "user" / "usys.pl").write_text('entry("sync");\n')
        (root / "kernel" / "syscall.c").write_text(
            "extern uint64 sys_sync(void);\n"
            "static uint64 (*syscalls[])(void) = {\n"
            "  [SYS_sync]    = sys_sync,\n"
            "};\n"
        )
        (root / "Makefile").write_text(
            "OBJS = \\\n  $K/sysproc.o \\\n\n"
            "UPROGS=\\\n"
            "\t$U/_zombie\\\n"
        )

    def test_installer_adds_complete_user_and_kernel_interface(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_fixture(root)
            subprocess.run(["python3", LAB / "apply_lab13.py", root], check=True)

            self.assertTrue((root / "kernel" / "sem.c").is_file())
            self.assertTrue((root / "user" / "semtest.c").is_file())
            self.assertTrue((root / "user" / "mix.c").is_file())
            self.assertIn("#define SYS_sem_init 24", (root / "kernel" / "syscall.h").read_text())
            self.assertIn("[SYS_sem_down] = sys_sem_down,", (root / "kernel" / "syscall.c").read_text())
            self.assertIn("$K/sem.o", (root / "Makefile").read_text())
            self.assertIn("$U/_semtest", (root / "Makefile").read_text())
            self.assertIn("$U/_mix", (root / "Makefile").read_text())

    def test_installer_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_fixture(root)
            for _ in range(2):
                subprocess.run(["python3", LAB / "apply_lab13.py", root], check=True)
            self.assertEqual((root / "kernel" / "syscall.h").read_text().count("SYS_sem_init"), 1)
            self.assertEqual((root / "user" / "usys.pl").read_text().count('entry("sem_down")'), 1)
            self.assertEqual((root / "Makefile").read_text().count("$U/_mix"), 1)


if __name__ == "__main__":
    unittest.main()
