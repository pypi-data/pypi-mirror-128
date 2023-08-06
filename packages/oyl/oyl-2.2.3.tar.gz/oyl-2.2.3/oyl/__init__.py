import sys
import os
import pickle as pk
import datetime as dt
import time

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
import xarray as xr

from .Methods import *
from .Drawings import *
from .Scores import classification_score



bar_color1 = 'darkturquoise'

def love():
    """
    A simple demo.
    """
    x = np.hstack([np.linspace(-1,-0.99,100),np.linspace(-0.99,0.99,800),np.linspace(0.99,1,100)])

    y = np.sqrt(1-x**2)+np.abs(x)
    plt.plot(x,y,color='orange',marker='.')

    y = -np.sqrt(1-x**2)+np.abs(x)
    plt.plot(x,y,'b.-')
    plt.legend([r'$y=\sqrt{1-x^2}+\left|x\right|$',r'$y=-\sqrt{1-x^2}+\left|x\right|$'])
    plt.show()


def shutdown(t=1):
    """
    Wait for t seconds to shutdown the computer
    """
    comand = 'shutdown -s -t '+str(t)
    os.system(comand)

def save(*args,path='./savings.pkl'):
    size = 0
    for i in args:
        size+=sys.getsizeof(i)
    with open(path,'wb') as f:
        if size>1073741824*3:
            pk.dump(args,f,protocol=4)
        else:
            pk.dump(args,f)

def readpkl(path='./savings.pkl'):
    with open(path,'rb') as f:
        return pk.load(f)

def timing(aim = None):
    if aim is not None:
        now = dt.datetime.now()
        tmp = aim - now
        res = tmp.seconds
        print('waitting for {} seconds'.format(res))
        time.sleep(res)


