sudo apt-get install apparmor apparmor-profiles apparmor-utils
sudo aa-complain cupsd
sudo apt-get install cups csh
sudo mkdir -p /usr/share/cups/model
sudo ln -s /etc/init.d/cups /etc/init.d/lpd
sudo mkdir -p /var/spool/lpd
sudo apt-get install sane-utils
sudo apt-get install psutils
sudo apt-get install lib32stdc++6
sudo dpkg -i --force-all ql700lpr-1.0.2-0.i386.deb
sudo dpkg -i --force-all ql700cupswrapper-1.0.2-0.i386.deb

echo 
echo "Rebootar para startar corretamente o cups e suas configuracoes, acessar a interface web do cups via localhost:631 em algum browser (usuario ufabc / senha ufabc - se nao rebootou nao aceitara a senha!)  e selecionar BROTHER em impressora local no MODIFY PRINTER... apenas /dev/usb/lp0 nao funciona!  Outra tarefa imoportante eh ajustar o tipo do papel (em Set Default Options), no caso, a largura correta da etiqueta, 62mm caso contrarioi, nada imprime."
