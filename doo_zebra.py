import cv2 as cv
import numpy as np
import sys

img_NDS = cv.imread('son.jpg')
if img_NDS is None:
    sys.exit("이미지를 찾을 수 없습니다.")

cv.imshow('img_NDS', img_NDS)

b = img_NDS[:, :, 0].astype(np.float32)
g = img_NDS[:, :, 1].astype(np.float32)
r = img_NDS[:, :, 2].astype(np.float32)

gray_NDS = 0.299 * r + 0.587 * g + 0.114 * b
gray_NDS = gray_NDS.astype(np.uint8)


cv.imshow('gray_NDS', gray_NDS)

value = int(input("밝기 입력 (범위 -255~255) : "))

def brightNdark(gray_NDS, value):
    gray_NDS = gray_NDS.astype(np.int32)#오버플로우 방지 형변환환
    gray_NDS = gray_NDS + value         

    for i in range(gray_NDS.shape[0]):#계산이 끝나고 0~255범위를 벗어난 픽셀을 조정
        for j in range(gray_NDS.shape[1]):
            if gray_NDS[i][j]>255:
                gray_NDS[i][j] = 255
            elif gray_NDS[i][j]<0:
                gray_NDS[i][j] = 0
    result = gray_NDS.astype(np.uint8)    # 다시 8비트로 변환
    return result

result_NDS = brightNdark(gray_NDS, value)

cv.imshow('result_NDS', result_NDS)
cv.waitKey(0)
cv.destroyAllWindows()
