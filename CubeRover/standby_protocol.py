"""Saves the temperature in Celsius and Farenheit, as well as the time stamp when in standby.

@author: James Rearden
"""
import glob
import time
import sys
# import paramiko

# # Define model ground station
# ipad = '10.153.54.1'
# user = 'james'
# psswrd = 'insert_user_password'

# Define thermal sensor file location
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# # Set up paramiko for SSH file transfer
# ssh_client=paramiko.SSHClient()
# ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh_client.connect(hostname=ipad,username=user,password=psswrd)
# # Raises BadHostKeyException, AuthenticationException, SSHException, socket error

# Function to read raw temp data


def read_temp_raw():
    """Reads the raw data of the temperature from the sensor

    Returns:
        String: Raw temperature data
    """
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Function to return temp data from raw temp data


def read_temp():
    """Translates the raw data of the temperature from the sensor
    to something readable in Celsius and Farenheit

    Returns:
        float: Translated temperature data in Celsius
        float: Translated temperature data in Farenheit
    """
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':  # WHILE sensor is connected
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]  # raw recorded temp
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


def main():
    """Reads the raw temperature data and returns the readable form 
    along with the time stamp formatted.

    Returns:
        String: Formatted time of recording and temperature data
    """
    # Read temp and time
    temp = read_temp()
    tm = time.asctime(time.localtime(time.time()))
    # Format the string and print to console updating
    time_temp = f"{tm},({temp[0]:.2f}C, {temp[1]:.2f}F)"
    print(f"{time_temp}\r")
    # Save temp and time to log
    with open('Rover_Temp.txt', 'a') as log:
        log.write("{},{}\n".format(tm, temp))

    return time_temp
    # # Send log to model ground station using SSH
    # ftp_client=ssh_client.open_sftp()
    # ftp_client.put('/home/pi/Rover_Temp.txt','Rover_Temp.txt')
    # ftp_client.close()

    # # Every 1 second
    # time.sleep(1)

if __name__ == '__main__':
    main()