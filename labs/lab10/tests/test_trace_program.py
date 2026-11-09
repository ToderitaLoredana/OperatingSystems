import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "trace.c"


class TraceProgramTests(unittest.TestCase):
    def test_trace_passes_the_mask_and_command_to_xv6_interfaces(self):
        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            (work / "kernel").mkdir()
            (work / "user").mkdir()
            (work / "kernel" / "types.h").write_text(
                "typedef unsigned int uint; typedef unsigned long uint64;\n"
            )
            (work / "kernel" / "stat.h").write_text("struct stat { int type; };\n")
            (work / "user" / "user.h").write_text(
                "int trace(int); int atoi(const char *); int exec(const char *, char **);\n"
                "int fprintf(int, const char *, ...); void exit(int);\n"
            )
            harness = work / "harness.c"
            harness.write_text(
                textwrap.dedent(
                    r'''
                    #include <stdarg.h>
                    #include <unistd.h>

                    int dprintf(int, const char *, ...);
                    int vdprintf(int, const char *, va_list);

                    int trace(int mask) {
                      dprintf(1, "mask=%d\n", mask);
                      return 0;
                    }

                    int exec(const char *path, char **argv) {
                      dprintf(1, "exec=%s", path);
                      for (int i = 1; argv[i] != 0; i++)
                        dprintf(1, " arg%d=%s", i, argv[i]);
                      dprintf(1, "\n");
                      return -1;
                    }

                    int fprintf(int fd, const char *format, ...) {
                      (void)fd;
                      va_list args;
                      va_start(args, format);
                      int result = vdprintf(1, format, args);
                      va_end(args);
                      return result;
                    }

                    void exit(int status) {
                      _exit(status);
                    }
                    '''
                )
            )
            binary = work / "trace"
            build = subprocess.run(
                [
                    "cc",
                    "-std=c99",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    "-fno-builtin",
                    "-I",
                    str(work),
                    str(SOURCE),
                    str(harness),
                    "-o",
                    str(binary),
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(build.returncode, 0, build.stderr)

            run = subprocess.run(
                [str(binary), "32", "grep", "hello", "README"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(run.returncode, 1)
            self.assertEqual(
                run.stdout,
                "mask=32\n"
                "exec=grep arg1=hello arg2=README\n"
                "trace: exec grep failed\n",
            )


if __name__ == "__main__":
    unittest.main()
