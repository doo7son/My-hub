

import cv2 as cv
import numpy as np
import sys


img_NDS = cv.imread('son.jpg')


if img_NDS is None:
    sys.exit("이미지를 찾을 수 없습니다.")


cv.imshow('img_NDS', img_NDS)


b= img_NDS[:, :, 0].astype(np.float32)#계산을 위해서 32비트로 변환, 오버플로우
g = img_NDS[:, :, 1].astype(np.float32)
r= img_NDS[:, :, 2].astype(np.float32)


gray_NDS = 0.299 * r + 0.587 * g + 0.114 * b
gray_NDS = gray_NDS.astype(np.uint8)#0~255 8비트 픽셀 값으로 다시 변환


cv.imshow('gray_NDS', gray_NDS)


cv.waitKey(0)
cv.destroyAllWindows()


