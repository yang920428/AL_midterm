clear all; clc; close all;

Episode=2;

goal.x=150; goal.y=250; % goal location
obs.x=150; obs.y=150; % obstacle location
robot0.x=150; robot0.y=50; robot0.t=1.57; % % robot initial location
W=ones(4,1); % Q-learning weighting
dt=0.1; % delta t
CoverMODE=2; M=1;m=1; Eff_robot=1; % GetLaser parameters

index=1;
for Epi=1:Episode
    Terminal=0;
    robot_t_1.x=robot0.x;
    robot_t_1.y=robot0.y;
    robot_t_1.t=robot0.t;
    a=3;
    while (Terminal==0)
        [robot_t]= motion_model(robot_t_1,a,dt);
        [R,Terminal]=Reward(robot_t,a,goal,obs);
        robot_data(m)=robot_t.x;robot_data(m+M)=robot_t.y;robot_data(m+2*M)=robot_t.t;
        laser=GetLaser(robot_data(1,1:M),robot_data(1,M+1:2*M),robot_data(1,2*M+1:3*M),Eff_robot,1,CoverMODE); % get laser data         
        robot_t_1.x=robot_t.x; robot_t_1.y=robot_t.y; robot_t_1.t=robot_t.t;    
        [a,Wt,J]= Q_learning(a,W,robot_t,goal,laser,R,Terminal);
        W=Wt
        title(['Episode=',num2str(Epi)]);hold off;
    end   
end
