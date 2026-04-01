#!/bin/bash

setPwd() {
	while true
	do
		read -sp "Set your password: " pswd
		if $(validPwd "$pswd"); then
			continue
		fi
		pswd=$(echo "$pswd" | sha256sum | cut -d" " -f 1 -)
		echo >&2
		read -sp "Confirm your password: " cpwd
		cpwd=$(echo "$cpwd" | sha256sum | cut -d" " -f 1 -)
		echo >&2
		if [[ "$pswd" == "$cpwd" ]]; then
			echo -e "$1\t$pswd" >> users.tsv
			echo "Player $1 has been registered to the hub." >&2
			break
		else
			echo "Passwords did not match, please try again!" >&2
		fi
	done
}

checkPwd() {
	pswd=$(grep -w "$1" users.tsv | cut -f 2 -)
	while true
	do
		read -sp "Enter your password: " epwd
		epwd=$(echo "$epwd" | sha256sum | cut -d" " -f 1 -)
		echo >&2
		if [[ "$pswd" == "$epwd" ]]; then
			echo "Player $1 verified." >&2
			break
		else
			echo "Entered password is incorrect! please try again." >&2
		fi
	done
}

validUsr() {
	if [[ "$1" == "" ]]; then
		echo "Username field cannot be blank" >&2
		echo true
	elif [[ "$1" =~ [[:space:]] ]]; then
		echo "Username should not contain spaces or tabs." >&2
		echo true
	elif [[ $(echo "$1" | wc -m) -le 4 ]]; then
		echo "Username should contain atleast 4 characters" >&2
		echo true
	else
		echo false
	fi
}

validPwd() {
        if [[ "$1" == "" ]]; then
		echo >&2
                echo "Password field cannot be blank." >&2
                echo true
        elif [[ "$1" =~ [[:space:]] ]]; then
		echo >&2
                echo "Password should not contain spaces or tabs." >&2
                echo true
        elif [[ $(echo "$1" | wc -m) -le 4 ]]; then
		echo >&2
                echo "Password should contain atleast 4 characters." >&2
                echo true
	elif [[ ! $1 =~ [a-z] || ! $1 =~ [A-Z] ]]; then
		echo >&2
		echo "Password should contain both uppercase and lowercase letters." >&2
		echo true
	elif [[ ! $1 =~ [^a-zA-Z0-9] ]]; then
		echo >&2
		echo "Password must contain atleast one special character." >&2
		echo true
        else
                echo false
        fi
}

Login() {
	while true
	do
		read -p "Identify yourself Player $1: " usr
		if $(validUsr "$usr"); then
			continue
		elif [[ "$(grep -w "$usr" users.tsv)" == "" ]]; then
	        	read -p "Looks like this is your first time in the hub. Would you like to make a new account?[y/n]: " ans
			while [[ "$ans" != [nN] && "$ans" != [yY] ]]
			do
				read -p "Input must be 'y' or 'n': " ans
			done
			if [[ "$ans" == [yY] ]]; then
				setPwd "$usr"
				echo "$usr"
				break
			fi
		else
			checkPwd "$usr"
			echo "$usr"
			break
		fi
	done
}	


echo "Welcome to GameHub!"
player1=$(Login 1)
player2=$(Login 2)
echo "Get ready ..."
python3 ./game.py "$player1" "$player2"
