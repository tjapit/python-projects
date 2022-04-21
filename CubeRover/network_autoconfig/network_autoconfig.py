#!/usr/bin/python
"""Service to auto-connect to a given local network on startup and
automatically tries reconnect whenever it fails to ping the router.

Code designed for Linux-based systems.

@author Timothy Japit
"""
import os
from time import sleep
# from datetime import date

"""Variables"""
# router IP address
router_ip = "192.168.1.1"
# sleep time
interval = 5
# service
service = "wpa_supplicant"
# driver for wpa_supplicant
driver = "nl80211"
# hardware interface on Pi
interface = "wlan0"
# configuration file for wpa_supplicant
wpa_supplicant_config = "/etc/wpa_supplicant/wpa_supplicant.conf"
# control interface path
control_interface_path = "/var/run/wpa_supplicant/wlan0"

"""Functions"""
def check_connection(router_ip):
    """Pings the given router IP, returns the 0 when connected.

    Args:
        router_ip (String):IP address of the router
    
    Returns:
        int:returns 0 when connected    
    """
    
    command = "ping -c 1 %s" %router_ip
    return os.system(command)

def initialize(config, service, driver):
    """Connects to the network with the given config file, service, and driver.

    Args:
        config (String):configuration file path
        
        
    Returns:
        int:returns 0 when wpa_supplicant successfully initialized
    """
    service = "wpa_supplicant"
    return os.system("sudo {} -B -i {} -D {} -c {}".format(service, interface, driver, config))

def remove_existing_interface(control_interface_path):
    """Removes the existing control interface from previous wpa_supplicant calls
    
    Args:
        control_interface_path (String):file path of the control interface
        
    Returns:
        int:returns 0 if successfully removed
    """
    command = "rm"
    path = "/var/run/wpa_supplicant/wlan0"
    return os.system("sudo {} {}".format(command, path))

def killall(service):
    """Kills all instances of a service that is running
    
    Args:
        service (String):name of the service to be killed
    
    Returns:
        int:returns 0 if services are succesfully killed
    """
    command = "killall"
    return os.system("sudo {} {}".format(command, service))


# def reconfig(interface):
#     """Forces wpa_supplicant to re-read its config file. (reconnects, basically)
#     
#     Args:
#         interface (String):WLAN hardware interface on device
#         
#     Returns:
#         int:returns 0 if successful in telling wpa_supplicant to reconfig
#     """
#     service = "wpa_cli"
#     command = "reconfigure"
#     return os.system("{} -i {} {}".format(service, interface, command))

def reconnect(service, control_interface_path, wpa_supplicant_config):
    """Kills all the service, and tries to reconnect to the network specified in the config file
    
    Args:
        service (String):service to be killed
        control_interface_path (String):path to the control interface file
        wpa_supplicant_config (String):wpa_supplicant configuration file path
        
    Returns:
        int:returns 0 if successful in reconnecting
    """
    # remove configuration from variable path, and re-do connection config
    remove_existing_interface(control_interface_path)
    # kill all wpa_supplicant services running
    killall(service)
    
    # wait a bit before reinitializing
    sleep(interval)
    
    # reinitialize config file
    initialize(wpa_supplicant_config, service, driver)

"""Main"""
def main():
    # continuously check connection with the specified interval
    while True:
        try:
            # ping the router
            response = check_connection(router_ip)
#             # wait for response
#             sleep(interval)
            # check response from router
            if response != 0:
                # network inactive, echo message indicating trying to reconnect
                os.system("sudo echo Reconnecting...")
                # turn on interface
                os.system("sudo ifconfig %s up" %interface)
                # reconnect
                reconnect(service, control_interface_path, wpa_supplicant_config)
                
                # wait a bit (this is the challenge with millenials like me, not enough patience)
                sleep(interval)
                  
            # network active, sleep before pinging again
            sleep(interval)
                                      
        # Ctrl + C to exit
        except KeyboardInterrupt:
            #os.system("ifconfig %s down" %interface)
            raise SystemExit
                    
if __name__ == "__main__":
    main()