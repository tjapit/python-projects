"""Client program for connecting to the rover.
Socket programming codes are based on the following tutorial: 
https://www.youtube.com/watch?v=3QiPPX-KeSc&list=PLH35dLTvD28zew9YLG-l5icHHvFpnlenD&index=4&t=2399s

@author Timothy Japit
"""
import socket
import sys
from time import sleep

# Server protocol and address
HEADER = 64
PACKET_LIMIT = 1024
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# create client socket, IPv4 and TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def ftp(client, filename):
    """Client-side ftp, receives the data from server and writes it to a file.
    Code adapted from: 
    https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python#9382116
    
    Args:
        client (Socket):client socket object
        filename (str):filename to save as
    """
    # create file to write to
    with open(filename, 'wb') as file:
        print(f"{filename} has been created.\n")
        # receiving data
        file_data = client.recv(PACKET_LIMIT)
        # receive disconnect message once file is done being transferred
        while (file_data != DISCONNECT_MESSAGE.encode(FORMAT)):
            # # debug
            # print(file_data)
            # write to file
            file.write(file_data)
            # receive more data
            file_data = client.recv(PACKET_LIMIT)
        file.close()

# def send(msg):
    # """Standard TCP messaging protocol.
    # """
    # # encode message to byte form
    # message = msg.encode(FORMAT)
    # msg_length = len(message)
    # # encode msg_length to byte form
    # send_length = str(msg_length).encode(FORMAT)
    # # pad to 64 (spaces = 64 - send_length) *remember byte rep of space (b' ')
    # send_length += b' ' * (HEADER - len(send_length))
    # # send header
    # client.send(send_length)
    # # send message
    # client.send(message)
    # # laziness
    # print(client.recv(PACKET_LIMIT).decode(FORMAT))

def goDistancePrompts():
    """Prompts for the direction, distance, and speed for the rover to travel.
    
    Returns:
        str: direction of travel (forward/backward) or exit code 'q'
        float: distance to travel in meters
        float: speed of travel in centimeters per second
    """
    # prompt for direction
    print('Enter Direction')
    print('f - forward')
    print('b - backward')
    print('q - quit')
    dir = input()
    # error checking for direction
    while dir != 'f' and dir != 'b' and dir != 'q':
        print('Error: Invalid Direction')
        print('Enter Direction')
        print('f - forward')
        print('b - backward')
        print('q - quit')
        dir = input()
    # exit code
    if (dir == 'q'):
        return dir, 0, 0
    # prompt for direction
    print('Enter distance to travel (in m)')
    xr = input()
    # error checking for distance
    while(1):
        try: 
            xr = float(xr)
            break
        except:
            print('Error: Input Cannot Be Converted to Float')
            print('Enter Distance to travel (in m)')
            xr = input()

    # prompt for speed
    print('Enter speed (in cm/s):')
    vr = input()
    # error checking for speed
    while(1):
        try:
            vr = float(vr)/100
            break
        except:
            print('Error: Input Cannot Be Converted to Float')
            print('Enter speed (in cm/s)')
            vr = input()
    # return values
    return dir, xr, vr

def rotateAnglePrompts():
    """Prompts user to enter direction and angle of rotation.

    Returns:
        str:direction (l)eft/(r)ight or exit code 'q'
        float:distance of travel in meters
    """   
    # direction prompt
    print('Enter Direction')
    print('r - right')
    print('l - left')
    print('q - quit')
    dir = input()
    
    # error checking for direction
    while dir != 'r' and dir != 'l' and dir != 'q':
        print('Error: Invalid Direction')
        print('Enter Direction')
        print('r - right')
        print('l - left')
        print('q - quit')
        dir = input()
    # if exit code received, return q and 0 angles
    if (dir == 'q'):
        return 'q', 0
    
    # prompt for angle
    print('Enter Angle to Rotate to (in degrees)')
    angle_target = input()
    # error checking for angle
    while(1):
        try: 
            angle_target = float(angle_target)
            break
        except:
            print('Error: Input Cannot Be Converted to Float')
            print('Enter Angle to Rotate to (in degrees)')
            angle_target = input()
    # return direction and angle
    return dir, angle_target

def initialPrompt():
    """Prompts the user with the available commands and returns the valid response
    
    Returns:
        str:valid response string
    """
    # prompt string
    prompt_str = (
               f"\tRTDT commands:\n"
               f"\t\tstandby - standby mode, prints temperature and time stamp\n"
               f"\t\tgodistance - moves the rover forward/backward with the specified distance and speed\n"
               f"\t\trotate - rotates the rover left/right with the specified angle\n"
               f"\t\tcamera - captures image in front of the rover and saves it to the specified filename\n"
               f"\t\tquit - disconnect from the rover\n"
           )
    while True:
        print(prompt_str)
        response = input("response: ")
        print()
        if response == 'standby' or response == 'godistance' or response == 'rotate' or response == 'camera':
            return response
        elif response == 'quit':
            return DISCONNECT_MESSAGE
    
def main():
    """Starts connection with server and requests the test file.

    """
    # prompt for server IP
    server_ip = input("Server IP address: ")
    addr = (server_ip, PORT)
    # connect to server address
    client.connect(addr)
    # CONNECTED
    print(client.recv(PACKET_LIMIT).decode(FORMAT))
    # connected to server
    connected = True
    while connected:
        # receive prompt
        # print(client.recv(PACKET_LIMIT).decode(FORMAT))
        # # answer prompt
        # response = input("response: ")
        
        # RTDT prompt 
        response = initialPrompt()
        # send response
        client.send(response.encode(FORMAT))
        # receive "message was received" response
        print(client.recv(PACKET_LIMIT).decode(FORMAT))
        # DISCONNECT
        if response == DISCONNECT_MESSAGE:
            # receive prompt to keep server up or otherwise
            print(client.recv(PACKET_LIMIT).decode(FORMAT))
            # error checking for response
            response = input()
            while response != 'y' and response != 'n':
                print("Keep server running? (y/n)")
                response = input()
            # send response
            client.send(response.encode(FORMAT))
            # break out of loop
            connected = False
            # send disconnect message
            client.send(response.encode(FORMAT))
            # close connection using client socket
            client.close()
            # DISCONNECTED
            print(f"[DISCONNECTED] {server_ip} connection closed.")
        # # RANGE TEST
        # elif response == 'r':
            # # number of reps
            # print(client.recv(PACKET_LIMIT).decode(FORMAT))
            # n = input()
            # client.send(n.encode(FORMAT))

            # # delay
            # print(client.recv(PACKET_LIMIT).decode(FORMAT))
            # delay = input()
            # client.send(delay.encode(FORMAT))

            # # filename
            # print(client.recv(PACKET_LIMIT).decode(FORMAT))
            # filename = input()
            # client.send(filename.encode(FORMAT))

            # # message indicating file is saved on pi
            # print(f"\nTest results are saved on the Pi, in {filename}\n")
        # STANDBY PROTOCOL
        elif response == "standby":
            # keep receiving temperature data while in standby
            standby = True
            while standby:
                # try block to catch ctrl + C
                try:
                    # receive time and temperature from rover
                    timetemp = client.recv(PACKET_LIMIT).decode(FORMAT)
                    # print on CLI, updated instead of new line
                    sys.stdout.write(timetemp + "\r")
                    sys.stdout.flush()
                    # send message to continue standby
                    client.send(b'n')
                    # delay before sending the next one check for CTRL + CAMERA
                    sleep(1)
                except KeyboardInterrupt:
                    # send break message
                    client.send(b'y')
                    # break out of standby mode
                    standby = False
                    print()
        # GO DISTANCE
        elif response == "godistance":
            # keep in GO DISTANCE mode unless exit message 'q' is received
            godistance = True
            while godistance:
                # prompts for user to enter direction, distance, and speed
                dir, xr, vr = goDistancePrompts()                
                # exit message 'q'
                if dir == 'q':
                    client.send('q'.encode(FORMAT))
                    godistance = False
                # otherwise, send direction, distance, and speed
                else:
                    # direction
                    client.send(dir.encode(FORMAT))
                    sleep(1)
                    # distance to travel
                    client.send(str(xr).encode(FORMAT))
                    sleep(1)
                    # speed of travel
                    client.send(str(vr).encode(FORMAT))
                    # receive actual distance travel and print
                    x = client.recv(PACKET_LIMIT).decode(FORMAT)
                    if dir == 'f':
                        print(f"RTDT has travelled {x} m forward")
                    else:
                        print(f"RTDT has travelled {x} m backward")
        # ROTATE ANGLE
        elif response == "rotate":
            # keep in ROTATE ANGLE mode unless exit message 'q' is received
            rotate = True
            while rotate:
                # prompts for user to enter direction, distance, and speed
                dir, angle_target = rotateAnglePrompts()
                # exit message 'q'
                if dir == 'q':
                    client.send('q'.encode(FORMAT))
                    rotate = False
                # otherwise, send direction and angle
                else:
                    # direction
                    client.send(dir.encode(FORMAT))
                    sleep(1)
                    # angle target
                    client.send(str(angle_target).encode(FORMAT))
                    # receive actual angle rotated and print
                    angle = client.recv(PACKET_LIMIT).decode(FORMAT)
                    if dir == 'r':
                        print(f"RTDT has rotated by {angle} degrees right")
                    else:
                        print(f"RTDT has rotated by {angle} degrees left")
        # CAMERA
        elif response == "camera":
            # prompt filename to save as
            filename = input("Filename to save as: ")
            # receive picture file
            ftp(client, filename)
            
        # # COMMAND UNRECOGNIZED
        # else:
            # print(client.recv(PACKET_LIMIT).decode(FORMAT))
    # # receive prompt to close server or keep it running
    # print(client.recv(PACKET_LIMIT).decode())
    # # send response
    # cont_response = input("response: ")

    # client.send(input("response: ")).encode(FORMAT))


if __name__ == '__main__':
    main()
