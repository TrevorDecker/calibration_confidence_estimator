function [ output_args ] = armDisplay( input_args )
time = [];
error = [];

markerTransform = [1 0 0 -4.56881;
                  0 1 0 -1.25001;
                  0 0 1 1.35242;
                  0 0 0 1];
               
armBaseFrame = [1 0 0 0;
                   0 1 0 0;
                   0 0 1 0;
                   0 0 0 1];  
               
               
% l1 = 
% l2 = 
% l3 = 
% l4 = 
% l5 = 
% l6 =
% 
% h1 = [1 0 0 0;
%       0 1 0 0;
%       0 0 1 0;
%       0 0 0 1]; 
% h2 = [1 0 0 0;
%       0 1 0 0;
%       0 0 1 0;
%       0 0 0 1]; 
% h3 = [1 0 0 0;
%       0 1 0 0;
%       0 0 1 0;
%       0 0 0 1];
% h4 = [1 0 0 0;
%       0 1 0 0;
%       0 0 1 0;
%       0 0 0 1];
% h5 = [1 0 0 0;
%       0 1 0 0;
%       0 0 1 0;
%       0 0 0 1];
% h6 = [1 0 0 0;
%       0 1 0 0;
%       0 0 1 0;
%       0 0 0 1];   

    armEndEffector = [-1 0 0 -.12425;
                  0 -1 0 -1.0242;
                  0 0 1 2.3254;
                  0 0 0 1];

for t = 0:200
    clf;
    th = .0005;
    armMotion = [ cos(th) -sin(th) 0 -.004;
                  sin(th) cos(th) 0 0;
                  0 0 1 0;
                  0 0 0 1]
%    armMotion = [1 0 0 .1
%                0 cos(th) -sin(th) 0
%                0 sin(th) cos(th) 0
%                0 0 0 1];
     armEndEffector = armMotion*armEndEffector;      

                         
    diff = (armEndEffector^-1)*(markerTransform);
    diff(1:3,4)  = diff(1:3,4) + [.03;.02;.05].*rand(3,1) + [.01; -.001;0];
    A = armEndEffector*diff;
    A - markerTransform
    subplot(2,1,1)
        displayFrame(markerTransform,'target');
        displayFrame(armEndEffector,'endEffector');
        displayFrame(armBaseFrame,'ArmBase');
        axis equal
    subplot(2,1,2)
        time = cat(1,time,t);
        error = cat(1,error,sqrt(A(1,4)^2 + A(2,4)^2 + A(3,4)^2)-4.8-.0001*t);
        plot(time,error)
        pause(.1)
end
th = -.2    ;
 armMotion = [ cos(th) -sin(th) 0 +.004;
                  sin(th) cos(th) 0 0;
                  0 0 1 0;
                  0 0 0 1]
%    armMotion = [1 0 0 .1
%                0 cos(th) -sin(th) 0
%                0 sin(th) cos(th) 0
%                0 0 0 1];
     armEndEffector = armMotion*armEndEffector;   
for t = 200:400
    clf;
    th = .0005;
    armMotion = [ cos(th) -sin(th) 0 +.004;
                  sin(th) cos(th) 0 0;
                  0 0 1 0;
                  0 0 0 1]
%    armMotion = [1 0 0 .1
%                0 cos(th) -sin(th) 0
%                0 sin(th) cos(th) 0
%                0 0 0 1];
     armEndEffector = armMotion*armEndEffector;      

                         
    diff = (armEndEffector^-1)*(markerTransform);
    diff(1:3,4)  = diff(1:3,4) + [.03;.02;.05].*rand(3,1) + [.01; -.001;0];
    if mod(t/12,2) == 0 
        diff(1:3,4)  = diff(1:3,4) + [.03;.02;.05].*rand(3,1) + [.01; -.001;0];        
    end
    if mod(t/10,3) == 0 
        diff(1:3,4)  = diff(1:3,4) + [.03;.02;.05].*rand(3,1) + [.01; -.001;0];        
    end
    A = armEndEffector*diff;
    A - markerTransform
    subplot(2,1,1)
        displayFrame(markerTransform,'target');
        displayFrame(armEndEffector,'endEffector');
        displayFrame(armBaseFrame,'ArmBase');
        axis equal
    subplot(2,1,2)
        time = cat(1,time,t);
        error = cat(1,error,sqrt(A(1,4)^2 + A(2,4)^2 + A(3,4)^2)-4.8+.0001*(400 -t));
        plot(time,error)
        pause(.1)
end












%april tags 

% x = [1 0 0 1]';
% y = [0 1 0 1]';
% z = [0 0 1 1]';
% c = [0 0 0 1]';
% 
% x = H*x;
% y = H*y;
% z = H*z;
% c = H*c;
% hold on
% plot3([c(1),x(1)],[c(2),x(2)],[c(3),x(3)],'b');
% text(x(1),x(2),x(3),'x');
% plot3([c(1),y(1)],[c(2),y(2)],[c(3),y(3)],'r');
% text(y(1),y(2),y(3),'y');
% plot3([c(1),z(1)],[c(2),z(2)],[c(3),z(3)],'g');
% text(z(1),z(2),z(3),'z');
%text(c(1),c(2),c(3),label)



% % if(zoom)
%     %extends the border around the image so that even if the image is zoomed in
%     %on a single letter the majority of the image is the backgorund color
%     newI = 0.0*ones(2*size(I,1),2*size(I,2),3);
%     newI(:,:,1) = I(1,1,1);
%     newI(:,:,2) = I(1,1,2);
%     newI(:,:,3) = I(1,1,3);
%     xoffset_ = floor((size(newI,1) - size(I,1))/2);
%     yoffset_ = floor((size(newI,2) - size(I,2))/2);
%     for layer = 1:3
%      newI(xoffset_+1:xoffset_+size(I,1),yoffset_+1:yoffset_+size(I,2),layer) = I(:,:,layer);
%     end
%     I = newI;
% end
% I = hsv2rgb(I);
% 
% %% resizes the input image so that run time and scale is regulated 
% if(~zoom)
%     rSize = 1000/size(I,2)
%     I = imresize(I, rSize);
% end
% 
% if(zoom)
%     xSize = 2*size(I,1);
%     ySize = 2*size(I,2);
% else
%     xSize = 100;
%     ySize = 100;
% end
% result = zeros(size(I,1),size(I,2));
% for x_start = 1:xSize/2:size(I,1)
%    for y_start = 1:ySize/2:size(I,2)
%     x_end = min(x_start+xSize,size(I,1));
%     y_end = min(y_start+ySize,size(I,2));
%     thisBlock = I(x_start:x_end,y_start:y_end,:);
%     C = rgb2hsv(thisBlock);
%     G = rgb2gray(thisBlock);
%     
%     C2 = C(:,:,2);
%     [counts,x] = imhist(C2);
%     peak = x(counts <mean(counts) == 0);
%     C2_min = min(min(C2));
%     C2_max = max(max(C2));
%     if(C2_max - C2_min < .1)
%         C2_result = 0;
%     else
%        C2_result = C2 >= peak(length(peak))+0;
%     end
%          
%     C3 = C(:,:,3);
%     [counts,x] =  imhist(C3);
%     peak = x(counts < mean(counts) == 0);
%     a = peak(1);
%     
%     C3_min = min(min(C3));
%     C3_max = max(max(C3));
% 
%     if(C3_max - C3_min < .1)
%         C3_result = 0;
%     else
%        C3_result = C(:,:,3) <= peak(1)+0;
%     end
%     [counts,x] =  imhist(G);
%     peak = x(counts < mean(counts) == 0);
%     peak(1);
%     G_mean = mean(mean(G));
%     G_min = min(min(G));
%     G_max = max(max(G));
%     if(G_max - G_min < .1)
%         G_result = 0;
%     else
%         G_result = G <= peak(1)+ 0;
%     end
%     thisResult =  G_result+ C3_result +C2_result;
%     thisResult = bwareaopen(thisResult,10);
%    result(x_start:x_end,y_start:y_end) = result(x_start:x_end,y_start:y_end)+thisResult ;
%     end
% end
% if(zoom)
%     %shrink image back to orignal size
%     [xoffset_, size(I,1) - xoffset_]
%     a = size(result,1)./4;
%     b = size(result,2)./4;
%     result = result(a+1:size(I,1)-a,b+1:size(I,2)-b);
%     size(result)
% else
%     I = imresize(I, 1/rSize);
% end
% imshow(result>0,[])


end

function displayFrame(H,label)
x = [1 0 0 1]';
y = [0 1 0 1]';
z = [0 0 1 1]';
c = [0 0 0 1]';

x = H*x;
y = H*y;
z = H*z;
c = H*c;
hold on
plot3([c(1),x(1)],[c(2),x(2)],[c(3),x(3)],'b');
text(x(1),x(2),x(3),'x');
plot3([c(1),y(1)],[c(2),y(2)],[c(3),y(3)],'r');
text(y(1),y(2),y(3),'y');
plot3([c(1),z(1)],[c(2),z(2)],[c(3),z(3)],'g');
text(z(1),z(2),z(3),'z');
text(c(1),c(2),c(3),label)



end

