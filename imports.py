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
import glob2

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'bank-widrawall-93d9f71edc38.json'
