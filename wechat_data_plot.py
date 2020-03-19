# --coding:utf-8--

import matplotlib.pyplot as plt
import numpy as np

class DrawPlot:
    def __init__(self):
        self.x_array = []
        self.y_array = []

    def draw_hist(self):
        max_num = max(self.y_array)


