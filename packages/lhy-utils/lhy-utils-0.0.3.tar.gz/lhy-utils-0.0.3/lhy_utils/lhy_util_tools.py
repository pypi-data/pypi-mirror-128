# coding: utf-8
import json
import math
import multiprocessing
import os
import logging
import re
import subprocess
import sys
import pickle as pkl
from logging.handlers import RotatingFileHandler

import numpy as np
import requests


class Logger:
    def __init__(self, log_file=None):
        print("init")
        self.logger = logging.getLogger(os.path.realpath(__file__))
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        self.fmt_str = "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s"
        self.formatter = logging.Formatter(self.fmt_str)
        self.sh = logging.StreamHandler()
        self.sh.setLevel(logging.INFO)
        self.sh.setFormatter(self.formatter)
        self.logger.addHandler(self.sh)
        if log_file:
            self.fh = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 64, backupCount=10, encoding="utf-8")
            self.fh.setLevel(logging.INFO)
            self.fh.setFormatter(self.formatter)
            self.logger.addHandler(self.fh)

    def get_logger(self):
        return self.logger

    def font_color(self, color):
        # 不同的日志输出不同的颜色
        formatter = logging.Formatter(color % self.fmt_str)
        self.sh.setFormatter(formatter)
        self.logger.addHandler(self.sh)

    # 显示方式（0: 默认; 1: 高亮; 4: 下划线; 5: 闪烁; 7: 反白显示; 8: 隐藏）
    # 前景色（30: 黑色; 31: 红色; 32: 绿色; 33: 黄色; 34: 蓝色; 35: 紫红色; 36: 青蓝色; 37: 白色）
    # 背景色（40: 黑色; 41: 红色; 42: 绿色; 43: 黄色; 44: 蓝色; 45: 紫红色; 46: 青蓝色; 47: 白色）

    def debug(self, message):
        self.font_color('\033[0;32m%s\033[0m')
        self.logger.debug(message)

    def info(self, message):
        self.font_color('\033[0;37m%s\033[0m')
        self.logger.info(message)

    def warning(self, message):
        self.font_color('\033[1;33m%s\033[0m')
        self.logger.warning(message)

    def error(self, message):
        self.font_color('\033[1;31m%s\033[0m')
        self.logger.error(message)
        exit(-1)

    def critical(self, message):
        self.font_color('\033[1;35m%s\033[0m')
        self.logger.critical(message)


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


def get_bert_path(model_name):
    system = sys.platform
    system = system.lower()
    if "linux" in system:
        bert_base = "/opt/models/bert/"
    elif "darwin" in system:
        bert_base = "/Users/lhy/Documents/bert_saved/"
    else:
        raise ValueError
    config_path = f'{bert_base}/{model_name}/bert_config.json'
    checkpoint_path = f'{bert_base}/{model_name}/bert_model.ckpt'
    dict_path = f'{bert_base}/{model_name}/vocab.txt'
    return config_path, checkpoint_path, dict_path


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
        logger.info(f"use gpu No.{index}")
        return str(index)
    except Exception as e:
        logger.error(str(e))
        return "-1"


def send_post(j_data, target_url, method="POST"):
    if method == "POST":
        result = requests.post(target_url, data=json.dumps(j_data), headers={'Content-Type': 'application/json'})
    else:
        result = requests.get(target_url)
    return result.text


def cut_list(target, batch_size):
    for i in range(0, len(target), batch_size):
        yield target[i: i + batch_size]


def read_json(j_path):
    with open(j_path, "r", encoding="utf-8") as fr:
        return json.load(fr)


def read_json_line(j_path):
    with open(j_path, "r", encoding="utf-8") as fr:
        return [json.loads(i.strip()) for i in fr.readlines()]


def write_json(j_data, j_path):
    with open(j_path, "w", encoding="utf-8") as fw:
        json.dump(j_data, fw, ensure_ascii=False, indent=4)


def write_json_line(j_data, j_path):
    with open(j_path, "w", encoding="utf-8") as fw:
        for data in j_data:
            fw.write(json.dumps(data, ensure_ascii=False) + "\n")


def save_pkl(obj, pkl_path):
    with open(pkl_path, "wb") as fwb:
        pkl.dump(obj, fwb)


def load_pkl(pkl_path):
    with open(pkl_path, "rb") as frb:
        return pkl.load(frb)