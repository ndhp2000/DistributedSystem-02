# Chuyên đề hệ thống phân tán
## Đồ Án 02 - Zacing Game

Xử lý đồng bộ trong game đa người chơi là một bài toán kỹ thuật khó, vì việc này đòi hỏi hệ thống phải có khả năng xử lý thời gian thực, hạn chế sự sai lệch thông tin game ở mỗi người chơi, xử lý các trường hợp đường truyền không ổn định và tốc độ thực thi không ổn định giữa các người chơi. Có nhiều giải pháp kỹ thuật để thiết kế game đa người chơi \cite{htpt}. Trong đồ án này, nhóm cài đặt một game đa người chơi thời gian thực dựa trên kiến trúc client-server và dựa vào bộ đếm frame để giải quyết vấn đề đồng bộ dữ liệu.

## Hướng dẫn:
Mở thư mục chứa project:
- `pip install -r requirements.txt`
- `python main.py`

Có thể điều chỉnh IP và PORT của client và server trong file config.py