function [f]= features(robot,goal,laser,a)

    %% WRITE YOUR CODE HERE
    f = ones(1, 4);
    f(2) = Distance(robot, goal);
    f(3) = Angle(robot, goal);
    f(4) = laser(a);
    if (f(4)<=70)
        f(4) = f(3);
    else
        f(4) = -f(3);
    end    
end

function ang = Angle(robot, goal)
    if robot.x == goal.x
        if robot.y < goal.y
            ang = 90;
        else
            ang = 270;
        end
    else
        ang = atan((goal.y - robot.y) / (goal.x - robot.x));
    end
end