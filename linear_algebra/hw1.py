#!/usr/bin/env python3
# Tiger3018 | MIT License
# dataset thanks to https://github.com/davidsonmizael/criminal-gan
import cv2
import os
import sys
import numpy as np

import traceback

configA = {
    "debug": True,
    "dimension": 35
}


def externGuiProvider():
    '''
    This function will be served
    '''


class colorSpaceMatrix():
    _matrix = None
    _project = None

    def __init__(self, *kargs):
        if len(kargs) != 1:
            raise Exception('Only 1 named argument required.')
        if hsv in kargs:
            pass

    def _convertProject(self):
        pass


class imagePCA():
    '''
    This class will be served
    '''
    path = ''
    name = ''
    _dimension = 0
    spaceRGB = None
    spaceHSV = None
    spaceGrey = None
    spaceOrigin = []

    def __init__(self, dim, *args):
        # print(args)
        _dimension = dim
        self.spaceOrigin = self._read(args[0] + str(args[1]) + ".pgm")
        for i in range(args[1] + 1, args[2] + 1):
            pathNow = args[0] + str(i) + ".pgm"
            self.spaceOrigin = np.hstack([self.spaceOrigin, self._read(pathNow)])
            # if(os.path.exists(pathNow)):
            #     self.spaceOrigin = np.hstack([self.spaceOrigin, self._open(pathNow)])
            # else:
            #     raise FileNotFoundError(pathNow)
        if configA["debug"]:
            print(self.spaceOrigin)

    def _read(self, path):
        # Based on https://zhuanlan.zhihu.com/p/26652435 + https://github.com/Wanggcong/Statistical-Analysis-Method-/blob/master/project3/16337292_%E8%A2%81%E6%B5%A9%E6%89%AC/%E7%BB%9F%E8%AE%A1%E5%88%86%E6%9E%90%E5%AE%9E%E9%AA%8C%E4%B8%89%EF%BC%9APCA%E5%9B%BE%E5%83%8F%E5%8E%8B%E7%BC%A9.md
        # Inspired by https://www.jianshu.com/p/09871c72a143
        # See https://jakevdp.github.io/PythonDataScienceHandbook/02.02-the-basics-of-numpy-arrays.html
        try:
            im = cv2.imread(path)  # it also read pgm as BGR
            imGrey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            # print(imGrey)
            imCol = imGrey.reshape(imGrey.size, 1)
            if configA["debug"]:
                print(im.shape, imGrey.shape, imCol.shape)
                # print(imCol)
            return imCol
        except Exception as e:
            print('\033[1;31mLoad {} failed. TYPE: {}\033[0m'.format(
                path, type(e)))
            traceback.print_exc()


imagePCA(35, sys.argv[1], 1, 10)
