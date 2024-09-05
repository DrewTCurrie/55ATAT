#!/bin/bash


#List of required packages for the system to operate
#This is a list of constant packages for ease of updating throughout the script. 
MARIA="mariadb-server"
PIP="python3-pip"
PYTHON="python3"

#Check for new updates on github incase there is a change between 
#clone and install
echo "Pulling latest changes from github..."

git fetch
git pull

#Force system update to get most up-to-date packages
echo "Performing system update"
sudo apt update

#Check package function. Checks if the package is installed and if not installs it.i

checkPackage(){
	PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $@|grep "install ok installed")
}

#Check for MariaDB - Required for the data management backend. 
echo checking for checkPackage $MARIA
if [ $PKG_OK = "" ]; then
	echo "Mising $MARIA. Installing $MARIA."
	sudo apt-get --yes install $MARIA
	sudo mysql_secure_installation;
fi

#Check for python3 and python3-pip required for data management backend. 
#Pip will be used to automatically install the required packages and specific 
#version of the packages needed to run the python API

echo checking for $PYTHON: $PKG_OK
if [ "" = "$PKG_OK" ]; then
	echo "Missing $PYTHON. Installing $PYTHON."
	sudo apt-get --yes install python3
	sudo apt install python3 python3-pip
fi
