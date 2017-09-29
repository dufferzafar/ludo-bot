echo $1 # foldername code or demo1 or demo2

xterm -hold -title "Server" -l -lf "server_log.txt" -e "$1/server/server 10000" &
sleep 1

xterm -hold -title "Player0" -l -lf "player0_log.txt" -e "$1/client/client 0.0.0.0 10000 main.py" &
sleep 1

xterm -hold -title "Player1" -l -lf "player1_log.txt" -e "$1/client/client 0.0.0.0 10000 --noBoard main.py" &

echo "Press any key to kill all xterms"
read

# pkill -SIGINT -f "server/server"
pkill -SIGINT -f "client/client 0.0.0.0"
killall xterm
