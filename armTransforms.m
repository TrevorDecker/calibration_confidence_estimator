function [ output_args ] = untitled( input_args )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
clf;
BASE_FRAME = eye(4,4);
  J1 =  degtorad(-87.8);
  J2 =  degtorad(13.3);
  J3 =  degtorad(18.9);
  J4 =  degtorad(-85.2);
  J5 =  degtorad(101);
  J6 =  degtorad(176.4);
T1 = [1 0 0 0;
      0 1 0 0;
      0 0 1 .180;
      0 0 0 1];
T2 = [cos(J1) -sin(J1) 0 0;
      sin(J1)  cos(J1) 0 0;
            0        0 1 0;
            0        0 0 1];
JOINT1_FRAME = BASE_FRAME*T1*T2;
T3 = [1 0 0 .100;
      0 1 0    0;
      0 0 1 .435;
      0 0 0    1;];
T4 = [cos(J2) 0 sin(J2) 0;
            0 1       0 0;
     -sin(J2) 0 cos(J2) 0;
            0 0       0 1];
JOINT2_FRAME = JOINT1_FRAME*T3*T4;
T5 = [1 0 0 0;
      0 1 0 0;
      0 0 1 .705;
      0 0 0 1];
T6 = [cos(J3) 0 sin(J3) 0;
            0 1       0 0;
     -sin(J3) 0 cos(J3) 0;
            0 0       0 1];
JOINT3_FRAME = JOINT2_FRAME*T5*T6;
T7 = [1      0         0 0;
      0 cos(J4) -sin(J4) 0;
      0 sin(J4)  cos(J4) 0;
      0       0        0 1];
JOINT4_FRAME = JOINT3_FRAME*T7;
T8 = [1 0 0 .755;
      0 1 0    0;
      0 0 1    0;
      0 0 0    1];
JOINT5_FRAME = JOINT4_FRAME*T8;
T9 = [cos(J5) 0 sin(J5) 0;
            0 1       0 0;
     -sin(J5) 0 cos(J5) 0;
            0 0       0 1];
JOINT6_FRAME = JOINT5_FRAME*T9;
T10 = [1 0 0 .085;
       0 1 0    0;
       0 0 1    0;
       0 0 0    1];
T11 = [1 0 0 0;
       0 cos(J6) -sin(J6) 0;
       0 sin(J6)  cos(J6) 0;
       0       0         0 1];
ENDEFECTOR_FRAME = JOINT6_FRAME*T10*T11;            
     



hold on 
drawAxis(BASE_FRAME,'Base Frame')
drawAxis(JOINT1_FRAME,'Joint 1')
drawAxis(JOINT2_FRAME,'Joint 2')
drawAxis(JOINT3_FRAME, 'Joint 3')
drawAxis(JOINT4_FRAME, 'Joint 4')
drawAxis(JOINT5_FRAME, 'Joint 5')
drawAxis(JOINT6_FRAME, 'Joint 6')
drawAxis(ENDEFECTOR_FRAME,'end effector')

%DRAWS lines between the links 



%axis normal
axis 'equal'

end

function drawAxis(H,label)
scale = .05;
x = [scale, 0, 0, 1];
y = [0, scale, 0, 1];
z = [0, 0, scale, 1];
center = [0, 0, 0, 1];
hold on 

x = H*x';
y = H*y';
z = H*z';
center = H*center';
plot3([center(1),x(1)],[center(2),x(2)],[center(3),x(3)],'r')
plot3([center(1),y(1)],[center(2),y(2)],[center(3),y(3)],'g')
plot3([center(1),z(1)],[center(2),z(2)],[center(3),z(3)],'b')
text(center(1),center(2),center(3),label)

end

