# # 输出目录在 scripts
# g++ -pthread -shared -O3 -fPIC -std=c++11 -o send.so ../src/common/communicator.cc 
# 输出目录在 src/common
g++ -pthread -shared -O3 -fPIC -std=c++11 -o ../src/common/send.so ../src/common/communicator.cc