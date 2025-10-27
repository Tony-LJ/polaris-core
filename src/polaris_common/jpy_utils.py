# -*- coding: utf-8 -*-

"""
descr: python调用java封装
auther: lj.michale
create_date: 2025/10/17 15:54
file_name: jpy_utils.py
"""

import jpype

# 启动 JVM（指定 jvm.dll 路径）
jpype.startJVM(jpype.getDefaultJVMPath(),
               "-ea",
               "-Djava.class.path=/path/to/your.jar")

# 导入 Java 类
ArrayList = jpype.JClass("java.util.ArrayList")
System = jpype.JClass("java.lang.System")

# 使用 Java 对象
java_list = ArrayList()
java_list.add("测试数据")
System.out.println(java_list)  # 输出: [测试数据]

# 调用静态方法
Collections = jpype.JClass("java.util.Collections")
Collections.sort(java_list)

# 关闭 JVM（程序结束前调用）
jpype.shutdownJVM()
