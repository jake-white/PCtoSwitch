import keyboard, serial

pcinputs = ['a','d','w','s','space','shift']
switchinputs = [False, False, False, False, False, False]

#starting up serial input
ser = serial.Serial('COM3', 9600, timeout=0.050)
connected = False
while True:
    line = ""
    for i in range(0, len(pcinputs)):
        if(not switchinputs[i] and keyboard.is_pressed(pcinputs[i])):
            #button down
            switchinputs[i] = True
            ser.write('{}'.format(i).encode())
        elif(switchinputs[i] and not keyboard.is_pressed(pcinputs[i])):
            #button up
            switchinputs[i] = False
            ser.write('{}'.format(i).encode())

    
