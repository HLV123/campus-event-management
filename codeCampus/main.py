# main.py - Simplified Campus Event Management System (Modular Architecture)

from file_manager import FileManager
from sample_data import initialize_sample_data
from event_operations import EventOperations
from registration_manager import RegistrationManager
from menu_manager import MenuManager
from view_manager import ViewManager
from statistics_manager import StatisticsManager
from search_manager import SearchManager

class SimpleCampusEventSystem:
    """Hệ thống quản lý sự kiện campus đơn giản - kiến trúc modular"""
    
    def __init__(self):
        # Core data
        self.users = {}
        self.events = {}
        self.current_role = None
        self.current_user = None
        
        # Managers
        self.file_manager = FileManager()
        
        # Initialize all operation managers
        self.event_ops = EventOperations(self)
        self.registration_mgr = RegistrationManager(self)
        self.menu_mgr = MenuManager(self)
        self.view_ops = ViewManager(self)
        self.stats_mgr = StatisticsManager(self)
        self.search_mgr = SearchManager(self)
        
        # Initialize sample data
        self.initialize_data()
    
    def initialize_data(self):
        """Khởi tạo dữ liệu với 4 sự kiện có sẵn"""
        print("CAMPUS EVENT MANAGEMENT SYSTEM")
        
        self.users, self.events = initialize_sample_data()
    
    # ====================== MAIN SYSTEM CONTROL ======================
    
    def run(self):
        """Chạy hệ thống chính"""
        try:
            while True:
                role = self.menu_mgr.select_role()
                
                if role == "Exit":
                    break
                elif role == "Admin":
                    self.menu_mgr.admin_menu()
                elif role == "EventOrganizer":
                    self.menu_mgr.organizer_menu()
                elif role in ["Student", "Visitor"]:
                    self.menu_mgr.student_visitor_menu()
                
                # Reset sau khi thoát khỏi menu
                self.current_role = None
                self.current_user = None
                
            print("\nCảm ơn bạn đã sử dụng hệ thống!")
            
        except KeyboardInterrupt:
            print("\n\nThoát hệ thống")
        except Exception as e:
            print(f"\nLỗi hệ thống: {e}")
        finally:
            # Lưu dữ liệu cuối cùng
            self.save_data()
    
    # ====================== DATA OPERATIONS ======================
    
    def save_data(self):
        """Lưu dữ liệu ra file"""
        try:
            success = self.file_manager.save_all_data(self.users, self.events)
            if success:
                print("Đã lưu tất cả dữ liệu")
            else:
                print("Có lỗi khi lưu dữ liệu")
            return success
        except Exception as e:
            print(f"Lỗi lưu dữ liệu: {e}")
            return False
    
    def load_data(self):
        """Load dữ liệu từ file (tính năng tương lai)"""
        # Có thể implement sau để load từ CSV
        pass
    
    def backup_data(self):
        """Backup dữ liệu (tính năng tương lai)"""
        # Có thể implement sau
        pass
    
    # ====================== UTILITY METHODS ======================
    
    def get_system_stats(self):
        """Lấy thống kê hệ thống nhanh"""
        return {
            'total_users': len(self.users),
            'total_events': len(self.events),
            'total_registrations': sum(len(e.attendees) for e in self.events.values()),
            'user_roles': {role: sum(1 for u in self.users.values() if u.role == role) 
                          for role in ['Admin', 'EventOrganizer', 'Student', 'Visitor']}
        }
    
    def validate_system_data(self):
        """Kiểm tra tính toàn vẹn dữ liệu"""
        issues = []
        
        # Kiểm tra events có organizer hợp lệ
        for event in self.events.values():
            if event.organizer_id not in self.users:
                issues.append(f"Event {event.event_id} có organizer_id không tồn tại")
        
        # Kiểm tra attendees có tồn tại
        for event in self.events.values():
            for attendee_id in event.attendees:
                if attendee_id not in self.users:
                    issues.append(f"Event {event.event_id} có attendee không tồn tại: {attendee_id}")
        
        return issues
    
    def show_system_architecture(self):
        """Hiển thị kiến trúc hệ thống"""
        print("\nKIẾN TRÚC HỆ THỐNG")
        print("="*40)
        print("main.py - File chính điều khiển")
        print("models.py - Định nghĩa các class")
        print("file_manager.py - Quản lý file I/O")
        print("sample_data.py - Dữ liệu mẫu")
        print("event_operations.py - Thao tác sự kiện")
        print("registration_manager.py - Quản lý đăng ký")
        print("menu_manager.py - Giao diện menu")
        print("view_manager.py - Hiển thị dữ liệu")
        print("statistics_manager.py - Thống kê báo cáo")
        print("search_manager.py - Tìm kiếm lọc")
        
        print(f"\nMANAGERS ĐƯỢC KHỞI TẠO:")
        print(f"   EventOperations - Tạo/Sửa/Xóa sự kiện")
        print(f"   RegistrationManager - Đăng ký tham dự")
        print(f"   MenuManager - Giao diện menu")
        print(f"   ViewManager - Hiển thị dữ liệu")
        print(f"   StatisticsManager - Báo cáo thống kê")
        print(f"   SearchManager - Tìm kiếm nâng cao")
        
        print(f"\nTHỐNG KÊ HIỆN TẠI:")
        stats = self.get_system_stats()
        print(f"   Users: {stats['total_users']}")
        print(f"   Events: {stats['total_events']}")
        print(f"   Registrations: {stats['total_registrations']}")
        
        # Kiểm tra tính toàn vẹn
        issues = self.validate_system_data()
        if issues:
            print(f"\nVẤN ĐỀ DỮ LIỆU:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"\nDữ liệu toàn vẹn")
        
        input("\nNhấn Enter để tiếp tục...")
    
    def show_feature_overview(self):
        """Hiển thị tổng quan tính năng"""
        print("\nTỔNG QUAN TÍNH NĂNG")
        print("="*40)
        
        print("ADMIN:")
        print("   - Tạo sự kiện mới")
        print("   - Cập nhật sự kiện (6 fields)")
        print("   - Xóa sự kiện (với confirmation)")
        print("   - Xem tất cả sự kiện & người tham dự")
        print("   - Thống kê tổng quan hệ thống")
        print("   - Xuất báo cáo (Excel/WPS format)")
        
        print("\nEVENT ORGANIZER:")
        print("   - Xem sự kiện được phân công")
        print("   - Quản lý đăng ký chi tiết")
        print("   - Xuất danh sách người tham dự")
        print("   - Thống kê sự kiện cá nhân")
        print("   - Xem thông tin chi tiết attendees")
        
        print("\nSTUDENT/VISITOR:")
        print("   - Xem danh sách sự kiện")
        print("   - Tìm kiếm & lọc sự kiện")
        print("   - Đăng ký tham gia")
        print("   - Xem lịch sử đăng ký")
        print("   - Tìm kiếm nâng cao")
        
        print("\nTÍNH NĂNG TÌM KIẾM:")
        print("   - Tìm theo tên sự kiện")
        print("   - Tìm theo địa điểm")
        print("   - Tìm theo ngày/khoảng thời gian")
        print("   - Tìm theo organizer")
        print("   - Lọc theo tình trạng đăng ký")
        print("   - Tìm kiếm nâng cao (nhiều tiêu chí)")
        
        print("\nBÁO CÁO & THỐNG KÊ:")
        print("   - Thống kê tổng quan")
        print("   - Thống kê theo vai trò")
        print("   - Thống kê theo organizer")
        print("   - Báo cáo chi tiết attendees")
        print("   - Export CSV (UTF-8 + BOM cho Excel)")
        print("   - Export CSV (UTF-8 thuần cho WPS)")
        
        print("\nTÍNH NĂNG NÂNG CAO:")
        print("   - Validation nghiêm ngặt input")
        print("   - Multi-step confirmation cho delete")
        print("   - Impact analysis trước khi xóa")
        print("   - Auto-save sau thay đổi quan trọng")
        print("   - Calendar view (7 ngày tới)")
        print("   - Compact & detailed display modes")
        
        input("\nNhấn Enter để tiếp tục...")

# ====================== MAIN PROGRAM ======================

def main():
    """Entry point của chương trình"""
    try:
        print("Khởi động Campus Event Management System...")
        print("Loading các modules...")
        
        system = SimpleCampusEventSystem()
        
        print("Hệ thống đã sẵn sàng!")
        print("Kiến trúc: 8 modules, 6 managers")
        
        # Hiển thị tổng quan nhanh
        stats = system.get_system_stats()
        print(f"Dữ liệu: {stats['total_events']} events, {stats['total_users']} users, {stats['total_registrations']} registrations")
        
        print("\n" + "="*60)
        
        system.run()
        
    except ImportError as e:
        print(f"Lỗi import module: {e}")
        print("Đảm bảo tất cả files .py đều có trong cùng thư mục")
    except Exception as e:
        print(f"Lỗi khởi tạo hệ thống: {e}")

if __name__ == "__main__":
    main()