#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int
main(void)
{
  const char *message = "hello, kernel\n";

  int fd = open("note.txt", O_CREAT | O_WRONLY | O_TRUNC, 0644);
  if(fd < 0){
    perror("open");
    return 1;
  }
  printf("open returned descriptor %d\n", fd);

  ssize_t count = write(fd, message, strlen(message));
  if(count < 0){
    perror("write");
    close(fd);
    return 1;
  }
  printf("write sent %zd bytes\n", count);
  close(fd);

  fd = open("note.txt", O_RDONLY);
  if(fd < 0){
    perror("open");
    return 1;
  }

  char buffer[64];
  count = read(fd, buffer, sizeof(buffer) - 1);
  if(count < 0){
    perror("read");
    close(fd);
    return 1;
  }
  buffer[count] = '\0';
  printf("read got %zd bytes: %s", count, buffer);
  close(fd);

  return 0;
}
