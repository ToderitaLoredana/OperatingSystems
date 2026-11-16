import platform
import subprocess
import tempfile
import unittest
from pathlib import Path


LAB = Path(__file__).resolve().parents[1]
SRC = LAB / "src"


class Lab11Tests(unittest.TestCase):
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
            for name in ("race", "mutex", "sem", "order", "parking"):
                with self.subTest(program=name):
                    self.compile(name, build)

    def test_mutex_never_loses_an_increment(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = self.compile("mutex", Path(directory))
            for _ in range(3):
                result = subprocess.run([binary], check=True, text=True, capture_output=True)
                self.assertEqual(result.stdout, "counter = 2000000 (expected 2000000)\n")

    def test_zero_initialized_signal_orders_reader_after_writer(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = self.compile("order", Path(directory))
            if platform.system() != "Linux":
                self.skipTest("unnamed POSIX semaphore execution is a Linux lab behavior")
            result = subprocess.run([binary], check=True, text=True, capture_output=True, timeout=5)
            self.assertEqual(
                result.stdout.splitlines(),
                [
                    "B: waiting for the message...",
                    "A: message written",
                    'B: I read "hello"',
                ],
            )

    def test_parking_capacity_is_never_exceeded(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = self.compile("parking", Path(directory))
            if platform.system() != "Linux":
                self.skipTest("unnamed POSIX semaphore execution is a Linux lab behavior")
            result = subprocess.run([binary], check=True, text=True, capture_output=True, timeout=10)
            inside = [int(line.rsplit(": ", 1)[1][:-1]) for line in result.stdout.splitlines()]
            self.assertEqual(max(inside), 3)
            self.assertEqual(inside[-1], 0)


if __name__ == "__main__":
    unittest.main()
