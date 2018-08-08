#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <syslog.h>
#include <string.h>
#include <time.h>

void log_message(char *filename, char *message)
{
    FILE *logfile;
    logfile = fopen(filename, "a");
    if (!logfile)
        return;
    fprintf(logfile, "%s\n", message);
    fclose(logfile);
}

int main(void)
{
    char filename[] = "/home/miecatt/Documents/WallChanger/log.txt";
    char msg[256];
    
    /* Our process ID and Session ID */
    pid_t pid, sid;

    /* Fork off the parent process */
    pid = fork();
    if (pid < 0)
    {
        exit(EXIT_FAILURE);
    }
    /* If we got a good PID, then
           we can exit the parent process. */
    if (pid > 0)
    {
        exit(EXIT_SUCCESS);
    }

    /* Change the file mode mask */
    umask(0);

    /* Open any logs here */
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    sprintf(msg, "[Deamon][info][%d:%d:%d]: Started.", tm.tm_hour, tm.tm_min, tm.tm_sec);
    log_message(filename, msg);

    /* Create a new SID for the child process */
    sid = setsid();
    if (sid < 0)
    {
        /* Log the failure */
        exit(EXIT_FAILURE);
    }

    /* Change the current working directory */
    if ((chdir("/")) < 0)
    {
        /* Log the failure */
        exit(EXIT_FAILURE);
    }

    /* Close out the standard file descriptors */
    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);

    /* Daemon-specific initialization goes here */

    /* The Big Loop */
    while (1)
    {
        /* Do some task here ... */
        t = time(NULL);
        tm = *localtime(&t);
        sprintf(msg, "[Deamon][info][%2d:%2d:%2d]: Shell started.", tm.tm_hour, tm.tm_min, tm.tm_sec);
        log_message(filename, msg);

        system("/home/miecatt/Documents/WallChanger/SetWP.sh");

        sleep(30); /* wait 30 seconds */
    }
    exit(EXIT_SUCCESS);
}