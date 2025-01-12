import cv2
import numpy as np
import threading
import subprocess

#ffmpg settings
ffmpeg_command = [
    "ffmpeg",
    "-f", "rawvideo",
    "-pix_fmt", "bgr24",
    "-s", "640x480",  # Set frame size
    "-i", "-",        # Input from stdin
    "-c:v", "libx264",
    "-preset", "ultrafast",
    "-tune", "zerolatency",
    "-f", "rtp",
    #192.168.0.162
    #
    #172.28.123.183
    "rtp://172.28.123.183:8004"
]
ffmpeg_command = [
    "ffmpeg",
    # Video Input
    "-f", "rawvideo",        # Raw video input
    "-pix_fmt", "bgr24",     # Pixel format (from OpenCV)
    "-s", "640x480",         # Frame size
    "-r", "30",              # Frame rate
    "-i", "-",               # Input from stdin

    # Video Encoding
    "-c:v", "libvpx",        # VP8 codec
    "-b:v", "1M",            # Bitrate
    "-an",                   # Disable audio for video stream

    # RTP Stream for Video
    "-f", "rtp",
    "rtp://192.168.0.162:5004?pkt_size=1200",
]


# Mode settings
mode = 'none'
modes = {'grey', 'edges', 'none', 'blue', 'red', 'green'}
find = False
on = True

# HSV color ranges
color_ranges = {
    'blue': (np.array([90, 100, 30]), np.array([130, 255, 255])),
    'red': (np.array([0, 100, 30]), np.array([10, 255, 255]), np.array([165, 100, 30]), np.array([179, 255, 255])),
    'green': (np.array([35, 100, 30]), np.array([75, 255, 255]))
}

lower = np.array([90, 100, 30])
upper = np.array([130, 255, 255])

# Function to handle terminal input
def get_input():
    global mode, lower, upper, find, on
    while True:
        user_input = input("Enter mode (grey, edges, none, blue, red, green, find) or 'q' to quit: ").lower()
        if user_input == 'q':
            print("Exiting program...")
            on = False
            break
        elif user_input in modes:
            mode = user_input
            print(f"Mode set to: {mode}")
        elif user_input == 'lower':
            lower = np.array([int(input("Lower H: ")), int(input("Lower S: ")), int(input("Lower V: "))])
        elif user_input == 'upper':
            upper = np.array([int(input("Upper H: ")), int(input("Upper S: ")), int(input("Upper V: "))])
        elif user_input == 'find':
            find = True

# Open the default camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

# Start the input thread
input_thread = threading.Thread(target=get_input)
input_thread.daemon = True  # Allows the thread to exit when the main program exits
input_thread.start()

#Start the stream
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

while on:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
        break
    
    # Process and display frames based on mode
    if mode == 'grey':
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Camera Stream", gray_frame)
    elif mode == 'edges':
        edges_frame = cv2.Canny(frame, 100, 200)
        cv2.imshow("Camera Stream", edges_frame)
    elif mode == 'none':
        cv2.imshow("Camera Stream", frame)
    elif find:
        if mode == 'blue':
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([90,100,30])
            upper_blue = np.array([130,255,255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            contours, heirarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
            if len(contours) !=0:
                for contour in contours:
                    if cv2.contourArea(contour) > 100:
                        x,y,w,h = cv2.boundingRect(contour)
                        cv2.rectangle(frame, (x,y),(x+w, y+h), (255, 0, 0), 2)

        if mode == 'green':
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([35, 100, 30])
            upper_blue = np.array([75, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            contours, heirarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
            if len(contours) !=0:
                for contour in contours:
                    if cv2.contourArea(contour) > 100:
                        x,y,w,h = cv2.boundingRect(contour)
                        cv2.rectangle(frame, (x,y),(x+w, y+h), (0, 255, 0), 2)
        
        if mode == 'red':
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask1 = cv2.inRange(hsv, color_ranges['red'][0], color_ranges['red'][1])
            mask2 = cv2.inRange(hsv, color_ranges['red'][2], color_ranges['red'][3])
            mask = cv2.bitwise_or(mask1, mask2)
            contours, heirarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
            if len(contours) !=0:
                for contour in contours:
                    if cv2.contourArea(contour) > 100:
                        x,y,w,h = cv2.boundingRect(contour)
                        cv2.rectangle(frame, (x,y),(x+w, y+h), (0, 0, 255), 2)

        cv2.imshow("Camera Stream", frame)
    elif mode in color_ranges:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if mode == 'red':
            mask1 = cv2.inRange(hsv, color_ranges['red'][0], color_ranges['red'][1])
            mask2 = cv2.inRange(hsv, color_ranges['red'][2], color_ranges['red'][3])
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            mask = cv2.inRange(hsv, color_ranges[mode][0], color_ranges[mode][1])
        color_frame = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow("Camera Stream", mask)
        cv2.imshow(f"{mode.capitalize()}", color_frame)
    

    # Send raw video frame to FFmpeg
    frame = cv2.resize(frame, (640,480))
    ffmpeg_process.stdin.write(frame.tobytes())

    # Wait for a short period to check if 'q' was pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
ffmpeg_process.stdin.close()
ffmpeg_process.wait()