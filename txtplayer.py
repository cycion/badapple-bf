import cv2, time, os
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

cap = cv2.VideoCapture("badapple.mp4")
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
PATH = ["ori", "bf", "bf2", "bf3"]
NAME = ["brainfk_interpreted_interpreted_interpreted", "brainfk_interpreted_interpreted", "brainfk_interpreted", "brainfk"]

print("5")
time.sleep(1)
print("4")
time.sleep(1)
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(3)
print("START")

# Barrier to "hopefully" sync the writing of the file
barrier = Barrier(4)

def play(path, name):
    for i in range(1, frameCount + 1):
        with open(f"res/text/{path}/{i}.txt") as f:
            frame = f.read()
        file = f"output/{name}.bf" if path != "ori" else f"output/{name}.txt"
        with open(file, "w") as player:
            player.write(frame)
            player.flush()# Force disk write
            os.fsync(player.fileno())
        
        # Double barrier to ensure shit don't get out of sync (It still does)
        barrier.wait()
        if PATH.index(path) == 0:
            time.sleep(0.1)
            barrier.wait()
        else:
            barrier.wait()
        # Wait for file watcher to detect change. The higher this value, the lower the framerate, the better the synchronisation
        time.sleep(1.5)

# Parralel to makes the animation in 4 files looks more synchronized
with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(play, PATH, NAME)

print("END")
