% HAND_EXTRACT - auto extract the "hand" region of interest from the training
%   image using thresholding, morphological cleaning etc.
%
%  B = hand_extract(I);
%
% I = an NxM gresyscale image (values range 0..1)
% B = Binary mask of extracted region

function B = hand_extract(I)

if (nargin<1)
  error('This function requires an image as input');
end
if (isa(I,'uint8'))
  I = double(I(:,:,1))/255;
end

% estimate a threshold using the isothresh function you have created.
threshold = hand_threshold(I); 

% 1. Threshold the image based on the isothresh estimate. Given that the
%    hand contains significant shadowing uou may need to scale up/down the
%    threshold estimate given by image_thresh(). 
%
% 2. Clean up the thresholded image. Remove isolated points, fill holes
%    in the etc... You can use any of the function in the image processing
%    toolbox to do this such as imerode,imdilate,imopen,imclose,imfill etc.
%    Make sure you test this on serval images from the dataset to be sure it works.
%    Again shadowing across the hand is likely to be an issue.
%
% 3. Return a binary image containing only the "hand", preferably as a single region. 
%    If you have multiple regions in the output (caused by fragmentation of the hand or
%    from noise not removed during the clean up stage) some of the feature estimation 
%    functions which you will use later on may return odd results. 
%
% IMPORTANT - the better this section is at cleaning up the imagery the better the 
% feature estimates are likely to be and hence the performance of the classifier. Also
% make sure you discuss how you came up with these steps in your report and include
% examples etc.
% ----------- FILL IN THE SECTION BELOW ------------------------------

    % Estimate threshold using the hand_threshold function    
    % Adjust threshold value to handle shadows in the palm of the hand
    adjustedThreshold = threshold * 1.2; % Example: multiply threshold by 1.2
    
    % Threshold the image to obtain a binary image
    B = (I > adjustedThreshold);
    
    % Clean up the binary image to remove noise and fill holes
    % Perform appropriate morphological operations (e.g., erosion, dilation, opening, closing, filling)
    % Experiment with different combinations to achieve desired cleaning
    
    % Example: Perform erosion followed by dilation
    se = strel('disk', 3); % Define structuring element for morphological operations
    B = imerode(B, se);
    B = imdilate(B, se);
    
    % Remove small isolated points (optional)
    B = bwareaopen(B, 50);
    
    % Fill holes in the hand region (optional)
    B = imfill(B, 'holes');
    
    % Keep only the largest connected component representing the hand
    labeledImage = bwlabel(B);
    regionProps = regionprops(labeledImage, 'Area');
    [~, idx] = max([regionProps.Area]);
    B = (labeledImage == idx);
    
    return
end
% ----------- FILL IN THE SECTION ABOVE ------------------------------


% -------------------------------------------------------------------
% END OF FILE