import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "syscalls.c"


class SyscallsProgramTests(unittest.TestCase):
    def test_program_writes_and_reads_the_expected_message(self):
        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            binary = work / "syscalls"
            build = subprocess.run(
                [
                    "cc",
                    "-std=c11",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    str(SOURCE),
                    "-o",
                    str(binary),
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(build.returncode, 0, build.stderr)

            run = subprocess.run(
                [str(binary)], cwd=work, text=True, capture_output=True
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(
                run.stdout,
                "open returned descriptor 3\n"
                "write sent 14 bytes\n"
                "read got 14 bytes: hello, kernel\n",
            )
            self.assertEqual((work / "note.txt").read_bytes(), b"hello, kernel\n")


if __name__ == "__main__":
    unittest.main()
