function [f]= features(robot,goal,laser,a)

    %% WRITE YOUR CODE HERE
    f = ones(4, 1); 

    dx = goal.x - robot.x;
    dy = goal.y - robot.y;
    f(2) = sqrt(dx^2 + dy^2)/100;

    goal_angle = atan2(dy, dx);
    %phi = wrapToPi(goal_angle);
    phi = wrapToPi(goal_angle - robot.t);
    f(3) = phi;
    if a == 1
        idx = 3;
    elseif a== 2
        idx = 2;
    elseif a ==3
        idx = 4;
    elseif a==4
        idx = 1;
    else
        idx = 5;
    end
    if laser(idx) <= 70
        f(4) = f(3);
    else
        f(4) = -f(3);
    end 
end
