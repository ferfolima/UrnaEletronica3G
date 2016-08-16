#!/bin/bash
for i in $( ls modules/*.deb); do
	sudo dpkg -i $i
done

for i in $( ls modules/*.gz); do
	tar -xzf $i --directory modules
	directory=${i%.tar.gz} 
	cd $directory
	sudo python setup.py install
	cd ..
	rm -rf $directory
done

for i in $( ls modules/*.zip); do
	unzip $i
	directory=${i%.zip}
	cd $directory
	sudo python setup.py install
	cd ..
	rm -rf $directory
done
