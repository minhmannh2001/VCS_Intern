echo "[Thong tin he thong]"
echo "\nTen may: `hostname`"
echo "Phien ban he dieu hanh: `grep 'PRETTY_NAME' /etc/os-release | cut -d '=' -f 2 | cut -d '"' -f 2` `grep 'VERSION=' /etc/os-release | cut -d '=' -f 2 | cut -d '"' -f 2`"
echo "Thong tin CPU: `awk -F':' '/^model name/ {print $2}' /proc/cpuinfo | uniq | sed -e 's/^[ \t]*//'`"
echo "Kien truc he thong: \c"
kien_truc_he_thong=`uname -m`
if [ "$kien_truc_he_thong" = "x86_64" ]
then
    echo "64bit"    
else
    echo "32bit" # kien_truc_he_thong="i686" hoac "i386"
fi
current_dec=97
end_dec=122
stop_criteria=0
total_disk_volume=0
free_disk_volume=0
while [ $current_dec -le $end_dec ]
do
    extension=`echo "obase=16; $current_dec" | bc | xxd -p -r`
    current_dec=`expr $current_dec + 1`
    for i in 1 2 3 4 5 6 7 8 9 10
    do
        disk_name="sd$extension$i"
        result_size=`df --output=size /dev/$disk_name 2> /dev/null`
        result_avail=`df --output=avail /dev/$disk_name 2> /dev/null`
        if [ $? -eq 1 ]
        then
            stop_criteria=1
            break
        fi
        partition_volume=`echo $result_size | cut -d ' ' -f 2`
        free_partition_volume=`echo $result_avail | cut -d ' ' -f 2`
        total_disk_volume=`expr $total_disk_volume + $partition_volume`
        free_disk_volume=`expr $free_disk_volume + $free_partition_volume`
    done
    if [ $stop_criteria -eq 1 ]
    then
        break
    fi
done
total_disk_volume=`expr $total_disk_volume / 1024`
free_disk_volume=`expr $free_disk_volume / 1024`
echo 'Dung luong o dia cua he thong:' `echo $total_disk_volume` MB
echo 'Dung luong con trong cua he thong:' `echo $free_disk_volume` MB
echo 'Danh sach dia chi IP cua he thong:'
for interface in eth0 lo sit0 tun0 docker0
do
    result=`ip addr show $interface 2> /dev/null | grep 'inet '`
    if [ $? -eq 1 ]
    then
        continue
    fi
    ip_addr=`echo $result | grep 'inet ' | awk '{print $2}' | cut -d '/' -f 1`
    echo $interface: $ip_addr
done
echo 'Danh sach user tren he thong:'
min_normal_user_id=`awk '/^UID_MIN/ {print $2}' /etc/login.defs`
max_normal_user_id=`awk '/^UID_MAX/ {print $2}' /etc/login.defs`
terminal=`tty`
exec < "/etc/passwd"
first_time=1
while read line
do
    uid=`echo $line | cut -d : -f 3`
    username=`echo $line | cut -d : -f 1`
    if [ $uid -ge $min_normal_user_id -a $uid -le $max_normal_user_id ]
    then
        if [ $first_time -eq 1 ]
        then
            echo $username > ./.tmp_file
            first_time=0
        else
            echo $username >> ./.tmp_file
        fi
        
    fi
done
exec < $terminal
sort ./.tmp_file # In ra danh sach nguoi dung theo thu tu abc
echo "Danh sach cac tien trinh dang chay voi quyen root:"
ps u -U root -u root
total_number=`ps ux -U root -u root | wc -l`
total_number=`expr $total_number - 1`
echo So luong: $total_number tien trinh
echo "Cac port dang mo:"
total_number=`sudo netstat -tunlp | wc -l`
total_number=`expr $total_number - 2`
sudo netstat -tunlp
echo Tong cong co $total_number port dang mo tren he thong
echo "Cac thu muc tren he thong cho phep other co quyen ghi:"
sudo find / -type d -perm -o=w 2> /dev/null
echo "Danh sach cac goi phan mem duoc cai tren he thong:"
echo "Goi phan mem \t Phien ban"
sudo dpkg-query -f '${binary:Package}/${source:Version}\n' -W
sudo echo -e 

