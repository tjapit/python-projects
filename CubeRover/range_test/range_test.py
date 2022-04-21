#!/usr/bin/python3
"""Script to test client-server connection in addition to the range test.

Commands designed for Linux servers.

@author Timothy Japit
"""
from time import sleep
import os
import sys
# Working on raspi Raspbian command line:
# sudo echo -e "Test 1:" >> iwconfig_output_test.txt & iwconfig wlan0 |
# grep -E 'wlan0|Bit|Signal|Frequency' >> iwconfig_output_test.txt &
# echo -e "\n" >> iwconfig_output_test.txt

def header(n, filename):
    """Generates test header string with commands to append it to the output file.

    Args:
        n (int):number of tests to run
        filename (String):file name to append to

    Returns:
        String:test header with commands to output to file
    """
#   echo -e "Test 1:" >> iwconfig_output_test.txt
    header = "Test " + str(n) + ":"
    output = f"echo -e {header} >> {filename} "
    return output

def rssi(filename):
    """Tests the network with iwconfig and checks the bit rate, frequency, and RSSI.

    Args:
        filename (String):filename to append to

    Returns:
        String:result of the test
    """
#   iwconfig wlan0 | grep -E 'wlan0|Bit|Signal|Frequency' >> iwconfig_output_test.txt
    command = "iwconfig wlan0"
    search_results = "grep -E 'wlan0|Bit|Signal|Frequency'"
    output = command + " | " + search_results + " >> " + filename
    return output

def create_file(filename):
    """Creates the given file and changes write permission to allow all.
    
    Args:
        filename (String):name of the file to be modified
        
    """
    # prepend the file path of range test script to save test results in the same folder
    filename = os.path.dirname(os.path.abspath("range_test.py")) + "/" + filename
    # create file and change write permission
    os.system(f"sudo touch {filename}")
    os.system(f"sudo chmod a+w {filename}")
    
def range_test(n, delay, filename):
    """Tests signal strength and writes the result to a file.

    Args:
        n (int):number of repetition of test
        delay (float):delay between each test in seconds
        filename (String):name of the file to write to

    """
    # create file
    create_file(filename)
    # admin access
    admin_access = "sudo"
    test_executed = 0
    for i in range(n):
        # Test header
        test_header = header(i + 1, filename)
        # RSSI test
        rssi_results = rssi(filename)
        # add newline
        newline = f"echo -e '\n' >> {filename}"
        # command to execute
        command = admin_access + " " + test_header + " && " + rssi_results
#         command = test_header + " && " + rssi_results
#         + " & " + newline
        # execute test in command line
        os.system(command)
        # print to command line which iteration
        sys.stdout.write(f"Test {i+1} in progress..." + '\r')
        sys.stdout.flush()
        # sleep with given delay
        sleep(delay)
    # Indicate test finished
    print(f"{n} tests completed and written to {filename}")
    
    
    
def main():
    """Runs the test.

    """
    # prompt admin for number of tests, delays in-between, and test results filename
    n = int(input("Number of tests to run: "))
    delay = float(input("Delay between each test in seconds: "))
    filename = input("Test filename: ")
    # signal strength test based on range
    range_test(n, delay, filename)
    

# run test 
if __name__ == '__main__':
    main()