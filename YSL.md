<!--
 * @Author: pinkfloyd-eminem 13219058346@163.com
 * @Date: 2023-05-10 21:44:04
 * @LastEditors: YSL88 slyangzz@163.com
 * @LastEditTime: 2023-05-11 22:40:01
 * @FilePath: /ysl/distributed-training-INA/YSL.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 部署
1. 宿主机上python环境太乱，无法分布式，用docker试试
2. cloud1 环境有问题，sudo apt install libjpeg-dev zlib1g-dev libssl-dev libffi-dev python-dev build-essential libxml2-dev libxslt1-dev 卡在这一步，暂时两台机器来分布式（cloud2 cloud 3）
3. 安装 miniconda
4. pip3 install torch==1.12.0+cpu torchvision torchaudio -f https://download.pytorch.org/whl/cpu/torch_stable.html
    pip3 install paramiko
5. conda 起不来 就 source ~/.bashrc
# 运行
1. 启动文件是 src/launch.py
2. common/communicator.cc .h communicator.py  tests/test_send.py 测试成功
3. 在~/distributed-training-INA目录下，bash test.sh 即可
4. 运行时 
    1. sudo /home/ysl/miniconda3/bin/python3 src/launch.py --master 1 --ip 192.168.1.12 --worker_num 1 --config_file config/workers.json --dataset CIFAR100 --model resnet50
    在每台机子上都装一个 miniconda 
    2. worker.py self.cmd = /home/ysl/miniconda3/bin/python3
5. 同步脚本


# 疑问
1. readme中 cpu only pytorch launch.py中 也是os.environ['CUDA_VISIBLE_DEVICES'] = '0'
是否意味着这版代码只能CPU 
2. distributed-training-INA/src/common/communicator.py 中 dst_ip_str = "192.168.1.11" 暂时只在本机发，这个最后怎么设置的
# bug 记录
1. 导入文件的路径要改，最好通过语法变成绝对路径 TODO
2. 查看 .so 文件中的函数是否存在
    1. nm src/common/send.so | grep send_gradients
    2. objdump -t src/common/send.so 会输出 send.so 文件中的符号表，包括函数名、地址、大小等信息。
    3. g++ gcc 编译会对 .cc 文件里面的函数做名称修饰，需要使用extern "C" 声明函数为 C 函数，并将其导出为符号。具体代码是：
    ``` c++
    #ifdef __cplusplus
    extern "C" {
    #endif

    void send_gradients(unsigned int* gradients, int size, unsigned int dest, int tag, unsigned int src, int rank);

    #ifdef __cplusplus
    }
    #endif
    ```
3. github 源文件中 train_dataset, test_dataset = datasets.load_datasets(dataset,DATASET_PATH) 中 load_datasets 没有 s 会报错
# src/distributed_training OK
## 1. 依赖
1. pytorch needed（server 不参与训练可不用

  ```bash
  sudo apt install libjpeg-dev zlib1g-dev libssl-dev libffi-dev python-dev build-essential libxml2-dev libxslt1-dev
  ```
2. 安装 miniconda
    目录一定要是 **/home/ysl/miniconda3/bin/python3**
    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

    bash Miniconda3-latest-Linux-x86_64.sh

    source ~/.bashrc

    conda --version  which python3 验证，如果python3不指向miniconda就source ~/.bashrc
    ```
3. python dependency  

    ```bash
    pip3 install pulp numpy tensorboard paramiko
    ```
4. pytorch 
    ```bash
    pip3 install torch==1.12.0+cpu torchvision torchaudio -f https://download.pytorch.org/whl/cpu/torch_stable.html
    ```
## 2. 运行
1. **修改** config/workers.json 中的节点信息
2. **修改** test.sh 中的 
    1. worker_num 为 config/workers.json 中的节点数量 
    TODO worker_num 怎么使美元符生效
    2. ip 为 server ip
    TODO 在 config/workers.json 中把 server 添加上是不是也行
3. **同步** 到所有机器上，可以写 sync.sh 脚本（只删一部分），也可以每个机器 rm 再 scp
    TODO 写一个 rm scp 脚本（全删
4. **检查防火墙** 开了的关掉就行，不放心就在代码里把端口固定，只开一个
    1. 查看防火墙状态 sudo firewall-cmd --state
    2. 开启防火墙 sudo systemctl start firewalld
    3. 关闭防火墙 sudo systemctl stop firewalld
    4. 添加到安全组 
        sudo firewall-cmd --zone=public --add-port=5201/tcp --permanent
        sudo firewall-cmd --reload
    5. 移出安全组
        sudo firewall-cmd --zone=public --remove-port=5201/tcp --permanent
        sudo firewall-cmd --reload
    6. 测试端口可达 telnet 192.168.1.11 5201
    7. 测试端口可达 1 上 iperf3 ... , 2 上 iperf3 ...
5. **运行** bash test.sh
    1. server 运行 master loop 打印信息到控制台
    TODO 打印到 data/log
    2. worker 运行 worker loop 打印信息到 data/log





