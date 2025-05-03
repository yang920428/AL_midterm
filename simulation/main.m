clear all; clc; close all;

Episode = 20;

goal.x = 150; goal.y = 250; % goal location
obs.x = 150; obs.y = 150;   % obstacle location
robot0.x = 150; robot0.y = 50; robot0.t = 1.57; % robot initial location
W = ones(4,1); % Q-learning weighting
dt = 0.1; % delta t
CoverMODE = 2; M = 1; m = 1; Eff_robot = 1; % GetLaser parameters

index = 1;
for Epi = 1:Episode
    Terminal = 0;
    robot_t_1 = robot0;  % 設定起始點
    a = 1;

    %%% 新增: 初始化前一狀態的激光數據 %%%
    prev_laser = zeros(size(GetLaser(robot0.x,robot0.y,robot0.t,Eff_robot,1,CoverMODE)));

    first_step = true; %%% 新增: 標記是否是第一步 %%%

    while (Terminal == 0)
        [robot_t] = motion_model(robot_t_1, a, dt);  % 執行動作a得到新位置
        [R, Terminal] = Reward(robot_t, a, goal, obs);

        robot_data(m) = robot_t.x;
        robot_data(m+M) = robot_t.y;
        robot_data(m+2*M) = robot_t.t;

        laser = GetLaser(robot_data(1,1:M),robot_data(1,M+1:2*M),robot_data(1,2*M+1:3*M),Eff_robot,1,CoverMODE); % get laser data         

        %### 預測下一步狀態（給 Q-learning 用來計算 TD target）
        a_tmp = a;  %### 保持目前的動作
        next_robot = motion_model(robot_t, a_tmp, dt);  %### 模擬下一個 state
        next_laser = GetLaser(next_robot.x, next_robot.y, next_robot.t, Eff_robot, 1, CoverMODE);  %### 取得下一個雷射感測資訊

        pause(0.001);

        %%% 修改: 調用Q_learning時傳遞前一狀態 %%%
        if first_step
            % 第一步時沒有真正的"前一狀態"，所以不傳遞
            [a, Wt, J] = Q_learning(a, W, robot_t, goal, laser, R, Terminal);  %### 無需傳 prev
            first_step = false;
        else
            % 正常情況下傳遞前一狀態與下個狀態
            [a, Wt, J] = Q_learning(a, W, robot_t, goal, laser, R, Terminal, ...
                                    robot_t_1, prev_laser, a_prev, ...
                                    next_robot, next_laser);  %### 傳入 prev + next 狀態資訊
        end

        %%% 新增: 保存當前狀態和動作作為下一時間步的"前一狀態" %%%
        a_prev = a;         % 保存當前動作
        prev_laser = laser; % 保存當前激光數據
        robot_t_1 = robot_t; % 保存當前位置作為下次的前一位置

        W = Wt;
        title(['Episode=', num2str(Epi)]); drawnow; hold off;
    end
end
