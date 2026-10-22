#include "kernel/types.h"
#include "kernel/stat.h"
#include "kernel/fs.h"
#include "kernel/fcntl.h"
#include "user/user.h"

static char *
basename(char *path)
{
  char *name = path + strlen(path);

  while(name > path && name[-1] != '/')
    name--;
  return name;
}

static void
find(char *start, char *target)
{
  char path[512];
  char name[DIRSIZ + 1];
  char *p;
  int fd;
  struct dirent de;
  struct stat st;

  if((fd = open(start, O_RDONLY)) < 0){
    fprintf(2, "find: cannot open %s\n", start);
    return;
  }

  if(fstat(fd, &st) < 0){
    fprintf(2, "find: cannot stat %s\n", start);
    close(fd);
    return;
  }

  if(strcmp(basename(start), target) == 0)
    printf("%s\n", start);

  if(st.type != T_DIR){
    close(fd);
    return;
  }

  if(strlen(start) + 1 + DIRSIZ + 1 > sizeof(path)){
    fprintf(2, "find: path too long %s\n", start);
    close(fd);
    return;
  }

  strcpy(path, start);
  p = path + strlen(path);
  if(p > path && p[-1] != '/')
    *p++ = '/';

  while(read(fd, &de, sizeof(de)) == sizeof(de)){
    if(de.inum == 0)
      continue;

    memmove(name, de.name, DIRSIZ);
    name[DIRSIZ] = 0;
    if(strcmp(name, ".") == 0 || strcmp(name, "..") == 0)
      continue;

    memmove(p, name, DIRSIZ + 1);
    find(path, target);
  }

  close(fd);
}

int
main(int argc, char *argv[])
{
  if(argc != 3){
    fprintf(2, "usage: find <dir> <name>\n");
    exit(1);
  }

  find(argv[1], argv[2]);
  exit(0);
}
