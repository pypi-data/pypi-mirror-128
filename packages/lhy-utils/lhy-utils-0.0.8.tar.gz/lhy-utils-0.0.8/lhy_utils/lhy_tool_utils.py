# coding: utf-8
# import json
import math
import multiprocessing
import re
import subprocess

import numpy as np


class MultiProcessBase:
    def __init__(self, data, work_nums=4):
        self.data = data
        self.data_num = len(self.data)
        self.work_nums = work_nums
        self.result = multiprocessing.Manager().dict()

    def task(self, inputs):
        # for input in process_inputs:
        #     data = self.data[input]
        #     self.result[input] = how to process data
        raise NotImplemented

    def run(self):
        inputs = list(cut_list(list(range(self.data_num)), math.ceil(self.data_num / self.work_nums)))
        jobs = [multiprocessing.Process(target=self.task, args=(inputs[i],)) for i in range(self.work_nums)]
        for job in jobs:
            job.start()
        for job in jobs:
            job.join()
        result_list = [0] * self.data_num
        for key, value in self.result.items():
            result_list[key] = value
        return result_list


def get_gpu_num():
    try:
        patter = r"[0-9]+MiB"
        all_gpu = []
        popen = subprocess.Popen("nvidia-smi", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        bz = False
        while popen.poll() is None:
            line = popen.stdout.readline().rstrip().decode()
            if bz:
                memory = re.findall(patter, line)[0].replace("MiB", "")
                all_gpu.append(int(memory))
                bz = False
            if "GeForce" in line:
                bz = True
        all_gpu = np.array(all_gpu)
        indexs = np.where(all_gpu == np.min(all_gpu))[0]
        index = -1 if len(indexs) == 0 else indexs[-1]
        return str(index)
    except Exception as e:
        print(str(e))
        return "-1"


def cut_list(target, batch_size):
    for i in range(0, len(target), batch_size):
        yield target[i: i + batch_size]


def args_to_str(args):
    return [str(i) for i in args]


def dict_set_value(input_data, args):
    assert len(args) == len(input_data.keys())
    for i, k in enumerate(input_data.keys()):
        input_data[k].append(args[i])
