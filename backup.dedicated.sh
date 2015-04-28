d=$(date +%d.%m.%y);

echo "Uploading..."
cd /usr/backup
find . -name "*${d}*" | xargs | xargs zip -0 -P password -r - | python /home/utils/pybackup/dedicated_backup.py upload_from_stdin > /home/utils/pybackup/upload_log 2>&1

echo "Cleaning up..."
python /home/utils/pybackup/dedicated_backup.py cleanup > /home/utils/pybackup/cleanup_log 2>&1

echo "Sending log..."
echo "[Files in package]" > /home/utils/pybackup/backup_log
find . -name "*${d}*" | xargs | xargs stat -c "%s %n (%y)" >> /home/utils/pybackup/backup_log

echo "" >> /home/utils/pybackup/backup_log
echo "[Upload]" >> /home/utils/pybackup/backup_log
cat /home/utils/pybackup/upload_log >> /home/utils/pybackup/backup_log

echo "" >> /home/utils/pybackup/backup_log
echo "[Cleanup]" >> /home/utils/pybackup/backup_log
cat /home/utils/pybackup/cleanup_log >> /home/utils/pybackup/backup_log
python /home/utils/pybackup/mailer.py /home/utils/pybackup/backup_log