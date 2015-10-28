#encoding:UTF-8
__author__ = 'auroua'

import os
import cv2
import numpy as np
import math
from time import clock

# original file path  /home/auroua/workspace/PycharmProjects/data/N20040103G/
# test file path  /home/auroua/workspace/PycharmProjects/data/test/

def getFiles(path='/home/auroua/workspace/PycharmProjects/data/N20040103G/'):
    '''获取制定目录下的文件的绝对路径,带文件名'''
    filelist = []
    FileNames = os.listdir(path)
    if len(FileNames)>0:
       for fn in FileNames:
            fullfilename = os.path.join(path, fn)
            filelist.append(fullfilename)

    # 对文件名排序
    if len(filelist)>0:
        filelist.sort()
    return filelist

def showImg_url(url):
    ''' 显示制定url中的图片 '''
    img = cv2.imread(url)
    cv2.namedWindow('aurora')
    cv2.imshow('aurora img', img)
    cv2.waitKey(0)

def showImg(img):
    '''显示制定url中的图片'''
    cv2.namedWindow('aurora')
    cv2.imshow('aurora img', img)
    cv2.waitKey(0)

def getChannel(img):
    '''because the three channels have the same value,so it is sensible to use one single channel to
    represent the img'''
    b, g, r = cv2.split(img)
    return b

def getImg(url):
    '''返回图像数据'''
    img = cv2.imread(url)
    return img

def avg_channel(img):
    b, g, r = cv2.split(img)
    return (b+r+g)/3

def hist(img):
    # img = avg_channel(img)
    hists, bins = np.histogram(img.ravel(), 256, [0, 256])
    return hists

def bgr2hsv(img):
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return hsv_img

def hsv_hist_16bins(img):
    h, s, v = cv2.split(img)
    print img.shape
    h_bins = 8
    s_bins = 4
    v_bins = 4
    h_range = [0,180]
    s_range = [0,255]
    v_range = [0,255]
    print np.max(h), np.min(h)
    print np.max(s), np.min(s)
    print np.max(v), np.min(v)

def generate_vector(files):
    img_b = getImg(files[0])
    img_b = getChannel(img_b)
    data_vector = np.zeros((len(files), img_b.shape[0], img_b.shape[1]),dtype=img_b.dtype)
    for index, url in enumerate(files):
        img_b = getImg(url)
        img_b = getChannel(img_b)
        data_vector[index, :, :] = img_b
        # print (data_matrix[index, :, :] == img_b).all()
        # cv2.imshow('image',data_matrix[0, :, :])
        # cv2.imshow('original',img_b)
        # cv2.waitKey(0)
    return data_vector

def gen_matrix(img_vector):
    img_vector = img_vector.astype(dtype=np.int32)
    img_matrix = np.zeros((img_vector.shape[0], img_vector.shape[0]))
    for i in range(0, img_vector.shape[0]):
        for j in range(0,img_vector.shape[0]):
            img_matrix[i, j] = np.abs(img_vector[i, :, :] - img_vector[j, :, :]).sum()
    np.save('/home/auroua/workspace/PycharmProjects/data/similary',img_matrix)
    return img_matrix

def caucal_gausses(i, j, sigma=3, d=20):
    d = -1*(1/20.)
    # return math.exp(d*((i-j)/3.)**2)
    return math.exp(d*((i-j)/13.)**2)

def gen_matrix_gausses(img_vector):
    #d=20, sigma = 3
    img_vector = img_vector.astype(dtype=np.int32)
    img_matrix = np.zeros((img_vector.shape[0], img_vector.shape[0]))
    w_gauss = 0
    for i in range(0, img_vector.shape[0]):
        for j in range(0,img_vector.shape[0]):
            img_matrix[i, j] = np.abs(img_vector[i, :, :] - img_vector[j, :, :]).sum()
            img_matrix[i, j] *= caucal_gausses(i, j)
    np.save('/home/auroua/workspace/PycharmProjects/data/similary_gausses_13',img_matrix)
    return img_matrix

if __name__=='__main__':
    # img = getImg('/home/auroua/workspace/PycharmProjects/data/N20040103G/N20040103G030001.bmp')

    data = generate_vector(getFiles())
    print '----------------------------------------'
    start = clock()
    print start
    # res_matrix = gen_matrix(data)
    res_matrix = gen_matrix_gausses(data)
    end = clock()
    print end
    print end - start

    print res_matrix.shape


