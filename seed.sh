#!/bin/bash

apt-get update -y
apt-get install git curl vim -y

cat > /etc/apt/sources.list.d/cloudera.list << EOF
deb [arch=amd64] http://archive.cloudera.com/cdh4/ubuntu/precise/amd64/cdh precise-cdh4 contrib
deb-src http://archive.cloudera.com/cdh4/ubuntu/precise/amd64/cdh precise-cdh4 contrib
EOF

curl -s http://archive.cloudera.com/cdh4/ubuntu/precise/amd64/cdh/archive.key | apt-key add -


if [ ! -d /usr/local/jdk1.6.0_45 ]; then 
  cd /usr/local
  sh /vagrant/media/jdk-6u45-linux-x64.bin
fi

cp /vagrant/media/bashrc /root/.bashrc
sudo -u vagrant cp /vagrant/media/bashrc /home/vagrant/.bashrc

cp /vagrant/media/environment /etc/environment 
export JAVA_HOME=/usr/local/jdk1.6.0_45
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/opt/vagrant_ruby/bin:/usr/local/jdk1.6.0_45/bin

apt-get update -y
apt-get install hadoop-hdfs-namenode  hadoop-hdfs-datanode -y
mkdir -p /var/lib/hadoop-hdfs/cache/hdfs/dfs/name
cp /vagrant/media/core-site.xml /etc/hadoop/conf
cp /vagrant/media/hdfs-site.xml /etc/hadoop/conf
chown hdfs /var/lib/hadoop-hdfs/cache/hdfs/dfs/name
/etc/init.d/hadoop-hdfs-namenode restart
/etc/init.d/hadoop-hdfs-datanode restart
mkdir -p /mnt/var/lib/hadoop-hdfs/cache/hdfs/dfs/name
chown hdfs.hdfs /mnt/var/lib/hadoop-hdfs/cache/hdfs/dfs/name
mkdir -p /mnt/dfs 
chown hdfs.hdfs /mnt/dfs
echo "Formatting namenode"
/etc/init.d/hadoop-hdfs-namenode init
/etc/init.d/hadoop-hdfs-namenode restart
/etc/init.d/hadoop-hdfs-datanode restart
mkdir -p /mnt/staging
chown hdfs /mnt/staging


exit 0
