% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TEST 1 - Motion blurring - Extras
K=0.01;  % noise standard deviation

I=double(imread('example.png'))/255; I=I(:,:,1);
I=double(imread('pout.tif'))/255;

B = fspecial("motion", 20,45);
Ib= noisy_image(blur_image(I,B),K);

Iinv=wiener_deblur(Ib,B,1*K);     % <--- I have used a more optimistic value here

figure;
colormap(gray);
subplot(1,7,[1 2]);
imagesc(I); axis equal tight; caxis([0 1]);
title('Original Image');
subplot(1,7,[3 4]);
imagesc(Ib); axis equal tight; caxis([0 1]);
title('Corrupted Data');
subplot(1,7,5);
imagesc(B); axis equal tight;
title('PSF');
subplot(1,7,[6 7]);
imagesc(Iinv); axis equal tight; caxis([0 1]);
title('Deconvoled Image');
drawnow;
% 
% try different settings for the blurring function, noise and
% K tuning parameters..
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TEST 1 - 2 - Motion blurring - Extras
K=0.01;  % noise standard deviation

I=double(imread('example.png'))/255; I=I(:,:,1);
I=double(imread('pout.tif'))/255;

B = fspecial("motion", 10,75);
Ib= noisy_image(blur_image(I,B),K);

Iinv=wiener_deblur(Ib,B,1*K);     % <--- I have used a more optimistic value here

figure;
colormap(gray);
subplot(1,7,[1 2]);
imagesc(I); axis equal tight; caxis([0 1]);
title('Original Image');
subplot(1,7,[3 4]);
imagesc(Ib); axis equal tight; caxis([0 1]);
title('Corrupted Data');
subplot(1,7,5);
imagesc(B); axis equal tight;
title('PSF');
subplot(1,7,[6 7]);
imagesc(Iinv); axis equal tight; caxis([0 1]);
title('Deconvoled Image');
drawnow;
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TEST 1 - 3 - Motion blurring - Extras
K=0.01;  % noise standard deviation

I=double(imread('example.png'))/255; I=I(:,:,1);
I=double(imread('pout.tif'))/255;

B = fspecial("motion", 20,0);
Ib= noisy_image(blur_image(I,B),K);

Iinv=wiener_deblur(Ib,B,1*K);     % <--- I have used a more optimistic value here

figure;
colormap(gray);
subplot(1,7,[1 2]);
imagesc(I); axis equal tight; caxis([0 1]);
title('Original Image');
subplot(1,7,[3 4]);
imagesc(Ib); axis equal tight; caxis([0 1]);
title('Corrupted Data');
subplot(1,7,5);
imagesc(B); axis equal tight;
title('PSF');
subplot(1,7,[6 7]);
imagesc(Iinv); axis equal tight; caxis([0 1]);
title('Deconvoled Image');
drawnow;
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TEST 1 - 4 - Motion blurring - Extras
% tic
K=0.001;  % noise standard deviation

I=double(imread('example.png'))/255; I=I(:,:,1);
I=double(imread('pout.tif'))/255;

B = fspecial("motion", 30,90);
Ib= noisy_image(blur_image(I,B),K);

Iinv=wiener_deblur(Ib,B,1*K);     % <--- I have used a more optimistic value here

figure;
colormap(gray);
subplot(1,7,[1 2]);
imagesc(I); axis equal tight; caxis([0 1]);
title('Original Image');
subplot(1,7,[3 4]);
imagesc(Ib); axis equal tight; caxis([0 1]);
title('Corrupted Data');
subplot(1,7,5);
imagesc(B); axis equal tight;
title('PSF');
subplot(1,7,[6 7]);
imagesc(Iinv); axis equal tight; caxis([0 1]);
title('Deconvoled Image');
drawnow;

% try different settings for the blurring function, noise and
% K tuning parameters...
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TEST 2 - Disk blurring

K=0.001;  % noise standard deviation

I=double(imread('example2.png'))/255; I=I(:,:,1);
B = fspecial('disk',20);
Ib= noisy_image(blur_image(I,B),K);
Iinv=wiener_deblur(Ib,B,0.1*K); % <--- I have again used a more optimistic value here
figure;
colormap(gray);
subplot(1,7,[1 2]);
imagesc(I); axis equal tight; caxis([0 1]);
title('Original Image');
subplot(1,7,[3 4]);
imagesc(Ib); axis equal tight; caxis([0 1]);
title('Corrupted Data');
subplot(1,7,5);
imagesc(B); axis equal tight;
title('PSF');
subplot(1,7,[6 7]);
imagesc(Iinv); axis equal tight; caxis([0 1]);
title('Deconvoled Image');
drawnow;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TEST 2 - 2 - Disk blurring

K=0.01;  % noise standard deviation

I=double(imread('example2.png'))/255; I=I(:,:,1);
B = fspecial('disk',30);
Ib= noisy_image(blur_image(I,B),K);
Iinv=wiener_deblur(Ib,B,0.1*K); % <--- I have again used a more optimistic value here
figure;
colormap(gray);
subplot(1,7,[1 2]);
imagesc(I); axis equal tight; caxis([0 1]);
title('Original Image');
subplot(1,7,[3 4]);
imagesc(Ib); axis equal tight; caxis([0 1]);
title('Corrupted Data');
subplot(1,7,5);
imagesc(B); axis equal tight;
title('PSF');
subplot(1,7,[6 7]);
imagesc(Iinv); axis equal tight; caxis([0 1]);
title('Deconvoled Image');
drawnow;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TEST 2 - 3 - Disk blurring

K=0.1;  % noise standard deviation

I=double(imread('example2.png'))/255; I=I(:,:,1);
B = fspecial('disk',10);
Ib= noisy_image(blur_image(I,B),K);
Iinv=wiener_deblur(Ib,B,1*K); % <--- I have again used a more optimistic value here
figure;
colormap(gray);
subplot(1,7,[1 2]);
imagesc(I); axis equal tight; caxis([0 1]);
title('Original Image');
subplot(1,7,[3 4]);
imagesc(Ib); axis equal tight; caxis([0 1]);
title('Corrupted Data');
subplot(1,7,5);
imagesc(B); axis equal tight;
title('PSF');
subplot(1,7,[6 7]);
imagesc(Iinv); axis equal tight; caxis([0 1]);
title('Deconvoled Image');
drawnow;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TEST 2 - 4 - Disk blurring

K=1;  % noise standard deviation

I=double(imread('example2.png'))/255; I=I(:,:,1);
B = fspecial('disk',01);
Ib= noisy_image(blur_image(I,B),K);
Iinv=wiener_deblur(Ib,B,0.1*K); % <--- I have again used a more optimistic value here
figure;
colormap(gray);
subplot(1,7,[1 2]);
imagesc(I); axis equal tight; caxis([0 1]);
title('Original Image');
subplot(1,7,[3 4]);
imagesc(Ib); axis equal tight; caxis([0 1]);
title('Corrupted Data');
subplot(1,7,5);
imagesc(B); axis equal tight;
title('PSF');
subplot(1,7,[6 7]);
imagesc(Iinv); axis equal tight; caxis([0 1]);
title('Deconvoled Image');
drawnow;
