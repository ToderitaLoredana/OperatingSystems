import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USER = ROOT / "src"


class Xv6ProgramTests(unittest.TestCase):
    def test_mystat_has_required_behavior(self):
        source = (USER / "mystat.c").read_text()
        for token in ("T_DIR", "T_FILE", "T_DEVICE", "stat(argv[i], &st)",
                      "st.ino", "st.nlink", "st.size"):
            self.assertIn(token, source)
        self.assertRegex(source, r"for\s*\(\s*int\s+i\s*=\s*1")

    def test_find_recurses_and_avoids_dot_entries(self):
        source = (USER / "find.c").read_text()
        for token in ("struct dirent", "de.inum == 0", 'strcmp(name, ".")',
                      'strcmp(name, "..")', "find(path, target)", "close(fd)"):
            self.assertIn(token, source)
        self.assertIn("DIRSIZ", source)

    def test_find_matches_directories_as_well_as_files(self):
        source = (USER / "find.c").read_text()
        match = "if(strcmp(basename(start), target) == 0)"
        self.assertIn(match, source)
        self.assertLess(source.index(match), source.index("if(st.type != T_DIR)"))

    def test_sources_compile_against_xv6_shaped_headers(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "kernel").mkdir()
            (base / "user").mkdir()
            (base / "kernel" / "types.h").write_text(
                "typedef unsigned int uint; typedef unsigned long uint64;\n"
            )
            (base / "kernel" / "stat.h").write_text(
                "#define T_DIR 1\n#define T_FILE 2\n#define T_DEVICE 3\n"
                "struct stat { int dev; uint ino; short type; short nlink; uint64 size; };\n"
            )
            (base / "kernel" / "fs.h").write_text(
                "#define DIRSIZ 14\nstruct dirent { unsigned short inum; char name[DIRSIZ]; };\n"
            )
            (base / "kernel" / "fcntl.h").write_text("#define O_RDONLY 0\n")
            (base / "user" / "user.h").write_text(
                "struct stat; int stat(const char*, struct stat*); int open(const char*, int);\n"
                "int fstat(int, struct stat*); int read(int, void*, int); int close(int);\n"
                "int printf(const char*, ...); int fprintf(int, const char*, ...);\n"
                "int strcmp(const char*, const char*); char *strcpy(char*, const char*);\n"
                "unsigned long strlen(const char*); void *memmove(void*, const void*, unsigned long);\n"
                "void exit(int);\n"
            )
            for name in ("mystat.c", "find.c"):
                result = subprocess.run(
                    ["cc", "-std=c99", "-Wall", "-Wextra", "-Werror", "-fno-builtin",
                     "-fsyntax-only",
                     "-I", str(base), str(USER / name)],
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
