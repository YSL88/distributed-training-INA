import os
import pickle
import socket
import struct
import time
import paramiko
from time import sleep
from threading import Thread

launch_time = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))


class Worker:
    def __init__(self, idx, dataset, model, use_cuda,epoch, batch_size, ip, ssh_port, ps_ip, ps_port, work_dir, ssh_usr,ssh_psw):
        self.idx = idx
        self.dataset = dataset
        self.model = model
        self.use_cuda = use_cuda
        self.epoch = epoch
        self.batch_size = batch_size
        self.worker_time = 0.0
        self.ip=ip
        self.ssh_port= ssh_port
        self.ps_ip=ps_ip
        self.ps_port=ps_port
        self.work_dir=work_dir
        self.ssh_usr=ssh_usr
        self.ssh_psw=ssh_psw
        self.socket = None
        self.updated_paras=None
        self.sending_time=None
        self.cmd=' cd ' + self.work_dir + '; sudo /home/inspur/miniconda3/bin/python3 ' + '-u src/launch.py' + \
                  ' --master ' + str(0) + \
                  ' --master_ip ' + str(self.ps_ip) + \
                  ' --master_port ' + str(self.ps_port) + \
                  ' --ip ' + str(self.ip) + \
                  ' --idx ' + str(self.idx) + \
                  ' --dataset ' + str(self.dataset) + \
                  ' --model ' + str(self.model) + \
                  ' --epoch ' + str(self.epoch) + \
                  ' --batch_size ' + str(self.batch_size) + \
                  ' > data/log/'+launch_time+'_worker_' + str(self.idx) + '.txt 2>&1'
        self.get_all()

    def get_all(self):
        print(", ".join([f"{attr}: {str(getattr(self, attr))}" for attr in dir(self)
                         if not callable(getattr(self, attr)) and not attr.startswith("__") 
                         and attr in ["idx", "dataset", "model", "use_cuda", "epoch", "batch_size", 
                                      "worker_time", "ip", "ssh_port", "ps_ip", "ps_port", "work_dir", 
                                      "ssh_usr", "ssh_psw", "socket", "updated_paras", "sending_time"]]))

    def launch(self, para, partition):
        try:
            if self.ip =="127.0.0.1":
                t= Thread(target=self._launch_local_process)
                t.start()
            else:
                # print("debug t start")
                t= Thread(target=self._launch_remote_process)
                t.start()
                # print("debug t end")

        except Exception as e:
            print(e)
            exit(1)
        else:
            # print("debug init")
            self._init_send_socket()
            init_config={
                'para':para,
                'train_data_index' : partition[0].use(self.idx),
                'test_data_index' : partition[1].use(self.idx)
            }
            self.send_data(init_config)
            # print("debug init end")

    def send_data(self, data):
        ser_data = pickle.dumps(data)
        self.socket.sendall(struct.pack(">I", len(ser_data)))
        self.socket.sendall(ser_data)
    
    def get_trained_model(self):
        try:
            timestamp=struct.unpack(">d", self.socket.recv(8))[0]
            data_len = struct.unpack(">I", self.socket.recv(4))[0]
            data = self.socket.recv(data_len, socket.MSG_WAITALL)
        except Exception as e:
            print(e)
            exit(1)
        else:
            self.sending_time=timestamp
            self.updated_paras = pickle.loads(data)
            # self.updated_paras.to()

    # server 给 worker 发数据的 socket
    def _init_send_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("debug self.socket.connect_ex((self.ip, int(self.ps_port)))")
        print("debug self.ip: " + str(self.ip) + " self.port: " + str(self.ps_port))
        print("dubug self.socket.connect_ex((self.ip, int(self.ps_port))) value is: " + str(int(self.socket.connect_ex((self.ip, int(self.ps_port))))))
        while self.socket.connect_ex((self.ip, int(self.ps_port))) != 0:
            sleep(0.5)
        print("debug _init_send_socket")

    def _launch_remote_process(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(hostname=self.ip, port=int(self.ssh_port),
                        username=self.ssh_usr, password=self.ssh_psw)  # server ssh worker 去
        except Exception as e:
            print(e)
            ssh.close()
            raise e
        else:
            print("Execute {}.".format(self.cmd))
            stdin, stdout, stderr = ssh.exec_command(self.cmd, get_pty=True)
            stdin.write(self.ssh_psw + '\n')
            output = []
            out = stdout.read()
            error = stderr.read()
            if out:
                print('[%s] OUT:\n%s' % (self.ip, out.decode('utf8')))
                output.append(out.decode('utf-8'))
                print(output)
            if error:
                print('ERROR:[%s]\n%s' % (self.ip, error.decode('utf8')))
                output.append(str(self.ip) + ' ' + error.decode('utf-8'))
                print(output)
                raise Exception("Launch Error.")
    
    def _launch_local_process(self):
        os.system(self.cmd)