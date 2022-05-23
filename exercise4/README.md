## Yêu cầu

Viết các chương trình thực hiện các chức năng GET, POST, download, upload lên
trang wordpress sau: [http://blogtest.vnprogramming.com/](http://blogtest.vnprogramming.com/), tài khoản test, mật khẩu test123QWE@AD. Lập
trình bằng raw socket (không sử dụng thư viện http có sẵn, có thể dùng bất kì
ngôn ngữ lập trình nào, recommend **python**).\

1. Thực hiện GET trang chủ và in ra title của trang.\
Tên chương trình: httpget\
Ví dụ:\
httpget --url http://45.32.110.240/\
Ouput:\
Title: anhtudsvk4
2. Thực hiện POST vào trang đăng nhập để đăng nhập vào
một tài khoản. In ra đăng nhập thành công hay thất bại.\
Tên chương trình: httppost\
Ví dụ:\
httppost --url http://45.32.110.240/ --user test --password test123QWE@AD\
Output:\
User test đăng nhập thành công\
Hoặc User test đăng nhập thất bại
3. Thực hiện upload một file ảnh lên Media Library. In ra
đường dẫn file được upload.\
Tên chương trình: httpupload\
Ví dụ:\
httpupload --url http://45.32.110.240/ --user test --password test123QWE@AD --local-file
/home/ubuntu/test.png\
Output:\
Upload success.\
File upload url: https://45.32.110.240/wp-content/uploads/2020/09/test.png\
Hoặc Upload failed.
4. Thực hiện GET để download một file ảnh trên máy chủ, hiển thị kích thước của file ảnh download được.\
Tên chương trình: httpdownload\
Ví dụ:
httpdownload --url http://45.32.110.240/ --remote-file /wp-content/uploads/2020/09/test.png\
Output:\
Kích thước file ảnh: 14574 bytes\
Hoặc Không tồn tại file ảnh

## Giới thiệu
Chương trình được viết bằng ngôn ngữ **python**, sử dụng module **socket**

Gồm 4 chương trình:
 - httpget.py
 - httppost.py
 - httpupload.py
 - httpdownload.py

Để các chương trình hoạt động hợp lý, nên tham khảo danh sách các tham số của chương trình thông qua tham số **-h**.

```
python example.py -h
```
Trong thư mục /videos có chứa các video demo hướng dẫn sử dụng tương ứng
