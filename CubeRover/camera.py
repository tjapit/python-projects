from picamera import PiCamera
from time import sleep
import os

# # initialize once only, otherwise "Out of resources" error caused
# global picam
# picam = PiCamera()

def camera():
    """Takes a picture and saves it to the pre-determined filepath
    
    Returns:
        str:the picture filename
    """
    picam = PiCamera()
    filename = 'image.jpg'
    filepath = f'/home/pi/MAE481/comms/{filename}' 
    # create file and change write permission, debug: file can't be created by PiCamera.capture()
    os.system(f"sudo touch {filepath}")
    os.system(f"sudo chmod a+w {filepath}")
    picam.start_preview()
    sleep(2)
    picam.capture(filepath)
    picam.stop_preview()
    # cleanup picam
    picam.close()
    return filename

if __name__ == '__main__':
    camera()