### Process Time Printer Class
import time
import numpy as np
from numpy import random

class process_time_printer():
    
    def __init__(self, count):
        self.count = count
        self.iteration = 1
        self.time_list = []
        self.start_time = time.time()
        
    def increment(self, st):
        self.time_list.append(self.get_time() - st)
        print('| {0}/{1} complete | {2} seconds elapsed | {3} estimated seconds remaining |     '.format(
            self.iteration, self.count, round(self.get_time() - self.start_time, 4)
            , round((self.count - self.iteration) * np.mean(self.time_list), 4)
        ), end='\r', flush=True)
        self.iteration += 1
        
    def get_time(self):
        return time.time()