#!/bin/bash

setPwd() {
	while true
	do
		read -rsp "Set your password: " pswd
		if $(validPwd "$pswd"); then
			continue
		fi
		pswd=$(echo "$pswd" | sha256sum | cut -d" " -f 1 -)
		echo >&2
		read -rsp "Confirm your password: " cpwd
		cpwd=$(echo "$cpwd" | sha256sum | cut -d" " -f 1 -)
		echo >&2
		
		if [[ "$pswd" == "$cpwd" ]]; then
			echo -e "$1\t$pswd" >> users.tsv
			echo -e "\033[0;32mPlayer $1 has been registered to the hub.\033[0m" >&2
			break
		else
			echo $'\033[0;31mPasswords did not match, please try again!\033[0m' >&2
		fi
	done
}

validUsr() {
        if [[ "$1" == "" ]]; then
                echo $'\033[0;31mUsername field cannot be blank\033[0m' >&2
                echo true
        elif [[ "$1" =~ [[:space:]] ]]; then
                echo $'\033[0;31mUsername should not contain spaces or tabs.\033[0m' >&2
                echo true
        elif [[ $(echo "$1" | wc -m) -le 4 ]]; then
                echo $'\033[0;31mUsername should contain atleast 4 characters\033[0m' >&2
                echo true
        else
                echo false
        fi
}

setUsr() {
        read -rp "What would you like to be called?: " name
        while true
        do
		if $(validUsr "$name"); then
                        read -rp "Enter a valid username: " name
                        continue
		elif [[ ! $(grep -w $name users.tsv) == "" ]]; then
                        read -rp $'\033[0;31mUsername is already taken, please try again: \033[0m' name
                        continue
                fi
		break
        done
        setPwd $name
	echo $name
}

checkPwd() {
	pswd=$(grep -w "$1" users.tsv | cut -f 2 -)
	while true
	do
		read -rsp "Enter your password: " epwd
		epwd=$(echo "$epwd" | sha256sum | cut -d" " -f 1 -)
		echo >&2
		if [[ "$pswd" == "$epwd" ]]; then
			echo -e "\033[0;32mPlayer $1 has entered the Hub.\033[0m" >&2
			break
		else
			echo $'\033[0;31mEntered password is incorrect! please try again.\033[0m' >&2
		fi
	done
}

validPwd() {
        if [[ "$1" == "" ]]; then
		echo >&2
                echo $'\033[0;31mPassword field cannot be blank.\033[0m' >&2
                echo true
        elif [[ "$1" =~ [[:space:]] ]]; then
		echo >&2
                echo $'\033[0;31mPassword should not contain spaces or tabs.\033[0m' >&2
                echo true
        elif [[ $(echo "$1" | wc -m) -le 4 ]]; then
		echo >&2
                echo $'\033[0;31mPassword should contain atleast 4 characters.\033[0m' >&2
                echo true
	elif [[ ! $1 =~ [a-z] || ! $1 =~ [A-Z] ]]; then
		echo >&2
		echo $'\033[0;31mPassword should contain both uppercase and lowercase letters.\033[0m' >&2
		echo true
	elif [[ ! $1 =~ [0-9] ]]; then
		echo >&2
		echo $'\033[0;31mPassword should contain atleast one number.\033[0m' >&2
		echo true		
	elif [[ ! $1 =~ [^a-zA-Z0-9] ]]; then
		echo >&2
		echo $'\033[0;31mPassword must contain atleast one special character.\033[0m' >&2
		echo true
        else
                echo false
        fi
}

Login() {
	read -rp "Is this your first time in the Hub Player $1?[y/n]: " reply
	while [[ ! $reply =~ ^[yYnN]$ ]]; do
		read -rp $'\033[0;31mInput must be "y" or "n": \033[0m' reply
	done
	if [[ $reply =~ ^[yY]$ ]]; then
		echo $(setUsr)
	else
		read -rp "Identify yourself player $1: " usr
		while [[ $(grep -w "$usr" users.tsv) == "" ]]
		do
			read -rp $'\033[0;31mNo such player exists. Please try again: \033[0m' usr
		done
		checkPwd "$usr"
		echo $usr
	fi	
}	


echo "Welcome to The GameHub!"
player1=$(Login 1)
player2=$(Login 2)
echo "Get ready ..."
python3 ./game.py "$player1" "$player2"
