# -*- coding: utf-8 -*-

"""
descr: GitLab工具类
auther: lj.michale
create_date: 2025/10/22 15:54
file_name: gitlab_utils.py
"""
import os
import sys
import re
import multiprocessing
# import subprocess
import gitlab

# def update_gitlab_repo(repo_dir):
#     """
#     更新gitlab仓库
#     :param repo_dir:
#     :return:
#     """
#     all_dirs_files = os.listdir(repo_dir)
#     for name_dir in all_dirs_files:
#         name_path = os.path.join(repo_dir, name_dir)
#         if os.path.isdir(name_path):
#             git_pull_cmd = " cd " + name_path + " && git pull "
#             code, result = subprocess.getstatusoutput(git_pull_cmd)
#             if code == 0:
#                 print("git pull "+ name_path + " successd")
#             else:
#                 print("git pull "+ name_path + " failed")
#     return 0