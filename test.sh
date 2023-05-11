
###
 # @Author: pinkfloyd-eminem 13219058346@163.com
 # @Date: 2023-05-10 21:10:09
 # @LastEditors: pinkfloyd-eminem 13219058346@163.com
 # @LastEditTime: 2023-05-11 17:04:04
 # @FilePath: /ysl/distributed-training-INA/test.sh
 # @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
### 
WORKER_NUM=$1
# sudo /home/ysl/miniconda3/bin/python3 src/launch.py --master 1 --ip 192.168.1.12 --worker_num $WORKER_NUM --config_file config/workers.json --dataset CIFAR100 --model resnet50
sudo /home/ysl/miniconda3/bin/python3 src/launch.py --master 1 --ip 192.168.1.12 --worker_num 1 --config_file config/workers.json --dataset CIFAR100 --model resnet50