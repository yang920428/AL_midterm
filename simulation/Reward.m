function [R,Terminal]= Reward(robot,a,goal,obs)

    %% WRITE YOUR CODE HERE
    % boundary
    R=-0.05;
    Terminal=0;
    if (robot.x<=5) || (robot.x>=295) || (robot.y<=5) || (robot.y>=295)
        Terminal=1;
        R=-1*10;   
    % obstacle 
    end
    if (Distance(robot, obs) < 10)
        Terminal = 1;
        R = -10;
    end
    % goal
    if (Distance(robot, goal) < 10)
        Terminal = 1;
        R = 10;
    end
end








