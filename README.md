# Campus Event Management System

Hệ thống quản lý sự kiện campus đơn giản với kiến trúc modular, hỗ trợ đa vai trò người dùng và các tính năng quản lý sự kiện hoàn chỉnh.

## 🚀 Tính năng chính

### 🔐 Quản lý vai trò
- **Admin**: Toàn quyền quản lý hệ thống
- **Event Organizer**: Quản lý sự kiện được phân công
- **Student/Visitor**: Đăng ký và tham gia sự kiện

### 🎯 Tính năng Admin
- ✅ Tạo sự kiện mới
- ✅ Cập nhật thông tin sự kiện (6 trường dữ liệu)
- ✅ Xóa sự kiện (với xác nhận nhiều bước)
- ✅ Xem tổng quan tất cả sự kiện
- ✅ Thống kê và báo cáo toàn hệ thống
- ✅ Xuất báo cáo (Excel/WPS format)

### 🎪 Tính năng Event Organizer
- ✅ Quản lý sự kiện được phân công
- ✅ Theo dõi đăng ký chi tiết
- ✅ Xuất danh sách người tham dự
- ✅ Thống kê hiệu suất sự kiện cá nhân

### 🎓 Tính năng Student/Visitor
- ✅ Xem danh sách sự kiện
- ✅ Tìm kiếm và lọc sự kiện
- ✅ Đăng ký tham gia sự kiện
- ✅ Theo dõi lịch sử đăng ký

### 🔍 Tính năng tìm kiếm nâng cao
- 🔎 Tìm theo tên sự kiện
- 📍 Tìm theo địa điểm
- 📅 Tìm theo ngày/khoảng thời gian
- 👤 Tìm theo người tổ chức
- 📊 Lọc theo tình trạng đăng ký
- 🎯 Tìm kiếm đa tiêu chí

## 🏗️ Kiến trúc hệ thống

### 📁 Cấu trúc thư mục
```
campus-event-management/
├── main.py                 # File chính điều khiển
├── models.py              # Định nghĩa các class
├── sample_data.py         # Dữ liệu mẫu
├── file_manager.py        # Quản lý I/O file
├── event_operations.py    # Thao tác sự kiện
├── registration_manager.py # Quản lý đăng ký
├── menu_manager.py        # Giao diện menu
├── view_manager.py        # Hiển thị dữ liệu
├── statistics_manager.py  # Thống kê báo cáo
├── search_manager.py      # Tìm kiếm nâng cao
├── events.csv            # Dữ liệu sự kiện (auto-generated)
├── users.csv             # Dữ liệu người dùng (auto-generated)
└── README.md             # Tài liệu này
```

### 🧩 Modules chính
- **Main Controller**: Điều khiển luồng chính
- **Models**: User, Event classes với validation
- **Managers**: 6 manager xử lý logic nghiệp vụ
- **File Operations**: Xuất/nhập dữ liệu CSV
- **Sample Data**: Dữ liệu demo có sẵn

## 💻 Cài đặt và chạy

### Yêu cầu hệ thống
- Python 3.7+
- Không cần thư viện bên ngoài (chỉ dùng built-in)

### Cách chạy
```bash
# Clone repository
git clone https://github.com/yourusername/campus-event-management.git
cd campus-event-management

# Chạy chương trình
python main.py
```

### Khởi chạy nhanh
```bash
# Chạy với dữ liệu mẫu có sẵn
python main.py

# Hệ thống sẽ tự động tạo:
# - 9 users (1 Admin, 3 Organizers, 3 Students, 2 Visitors)
# - 4 events có sẵn
# - Sample registrations
```

## 🎮 Hướng dẫn sử dụng

### Bước 1: Chọn vai trò
```
1. Admin - Quản trị viên
2. Event Organizer - Người tổ chức sự kiện  
3. Student - Sinh viên
4. Visitor - Khách mời
```

### Bước 2: Sử dụng theo vai trò

#### 🔑 Admin Dashboard
```
1. Tạo sự kiện
2. Cập nhật sự kiện
3. Xóa sự kiện
4. Xem tất cả sự kiện
5. Xem tất cả người tham dự
6. Thống kê và báo cáo
7. Lưu dữ liệu
```

#### 🎪 Organizer Dashboard
```
1. Xem sự kiện của tôi
2. Quản lý đăng ký
3. Xem tất cả sự kiện
4. Thống kê sự kiện của tôi
```

#### 🎓 Student/Visitor Dashboard
```
1. Xem sự kiện
2. Đăng ký sự kiện
3. Xem sự kiện đã đăng ký
4. Tìm kiếm sự kiện
```

## 📊 Dữ liệu mẫu

### Users có sẵn
- **Admin**: Quản trị viên Hệ thống
- **Organizers**: 3 người tổ chức
- **Students**: 3 sinh viên
- **Visitors**: 2 khách mời

### Events có sẵn
1. **Hội thảo Công nghệ AI 2025** - 100 chỗ
2. **Workshop Lập trình Python** - 30 chỗ
3. **Ngày hội Khởi nghiệp 2025** - 200 chỗ
4. **Seminar Phát triển Nghề nghiệp** - 80 chỗ

## 🎯 Tính năng nổi bật

### 🔍 Tìm kiếm thông minh
- Tìm kiếm đa tiêu chí
- Lọc theo trạng thái đăng ký
- Tìm kiếm theo khoảng thời gian
- Xuất kết quả tìm kiếm

### 📈 Báo cáo và thống kê
- Thống kê tổng quan hệ thống
- Báo cáo theo vai trò người dùng
- Thống kê hiệu suất organizer
- Xuất báo cáo Excel/WPS format

### 🔒 Bảo mật và validation
- Phân quyền nghiêm ngặt
- Validation đầu vào toàn diện
- Xác nhận nhiều bước cho thao tác nguy hiểm
- Phân tích tác động trước khi xóa

### 💾 Quản lý dữ liệu
- Auto-save sau thay đổi quan trọng
- Xuất CSV tương thích Excel (UTF-8 BOM)
- Xuất CSV tương thích WPS (UTF-8 thuần)
- Backup và khôi phục dữ liệu

## 🛡️ Validation và bảo mật

### Validation đầu vào
```python
# Tên sự kiện tối thiểu 5 ký tự
# Ngày không được trong quá khứ
# Sức chứa phải là số nguyên dương
# Email phải đúng format
```

### Phân quyền
- **Admin**: Toàn quyền CRUD
- **Organizer**: Chỉ quản lý sự kiện được phân công
- **Student/Visitor**: Chỉ xem và đăng ký

### Confirmation workflows
- Xóa sự kiện: Multi-step confirmation
- Cập nhật sức chứa: Kiểm tra conflict
- Thay đổi ngày: Validation timeline

## 📋 API Classes

### Core Models
```python
class User:
    - user_id, username, full_name, email, role
    
class Event:
    - event_id, name, description, date, time
    - location, max_capacity, organizer_id, attendees
    - Validation methods
    - Update/Delete methods
```

### Managers
```python
EventOperations: create, update, delete events
RegistrationManager: handle registrations
MenuManager: user interface
ViewManager: display data
StatisticsManager: reports and analytics
SearchManager: advanced search
FileManager: CSV import/export
```

## 🔧 Customization

### Thêm vai trò mới
```python
# Trong models.py
class NewRole(User):
    def __init__(self, user_id, username, full_name, email):
        super().__init__(user_id, username, full_name, email, "NewRole")
```

### Thêm field cho Event
```python
# Trong models.py class Event
self.new_field = new_value

# Cập nhật validation và export methods
```

### Thêm tính năng tìm kiếm
```python
# Trong search_manager.py
def search_by_new_criteria(self):
    # Implementation
```

## 📊 Export formats

### CSV Reports
- **Excel format**: UTF-8 với BOM
- **WPS format**: UTF-8 thuần
- **Statistics**: Thống kê tổng quan
- **Attendee lists**: Danh sách chi tiết

### File outputs
```
statistics_Excel_YYYYMMDD_HHMMSS.csv
statistics_WPS_YYYYMMDD_HHMMSS.csv
attendee_details_YYYYMMDD_HHMMSS.csv
search_results_YYYYMMDD_HHMMSS.csv
```

## 🐛 Debug và troubleshooting

### Lỗi thường gặp
1. **Import Error**: Đảm bảo tất cả files trong cùng thư mục
2. **CSV Encoding**: Hệ thống tự động xử lý UTF-8
3. **Permission Error**: Kiểm tra phân quyền user
4. **Date Format**: Sử dụng YYYY-MM-DD


## 🔄 Updates và phiên bản

### v1.0.0 (Current)
- ✅ Core functionality hoàn chỉnh
- ✅ 4 vai trò người dùng
- ✅ 6 manager modules
- ✅ Advanced search
- ✅ Export functionality
- ✅ Validation system

### Planned features
- [ ] Database integration
- [ ] Web interface
- [ ] Email notifications
- [ ] Calendar integration
- [ ] Multi-language support

## 🤝 Contributing

### Contribution guidelines
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

### Code style
- Follow PEP 8
- Add docstrings
- Include validation
- Write tests

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết

## 🎉 Acknowledgments

- Python community
- Open source contributors
- Campus event management inspiration

---

⭐ **Star this repository if you find it useful!** ⭐

📝 **Found a bug or want to contribute? Open an issue or submit a PR!**

🚀 **Happy Event Managing!**
