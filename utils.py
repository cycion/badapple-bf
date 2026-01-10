import cv2
from pathlib import Path

cap = cv2.VideoCapture("badapple.mp4")
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

PATH = ["ori","bf","bf2","bf3"]
PATH2 = ["text", "bfcode"]

def bfcodestat():                                                                       # Determines the optimal filler, resolution and gives useful stats
    symbol = ["+", "-", ">", "<", "[", "]", "."]
    for path in PATH[1:]:
        sumChar = 0
        maxChar = 0
        minChar = 100000000000000
        occurence = [0, 0, 0, 0, 0, 0, 0]
        for i in range(1,frameCount + 1):
            with open(f"res/bfcode/{path}/{i}.bf") as f:
                content = f.read()
                size = len(content)
                for i in range(len(symbol)):
                    occurence[i] += content.count(symbol[i])
                sumChar += size
                if size > maxChar:
                    maxChar = size
                if size < minChar:
                    minChar = size
        print(f"================ {path} ================")
        print(f"Average character count: {sumChar // frameCount}")
        print(f"Average count for {symbol}: {[o // frameCount for o in occurence]}")
        print(f"Max character count: {maxChar}")
        print(f"Min character count: {minChar}")
        height = round((minChar / 3)**0.5)
        width = height*3
        print(f"Optimal next resolution: {width} x {height}")
        print(f"Optimal filler (ASCII ordinal): '{chr(sum( [ord(c)*o for c,o in zip(symbol, occurence)] )//sumChar)}' ({sum( [ord(c)*o for c,o in zip(symbol, occurence)] )//sumChar})")
        opb = brightness(sum( [brightness(c)*o for c,o in zip(symbol, occurence)] ) / sumChar)
        print(f"Optimal filler (visual density): '{opb}' ({ord(opb)})")


def cleanup(choice1, choice2):
    if choice2 == None or choice1 == None:
        exit(2)
    print(f"Cleaning res/{PATH2[choice2]}/{PATH[choice1]}")
    directory = Path(f"res/{PATH2[choice2]}/{PATH[choice1]}")
    
    for file in directory.glob('*'):
        if file.is_file():
            file.unlink()

def closest(givenList, target):

    def difference(givenList):
        return abs(givenList - target)

    result = min(givenList, key=difference)
    return result

def brightness(c) :
    characters = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
    density = [0, 0.0751, 0.0829, 0.0848, 0.1227, 0.1403, 0.1559, 0.185, 0.2183, 0.2417, 0.2571, 0.2852, 0.2902, 0.2919, 0.3099, 0.3192, 0.3232, 0.3294, 0.3384, 0.3609, 0.3619, 0.3667, 0.3737, 0.3747, 0.3838, 0.3921, 0.396, 0.3984, 0.3993, 0.4075, 0.4091, 0.4101, 0.42, 0.423, 0.4247, 0.4274, 0.4293, 0.4328, 0.4382, 0.4385, 0.442, 0.4473, 0.4477, 0.4503, 0.4562, 0.458, 0.461, 0.4638, 0.4667, 0.4686, 0.4693, 0.4703, 0.4833, 0.4881, 0.4944, 0.4953, 0.4992, 0.5509, 0.5567, 0.5569, 0.5591, 0.5602, 0.5602, 0.565, 0.5776, 0.5777, 0.5818, 0.587, 0.5972, 0.5999, 0.6043, 0.6049, 0.6093, 0.6099, 0.6465, 0.6561, 0.6595, 0.6631, 0.6714, 0.6759, 0.6809, 0.6816, 0.6925, 0.7039, 0.7086, 0.7235, 0.7302, 0.7332, 0.7602, 0.7834, 0.8037, 0.9999]
    if type(c) == type('c'):
        return density[characters.index(c)]
    if type(c) == type(0.1):
        return characters[density.index(closest(density, c))]
