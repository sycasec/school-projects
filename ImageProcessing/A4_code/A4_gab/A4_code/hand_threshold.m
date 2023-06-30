% IMAGE_THRESH - estimate a suitable image threshold value using isothresh
%
function T = hand_threshold(I)

if (isa(I,'uint8'))
  I=double(I)/255;
end


% TO BE FILLED IN BY YOU (See assignment sheet)
% this should implement isothresh for at least 10 iterations. I
% suggest you use the mean of the whole image as the initial value for
% T.

% ---------- INSERT YOUR CODE BELOW ------------------------------------
     
    
    % Compute initial estimate of the overall average image intensity
    avgIntensity = mean(I(:));
    
    % Set initial threshold value
    T = avgIntensity;
    
    % Perform isothresh calculation for at least 10 iterations
    for iteration = 1:10
        % Calculate mean values of pixels below and above the threshold
        belowMean = mean(I(I < T));
        aboveMean = mean(I(I >= T));
        
        % Update threshold value
        T = (belowMean + aboveMean) / 2;
    end
end


% ---------- INSERT YOUR CODE ABOVE ------------------------------------

% END FO FILE
    


