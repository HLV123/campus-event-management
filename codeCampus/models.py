# models.py - Simplified Models (No password required) - Updated with validation methods

from datetime import datetime

class User:
    """Base class cho tất cả user types"""
    def __init__(self, user_id, username, full_name, email, role):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.email = email
        self.role = role

class Admin(User):
    """Admin class - có quyền cao nhất"""
    def __init__(self, user_id, username, full_name, email):
        super().__init__(user_id, username, full_name, email, "Admin")

class EventOrganizer(User):
    """Event Organizer class - quản lý events của mình"""
    def __init__(self, user_id, username, full_name, email):
        super().__init__(user_id, username, full_name, email, "EventOrganizer")

class Student(User):
    """Student class - có thể đăng ký events"""
    def __init__(self, user_id, username, full_name, email):
        super().__init__(user_id, username, full_name, email, "Student")

class Visitor(User):
    """Visitor class - tương tự Student"""
    def __init__(self, user_id, username, full_name, email):
        super().__init__(user_id, username, full_name, email, "Visitor")

class Event:
    """Event class - chứa thông tin sự kiện"""
    def __init__(self, event_id, name, description, date, time, location, max_capacity, organizer_id):
        self._validate_inputs(name, date, max_capacity)
        self.event_id = event_id
        self.name = name
        self.description = description
        self.date = date
        self.time = time
        self.location = location
        self.max_capacity = int(max_capacity)
        self.organizer_id = organizer_id
        self.attendees = []
    
    def _validate_inputs(self, name, date, max_capacity):
        """Xác thực đầu vào theo yêu cầu đề bài"""
        # Validate event name
        if not name or len(name.strip()) < 5:
            raise ValueError("Tên sự kiện phải có ít nhất 5 ký tự")
        
        # Validate date (không được trong quá khứ)
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()
        
        if date < datetime.now().date():
            raise ValueError("Ngày sự kiện không được trong quá khứ")
        
        # Validate capacity
        if int(max_capacity) <= 0:
            raise ValueError("Sức chứa phải là số nguyên dương")
    
    def add_attendee(self, user_id):
        """Thêm người tham dự với kiểm tra sức chứa"""
        if len(self.attendees) >= self.max_capacity:
            raise ValueError("Sự kiện đã đầy, không thể đăng ký thêm")
        
        if user_id in self.attendees:
            raise ValueError("Bạn đã đăng ký sự kiện này rồi")
        
        self.attendees.append(user_id)
        return True
    
    def remove_attendee(self, user_id):
        """Xóa người tham dự"""
        if user_id in self.attendees:
            self.attendees.remove(user_id)
            return True
        return False
    
    # ====================== NEW UPDATE/DELETE METHODS ======================
    
    def can_be_updated_by(self, user_id, user_role):
        """Kiểm tra xem user có quyền update event này không"""
        if user_role == "Admin":
            return True
        if user_role == "EventOrganizer" and self.organizer_id == user_id:
            return True
        return False
    
    def can_be_deleted_by(self, user_id, user_role):
        """Kiểm tra xem user có quyền delete event này không"""
        if user_role == "Admin":
            return True
        if user_role == "EventOrganizer" and self.organizer_id == user_id:
            return True
        return False
    
    def can_update_capacity(self, new_capacity):
        """Kiểm tra có thể update capacity không"""
        try:
            new_cap = int(new_capacity)
            if new_cap <= 0:
                return False, "Sức chứa phải là số nguyên dương"
            
            current_attendees = len(self.attendees)
            if new_cap < current_attendees:
                return False, f"Không thể giảm sức chứa xuống {new_cap}. Hiện có {current_attendees} người đã đăng ký"
            
            return True, "OK"
        except ValueError:
            return False, "Sức chứa phải là số nguyên"
    
    def validate_update_data(self, field, new_value):
        """Validate dữ liệu update cho từng field"""
        if field == "name":
            if not new_value or len(new_value.strip()) < 5:
                return False, "Tên sự kiện phải có ít nhất 5 ký tự"
        
        elif field == "date":
            try:
                if isinstance(new_value, str):
                    new_date = datetime.strptime(new_value, "%Y-%m-%d").date()
                else:
                    new_date = new_value
                
                if new_date < datetime.now().date():
                    return False, "Ngày sự kiện không được trong quá khứ"
            except ValueError:
                return False, "Format ngày không đúng (YYYY-MM-DD)"
        
        elif field == "time":
            try:
                if isinstance(new_value, str):
                    datetime.strptime(new_value, "%H:%M")
            except ValueError:
                return False, "Format giờ không đúng (HH:MM)"
        
        elif field == "max_capacity":
            return self.can_update_capacity(new_value)
        
        elif field == "description":
            if not new_value or len(new_value.strip()) == 0:
                return False, "Mô tả không được để trống"
        
        elif field == "location":
            if not new_value or len(new_value.strip()) == 0:
                return False, "Địa điểm không được để trống"
        
        return True, "OK"
    
    def update_field(self, field, new_value):
        """Update một field cụ thể sau khi đã validate"""
        valid, message = self.validate_update_data(field, new_value)
        if not valid:
            raise ValueError(message)
        
        if field == "name":
            self.name = new_value.strip()
        elif field == "description":
            self.description = new_value.strip()
        elif field == "date":
            if isinstance(new_value, str):
                self.date = datetime.strptime(new_value, "%Y-%m-%d").date()
            else:
                self.date = new_value
        elif field == "time":
            if isinstance(new_value, str):
                self.time = datetime.strptime(new_value, "%H:%M").time()
            else:
                self.time = new_value
        elif field == "location":
            self.location = new_value.strip()
        elif field == "max_capacity":
            self.max_capacity = int(new_value)
        
        return True
    
    def get_deletion_impact(self):
        """Lấy thông tin impact khi xóa event"""
        impact = {
            "attendees_count": len(self.attendees),
            "attendees_list": self.attendees.copy(),
            "event_name": self.name,
            "event_date": str(self.date),
            "can_delete": True,
            "warnings": []
        }
        
        if len(self.attendees) > 0:
            impact["warnings"].append(f"Sẽ hủy đăng ký cho {len(self.attendees)} người tham dự")
        
        # Check if event is soon (within 3 days)
        days_until_event = (self.date - datetime.now().date()).days
        if days_until_event <= 3:
            impact["warnings"].append(f"Sự kiện diễn ra trong {days_until_event} ngày nữa")
        
        return impact
    
    def prepare_for_deletion(self):
        """Chuẩn bị xóa event - clear tất cả attendees"""
        removed_attendees = self.attendees.copy()
        self.attendees.clear()
        return removed_attendees
    
    def __str__(self):
        """String representation của Event"""
        return f"Event({self.event_id}): {self.name} on {self.date} at {self.location}"