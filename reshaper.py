import cv2
import sys

cap = cv2.VideoCapture("badapple.mp4")
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

PATH = ["bf", "bf2", "bf3"]

def reshape(choice):
    path = PATH[choice]
    for i in range(1, frameCount + 1):
        with open(f"res/text/{path}/{i}.txt", 'r') as f:
            template = f.read()
        
        with open(f"res/bfcode/{path}/{i}.bf", 'r') as bf:
            content = bf.read()
        
        sys.stdout.write(f"\rReshaping files {i}/{frameCount}.bf in \'res/text/{path}\'")
        sys.stdout.flush()
        
        result = ""
        pointer = 0
        
        for j in range(len(template)):
            if template[j] == " " or template[j] == "\n":
                result += template[j]
            else:
                if pointer >= len(content):
                    result += template[j]
                else:
                    result += content[pointer]
                    pointer += 1
        
        if pointer < len(content):
            result += content[pointer:]
        
        # Write the result back to the template file
        with open(f"res/text/{path}/{i}.txt", 'w') as f:
            f.write(result)
    sys.stdout.write("\n")
    sys.stdout.flush()