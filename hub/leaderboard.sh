#!/bin/bash
echo -e "\033[0;32m\t\t\t\tLEADERBOARD\033[0m"

games=("tictactoe" "connect4" "othello")
for game in "${games[@]}"
do
	touch tmp.txt
	echo -e "\e[1m\t\t\t\t$game\e[0m"
	echo -e "\tPlayer\t\tWins\t\tLosses\t\tW/L ratio"
	while read -r line
	do
		name=$(echo $line | cut -d" " -f 1 -)
		wins=$(grep -wE "^$game,$name,.*$" history.csv | wc -l)
		losses=$(grep -wE "^$game,.*,$name$" history.csv | wc -l)
		total=$(($wins+$losses))
		if [[ $losses -ne 0 ]]; then
			wlratio=$(echo "scale = 2; $wins / $losses" | bc)
		elif [[ $wins -eq 0 ]]; then
			wlratio=0
		else
			wlratio=INF
		fi
		echo -e "$name\t\t$wins\t\t$losses\t\t$total\t\t$wlratio" >> tmp.txt
		x=$(($x+1))
	done < users.tsv
	if [[ $1 -eq 1 ]]; then
		cut -f 1,2,3,4,5,6,9 tmp.txt | sort -n -k2,2r -k3,3 | cat -n - | head -5
	elif [[ $1 -eq 2 ]]; then
		cut -f 1,2,3,4,5,6,9 tmp.txt | sort -n -k3,3r -k2,2 | cat -n - | head -5
	elif [[ $1 -eq 3 ]]; then
		touch out.txt
		cut -f 1,2,3,4,5,6,9 tmp.txt | grep -wE "^.*INF$" - | sort -nr -k2,2 - > out.txt
		cut -f 1,2,3,4,5,6,9 tmp.txt | grep -wvE "^.*INF$" - | sort -nr -k4,4 -k3,3 - >> out.txt
		cat -n out.txt | head -5
		rm -f out.txt
	else
		sort -nr -k4,4 -k2,2 tmp.txt | cut -f 1,2,3,4,5,6,9 - | cat -n - | head -5
	fi
	rm -f tmp.txt
done
