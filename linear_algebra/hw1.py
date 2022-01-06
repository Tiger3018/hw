#!/usr/bin/env python3
# Tiger3018 | MIT License
# dataset thanks to https://github.com/davidsonmizael/criminal-gan
# wikimedia thanks to https://commons.wikimedia.org/wiki/File:%E9%87%8D%E5%BA%86_%E6%B1%9F%E5%8C%97.jpg
import cv2
import numpy as np
import os, sys

import traceback

configA = {
    "debug": True,
    "dimension": 35
}


def externGuiProvider(colorSpace):
    '''
    This function will be served as hw1 example.

    - See https://stackoverflow.com/questions/15221476/show-multiple-images-in-same-window-with-python-opencv
    '''
    if len(colorSpace) != 4:
        raise TypeError("len(colorSpace) -nq 4.")
    showLine1 = np.concatenate([colorSpace[0], np.repeat(colorSpace[1][:,:, None], 3, 2)], axis = 1)
    showLine2 = np.concatenate([colorSpace[1], colorSpace[2]], axis = 1)
    showLine2 = np.repeat(showLine2[:,:, None], 3, 2)
    showALL = np.vstack([showLine1, showLine2])
    showALL = cv2.resize(showALL, (1600, 1200))
    cv2.imshow("Open CV & Numpy for multiple grey space method.", showALL)
    cv2.imwrite("hw1.jpg", showALL)
    cv2.waitKey(0)


class colorSpaceMatrix():
    _matrix = None
    _project = None
    space = []
    spaceRGB = []
    spaceHSV = []
    spaceGrey = []
    _spaceBGR = []
    _spaceUTIL = {
    }

    def __init__(self, **kwargs):
        if len(kwargs) != 1:
            raise Exception('Only 1 named argument required.')
        key, spaceValue = list(kwargs.items())[0]
        if key == 'BGR':
            self._spaceBGR = spaceValue
            self.convertBGR()
            self._convertGreyVary()
        elif key == "RGB":
            self.spaceRGB = spaceValue
            self._convertGreyVary()
        else:
            raise NotImplementedError("This format of space can't be init.")

    # See https://jakevdp.github.io/PythonDataScienceHandbook/02.02-the-basics-of-numpy-arrays.html
    def convertBGR(self):
        # self.spaceRGB = np.dstack([self._spaceBGR[:, :, 3], )
        self.spaceRGB = np.flip(self._spaceBGR, 2)

    def _convertProject(self):
        pass

    def _convertGreyVary(self):
        """
        The default impletion of RGB -> GREY is weighted mean.
        See https://docs.opencv.org/4.5.3/de/d25/imgproc_color_conversions.html
        """
        self.spaceGrey = np.average(self.spaceRGB, 2, [0.299, 0.578, 0.114]).astype(np.uint8) # more config on uint8
        self._spaceUTIL["GREY-M"] = np.mean(self.spaceRGB, 2).astype(np.uint8)
        self._spaceUTIL["GREY-A"] = np.amax(self.spaceRGB, 2)
        self.space = [self.spaceRGB, self.spaceGrey, self._spaceUTIL["GREY-M"], self._spaceUTIL["GREY-A"]]
        return
    
    def getSpaceUTIL(self):
        return 

class imagePCA():
    '''
    This class will be served
    '''
    path = ''
    name = ''
    _dimension = 0
    spaceOrigin = []

    def __init__(self, dim, *args):
        _dimension = dim
        if imSpace := self._readSingle(args[0]):
            externGuiProvider([imSpace._spaceBGR, imSpace._spaceUTIL["GREY-A"],
                imSpace._spaceUTIL["GREY-M"], imSpace.spaceGrey])

    def _readPGM(self, *args):
        self.spaceOrigin = self._readSingle(args[0] + str(args[1]) + ".pgm")
        for i in range(args[1] + 1, args[2] + 1):
            pathNow = args[0] + str(i) + ".pgm"
            self.spaceOrigin = np.hstack([self.spaceOrigin, self._readSingle(pathNow)])
            # if(os.path.exists(pathNow)):
            #     self.spaceOrigin = np.hstack([self.spaceOrigin, self._open(pathNow)])
            # else:
            #     raise FileNotFoundError(pathNow)
        if configA["debug"]:
            print(self.spaceOrigin)

    def _readSingle(self, path):
        # Based on https://zhuanlan.zhihu.com/p/26652435 + https://github.com/Wanggcong/Statistical-Analysis-Method-/blob/master/project3/16337292_%E8%A2%81%E6%B5%A9%E6%89%AC/%E7%BB%9F%E8%AE%A1%E5%88%86%E6%9E%90%E5%AE%9E%E9%AA%8C%E4%B8%89%EF%BC%9APCA%E5%9B%BE%E5%83%8F%E5%8E%8B%E7%BC%A9.md
        # Inspired by https://www.jianshu.com/p/09871c72a143
        try:
            im = cv2.imread(path)  # it also read pgm as BGR
            # imSpace = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            imSpace = colorSpaceMatrix(BGR = im)
            return imSpace
            # print(imGrey)
            # imCol = imGrey.reshape(imGrey.size, 1)
            # if configA["debug"]:
                # print(im.shape, imGrey.shape, imCol.shape)
                # print(imCol)
            # return imCol
        except Exception as e:
            print('\033[1;31mLoad {} failed. TYPE: {}\033[0m'.format(
                path, type(e)
                ))
            traceback.print_exc()
            return None

def main():
    # imagePCA(35, rgv, 1, 10)
    if len(sys.argv) > 1:
        tmpPath = sys.argv[1]
    else:
        tmpPath = "./img/Glabb-wikimedia-重庆_江北-cc3-by-sa.jpg"
    imagePCA(35, tmpPath)

if __name__ == "__main__":
    main()