import platform
import subprocess
import tempfile
import unittest
from pathlib import Path


LAB = Path(__file__).resolve().parents[1]
SRC = LAB / "src"


class Lab12Tests(unittest.TestCase):
    def compile(self, name: str, build: Path) -> Path:
        binary = build / name
        flags = ["-Wall", "-Werror", "-pthread"]
        if platform.system() == "Darwin":
            flags.append("-Wno-deprecated-declarations")
        subprocess.run(
            ["cc", *flags, "-o", binary, SRC / f"{name}.c"],
            check=True,
            text=True,
            capture_output=True,
        )
        return binary

    def test_required_programs_compile(self):
        with tempfile.TemporaryDirectory() as directory:
            build = Path(directory)
            for name in ("prodcons", "condvar", "readers", "deadlock", "deadlock_original"):
                with self.subTest(program=name):
                    self.compile(name, build)

    def test_condition_variable_preserves_message_order(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = self.compile("condvar", Path(directory))
            result = subprocess.run([binary], check=True, text=True, capture_output=True, timeout=5)
            self.assertEqual(
                result.stdout.splitlines(),
                ["B: not ready, I sleep", "A: message written", 'B: I read "hello"'],
            )

    def test_fixed_lock_order_finishes(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = self.compile("deadlock", Path(directory))
            result = subprocess.run([binary], check=True, text=True, capture_output=True, timeout=5)
            self.assertEqual(result.stdout.splitlines()[-1], "done")
            self.assertEqual(result.stdout.count("I have both"), 2)

    def test_producer_consumer_finishes_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = self.compile("prodcons", Path(directory))
            if platform.system() != "Linux":
                self.skipTest("unnamed POSIX semaphore execution is a Linux lab behavior")
            result = subprocess.run([binary], check=True, text=True, capture_output=True, timeout=10)
            counts = [int(line.rsplit(": ", 1)[1][:-1]) for line in result.stdout.splitlines()]
            self.assertLessEqual(max(counts), 4)
            self.assertEqual(counts[-1], 0)


if __name__ == "__main__":
    unittest.main()
