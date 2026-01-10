import cv2, sys
from math import sqrt
import reshaper

cap = cv2.VideoCapture("badapple.mp4")
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

PATH = ["ori", "bf", "bf2", "bf3"]
def generate(content):                                                                              #Generate a simple unoptimised string to display the animation
    fileBuffer = ""
    prevOrd = 0
    for c in content:
        curOrd = ord(c)
        fileBuffer += "+"* (curOrd - prevOrd) if curOrd >= prevOrd else "-"* (prevOrd - curOrd)
        prevOrd = curOrd
        fileBuffer += "." 
    fileBuffer = optimize(fileBuffer)
    return fileBuffer


def optimize(bfcode):
    prevChar = bfcode[0]
    optimized = ""
    _ = 1
    rep = 1
    global optFlag
    optFlag = False
    for c in bfcode[1:]:
        if c == prevChar:
            rep += 1
        else:
            if rep < 15:
                optimized += prevChar * rep
            else:
                optimized += groupAndLoop(rep, prevChar, optFlag)
                optFlag = True
            rep = 1
            prevChar = c
        if _ == len(bfcode) - 1:
            if rep < 15:
                optimized += prevChar * rep
            else:
                optimized += groupAndLoop(rep, prevChar, optFlag)
                optFlag = True
            rep = 1
            prevChar = c
        _ += 1
    return optimized

            
def groupAndLoop(rep, pattern, opt):                                                      
# Groups repetitive characters into a loop  
# I don't even know how I wrote this
    sieve = [True] * (rep + 1)
    sieve[0] = sieve[1] = False

    for i in range(2, int(sqrt(rep)) + 1):
        if sieve[i]:
            for j in range(i * i, rep + 1, i):
                sieve[j] = False
    minSuma = 0
    minSumb = 0
    minSumc = 0
    minSum = rep
    for i in range(rep, 1, -1):
        if sieve[i] == True:
            continue
        else:
            a = 0
            b = 0
            c = rep - i
            for j in range(int(sqrt(i)), 1, -1):
                if i % j == 0:
                    a = j
                    b = i // a
                    break
            if a + b + c + 5 < minSum:
                minSum = a + b + c + 5
                minSuma = a
                minSumb = b
                minSumc = c
            elif a + b + c + 5 == rep:
                break
    if opt == True:                                                                         # Botched fix to reset the brainfuck pointer
        shortened = "<"
        optFlag = False
    else: 
        shortened = ""
    shortened += "+"* minSuma + "[>" + pattern*minSumb + "<-]>" + pattern* minSumc
    return shortened

for j in range(len(PATH) - 1):
    if j != 0:
        reshaper.reshape(j-1)
    for i in range(1, frameCount+1):
        with open(f"res/text/{PATH[j]}/{i}.txt", "r") as f:
            content = f.read()
        with open(f"res/bfcode/{PATH[j+1]}/{i}.bf", "w") as bf:
            sys.stdout.write(f"\rGenerating Brainfuck code {i}/{frameCount}.bf in \'res/bfcode/{PATH[j+1]}\'")
            sys.stdout.flush()
            bf.write(generate(content))
    sys.stdout.write("\n")
    sys.stdout.flush()
    if j == len(PATH) - 2:
        reshaper.reshape(j)