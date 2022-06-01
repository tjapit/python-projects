/**
 *	@file ping.c
 *	@author Timothy Japit
 *
 *	Short script to test the WLAN 2.4 GHz on-board the RasPi.
 */
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include <unistd.h>

/** Array length for the strings. */
#define STRING_SIZE 100

/**
 * Returns error if the test to file character is not 'y' or 'n'.
 */
static void usage()
{
  fprintf(stderr, "Response should be 'y' or 'n'\n");
  exit(EXIT_FAILURE);
}

/**
 * Returns 1 if the user chooses to save to file, and 0 otherwise.
 *
 * @param response user response to file saving prompt
 * @return 1 if the user chooses to save to file
 */
static int saveToFile(const char *response)
{
  // save file
  if (strcasecmp("y", response) == 0)
  {
    return 1;
  }
  // no to file saving
  else
  {
    return 0;
  }
}

/**
 * Program starting point.
 *
 * @param argc number of arguments from the command-line
 * @param argv String array of the arguments from the user
 * @return exit status code
 */
int main(int argc, char *argv[])
{
  /** Number of runs */
  int runs = 0;

  /** Save to file response */
  char *response = (char*) malloc(STRING_SIZE * sizeof(char));

  /** Filename */
  char *filename = (char*) malloc(STRING_SIZE * sizeof(char));

  /** Pi IP address */
  char *addr = (char*) malloc(STRING_SIZE * sizeof(char));

  /** Ping command */
  char *command = (char*) malloc(STRING_SIZE * sizeof(char));

  // ping command
  printf("Command: ");
  gets(command);

  // prompt for ip address
  printf("Pi IP address: ");
  gets(addr);

  // save test to file?
  printf("Save test results to file? (y/n) ");
  gets(response);

  // response error checking
  if (strcasecmp("y", response) != 0 && strcasecmp("n", response) != 0)
  {
    usage();
  }
  else
  {
    // valid response
    if (saveToFile(response))
    {
      // filename
      printf("Filename: ");
      gets(filename);

      /*
       * Code from https://stackoverflow.com/questions/230062/whats-the-best-way-to-check-if-a-file-exists-in-c
       */
      // if file exists, append
      if (access(filename, F_OK) == 0)
      {
        printf("\nResults will be appended to the file.\n\n");
      }
      // otherwise create new
      else
      {
        printf("\nResults will be written to a new file.\n\n");
      }
      strcat(addr, " >> ");

      // concatenate ip address to file
      strcat(addr, filename);

    }
  }

  // prompt for number of runs
  printf("Number of runs: ");
  (void) scanf("%d", &runs);
  printf("\n");

  // concatenating command, address, and output redirection to file
  strcat(command, " ");
  strcat(command, addr);

  for (int i = 0; i < runs; ++i)
  {
    // running command on shell
    system(command);
  }

  // open in console if saved to file
  if (saveToFile(response))
  {
    char consoleOut[STRING_SIZE] = "more ";
    strcat(consoleOut, filename);
    system(consoleOut);
  }

  printf("\n");

  // free mem
  free(response);
  free(filename);
  free(addr);
  free(command);

  exit(EXIT_SUCCESS);
}
