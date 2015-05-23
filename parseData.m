function parseData()
global data
    addpath('CovarianceRegression/matlab/experiment3D')
    addpath('CovarianceRegression/matlab/quaternions')

    
    NumDataPoints = 1;
    data = cell(NumDataPoints,1);
    results = zeros(NumDataPoints,6)
 %   log_file_folder = 'log_files/1420757910.12/';
 %   log_file_folder = 'log_files/1421051684.58/';
    log_file_folder = 'log_files/1421074243.57/';
%     log_file_folder = 'log_files/1421968202.4/';


   
   k = 1; 
for id = 1:100:16000%1
    valid = true;
    %reads in the arm state
    file_str = strcat(log_file_folder,num2str(id),'armState.txt');
    fid = fopen(file_str);
    if(fid > 0)
        info = zeros(7,1);
        for i = 1:7%(ischar(tline))
            tline = fgets(fid);
            if(tline == -1)
               valid = false;
               break; 
            end
            splitStr = regexp(tline,',','split');
            value = splitStr(2);
            info(i) = str2num(value{1})/1000;
        end
        results(k,1) = info(1);
        results(k,2) = info(2);
        results(k,3) = info(3);
        armState = struct('x',info(1),'y',info(2),'z',info(3),'q0',info(4),'q1',info(5),'q2',info(6),'q3',info(7));
        fclose(fid);
        
        %reads in the AprilTag detections
        file_str = strcat(log_file_folder,num2str(id),'.txt')
        fid = fopen(file_str);
        if(fid > 0 )
        info = zeros(9,1);
        for i = 1:9
            %TODO parse data when more then one tag is detected TODO
            tline = fgets(fid);
            if(tline == -1)
               valid = false;
               break; 
            end
            splitStr = regexp(tline,',','split');
            value = splitStr(2);
            info(i) = str2num(value{1});
        end
        
        results(k,4) = info(3);
        results(k,5) = info(4);
        results(k,6) = info(5);
        fclose(fid);
        aprilTag = struct('id',info(1),'hamming',info(2),'x',info(4),'y',info(5),'z',info(6),'yaw',info(7),'pitch',info(8),'roll',info(9)); %TODO
        aprilTags = [aprilTag]; %TODO multiple april tags
        I = imread(strcat(log_file_folder,num2str(id),'.jpg'));
        I = imresize(I,.25);
        if(valid)
            dataPoint = struct('armState',armState,'aprilTags',aprilTags,'image',I);
         data{k} = dataPoint;
            k = k+1;
        end
        else
            'bad data'
            file_str
        end
    else
        'bad data'
        file_str
    end
end
%save('1420757910.mat','data')
%save('1421051684.mat','data')
%save('1421074243.mat','data')
%save('1421968202.mat','data')




% %note ignoring rotation for now 
% n = size(results,1);
% ATag = zeros(6,n);
% ATag(1,:) = results(:,4);
% ATag(2,:) = results(:,5);
% ATag(3,:) = results(:,6);
% 
% armState = zeros(6,n);
% armState(1,:) = results(:,1);
% armState(2,:) = results(:,2);
% armState(3,:) = results(:,3);
% 
% 
% tag_actual = SE3([0,0,0,0,0,0]');
% tag_location = SE3(ATag);
% arm_location = SE3(armState);
% 
 x0 = [-.045 0 .025 0 -.6756 0 0.7373]';
% 
% 
% 
 x = fminunc(@error_fun,x0)
 x_0 = x;
 x_0(4:7) = x_0(4:7)/sqrt(x_0(4)*x_0(4) + x_0(5)*x_0(5) + x_0(6)*x_0(6) + x_0(7)*x_0(7))


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%tag_beilved = arm_location*C*tag_location;
%bestError = 100000;
%bestValue = [0,0];

% for roll = 0:.25:2*pi
% for pitch = 0:.25:2*pi
% for yaw =  0:.25:2*pi
% for z = -.3:.1:.3
% for y = -.3:.1:.3
% for x = -.3:.1:.3
% total_error = 0;
%    A = SE3([x,y,z,roll,pitch,yaw]');
%     cam_in_tool = A.GetTransform();
%     [x,y,z,roll,pitch,yaw]
% for i = 2:n
%     tag_in_cam_1 = tag_location(i).GetTransform();
%     tag_in_cam_0 = tag_location(i-1).GetTransform();
%     tag_in_cam_d = inv(tag_in_cam_0)*tag_in_cam_1;
%     
%     tool_in_arm_1 = arm_location(i).GetTransform();
%     tool_in_arm_0 = arm_location(i-1).GetTransform();
%     tool_in_arm_d = inv(tool_in_arm_0)*tool_in_arm_1;
%     
%  
%     this_error = (tool_in_arm_d*cam_in_tool)*[0,0,0,1]' - tag_in_cam_d*[0,0,0,1]';
%     this_error = this_error(1)*this_error(1) + this_error(2)*this_error(2) + this_error(3)*this_error(3);
%     total_error = total_error + this_error;
% end
% if(bestError > total_error)
%     bestError = total_error;
%     bestValue = [x,y,z,roll,pitch,yaw];
% end
% end
% end
% end
% end
% end
% end
%bestError
%bestValue = [0,.2,-.3,5,3,2];

%H = SE3(bestValue');
%H = H.GetTransform();
%d = ones(n,4);
%d(:,1:3) = results(:,1:3); 
%size(d')
%R = H*d'
%R = R'
%R(2:size(R,1),:) - R(1:size(R,1)-1,:)
%Results(2:size(results,1),4:6) - results(1:size(results,1) - 1,4:6)
%for i = 1:n
    
    
%end


% 
% %Xa = results_H * C * A_H;
% %error = Xa - tag_location
% %min sum(error)^2
% 
% %subplot(1,2,1)
% hold on
% %results(:,1) =  results(:,1) +0; 
% %results(:,2) = 2.14*results(:,2)+ 1.45;
% plot3(results(:,2),results(:,1),results(:,3),'b');
% %th = 2.5 ;
% %H = [cos(th) -sin(th) 0 -.1;
% %     sin(th)  cos(th) 0 -0.005;
% %           0        0 1 0;
% %           0        0 0 1];
% %       A = ones(NumDataPoints,4);
%        A(:,1:3) = results(:,4:6);
% %       A = A';
% %       A = H*A;
% %       A = A';
% %%       A = flipud(A);
% da = results(2:size(results,1),:) - results(1:size(results,1) - 1,:)
% plot3(A(:,1),A(:,2),A(:,3),'r');  'arm position'
% axis equal 
% 
% %subplot(3,2,2)
% %plot(1:NumDataPoints,abs(A(:,1) - results(:,1)))
% %title('x error')
% %ylabel('meters')
% %xlabel('dataPoint')
% %subplot(3,2,4)
% %plot(1:NumDataPoints,abs(A(:,2) - results(:,2)))
% %title('y error')
% %ylabel('meters')
% %xlabel('dataPoint')
% %subplot(3,2,6)
% %plot(1:NumDataPoints,abs(A(:,3) - results(:,3)))
% %title('z error')
% %xlabel('dataPoint')
% %ylabel('meters')
% %A(1,1:3)
% %A(NumDataPoints,1:3)
% %results(1,1:3)
% %results(NumDataPoints,1:3)

end

function E = error_fun(x_0) 
    global data
    x_0(4:7) = x_0(4:7)/sqrt(x_0(4)*x_0(4) + x_0(5)*x_0(5) + x_0(6)*x_0(6) + x_0(7)*x_0(7))
    x = SE3(x_0);
    E = 0;
    %need to normilize  x  TODO THIS LIKE NOW 
    for i = 2:size(data,2)
    m_2 = SE3([data{i}.aprilTags.x,data{i}.aprilTags.y,data{i}.aprilTags.z,data{i}.aprilTags.yaw,data{i}.aprilTags.pitch,data{i}.aprilTags.roll]');
    m_2 = m_2.GetTransform();
    m_1 = SE3([data{i-1}.aprilTags.x,data{i-1}.aprilTags.y,data{i-1}.aprilTags.z,data{i-1}.aprilTags.yaw,data{i-1}.aprilTags.pitch,data{i-1}.aprilTags.roll]');
    m_1 = m_1.GetTransform();
    C = x.GetTransform();
    A_2 = SE3([data{i}.armState.x,data{i}.armState.y,data{i}.armState.z,data{i}.armState.q1,data{i}.armState.q2,data{i}.armState.q3,data{i}.armState.q0]');
    A_2 = A_2.GetTransform();
    A_1 = SE3([data{i-1}.armState.x,data{i-1}.armState.y,data{i-1}.armState.z,data{i-1}.armState.q1,data{i-1}.armState.q2,data{i-1}.armState.q3,data{i-1}.armState.q0]');
    A_1 = A_1.GetTransform();
    d = A_1 \ A_2;
    this_E = (inv(m_2)*inv(C)*inv(d)*C*m_1);
    for j = 1:size(this_E,1)
        for k = 1:size(this_E,2)
            E = E + this_E(j,k)*this_E(j,k);
        end
    end
    end
    E
end