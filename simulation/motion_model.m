function [robot_t]= motion_model(robot_t_1,a,dt)

    VW.v = 15;
    if a == 1
        VW.w = -30 * pi / 180;
    elseif a == 2
        VW.w = -15 * pi / 180;
    elseif a == 3
        VW.w = 0;
    elseif a == 4
        VW.w = 15 * pi / 180;
    elseif a == 5
        VW.w = 30 * pi / 180;
    end


    %%motion model
    robot_t.x=robot_t_1.x+VW.v*cos(robot_t_1.t)*dt;
    robot_t.y=robot_t_1.y+VW.v*sin(robot_t_1.t)*dt;
    robot_t.t=robot_t_1.t+VW.w*dt;
end
