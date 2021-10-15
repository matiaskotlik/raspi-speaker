logfile=/home/pi/matias-speaker/spotify_events.log
reset=/home/pi/matias-speaker/reset.sh

while true; do
	sleep 60
	now=$(date +%s)
	last_event=$(</home/pi/.last_event)
	cutoff=$((now - 1200))
	if [[ $last_event < $cutoff ]]; then
		echo '[idle_watcher] [$(date)] resetting due to inactivity' >> $logfile
		. $reset
	fi
done
