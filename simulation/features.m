function [f] = features(robot, goal, laser, a)
    dist_to_goal = sqrt((robot.x - goal.x)^2 + (robot.y - goal.y)^2) / 100;
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
    
    cover = (laser(idx) / 100 + min(idx) / 100);


    w = 0;
    if cos(angle_to_goal) >  cos(15 * pi/ 180)
        if idx == 3
            w = 1;
        else
            w = 0.2;
        end
    elseif angle_to_goal > 0  
        if idx >= 4
            w = 0.7;
        end
    else
        if idx <= 2
            w = 0.7;
        end
    end
    
    f = [
        1;                     
        dist_to_goal;       
        angle_to_goal;       
        f4;                    
        w;
        -1/(cover + 0.01);
    ];
end