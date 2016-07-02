apt-get -y install python
apt-get -y install mysql-server-5.5

MYSQL=`which mysql`
Q1="CREATE DATABASE IF NOT EXISTS eleicoesdb;"
Q2="GRANT ALL ON *.* TO 'root'@'localhost' IDENTIFIED BY '#F20e12R90#';"
Q3="FLUSH PRIVILEGES;"
SQL="${Q1}${Q2}${Q3}"
$MYSQL -uroot -p -e "$SQL"

apt-get -y install python-mysql
apt-get -y install python-pip
apt-get -y install python-pyside
apt-get -y install python-numpy
apt-get -y install python-scipy
apt-get -y install python-matplotlib
apt-get -y install ipython
apt-get -y install ipython-notebook
apt-get -y install python-pandas
apt-get -y install python-sympy
apt-get -y install python-nose
apt-get -y install python-zbar
apt-get -y install python-pil
apt-get -y install python-reportlab
apt-get -y install build-essential
apt-get -y install libssl-dev
apt-get -y install libffi-dev
apt-get -y install python-dev
apt-get -y install python-pyaudio
/usr/bin/yes | pip install pypng
/usr/bin/yes | pip install pyqrcode

echo "Tudo foi instalado corretamente"