d=$(date +%d.%m.%y);

echo "storage..."
cd /var/www/breezeme.su/storage
zip -r /usr/backup/storage/storage_"$d".zip * > /dev/null

echo "logs/bm..."
cd /var/www/logs
zip -r /usr/backup/logs/logs_bm_"$d".zip * > /dev/null

echo "logs/apache..."
cd /var/log/apache2
zip -r /usr/backup/logs/logs_apache_"$d".zip * > /dev/null

# servers=( "classic" "industrial" "hardcore" "creative" "technology" );
servers=( "servers here" )

for s in "${servers[@]}"
do
	cd /home/"$s"
	
	echo "$s/log..."
	mkdir /usr/backup/servers/"$s" &> /dev/null
	zip -r /usr/backup/servers/"$s"/"$s"_log_"$d".zip server.log > /dev/null
done
