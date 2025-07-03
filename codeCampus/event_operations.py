# event_operations.py - Quản lý các thao tác sự kiện

from models import Event
from datetime import datetime
import uuid

class EventOperations:
    """Class quản lý các thao tác với sự kiện"""
    
    def __init__(self, system):
        self.system = system
    
    def generate_id(self):
        """Tạo ID ngẫu nhiên"""
        return str(uuid.uuid4())[:8]
    
    # ====================== EVENT MANAGEMENT ======================
    
    def create_event(self):
        """Tạo sự kiện mới - CHỈ ADMIN"""
        if self.system.current_role != "Admin":
            print("Chỉ Admin mới có quyền tạo sự kiện")
            return
        
        print("\n=== TẠO SỰ KIỆN MỚI ===")
        try:
            name = input("Tên sự kiện: ").strip()
            description = input("Mô tả: ").strip()
            date_str = input("Ngày (YYYY-MM-DD): ").strip()
            time_str = input("Giờ (HH:MM): ").strip()
            location = input("Địa điểm: ").strip()
            max_capacity = input("Sức chứa tối đa: ").strip()
            
            # Parse date và time
            event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            event_time = datetime.strptime(time_str, "%H:%M").time()
            
            # Tạo event
            event_id = self.generate_id()
            event = Event(
                event_id=event_id,
                name=name,
                description=description,
                date=event_date,
                time=event_time,
                location=location,
                max_capacity=max_capacity,
                organizer_id=self.system.current_user.user_id
            )
            
            self.system.events[event_id] = event
            print(f"Tạo sự kiện thành công: {name} (ID: {event_id})")
            
        except ValueError as e:
            print(f"Lỗi: {e}")
        except Exception as e:
            print(f"Lỗi không xác định: {e}")
    
    def update_event(self):
        """Cập nhật sự kiện - CHỈ ADMIN"""
        if self.system.current_role != "Admin":
            print("Chỉ Admin mới có quyền cập nhật sự kiện")
            return
        
        if not self.system.events:
            print("Không có sự kiện nào để cập nhật")
            return
        
        print("\n=== CẬP NHẬT SỰ KIỆN ===")
        print(f"{'ID':<8} {'Tên sự kiện':<30} {'Ngày':<12} {'Attendees':<10}")
        print("-" * 70)
        
        for event in self.system.events.values():
            attendance = f"{len(event.attendees)}/{event.max_capacity}"
            print(f"{event.event_id:<8} {event.name[:29]:<30} {event.date:<12} {attendance:<10}")
        
        # Chọn event để update
        event_id = input("\nNhập ID sự kiện cần cập nhật: ").strip()
        
        if event_id not in self.system.events:
            print("Không tìm thấy sự kiện")
            return
        
        event = self.system.events[event_id]
        
        # Hiển thị thông tin hiện tại
        print(f"\n=== THÔNG TIN HIỆN TẠI: {event.name} ===")
        print(f"1. Tên: {event.name}")
        print(f"2. Mô tả: {event.description}")
        print(f"3. Ngày: {event.date}")
        print(f"4. Giờ: {event.time}")
        print(f"5. Địa điểm: {event.location}")
        print(f"6. Sức chứa: {event.max_capacity} (hiện có {len(event.attendees)} người)")
        print("0. Hủy cập nhật")
        
        while True:
            try:
                choice = input("\nChọn thông tin cần cập nhật (0-6): ").strip()
                
                if choice == '0':
                    print("Hủy cập nhật")
                    return
                elif choice == '1':
                    self._update_event_name(event)
                elif choice == '2':
                    self._update_event_description(event)
                elif choice == '3':
                    self._update_event_date(event)
                elif choice == '4':
                    self._update_event_time(event)
                elif choice == '5':
                    self._update_event_location(event)
                elif choice == '6':
                    self._update_event_capacity(event)
                else:
                    print("Lựa chọn không hợp lệ")
                    continue
                
                # Hỏi có muốn tiếp tục update không
                continue_update = input("\nCập nhật thêm thông tin khác? (y/n): ").lower()
                if continue_update != 'y':
                    break
                    
            except ValueError as e:
                print(f"Lỗi: {e}")
            except Exception as e:
                print(f"Lỗi không xác định: {e}")
        
        print(f"Cập nhật sự kiện '{event.name}' thành công!")
    
    def delete_event(self):
        """Xóa sự kiện - CHỈ ADMIN"""
        if self.system.current_role != "Admin":
            print("Chỉ Admin mới có quyền xóa sự kiện")
            return
        
        if not self.system.events:
            print("Không có sự kiện nào để xóa")
            return
        
        print("\n=== XÓA SỰ KIỆN ===")
        print(f"{'ID':<8} {'Tên sự kiện':<30} {'Ngày':<12} {'Attendees':<10}")
        print("-" * 70)
        
        for event in self.system.events.values():
            attendance = f"{len(event.attendees)}/{event.max_capacity}"
            print(f"{event.event_id:<8} {event.name[:29]:<30} {event.date:<12} {attendance:<10}")
        
        # Chọn event để xóa
        event_id = input("\nNhập ID sự kiện cần xóa: ").strip()
        
        if event_id not in self.system.events:
            print("Không tìm thấy sự kiện")
            return
        
        event = self.system.events[event_id]
        
        # Phân tích impact của việc xóa
        impact = event.get_deletion_impact()
        
        print(f"\n=== PHÂN TÍCH TÁC ĐỘNG XÓA SỰ KIỆN ===")
        print(f"Sự kiện: {impact['event_name']}")
        print(f"Ngày: {impact['event_date']}")
        print(f"Số người đã đăng ký: {impact['attendees_count']}")
        
        if impact['warnings']:
            print("\nCẢNH BÁO:")
            for warning in impact['warnings']:
                print(f"   - {warning}")
        
        # Hiển thị danh sách attendees sẽ bị ảnh hưởng
        if impact['attendees_count'] > 0:
            print(f"\nDANH SÁCH NGƯỜI SẼ BỊ HỦY ĐĂNG KÝ:")
            for i, user_id in enumerate(impact['attendees_list'], 1):
                if user_id in self.system.users:
                    attendee = self.system.users[user_id]
                    print(f"   {i}. {attendee.full_name} ({attendee.email})")
                else:
                    print(f"   {i}. Unknown User (ID: {user_id})")
        
        # Confirmation với multiple steps
        print(f"\nXÁC NHẬN XÓA SỰ KIỆN")
        print(f"Bạn có chắc chắn muốn xóa sự kiện '{event.name}'?")
        
        # Step 1: Basic confirmation
        confirm1 = input("Nhập 'YES' để xác nhận: ").strip()
        if confirm1 != 'YES':
            print("Hủy xóa sự kiện")
            return
        
        # Step 2: Type event name for final confirmation
        if impact['attendees_count'] > 0:
            print(f"\nCẢNH BÁO CUỐI CÙNG:")
            print(f"Hành động này sẽ hủy đăng ký cho {impact['attendees_count']} người!")
            confirm2 = input(f"Nhập tên sự kiện '{event.name}' để xác nhận: ").strip()
            if confirm2 != event.name:
                print("Tên sự kiện không khớp. Hủy xóa")
                return
        
        # Thực hiện xóa
        try:
            print("\nĐang xóa sự kiện...")
            
            # Chuẩn bị xóa và lấy danh sách attendees bị ảnh hưởng
            removed_attendees = event.prepare_for_deletion()
            
            # Xóa event khỏi dictionary
            event_name = event.name
            del self.system.events[event_id]
            
            print(f"Đã xóa sự kiện '{event_name}' thành công!")
            
            if removed_attendees:
                print(f"Đã hủy đăng ký cho {len(removed_attendees)} người")
                print("Khuyến nghị: Thông báo cho những người đã đăng ký về việc hủy sự kiện")
            
            # Tự động lưu dữ liệu sau khi xóa
            print("Đang lưu dữ liệu...")
            self.system.save_data()
            
        except Exception as e:
            print(f"Lỗi khi xóa sự kiện: {e}")
            print("Sự kiện vẫn còn trong hệ thống")
    
    # ====================== HELPER METHODS ======================
    
    def _update_event_name(self, event):
        """Update tên sự kiện"""
        current_name = event.name
        new_name = input(f"Tên mới (hiện tại: {current_name}): ").strip()
        
        if not new_name:
            print("Hủy cập nhật tên")
            return
        
        if new_name == current_name:
            print("Tên không thay đổi")
            return
        
        event.update_field("name", new_name)
        print(f"Đã cập nhật tên: {current_name} → {new_name}")
    
    def _update_event_description(self, event):
        """Update mô tả sự kiện"""
        current_desc = event.description
        print(f"Mô tả hiện tại: {current_desc}")
        new_desc = input("Mô tả mới: ").strip()
        
        if not new_desc:
            print("Hủy cập nhật mô tả")
            return
        
        if new_desc == current_desc:
            print("Mô tả không thay đổi")
            return
        
        event.update_field("description", new_desc)
        print("Đã cập nhật mô tả")
    
    def _update_event_date(self, event):
        """Update ngày sự kiện"""
        current_date = event.date
        new_date_str = input(f"Ngày mới (YYYY-MM-DD, hiện tại: {current_date}): ").strip()
        
        if not new_date_str:
            print("Hủy cập nhật ngày")
            return
        
        event.update_field("date", new_date_str)
        print(f"Đã cập nhật ngày: {current_date} → {event.date}")
    
    def _update_event_time(self, event):
        """Update giờ sự kiện"""
        current_time = event.time
        new_time_str = input(f"Giờ mới (HH:MM, hiện tại: {current_time}): ").strip()
        
        if not new_time_str:
            print("Hủy cập nhật giờ")
            return
        
        event.update_field("time", new_time_str)
        print(f"Đã cập nhật giờ: {current_time} → {event.time}")
    
    def _update_event_location(self, event):
        """Update địa điểm sự kiện"""
        current_location = event.location
        new_location = input(f"Địa điểm mới (hiện tại: {current_location}): ").strip()
        
        if not new_location:
            print("Hủy cập nhật địa điểm")
            return
        
        if new_location == current_location:
            print("Địa điểm không thay đổi")
            return
        
        event.update_field("location", new_location)
        print(f"Đã cập nhật địa điểm: {current_location} → {new_location}")
    
    def _update_event_capacity(self, event):
        """Update sức chứa sự kiện"""
        current_capacity = event.max_capacity
        current_attendees = len(event.attendees)
        
        print(f"Sức chứa hiện tại: {current_capacity}")
        print(f"Đã đăng ký: {current_attendees} người")
        print(f"Sức chứa tối thiểu: {current_attendees}")
        
        new_capacity_str = input(f"Sức chứa mới (>={current_attendees}): ").strip()
        
        if not new_capacity_str:
            print("Hủy cập nhật sức chứa")
            return
        
        try:
            new_capacity = int(new_capacity_str)
            if new_capacity == current_capacity:
                print("Sức chứa không thay đổi")
                return
            
            event.update_field("max_capacity", new_capacity)
            print(f"Đã cập nhật sức chứa: {current_capacity} → {new_capacity}")
            
            # Hiển thị thông tin sau update
            available_spots = new_capacity - current_attendees
            print(f"Còn lại: {available_spots} chỗ trống")
            
        except ValueError:
            print("Sức chứa phải là số nguyên")