echo $1 # foldername code or demo1 or demo2
xterm -hold -title "Server" -e "$1/server/server 10000" &
sleep 1
xterm -hold -title "Player1" -e "$1/client/client 0.0.0.0 10000 main.py" &
sleep 1
xterm -hold -title "Player2" -e "$1/client/client 0.0.0.0 10000 main.py" &
echo "Press any key to kill all xterms"
read
killall xterm