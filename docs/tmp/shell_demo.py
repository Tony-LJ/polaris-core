import paramiko

# 远程服务器的信息
hostname = '10.53.0.71'
port = 22  # SSH默认端口是22
username = 'root'
password = 'EEEeee111'

# 要执行的命令
command = 'ls -l'

# 创建SSH对象
ssh = paramiko.SSHClient()

# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接服务器
ssh.connect(hostname, port, username, password)

# 执行命令
stdin, stdout, stderr = ssh.exec_command(command)

# 获取命令结果
result = stdout.read().decode()
error = stderr.read().decode()

# 关闭连接
ssh.close()

# 打印结果或错误信息
print("Result:", result)
if error:
    print("Error:", error)