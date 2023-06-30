% HAND_FEATURES - extract shape features for the supplied region of
%  interest suitable for classification.
%
% F = hand_features(B)
% 
% B = binary image mask
%
% F - an 1xN row-vector of feature measurement (real numbers)

function F = hand_features(B)

% Extract features related to shape. Make use of the concepts covered
% in the lectures. MATLAB has a number of useful pre-existing feature 
% measures to try out but I suggest you also create some of your own
% if you wish to get good results.

% ---------- INSERT YOUR CODE BELOW ------------------------------------


    % Extract features related to shape
    regionProps = regionprops(B, 'Area', 'Perimeter', 'Eccentricity', 'Solidity', 'MajorAxisLength', 'MinorAxisLength', 'Orientation');
    
    % Calculate additional shape measures
    % Example measures: ratio of boundary length to area and circularity
    boundaryLength = regionProps.Perimeter;
    area = regionProps.Area;
    ratioBLtoA = boundaryLength / area;
    circularity = (4 * pi * area) / (boundaryLength^2);
    
    % Construct the feature vector
    F = [ratioBLtoA, circularity];
    
    % Add more shape-related measures to the feature vector
    
    return
end


% ---------- INSERT YOUR CODE ABOVE ------------------------------------

return

% END OF FILE
