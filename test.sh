for i in "$@"
do
case $i in
    -r|--restart)
    RESTART="1"
    ;;

    -s=*|--searchpath=*)
    SEARCHPATH="${i#*=}"
    ;;

    -l=*|--lib=*)
    DIR="${i#*=}"
    ;;

    --default)
    DEFAULT=YES
    ;;

    *)
    ;;
esac
done


declare -a scripts=("420bits-service.py" "420bits-webserver.py")
for script in "${scripts[@]}"
do
   echo "$script"
   	if [ "$RESTART" == "1" ]; then
   		PID=`ps -eaf | grep $script | grep -v grep | awk '{print $2}'`
		if [[ "" !=  "$PID" ]]; then
		  echo "killing $PID"
		  kill -9 $PID
		fi
   	fi

	if (( $(ps -aux | grep -v grep | grep "$script" | wc -l) > 0 ))
	then
	echo "$script is already running"
	else
	echo "Will start $script"
	/usr/bin/python "/home/pi/420bits/local-sever/$script" > "/home/pi/420bits/logs/$script.log" 2>&1 &
	echo "Did start $script --"
	fi
done