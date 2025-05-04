function [f] = features(robot, goal, laser, a)
    % 1. 基礎目標特徵 (強化這些特徵)
    dist_to_goal = sqrt((robot.x - goal.x)^2 + (robot.y - goal.y)^2);
    angle_to_goal = atan2(goal.y - robot.y, goal.x - robot.x) - robot.t;
    angle_to_goal = wrapToPi(angle_to_goal);
    
    % 2. 簡化版的作業要求f4特徵 (保持但降低影響)
    if a == 1
        idx = 3;
    elseif a == 2
        idx = 2;
    elseif a == 3
        idx = 4;
    elseif a == 4
        idx = 1;
    else
        idx = 5;
    end
    
    f4 = angle_to_goal; % 簡化版本，移除了條件判斷
    
    % 3. 關鍵改進：強目標吸引特徵
    % goal_attraction = 10/(dist_to_goal + 1); % 距離越近值越大
    
    % 4. 障礙物特徵 (簡化並弱化)
    front_laser = laser(idx) / 100;
    f_obstacle = -0.5 / (front_laser + 0.3); 
    
    % 5. 方向對齊獎勵
    alignment_bonus = cos(angle_to_goal); % 對準目標時接近1


    action_value = 0;
    if abs(angle_to_goal) < 0.5  % 如果目標基本在前方
        % 對於接近直線行駛的動作(a=3)给更高權重
        if idx == 3
            action_value = 1;
        else
            action_value = 0.2;
        end
    elseif angle_to_goal > 0  % 目標在左侧
        % 對左轉動作(a=4,5)给予更高權重
        if idx >= 4
            action_value = 0.7;
        end
    else  % 目標在右側
        % 對右轉動作(a=1,2)给更高權重
        if idx <= 2
            action_value = 0.7;
        end
    end
    
    % 特徵向量 (簡化版本)
    f = [
        1;                      % 偏置項
        dist_to_goal;        % 強化目標吸引
        angle_to_goal;       % 方向對齊獎勵
        f4;                     % 作業要求特徵(簡化)
        f_obstacle;             % 弱化的障礙物懲罰
        alignment_bonus;
        action_value;
    ];
end


% function [f] = features(robot, goal, laser, a)
%     % 計算到目標的距離
%     dist_to_goal = sqrt((robot.x - goal.x)^2 + (robot.y - goal.y)^2);
% 
%     % 計算到目標的角度差
%     angle_to_goal = atan2(goal.y - robot.y, goal.x - robot.x) - robot.t;
%     angle_to_goal = wrapToPi(angle_to_goal);
% 
%     % 獲取當前動作的轉向角度
%     degrees = [-30, -15, 0, 15, 30];
%     action_angle = degrees(a) * (pi / 180);
% 
%     % 計算動作角度與目標角度的匹配度
%     angle_match = cos(angle_to_goal - action_angle);
%     if (laser(a) <= 70)
%         f4 = -angle_to_goal;
%     else 
%         f4 = angle_to_goal;
%     end
% 
%     % 障礙物接近度
%     obstacle_proximity = min(laser)/100;
% 
%     % 動作特定特徵 - 根據不同動作角度與目標方向的匹配度
%     action_value = 0;
%     if abs(angle_to_goal) < 0.5  % 如果目標基本在前方
%         % 對於接近直線行駛的動作(a=3)给更高權重
%         if a == 3
%             action_value = 1;
%         else
%             action_value = 0.5;
%         end
%     elseif angle_to_goal > 0  % 目標在左侧
%         % 對左轉動作(a=4,5)给予更高權重
%         if a >= 4
%             action_value = 0.8;
%         end
%     else  % 目標在右側
%         % 對右轉動作(a=1,2)给更高權重
%         if a <= 2
%             action_value = 0.8;
%         end
%     end
%     % 正前方障礙物的強懲罰項
%     front_laser = laser(a);  % 正前方雷射
%     f_obstacle = -1.7 / (front_laser / 100 + 0.1);  % 雷射越短 → 懲罰越大
% 
% 
%     % 返回特徵向量
%     f = [
%         1;  % 常數特徵
%         1/(dist_to_goal/100 + 0.1);  % 距離特徵（使用倒數）
%         angle_to_goal;  % 動作方向與目標方向的匹配度 angle_match
%         f4; % 
%         -1/(obstacle_proximity + 0.1);  % 障礙物接近度 %-0.1*obstacle_proximity;
%         action_value;  % 動作特定價值
%         f_obstacle;
%     ];
% end