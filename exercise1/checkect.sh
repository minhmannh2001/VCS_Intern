last_run_date=`date +'%Y%m%d%H%M'`

ls ./.tmp_checkect >> /dev/null 2>&1 

if [ $? -eq 2 ]
then
	touch .tmp_checkect
	echo $last_run_date > .tmp_checkect
	echo "Khong hien thi ket qua trong lan chay dau"
	echo "Khong hien thi ket qua trong lan chay dau" > /var/log/checketc.log
else
	last_run_date=`cat .tmp_checkect`
	echo "" > /var/log/checketc.log
fi

last_run_time_hour=`echo $last_run_date | cut -c 9-10`
last_run_time_minute=`echo $last_run_date | cut -c 11-12`
last_run_time_day=`echo $last_run_date | cut -c 7-8`
last_run_time_month=`echo $last_run_date | cut -c 5-6`
last_run_time_year=`echo $last_run_date | cut -c 1-4`
last_run_time=`echo $last_run_time_year-$last_run_time_month-$last_run_time_day $last_run_time_hour:$last_run_time_minute`
last_run_time=`date +'%s' -d "$last_run_time"`
echo Lan chay gan nhat: $last_run_time_hour:$last_run_time_minute $last_run_time_day/$last_run_time_month/$last_run_time_year
echo Lan chay gan nhat: $last_run_time_hour:$last_run_time_minute $last_run_time_day/$last_run_time_month/$last_run_time_year >> /var/log/checketc.log

touch .tmp_current_file_list_checkect
find /etc -type f > .tmp_current_file_list_checkect

touch -t $last_run_date .tmp_checkect
find /etc -type f -newer .tmp_checkect > .new_created_file_list

echo === Danh sach file tao moi ===
echo === Danh sach file tao moi === >> /var/log/checketc.log

terminal=`tty`
exec < .new_created_file_list

while read line
do
	birth_time=`stat $line | grep Birth | cut -d ' ' -f 3-4` 2> /dev/null
	birth_time=`echo $birth_time | cut -c 1-19`
	birth_time=`date +'%s' -d "$birth_time"`
	if [ $birth_time -ge $last_run_time ]
	then
		file $line | grep text >> /dev/null 2>&1
		if [ $? -eq 0 ]
		then
			echo $line
			echo Noi dung cua file:
			head -10 $line
			echo -----------------
			echo $line >> /var/log/checketc.log
			echo Noi dung cua file: >> /var/log/checketc.log
			head -10 $line >> /var/log/checketc.log
			echo ----------------- >> /var/log/checketc.log
		else
			echo $line
			echo $line >> /var/log/checketc.log
		fi
	fi
done

exec < $terminal

# Hien thi danh sach cac file duoc chinh sua ke tu lan chay truoc

echo === Danh sach file moi chinh sua ===
echo === Danh sach file moi chinh sua === >> /var/log/checketc.log

ls ./.tmp_last_file_list_checkect >> /dev/null 2>&1
if [ $? -eq 2 ]
then
	touch .tmp_last_file_list_checkect
fi

exec < .tmp_last_file_list_checkect

while read line
do
	last_change_time=`stat $line | grep Change | cut -d ' ' -f 2-3` 2> /dev/null
	last_change_time=`echo $last_change_time | cut -c 1-19`
	last_change_time=`date +'%s' -d "$last_change_time"`
	if [ $last_change_time -ge $last_run_time ]
	then
		echo $line
		echo $line  >> /var/log/checketc.log
	fi
done

exec < $terminal

# Kiem tra xem thu muc /etc co file nao bi xoa khong

last_files_number=`wc -l .tmp_last_file_list_checkect | cut -d ' ' -f1`
current_files_number=`wc -l .tmp_current_file_list_checkect | cut -d ' ' -f1`

echo === Danh sach file da bi xoa ===
echo === Danh sach file da bi xoa === >> /var/log/checketc.log

if [ $last_files_number -ne $current_files_number ]
then
	exec < .tmp_last_file_list_checkect

	while read line
	do
		grep $line .tmp_current_file_list_checkect > /dev/null 2>&1
		if [ $? -ne 0 ]
		then
			echo $line
			echo $line  >> /var/log/checketc.log
		fi
	done

	exec < $terminal
fi

# Gui mail thong bao cho quan tri vien
mail -s "/etc Dir Log" -a "/var/log/checketc.log" root@kali < /dev/null

find /etc -type f > .tmp_last_file_list_checkect
date +'%Y%m%d%H%M' > .tmp_checkect


