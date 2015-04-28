d=$(date +%d.%m.%y);

echo "site..."
cd /var/www/breezeme.su
zip -r -y /usr/backup/site/site_"$d".zip * -x storage/\* \*.rar client/dl/\* > /dev/null

echo "mysql..."
cd /var/lib/mysql
zip -r /usr/backup/mysql/mysql_"$d".zip *

echo "utils..."
cd /home/utils
zip -r /usr/backup/utils/utils_"$d".zip * -x client/current/\* client/development/\* client/archive/\* > /dev/null

# servers=( "classic" "industrial" "hardcore" "creative" "technology")
servers=( "servers here" )
worlds=("world" "world_nether" "wcustom")
backups=("3d" "7d" "14d" "30d")

for s in "${servers[@]}"
do
	cd /home/"$s"
	
	mkdir /usr/backup/servers/"$s" &> /dev/null
	
	for fw in "${worlds[@]}"
	do	
		if [ "$fw" = "wcustom" ]
		then
			if [ "$s" = "creative" ]
			then 
				w="world_flat"
			else 
				w="world_the_end"
			fi
		else
			w="$fw"
		fi
		
		echo "$s/$w..."
		mkdir /usr/backup/servers/"$s"/"$w" &> /dev/null
		zip -r -y /usr/backup/servers/"$s"/"$w"/"$w"_"$s"_"$d".zip "$w" > /dev/null

		#rm we_backup/"$w"/lastbackup.zip &> /dev/null
		echo "copying $s/$w/lastbackup..."
		cp /usr/backup/servers/"$s"/"$w"/"$w"_"$s"_"$d".zip we_backup/"$w"/lastbackup.zip
				
		if [ "$s" = "technology" ]
		then
			zip --delete we_backup/"$w"/lastbackup.zip "world/DIM-1*"
		fi
		touch -d '2010-01-02 00:00:00' we_backup/"$w"/lastbackup.zip
		
		for bck in "${backups[@]}"
		do
			param="date +%d.%m.%y --date=-${bck}ay";
			td=`$param`
			echo "copying $s/$w/lastbackup/$bck..."
			cp /usr/backup/servers/"$s"/"$w"/"$w"_"$s"_"$td".zip we_backup/"$w"/lastbackup_"$bck".zip
			if [ "$s" = "technology" ]
			then
				zip --delete we_backup/"$w"/lastbackup_"$bck".zip "world/DIM-1*"
			fi
			touch -d '2010-01-01 00:00:00' we_backup/"$w"/lastbackup_"$bck".zip
		done		
	done
	
	echo "$s/core..."
	zip -r /usr/backup/servers/"$s"/"$s"_core_"$d".zip * -x \*.zip world\* DIM\* server.log recycler.log interacts.log > /dev/null
	
   echo "done $s"
done
