#!/usr/bin/python
import os

# test outputs
interface = "wlan0"
router_ip = "192.168.1.1"

# # ifconfig test
# command = "ifconfig " + interface
# response = os.system(command)
# print(response)

# # wpa_cli test
# command = "wpa_cli -i {} reconfigure".format(interface)
# print(os.system(command))

# ping test
command = "ping -c 1 {}".format(router_ip)
if os.system(command) == 0:
    print("\nSucc\n")