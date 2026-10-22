#include "kernel/types.h"
#include "user/user.h"

int
main(int argc, char *argv[])
{
  if(argc != 2){
    fprintf(2, "usage: sleep <ticks>\n");
    exit(1);
  }

  // The course xv6 tree renames the traditional sleep system call to pause.
  pause(atoi(argv[1]));
  exit(0);
}
