#!/usr/bin/env python3
# Tiger3018 | MIT License
'''
README at hw2
RESULT at img/hw2_fig1.jpg
使用多种滤波器实现平滑去噪（低通滤波），区分非线性滤波器，同时输出一些分析图象。
ref: <https://zhuanlan.zhihu.com/p/67197912> 基于导数性质分析卷积。
<https://www.jianshu.com/p/cbd1a1f86d1b>
'''

import cv2, matplotlib, scipy.ndimage, numba
import numpy as np # as a fallback
import matplotlib.pyplot as plt

from matplotlib.axes import SubplotBase
import sys, os, time

meanFilterKernel = {}
# numba.typed.Dict.empty(
#     key_type=numba.types.uint,
#     value_type=numba.types.double[:][:]
# )
gaussianFilterKernel = {}


def extern_gui_provider(image: np.ndarray, axesImage: SubplotBase, axesPlot: SubplotBase, description: str):
    '''This call implement a plot view of image and its histgram, line pixel value as a stream view.
    '''
    axesImage.set_ylabel(description)
    axesImage.imshow(image, cmap=plt.cm.gray)
    # See https://blog.gtwang.org/programming/python-opencv-matplotlib-plot-histogram-tutorial/
    if image.ndim == 3:
        axesPlot.set_ylabel("averge scale")
        axesPlot.hist(image.mean(2).ravel(), 256, [
                      0, 256], orientation="horizontal", color=["#A6E22E"])
    else:
        axesPlot.set_ylabel("gray scale")
        axesPlot.hist(image.ravel(), 256, [
                      0, 256], orientation="horizontal", color=["#A6E22E"])
    axTwinY = axesPlot.twiny()
    # axTwinY.set_xlabel("at y=40 x-axis 2d wave")
    axTwinY.plot(range(image.shape[0]), selected_2darray_plot(
        image, [0, int(float(image.shape[1] / 2))], 256), color='#FD9726', linewidth=0.4)
    axTwinY.plot(range(image.shape[1]), selected_2darray_plot(
        image, [int(float(image.shape[0] / 2)), 0], 256), color='black', linewidth=0.4)
    return image


def liner_filter(image: np.ndarray, kernel) -> np.ndarray:
    ''' This function implement **non-inverted** convolution with reflect boundray using filter kernel.
    opencv: see cvSmooth
    fit to: mean filter, gaussian filter,
    '''
    if not isinstance(kernel, np.ndarray):
        kernel = np.array(kernel)
    if(image.ndim == 3):
        sciReturn = scipy.ndimage.convolve(image, kernel[:, :, None])
    else:
        # nearest == reflect when 3x3 kernel
        sciReturn = scipy.ndimage.convolve(image, kernel)
    return sciReturn

# @numba.jit(["uint8[:, :](uint8[:, :])"], nopython=True)
@numba.jit(nopython=True)
def median_filter(image: np.ndarray) -> np.ndarray:
    '''
    opencv: see medianBlur
    fit to: median filter
    '''
    # imageBorder = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_REFLECT) # numba is not familiar with cv2
    # imageBorder = np.pad(image, 1, 'reflect') # numba did not implement it...
    '''implement of np.pad('reflect'), where 0 stands for x-axis
    # TIP not implement in matlab
    # TIP not implement in numba
    for **np.insert**, use image.shape[0] rather than -1, to make new row appear at the end.
    # imageBorder = np.insert(image, [0, image.shape[0]], [image[1, :], image[-2, :]], 0)
    for **np.concatenate**, normal [] braces doesn't make sense
    '''
    imageBorder = image  # ref, not copy
    imageReturn = np.zeros(imageBorder.shape, dtype=np.uint8)
    imageBorder = np.concatenate(
        (
            np.expand_dims(imageBorder[1, :, ], 0),
            imageBorder,
            np.expand_dims(imageBorder[-2, :, ], 0)
        ), 0
    )
    imageBorder = np.concatenate(
        (
            np.expand_dims(imageBorder[:, 1, ], 1),
            imageBorder,
            np.expand_dims(imageBorder[:, -2, ], 1)
        ), 1
    )
    for i in range(imageReturn.shape[0]):
        for j in range(imageReturn.shape[1]):
            # imageReturn[i, j] = np.median(imageBorder[i : i + 3, j : j + 3], (0, 1))
            # if imageReturn.ndim == 2:
            #     imageReturn[i, j] = np.median(imageBorder[i : i + 3, j : j + 3])
            # else:
            # for k in range(imageReturn.shape[2]):
            #     imageReturn[i, j, k] = np.median(
            #         imageBorder[i : i + 3, j : j + 3, k]
            #     )
            # pass
            imageReturn[i, j] = np.median(imageBorder[i: i + 3, j: j + 3])
            # Only support single channel of image.
    return imageReturn


def gaussian_filter_generator(nSize, sigma) -> list:
    '''
    opencv: see gaussianBlur
    '''
    return [[0.0947, 0.1183, 0.0947], [0.1183, 0.1478, 0.1183], [0.0947, 0.1183, 0.0947]]  # sigma = 1.5
    pass

# @numba.jit(nopython = True)
def mean_filter_generator(nSize) -> np.ndarray:
    if nSize not in meanFilterKernel:
        meanFilterKernel[nSize] = np.full((nSize, nSize), 1 / nSize ** 2)
    return meanFilterKernel[nSize]


def bilateral_filter():
    pass


def histgram_wrapper(image):
    '''use cv.calchist
    '''
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    pass


def selected_2darray_plot(image: np.ndarray, pos: list, len):
    '''Choose a line of selected image to extract grey / red (or Channel 0) value on it.'''
    if 3 < image.ndim or not isinstance(pos, list):
        return None
    try:
        if pos[0]:
            npReturn = image[pos[0], :]
        else:
            npReturn = image[:, pos[1]]
        if npReturn.ndim == 2:
            npReturn = npReturn[:, 0]
        return npReturn  # np.interp()
    except IndexError:
        return None


def main():
    file = []
    print(cv2.__version__, matplotlib.__version__)

    if len(sys.argv) >= 2:
        os.path.isdir(sys.argv[1])
    for i in range(1, 11):
        imMatrix = cv2.imread("./dataset/s13/s13_{}.jpg".format(i))

        imMatrix = cv2.cvtColor(imMatrix,
                                cv2.COLOR_BGR2RGB  # opencv read image as BGR colorspace
                                # cv2.COLOR_BGR2GRAY # weighted mean, like ./hw1.py#68
                                )

        fig, ax = plt.subplots(4, 2, sharex='col', sharey='col', gridspec_kw={
                               'width_ratios': [1, 7]})
        extern_gui_provider(imMatrix, ax[0, 0], ax[0, 1], "Origin Image")
        extern_gui_provider(liner_filter(
            imMatrix, mean_filter_generator(3)), ax[1, 0], ax[1, 1], "Mean filter")
        print(time.time())
        extern_gui_provider(median_filter(imMatrix),
                            ax[2, 0], ax[2, 1], "Median filter")  # ~3s
        print(time.time())
        extern_gui_provider(liner_filter(imMatrix, gaussian_filter_generator(
            3, 1.5)), ax[3, 0], ax[3, 1], "Gaussian filter")
        plt.show()
        # plt.savefig()


if __name__ == "__main__":
    main()

hw2Config = {0: lambda x: x, 1: median_filter, 2: lambda x: liner_filter(x, mean_filter_generator(3)),
             3: lambda x: liner_filter(x, gaussian_filter_generator(3, 1.5))}


