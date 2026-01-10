import numpy as np
import cv2 as cv
import sys, random
from concurrent.futures import ThreadPoolExecutor

# The value of each key is the resolution (Width, Height). Set to None to disable the key
SETTINGS = {"ori": (99, 33), "bf": (150, 50), "bf2": (225, 75), "bf3": (339, 113)}

currentFrame = 0 # Frame counter
cap = cv.VideoCapture('badapple.mp4')
frameCount = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

def fillchoice(brightness):                                                                                                 # Function to output a character base on its brightness
    char = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
    return char[round(brightness * (len(char) - 1) / 255)]

def frame2txt(args):                                                                                                        # Function to converts an image to ASCII arts
    path, resolution, frame, frame_num = args
    
    if resolution == None:
        return None
    
    resized = cv.resize(frame, resolution, interpolation=cv.INTER_AREA)                                                     # Resizing to the wanted resolution with INTER_AREA (stackoverflow said it is good for downscaling)
    ret, binary = cv.threshold(resized, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    binary = binary.astype(np.uint8)
    binary = np.stack([binary]*3, axis=-1)

    with open(f"res/text/{path}/{frame_num}.txt", 'w') as f:
        lineBuffer = ""
        for i in range(resized.shape[0]):                                                                                   # resized.shape is [height, width]
            for j in range(resized.shape[1]):                                                                               # resized[height, width] is pixel brightness
                lineBuffer += fillchoice(int(resized[i, j])) if path == "ori" else "+" if any(binary[i,j]) else " "         # Original file's filler is determined by fillchoice(), bfcode file's filler is determined by any(binary[i,j])
                if j == resized.shape[1] - 1:
                    lineBuffer += "\n"
                    f.write(lineBuffer)
                    lineBuffer = ""

while cap.isOpened():
    ret, frame = cap.read()
 
    # Break when the video stream ends
    if not ret:
        print("\nStream ended, exiting...")
        break
    
    currentFrame += 1

    sys.stdout.write(f"\rProcessing video frames {currentFrame}/{frameCount}")                                              # Progress tracker
    sys.stdout.flush()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)                                                                            # Converts the image to grayscale for processing
    
    # Parallel execution to "hopefully" save some time (I know it doesn't)
    tasks = [(path, resolution, gray, currentFrame) 
             for path, resolution in SETTINGS.items()]
    
    with ThreadPoolExecutor(max_workers=len(SETTINGS)) as executor:
        executor.map(frame2txt, tasks)
 
cap.release()
cv.destroyAllWindows()
