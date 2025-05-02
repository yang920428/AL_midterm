function d = Distance(robot, goal)
   % d = abs(robot.x - goal.x) + abs(robot.y - goal.y);
    d = sqrt((robot.x - goal.x)^2 + (robot.y - goal.y)^2);
end