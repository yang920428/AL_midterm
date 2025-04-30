function d = Distance(robot, goal)
    d = sqrt((robot.x - goal.x)^2 + (robot.y - goal.y)^2);
end