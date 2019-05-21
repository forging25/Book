yum -y install bzip2 wget vim git

vim /etc/yum.repos.d/mongodb-org-3.6.repo

[mongodb-org-3.6]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2013.03/mongodb-org/3.6/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.6.asc

sudo yum install mongodb-org
sudo systemctl start mongod
ps -aux |grep mongod
sudo systemctl status mongod

yum install epel-release yum-utils
yum install http://rpms.remirepo.net/enterprise/remi-release-7.rpm
yum-config-manager --enable remi
yum install redis

vim /etc/redis.conf
# 使 redis 能在后台运行
daemonize yes

systemctl restart redis

pip install pipenv
#安装程序所需的环境
pipenv install
python run.py