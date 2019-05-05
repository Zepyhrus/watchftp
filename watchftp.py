# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s 

Authenticated by Sherk
Any question please refer to:
    sherkfung@gmail.com
"""
import io
import time
import random


import ftplib
import logging

import cv2
import numpy as np
import pandas as pd
#%%
FTP_HOST = '127.0.0.1'
FTP_PORT = 21
FTP_USER = 'username'
FTP_PSWD = 'password'


SRS_DIR = 'tools/img/'
DES_DIR = 'tools/test/'

# the limit of img uploaded
LIMIT = 10
#%%
logging.basicConfig(
  filename='test.log', level=logging.INFO,
  format='[%(asctime)s - %(levelname)s]: %(message)s')



## initialize the source directory
ftp = ftplib.FTP()
ftp.connect(host=FTP_HOST, port=FTP_PORT)
ftp.login(user=FTP_USER, passwd=FTP_PSWD)
ftp.cwd(SRS_DIR)

# initialzie the destiation directory
des_ftp = ftplib.FTP()
des_ftp.connect(host=FTP_HOST, port=FTP_PORT)
des_ftp.login(user=FTP_USER, passwd=FTP_PSWD)
des_ftp.cwd(DES_DIR)


#%%
def img_transport(img, ftp, des_ftp):
  '''
  transport img from source foleder to destination folder, without explicit 
  saving them to the hard disk, only in the memory buffer:
  Input:
    img: file name in source ftp; 
    ftp: source ftp directory; 
    des_ftp: destination ftp directory;
  Output: 
    the transport is successed or not  
  '''
  try:
    bio = io.BytesIO()
    
    ftp.retrbinary('RETR '+img, bio.write)
    
    img_arr = cv2.imdecode(
      np.asarray(bytearray(bio.getvalue()), dtype='uint8'), cv2.IMREAD_COLOR)


    # do whatever you want to do here
    cv2.rectangle(img_arr, (0, 0), (1000, 1000), (0, 255, 0), 10)
    
    _, buffer = cv2.imencode('.JPG', img_arr)
    io_buf = io.BytesIO(buffer)
    
    des_ftp.storbinary('STOR '+img, io_buf)
    
    return True
  except:
    return False
    
#%%
if __name__ == '__main__':
  old_imgs = ftp.nlst()
  
  while True:
    try:
      new_imgs = ftp.nlst()
      
      add_imgs = [img for img in new_imgs if img not in old_imgs]
      
      if len(add_imgs):
        if len(add_imgs) > LIMIT:
          logging.warning('More than %s images are loaded!' % LIMIT)
          print('More than %s images are loaded!' % LIMIT)
          
          add_imgs = random.sample(add_imgs, LIMIT)
          
        for img in add_imgs:
          logging.info(img)
        rst = pd.Series([img_transport(img, ftp, des_ftp) for img in add_imgs])
        
        print(rst.value_counts())
      else:
        logging.info('No image added.')
        print('No image added.')
        time.sleep(30)
        
      old_imgs = new_imgs.copy()
    except Exception as ecpt:
      logging.error(ecpt)
      print(ecpt)
      break
  ftp.close()
  des_ftp.close()
        
























