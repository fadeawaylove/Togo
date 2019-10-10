# step 1: 安装必要的一些系统工具
sudo apt-get update && \
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
# step 2: 安装GPG证书
curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
# Step 3: 写入软件源信息
sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
# Step 4: 更新并安装Docker-CE
sudo apt-get -y update
sudo apt-get -y install docker-ce

# 将当前用户添加到docker用户组，避免使用sudo
sudo gpasswd -a ${USER} docker
# 重启docker
sudo systemctl restart docker
# 如果执行命令还是出现权限问题
sudo chmod a+rw /var/run/docker.sock