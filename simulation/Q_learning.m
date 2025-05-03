function [opt_a,Wt,J]= Q_learning(a,W,robot,goal,laser,R,terminal,prev_robot,prev_laser,prev_a,next_robot,next_laser)
    %% WRITE YOUR CODE HERE
    alpha = 1e-3;                  %### 提高學習率，讓權重更新更有效
    gamma = 0.9;
    epsilon = 0.3;
    num_actions = 5;

    has_prev = nargin >= 10 && ~isempty(prev_robot) && ~isempty(prev_laser) && ~isempty(prev_a);  %### 更明確的條件檢查

    if has_prev
        f_prev = features(prev_robot, goal, prev_laser, prev_a);
        Q_prev = W' * f_prev;
    else 
        Q_prev = 0;
    end

    f_current = features(robot, goal, laser, a);  % 目前狀態 + 現在動作
    Q_current = W' * f_current;

    if terminal
        Q_target = R;
    else
        Q_next = zeros(num_actions, 1);
        for a_next = 1:num_actions
            f_next = features(next_robot, goal, next_laser, a_next);  %### 用 next_state 特徵
            Q_next(a_next) = W' * f_next;
        end
        Q_target = R + gamma * max(Q_next);
    end

    TD_error = Q_target - Q_prev;
    J = TD_error^2;

    if has_prev  %### 只有在有前一步資訊時才更新 W
        Wt = W + alpha * TD_error * f_prev;
    else
        Wt = W;
    end

    % Epsilon-greedy action selection based on updated weights
    if rand < epsilon
        opt_a = randi(num_actions);  % 探索
    else
        Q_eval = zeros(num_actions,1);
        for a_candidate = 1:num_actions
            f = features(robot, goal, laser, a_candidate);  %### 保持使用 current state 選動作
            Q_eval(a_candidate) = Wt' * f;
        end
        [~, opt_a] = max(Q_eval);  % 利用
    end
end
