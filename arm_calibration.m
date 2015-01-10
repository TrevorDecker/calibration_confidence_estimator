function [ output_args ] = arm_calibration( input_args )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

%id, H Degree, H minute, H seconds, V Degree, V minute, V seconds, Easting,
%Northing, elevation, x, y, z, q1, q2, q3, q4 

data = [
        3   11	55	19	91	6	57	1000.192	2003.8291	2999.7953	-61.7    1238	1308.3	0.51025	 0.64363	-0.48052	-0.30739
        4	10	21	10	91	16	46	1000.7124	2003.8998	2999.908	355.6	-1001.6	1308.1	0.4078	 0.47577	-0.64622	-0.43559
        5	9	7	29	95	59	35	1000.6628	2004.1266	2999.5612	351     -1001.7	928.8	0.40777	 0.47578	-0.64624	-0.43558
        6	7	47	39	95	32	15	1000.6158	2004.4992	2999.5597	238.5	-730.3	769.3	0.29212	 0.51731	-0.34901	-0.72474
        7	18	35	51	82	16	54	1001.4106	2004.192	3000.5995	617.4	-405.8	1851.8	0.0664	 0.7842     -0.5901      0.18001
        8	0	38	47	81	17	2	1000.0445	2003.9421	3000.5995	-108.7	-764.5	1931.7	0.36676	 0.20698	-0.66791	 0.61363
        9	1	26	42	89	44	54	1000.0998	2003.9541	3000.0174	-144.2	-1105.4	1497.1	0.23359	 0.14348	-0.69232	 0.66749
        10	7	58	23	89	10	40	1000.5412	2003.8643	3000.056	180.8	-1006.3	1480.4	0.55099	-0.11372	-0.76196	 0.32076
        11	353	18	3	93	58	57	999.4415	2004.7551	2999.6667	-938.3	-580.9	1110.9	0.8769	-0.4396     -0.17011	-0.09467
        12	18	11	25	91	41	50	1001.7841	2005.4294	2999.9305	877.8	 481.1	1359.7	0.29082	 0.20759	-0.93095	-0.07524
        13	6	25	6	80	29	0	1000.4348	2003.8648	3000.652	140.8	-721.7	1946.2	0.5502	 0.45155	0.59426     -0.37448
        14	6	6	12	91	18	58	1000.4279	2004.0015	2999.9075	166     -1081	1268.8	0.62729	 0.77866	0.00959     -0.01016
        15	358	19	39	92	39	14	999.8903	2003.7568	2999.8258	-242.5	-1371.6	1398.2	0.547	 0.62854	0.42676     -0.35158
        16	2	56	31	97	57	55	1000.2      2003.8913	2999.4548	-25.7	-1445	931.4	0.56347	 0.81122	0.06112     -0.14386
        17	4	47	37	96	49	45	1000.3845	2004.5854	2999.4489	-60.1	-846.9	510.3	0.16952	 0.91896	0.0598      -.35101
        ]
    
 
 h_d = data(:,2);
 h_m = data(:,3);
 h_s = data(:,4);
 v_d = data(:,5);
 v_m = data(:,6);
 v_s = data(:,7);
 easting = data(:,8);
 northing = data(:,9);
 elevation = data(:,10);
 xs = data(:,11)./1000; %converts to meters
 ys = data(:,12)./1000; %converts to meters
 zs = data(:,13)./1000; %converts to meters
 q1s = data(:,14);
 q2s = data(:,15);
 q3s = data(:,16);
 q4s = data(:,17);

 
 K = 1;
     H = getHmatrix(xs(K),ys(K),zs(K),q1s(K),q2s(K),q3s(K),q4s(K));
     A = getHmatrix_(h_d(K),h_m(K),h_s(K),v_d(K),v_m(K),v_s(K),easting(K),northing(K),elevation(K));
     B = A \ H;
     B(:,4) = [0, 0, 0, 1]';
     B
     
     robotFrameAvg = zeros(4);
for i =1:size(data,1)
     H = getHmatrix(xs(i),ys(i),zs(i),q1s(i),q2s(i),q3s(i),q4s(i));
     A = getHmatrix_(h_d(i),h_m(i),h_s(i),v_d(i),v_m(i),v_s(i),easting(i),northing(i),elevation(i));

%      subplot(1,2,1)
%      drawAxis(H);
%      axis equal
%      subplot(1,2,2)
%      drawAxis(H_2);


%   A_1*B*inv(H_1) = 0
%  A_1*B = H_1
%  B = inv(A_1)*H_1

     
robotFrame = A*B*inv(H);
robotFrameAvg = robotFrameAvg + robotFrame;
drawAxis(robotFrame)
     axis equal
end
robotFrameAvg = robotFrameAvg./size(data,1)
drawAxis(robotFrameAvg)





end

function d = dms_to_d(degree,minutes,seconds)
    d = degree + minutes/60 + seconds/3600;
end

function [degree,minutes,seconds] = d_to_dms(d)
degree = floor(d);
A = mod(d,1);
B = 60*A;
minutes = floor(B);
seconds =    (B - minutes)*60;

end

function H = getHmatrix_(H_degree,H_minute,H_seconds,V_degree,v_minute,v_seconds,easting,northing,elevation)
     H_ = [1 0 0 easting;
           0 1 0 northing;
           0 0 1 elevation;
           0 0 0         1];
     h_degree = dms_to_d(H_degree,H_minute,H_seconds);
     h_raid = degtorad(h_degree);
     %rot Z assumed to be horizon 
     a = [cos(h_raid) -sin(h_raid) 0 0;
          sin(h_raid)  cos(h_raid) 0 0;
                      0              0 1 0;
                      0              0 0 1];
                  
     v_degree = dms_to_d(V_degree,v_minute,v_seconds);
     v_raid = degtorad(v_degree);
     %rot y asumed to be V
     b = [cos(v_raid) 0 sin(v_raid) 0;
                      0 1             0 0;
         -sin(v_raid) 0 cos(v_raid) 0;
                      0 0             0 1];
     H = H_*a*b;
end

function H =  getHmatrix(x,y,z,q1,q2,q3,q4)
H = [1 0 0 x;
     0 1 0 y;
     0 0 1 z; 
     0 0 0 1];
R = quaternion2matrix([q1,q2,q3,q4]);
H(1:3,1:3) = R;

end

function drawAxis(H)
orig = H*[0, 0, 0, 1]';
x    = H*[1, 0, 0, 1]';
y    = H*[0, 1, 0, 1]';
z    = H*[0, 0, 1, 1]';

hold on 
plot3([orig(1),x(1)],[orig(2),x(2)],[orig(3),x(3)],'r')
plot3([orig(1),y(1)],[orig(2),y(2)],[orig(3),y(3)],'g')
plot3([orig(1),z(1)],[orig(2),z(2)],[orig(3),z(3)],'b')




end

