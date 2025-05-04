function [f] = features(robot, goal, laser, a)
    dist_to_goal = sqrt((robot.x - goal.x)^2 + (robot.y - goal.y)^2);
    angle_to_goal = atan2(goal.y - robot.y, goal.x - robot.x) - robot.t;
    angle_to_goal = wrapToPi(angle_to_goal);
    
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
    
    f4 = -angle_to_goal;
    if laser(idx) <= 70
        f4 = angle_to_goal;
    end
    
    % 3. 強目標吸引特徵
    % goal_attraction = 10/(dist_to_goal + 1); % 距離越近值越大
    
    % 4. 障礙物特徵
    front_laser = laser(idx) / 100;
    f_obstacle = -0.5 / (front_laser + 0.3); 
    
    % 5. 方向對齊獎勵
    alignment_bonus = cos(angle_to_goal); % 對準目標時接近1


    action_value = 0;
    if abs(angle_to_goal) < 0.5  % 如果目標基本在前方
        if idx == 3
            action_value = 1;
        else
            action_value = 0.2;
        end
    elseif angle_to_goal > 0  % 目標在左侧
        if idx >= 4
            action_value = 0.7;
        end
    else  % 目標在右側
        if idx <= 2
            action_value = 0.7;
        end
    end
    
    f = [
        1;                      % 偏置項
        dist_to_goal;        % 強化目標吸引
        angle_to_goal;       % 方向對齊獎勵
        f4;                     % 作業要求特徵(簡化)
        % f_obstacle;             % 弱化的障礙物懲罰
        % alignment_bonus;
        % action_value;
    ];
end