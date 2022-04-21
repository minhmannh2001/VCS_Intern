# lay ra thoi gian chay script gan nhat, neu khong co, lay tat ca cac log
last_time=`cat .sshmonitor_last_xtime`
echo "Thoi gian chay script gan nhat: " $last_time
echo "Dang tien hanh phan tich..."
last_time=`date -d "$last_time" +%s`
# luu thoi gian khoi chay script
date +"%b %d %T" > .sshmonitor_last_xtime
# lay ra danh sach cac log cua tien trinh sshd
touch .ssh_acceptance_log
cat /var/log/auth.log | grep sshd -a | grep Accepted > .ssh_acceptance_log
# duyet qua danh sach cac log da luu, chi lay nhung log duoc ghi sau lan chay script truoc
terminal=`tty`
exec < .ssh_acceptance_log

# xoa file duoc tao ra o lan chay truoc
rm .filtered_ssh_acceptance_log 2> /dev/null
touch .filtered_ssh_acceptance_log

while read line
do
    log_time=`echo $line | awk '{print $1 " " $2 " " $3}'`
    log_time=`date -d "$log_time" +%s`
    if [ $log_time -ge $last_time ]
    then
        echo $line >> .filtered_ssh_acceptance_log
    fi
done

exec < $terminal

# Xoa cac phien dang nhap da ket thuc o lan chay script nay khoi file .living_ssh_sessions

ls .living_ssh_sessions >> /dev/null 2>&1
if [ $? -eq 2 ]
then
    touch .living_ssh_sessions > /dev/null 
    echo "Cac phien dang nhap hien dang duoc duy tri:" > .living_ssh_sessions
fi

exec < .living_ssh_sessions

while read line
do
    line_to_search=`echo $line | awk '{print $1 " " $3 " " $4 " " $5}'`
    cat /var/log/auth.log | grep sshd -a | grep Disconnected | grep "$line_to_search" >> /dev/null 2>&1
    if [ $? -eq 0 ]
    then
        line_number=`grep "$line" .living_ssh_sessions -n | awk -F : '{print $1}'`
        sed -i ${line_number}d .living_ssh_sessions
    fi
done

exec < $terminal

sed -i '/Cac phien dang nhap moi:/d' .living_ssh_sessions > /dev/null
echo "Cac phien dang nhap moi:" >> .living_ssh_sessions

# Luu phien dang nhap da duoc loc vao trong file .living_ssh_sessions
cat .filtered_ssh_acceptance_log | awk '{print $9 " " $10 " " $11 " " $12 " " $13 " - " $1 " " $2 " " $3}' >> .living_ssh_sessions

sudo cp .living_ssh_sessions /var/log/checketc.log

# gui mail cho quan tri vien root
# line_number=`grep "Cac phien dang nhap moi:" .living_ssh_sessions -n | awk -F : '{print $1}'`
# sed -i 1,${line_number}d .living_ssh_sessions

mail -s "New SSH Sessions Detection" -a ".living_ssh_sessions" root@kali < /dev/null > /dev/null

# rm .ssh_acceptance_log
# rm .filtered_ssh_acceptance_log
# rm .living_ssh_sessions

echo "Da chay xong."

