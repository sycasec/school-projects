% HAND_SIGNATURE - estimate the signature of the given hand region
%
% S = HAND_SIGNATURE(B)
%
% S is a 1x260 element array of distances one for each angle between 0 and
% 359 degrees.

function S = hand_signature(B)
%
% 1.	Find the centroid of the hand and the coordinates of pixels on the hand boundary (this can be readily obtained using regionprops)
% 2.	Subtract the centroid position (cx,cy) from the boundary pixel coordinates to give a list of points centred on (0,0).
% 3.	For each rotation X from 0 to 359 degrees:
%   a.	Rotate the coordinates by angle X
%   b.	Find the edge points within approximately 2 pixels of the y-axis.
%   c.	Set the signature for angle X to be the maximum y value of the identified points. If the value is less than zero then set it to zero.

% ----- INSERT YOUR CODE HERE ---

    % Find the centroid and boundary of the hand region
    regionProps = regionprops(B, 'Centroid', 'PixelList');
    centroid = regionProps.Centroid;
    boundary = regionProps.PixelList;

    % Center the boundary points around (0, 0)
    centeredBoundary = boundary - centroid;

    % Initialize the signature array
    S = zeros(1, 360);

    % Compute the signature for each rotation angle
    for angle = 0:359
        % Rotate the centered coordinates by the angle
        rotatedBoundary = imrotate(centeredBoundary, angle, 'crop');

        % Find the edge points close to the y-axis (within 2 pixels)
        edgePoints = rotatedBoundary(abs(rotatedBoundary(:, 1)) <= 2, :);

        % Set the signature for the angle to the maximum y value
        maxY = max(edgePoints(:, 2));
        if maxY < 0
            maxY = 0;
        end
        S(angle+1) = maxY;
    end

    return
end


% ----- INSERT YOUR CODE ABOVE ----

% % PLOT - use this for debugging as needed
%subplot(2,2,1);
%imagesc(B);
%title('Region');
%subplot(2,1,2);
%plot(S); title('Signature');
%xlabel('Angle (deg)');
%ylabel('Distance');
%drawnow;
