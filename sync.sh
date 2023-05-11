# scp -r current_path ssh_usr@machine_ip:dest_path
###
 # @Author: pinkfloyd-eminem 13219058346@163.com
 # @Date: 2023-05-10 19:27:12
 # @LastEditors: pinkfloyd-eminem 13219058346@163.com
 # @LastEditTime: 2023-05-11 11:35:34
 # @FilePath: /ysl/distributed-training-INA/deploy.sh
 # @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
### 
# scp -r distributed-training-INA ysl@192.168.1.13:~

#!/bin/bash

# 删除远程主机上的对应文件
sshpass -p "kb310" ssh 192.168.1.13 "rm -rf ~/distributed-training-INA/config"
sshpass -p "kb310" ssh 192.168.1.13 "rm -rf ~/distributed-training-INA/scripts"
sshpass -p "kb310" ssh 192.168.1.13 "rm -rf ~/distributed-training-INA/src"
sshpass -p "kb310" ssh 192.168.1.13 "rm -rf ~/distributed-training-INA/tests"
sshpass -p "kb310" ssh 192.168.1.13 "rm -f ~/distributed-training-INA/sync.sh"
sshpass -p "kb310" ssh 192.168.1.13 "rm -f ~/distributed-training-INA/test.sh"

# 将本地目录同步到远程主机上
sshpass -p "kb310" scp -r /home/ysl/distributed-training-INA/config 192.168.1.13:~/distributed-training-INA/
sshpass -p "kb310" scp -r /home/ysl/distributed-training-INA/scripts 192.168.1.13:~/distributed-training-INA/
sshpass -p "kb310" scp -r /home/ysl/distributed-training-INA/src 192.168.1.13:~/distributed-training-INA/
sshpass -p "kb310" scp -r /home/ysl/distributed-training-INA/tests 192.168.1.13:~/distributed-training-INA/
sshpass -p "kb310" scp  /home/ysl/distributed-training-INA/sync.sh 192.168.1.13:~/distributed-training-INA/
sshpass -p "kb310" scp  /home/ysl/distributed-training-INA/test.sh 192.168.1.13:~/distributed-training-INA/
