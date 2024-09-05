#!/bin/bash


#List of required packages for the system to operate
#This is a list of constant packages for ease of updating throughout the script. 
MARIA="mariadb-server"
MARIACONNCETOR="libmariadb3"
MARIADEV="libmariadb-dev"
PIP="python3-pip"
PYTHON="python3"
VENV="virtualenv"


#Check for new updates on github incase there is a change between 
#clone and install
printf "Pulling latest changes from github..."

git fetch
git pull

#Force system update to get most up-to-date packages
printf "Performing system update"
sudo apt update

#Check package function. Checks if the package is installed and if not installs it.i

checkPackage(){
	PACKAGE_TEST=$@
	PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $PACKAGE_TEST|grep "install ok installed")

	if [ "$PKG_OK" = "" ]; then 
		printf "Missing $PACKAGE_TEST. Installing $PACKAGE_TEST"
		sudo apt-get --yes install $PACKAGE_TEST
	fi
}

#Check for MariaDB - Required for the data management backend. 
printf "checking for checkPackage $MARIA"
checkPackage $MARIA

#This needs an additional check because MariaDB has an interactive installer
if [ "$PKG_OK" = "" ]; then
	sudo mysql_secure_installation;
fi

printf "Checking for $MARIA dependancies\n\r"
checkPackage $MARIACONNECTOR
checkPackage $MARIADEV

#Check for python3 and python3-pip required for data management backend. 
#Pip will be used to automatically install the required packages and specific 
#version of the packages needed to run the python API. Virtual env is needed 
#to create the python virtual envoirment for this device
printf "checking for $PYTHON\n\r"
checkPackage $PYTHON

printf "Checking for $PIP\n\r"
checkPackage $PIP

printf "Checking for $VENV\n\r"
checkPackage $VENV

printf "Creating venv\n\r"
virtualenv ../venv && source ../venv/bin/activate

printf "Success. Virtual enviroment created and activated\n\r"

pip install -r ../requirements.txt
