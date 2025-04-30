function [R,Terminal]= Reward(robot,a,goal,obs)

    %% WRITE YOUR CODE HERE
    R=-0.05;
    Terminal=0;

    % boundary
    if (robot.x<=5) || (robot.x>=295) || (robot.y<=5) || (robot.y>=295)
        Terminal=1;
        R=-1*10;   
    % obstacle 
    elseif (D(robot, obs) < 10)
        Terminal = 1;
        R = -10;
    % goal
    elseif (D(robot, goal) < 10)
        Terminal = 1;
        R = 10;
    end
end

function d = D(robot, goal)
    d = sqrt((robot.x - goal.x)^2 + (robot.y - goal.y));
end






