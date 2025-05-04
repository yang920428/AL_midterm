function [opt_a,Wt,J]= Q_learning(a,W,robot,goal,laser,R,terminal)

    %% WRITE YOUR CODE HERE
    alpha = 1e-4;
    gamma = 0.9;
    epsilon = 0.1;
    num_actions = 5;

    f_current = features(robot, goal, laser, a);
    Q_current = W' * f_current;

    if terminal
        Q_target = R;
    else
        Q_next = zeros(num_actions, 1);
        for a_next = 1:num_actions
            f_next = features(robot, goal, laser, a_next);
            Q_next(a_next) = W' * f_next;
        end
        Q_target = R + gamma * max(Q_next);
    end

    TD_error = Q_target - Q_current;
    J = TD_error^2;

    Wt = W + alpha * TD_error * f_current;

    if rand < epsilon
        opt_a = randi(num_actions);
    else
        Q_eval = zeros(num_actions,1);
        for a_candidate = 1:num_actions
            f = features(robot, goal, laser, a_candidate);
            Q_eval(a_candidate) = Wt' * f;
        end
    [~, opt_a] = max(Q_eval);
    end
end