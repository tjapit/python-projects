"""Server program for the RTDT rover.
Socket programming codes are based on the following tutorial: 
https://www.youtube.com/watch?v=3QiPPX-KeSc&list=PLH35dLTvD28zew9YLG-l5icHHvFpnlenD&index=4&t=2399s

@author Timothy Japit
"""
import socket
import sys
import os
from time import sleep
# NETWORK AUTOCONFIG MODULE
autoconfig_path = '/home/pi/MAE481/comms/network_autoconfig'
sys.path.insert(0, autoconfig_path)
import network_autoconfig

# # RANGE TEST MODULE
# range_test_path = '/home/pi/MAE481/comms/range_test'
# sys.path.insert(0, range_test_path)
# import range_test

# STANDBY PROTOCOL MODULE
standby_protocol_path = '/home/pi/MAE481/comms/'
sys.path.insert(0, standby_protocol_path)
import standby_protocol

# GO DISTANCE MODULE
goDistance_path = '/home/pi/MAE481/comms/'
sys.path.insert(0, goDistance_path)
import goDistance

# ROTATE ANGLE MODULE
rotateAngle_path = '/home/pi/MAE481/comms/'
sys.path.insert(0, rotateAngle_path)
import rotateAngle


# CAMERA MODULE
camera_path = '/home/pi/MAE481/comms/'
sys.path.insert(0, camera_path)
import camera


# Server socket info
HEADER = 64
PACKET_LIMIT = 1024
PORT = 5050
SERVER = "192.168.1.52"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# initialize server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4, TCP
# bind server socket to address
server.bind(ADDR)


def ftp(conn, filename):
     """Server-side ftp, reads from a file and sends it to the client.
     Code adapted from: 
     https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python#9382116
     
     Args:
        conn (Socket):client socket
        filename (str):name of the file to send
     """
     # open the file to send
     with open(filename, 'rb') as file:
        #  read file and keep reading while content is still available
         file_data = file.read(PACKET_LIMIT)
         while file_data:
             # sending data
             conn.send(file_data)
             # keep reading
             file_data = file.read(PACKET_LIMIT)
         file.close()
         # debug: prompt was resent before ftp loop was exited in client
         sleep(5)
         # send disconnect code for client to exit out of ftp mode
         conn.send(DISCONNECT_MESSAGE.encode(FORMAT))

def main():
    """Server starts listening for a new connection.
    
    Return:
        int:returns 0 when server is terminated by client
    """
    # indicate server starting
    print("[STARTING] Server is starting...")
    server_up = True
    while server_up:
        # listening, only 1 device allowed to connect at any time
        server.listen(1)
        print(f"[LISTENING] Server is listening on {SERVER}")

        # store client socket and address after accepting connection
        conn, addr = server.accept()

        # indicate connected by printing to cmd and client
        print(f"[CONNECTED] {addr} connected.")
        conn.send(f"[CONNECTED] {SERVER} connected.\n".encode(FORMAT))

#         # run range test directly with the command line
#         os.system("sudo python3 range_test.py")

        # connected to client and listening for message
        connected = True
        while connected:
#             # prompt string in binary
#             prompt_bin = (
#                 b"\tRTDT commands:\n"
#                 b"\t\tstandby - standby mode, prints temperature and time stamp\n"
#                 b"\t\tgodistance - moves the rover forward/backward with the specified distance and speed\n"
#                 b"\t\trotate - rotates the rover left/right with the specified angle\n"
#                 b"\t\tcamera - captures image in front of the rover and saves it to the specified filename\n"
#             )
#             # prompt client for action
#             conn.send(prompt_bin)
            # receive message from client
            msg = conn.recv(PACKET_LIMIT).decode(FORMAT)
            # print message received and indicate to client that message was
            # received
            print('\n' + msg + '\n')
            conn.send(b"Message received.\n")
            # DISCONNECT FROM ROVER
            if msg == DISCONNECT_MESSAGE:
                # prompt to keep server up or otherwise
                conn.send(b"Keep server running?(y/n)")
                # receive response
                resp = conn.recv(PACKET_LIMIT).decode(FORMAT)
                # server down
                if resp == 'n':
                    server_up = False
                # connection flag
                connected = False
                # disconnect message
                print(f"[DISCONNECTED] {addr} connection closed.")
#             # RANGE TEST
#             elif msg == 'r':
#                 # number of reps
#                 conn.send(b"Number of tests to run: ")
#                 n = int(conn.recv(PACKET_LIMIT).decode(FORMAT))
# 
#                 # delay
#                 conn.send(b"Delay between each test in seconds: ")
#                 delay = float(conn.recv(PACKET_LIMIT).decode(FORMAT))
# 
#                 # filename
#                 conn.send(b"Test filename: ")
#                 filename = conn.recv(PACKET_LIMIT).decode(FORMAT)
# 
#                 # run range test by calling the script that actually tests it
#                 # debug: need to create the file first and change mod permission before writing to it
#                 # otherwise permission denied error
#                 range_test.range_test(n, delay, filename)
            # STANDBY PROTOCOL
            elif msg == "standby":
                # keep rereading & resending temperature data while in standby
                standby = True
                while standby:
                    # store standby mode temperature and time stamp string
                    timetemp = standby_protocol.main()
                    # send to client
                    conn.send(timetemp.encode(FORMAT))
                    # delay a bit before redoing the loop
                    sleep(1)
                    # receive message from client to continue or break out of
                    # standby
                    stdby_break = conn.recv(PACKET_LIMIT).decode(FORMAT)
                    # safe word to break out of standby mode = 'y'
                    if stdby_break == 'y':
                        standby = False
            # GO DISTANCE
            elif msg == "godistance":
                # keep in GO DISTANCE mode unless exit message 'q' is received
                godistance = True
                while godistance:
                    # receive direction from client
                    dir = conn.recv(PACKET_LIMIT).decode(FORMAT)
                    # exit message 'q'
                    if dir == 'q':
                        godistance = False
                    # if not exit,
                    else:
                        # receive distance and speed 
                        xr = conn.recv(PACKET_LIMIT).decode(FORMAT)
                        sleep(1)
                        vr = conn.recv(PACKET_LIMIT).decode(FORMAT)
                        # convert distance and speed to float
                        xr = float(xr)
                        vr = float(vr)
                        # execute GO DISTANCE
                        x = goDistance.goDistance(dir, xr, vr)
                        # format actual distance traveled
                        x_str = f"{x:.1f}"
                        # send actual distance traveled
                        conn.send(x_str.encode(FORMAT))
            # ROTATE ANGLE
            elif msg == "rotate":
                # keep in ROTATE ANGLE mode unless exit message 'q' is received
                rotate = True
                while rotate:
                    # receive rotation direction from client
                    dir = conn.recv(PACKET_LIMIT).decode(FORMAT)
                    # exit message 'q'
                    if dir == 'q':
                        rotate = False
                    # if not exit,
                    else:
                        # receive angle target
                        angle_target = conn.recv(PACKET_LIMIT).decode(FORMAT)
                        # convert angle back to float
                        angle_target = float(angle_target)
                        # execute ROTATE ANGLE
                        angle = rotateAngle.rotateAngle(dir, angle_target)
                        # format actual angle rotated
                        angle_str = f"{angle:.1f}"
                        # send actual angle rotated
                        conn.send(angle_str.encode(FORMAT))
            # CAMERA
            elif msg == "camera":
                # takes a picture
                filename = camera.camera()
                # send picture file
                ftp(conn, filename)
                
#             # COMMAND NOT RECOGNIZED
#             else:
#                 conn.send(b"Try again.\n")
#                 sleep(1)

        # close connection
        conn.close()
    # server down message
    print(f"[SERVER DOWN] Server terminated by {addr}")
    return 0
#
#         # closing connection to client
#         conn.close()
#         # send file
#         ftp(conn)

#         # close connection
#         msg = conn.recv(PACKET_LIMIT).decode(FORMAT)
#         if msg == DISCONNECT_MESSAGE:
#             print(f"[DISCONNECTED] {addr} connection closed.")
#             conn.close()
#             raise SystemExit

#         # prompt client to continue or close server
#         conn.send("Closing connection, keep server running?(y/n)".encode(FORMAT))
#         cont_response = conn.recv(PACKET_LIMIT).decode(FORMAT)
#
#         # close connection
#         conn.close()
#
#         # exit
#         if cont_response == 'n':
#             raise SystemExit


if __name__ == '__main__':
    main()
#     # router ip address
#     router_ip = '192.168.1.1'
#     # emulated do-while loop to check if network is online
#     ping_result = network_autoconfig.check_connection(router_ip)
#     if ping_result == 0:
#         online = True
#     else:
#         online = False
#     # if not online then it will not run server until connection to router has been made
#     while (not online):
#         ping_result = network_autoconfig.check_connection(router_ip)
#         if ping_result == 0:
#             online = True
#         else:
#             online = False
#     # if it's online, run server continuously unless terminated by client
#     server_up = True
#     while (server_up):
#         terminated = main()
#         if (terminated == 0):
#             server_up = False
