from google.cloud import vision
import io
import os
import requests
import shutil
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'handy-balancer-369316-5ccaaba05b4c.json'
