Turn on the main braker for the ABB 
Turn on the main swich for the ABB 

make sure the robot is turned to manual mode (the hand on the dial).
     Click on ABB and select calibrate  
     Click update revolte counter 
     Make sure that all axis are selected
     select update 

Make sure that the black ethernet cord is pluged into the ABB box and the router
Make sure that the white ethernet cord  is pluged into the router and the ABB computer 

robot IP should be 192.168.125.1

set your ip address for the wired connection eto0 to 192.168.125.x,  x > 1 x <= 255

To run the program 
   Make sure that the robot is auto mode (the key is switched to the 3 circles) 
   Make sure all E stops are off 
   Push the white blinking button so that it becomes a solid color 
Select ABB 
       click production window
       click pp to main 
       if a text box appears select yes
       press the play button (physical button) on the abb controller handset 

On the computer run python runExperiment.py 

If you get an error in runExperiment you will need to reset pp to main and press play again. 







make sure that python-image-tk is installed 
