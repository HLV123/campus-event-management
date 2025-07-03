# view_manager.py - Quản lý hiển thị dữ liệu

class ViewManager:
    """Class quản lý hiển thị dữ liệu"""
    
    def __init__(self, system):
        self.system = system
    
    def view_all_events(self):
        """Xem tất cả sự kiện"""
        if not self.system.events:
            print("Không có sự kiện nào")
            return
        
        print("\n=== TẤT CẢ SỰ KIỆN ===")
        self.display_events_table(list(self.system.events.values()))
        
        # Xem chi tiết
        detail = input("\nXem chi tiết sự kiện nào? (Event ID hoặc Enter): ").strip()
        if detail and detail in self.system.events:
            self.show_event_details(self.system.events[detail])
    
    def view_my_events(self):
        """Xem sự kiện của organizer"""
        my_events = [e for e in self.system.events.values() 
                    if e.organizer_id == self.system.current_user.user_id]
        
        if not my_events:
            print("Bạn chưa được phân công tổ chức sự kiện nào")
            return
        
        print("\n=== SỰ KIỆN CỦA TÔI ===")
        self.display_events_table(my_events)
        
        # Xem chi tiết
        detail = input("\nXem chi tiết sự kiện nào? (Event ID hoặc Enter): ").strip()
        if detail and detail in self.system.events:
            event = self.system.events[detail]
            if event.organizer_id == self.system.current_user.user_id:
                self.show_event_details(event)
            else:
                print("Bạn chỉ có thể xem chi tiết sự kiện của mình")
    
    def display_events_table(self, events):
        """Hiển thị danh sách events dạng table"""
        if not events:
            print("Không có sự kiện nào")
            return
        
        # Sắp xếp theo ngày
        events_sorted = sorted(events, key=lambda e: e.date)
        
        print(f"{'ID':<8} {'Tên sự kiện':<30} {'Ngày':<12} {'Đăng ký':<10} {'Trạng thái':<10}")
        print("-" * 80)
        
        for event in events_sorted:
            attendance = f"{len(event.attendees)}/{event.max_capacity}"
            
            # Xác định trạng thái
            fill_rate = len(event.attendees) / event.max_capacity if event.max_capacity > 0 else 0
            if fill_rate >= 1.0:
                status = "Đầy"
            elif fill_rate >= 0.8:
                status = "Gần đầy"
            elif fill_rate >= 0.5:
                status = "Khá tốt"
            elif fill_rate > 0:
                status = "Còn chỗ"
            else:
                status = "Chưa có"
            
            print(f"{event.event_id:<8} {event.name[:29]:<30} {event.date:<12} {attendance:<10} {status:<10}")
        
        print(f"\nTổng cộng: {len(events)} sự kiện")
    
    def show_event_details(self, event):
        """Hiển thị chi tiết sự kiện"""
        print(f"\n" + "="*50)
        print(f"CHI TIẾT SỰ KIỆN: {event.name}")
        print("="*50)
        
        print(f"ID: {event.event_id}")
        print(f"Tên: {event.name}")
        print(f"Mô tả: {event.description}")
        print(f"Ngày: {event.date}")
        print(f"Giờ: {event.time}")
        print(f"Địa điểm: {event.location}")
        
        # Thông tin đăng ký
        registered = len(event.attendees)
        capacity = event.max_capacity
        available = capacity - registered
        fill_rate = (registered / capacity) * 100 if capacity > 0 else 0
        
        print(f"\nTHÔNG TIN ĐĂNG KÝ:")
        print(f"   Đã đăng ký: {registered}/{capacity} người ({fill_rate:.1f}%)")
        print(f"   Còn lại: {available} chỗ")
        
        # Hiển thị organizer
        if event.organizer_id in self.system.users:
            organizer = self.system.users[event.organizer_id]
            print(f"\nNgười tổ chức: {organizer.full_name} ({organizer.email})")
        
        # Hiển thị trạng thái
        if fill_rate >= 100:
            print(f"\nTrạng thái: SỰ KIỆN ĐÃ ĐẦY")
        elif fill_rate >= 80:
            print(f"\nTrạng thái: SẮP ĐẦY ({available} chỗ còn lại)")
        elif fill_rate >= 50:
            print(f"\nTrạng thái: CÒN CHỖ ({available} chỗ còn lại)")
        else:
            print(f"\nTrạng thái: NHIỀU CHỖ TRỐNG ({available} chỗ còn lại)")
        
        # Hiển thị danh sách người đăng ký nếu là organizer hoặc admin
        if (self.system.current_role == "Admin" or 
            (self.system.current_role == "EventOrganizer" and 
             event.organizer_id == self.system.current_user.user_id)):
            
            self._show_attendees_list(event)
    
    def _show_attendees_list(self, event):
        """Hiển thị danh sách người đăng ký"""
        if not event.attendees:
            print(f"\nNGUỜI THAM DỰ: Chưa có ai đăng ký")
            return
        
        print(f"\nDANH SÁCH NGƯỜI THAM DỰ ({len(event.attendees)} người):")
        print("-" * 50)
        
        # Nhóm theo vai trò
        attendees_by_role = {}
        for user_id in event.attendees:
            if user_id in self.system.users:
                user = self.system.users[user_id]
                role = user.role
                if role not in attendees_by_role:
                    attendees_by_role[role] = []
                attendees_by_role[role].append(user)
            else:
                if "Unknown" not in attendees_by_role:
                    attendees_by_role["Unknown"] = []
                attendees_by_role["Unknown"].append(f"User ID: {user_id}")
        
        # Hiển thị theo từng nhóm
        for role, users in attendees_by_role.items():
            print(f"\n{role} ({len(users)} người):")
            for i, user in enumerate(users, 1):
                if isinstance(user, str):  # Unknown user
                    print(f"   {i}. {user}")
                else:
                    print(f"   {i}. {user.full_name} ({user.email})")
    
    def show_events_by_date_range(self, start_date=None, end_date=None):
        """Hiển thị sự kiện theo khoảng thời gian"""
        from datetime import datetime, date
        
        if not start_date:
            start_date = date.today()
        if not end_date:
            end_date = date(2025, 12, 31)
        
        filtered_events = []
        for event in self.system.events.values():
            if start_date <= event.date <= end_date:
                filtered_events.append(event)
        
        if not filtered_events:
            print(f"Không có sự kiện nào từ {start_date} đến {end_date}")
            return
        
        print(f"\n=== SỰ KIỆN TỪ {start_date} ĐẾN {end_date} ===")
        self.display_events_table(filtered_events)
    
    def show_events_by_location(self, location_filter=""):
        """Hiển thị sự kiện theo địa điểm"""
        if not location_filter:
            print("Cần nhập từ khóa tìm kiếm địa điểm")
            return
        
        filtered_events = []
        for event in self.system.events.values():
            if location_filter.lower() in event.location.lower():
                filtered_events.append(event)
        
        if not filtered_events:
            print(f"Không có sự kiện nào tại '{location_filter}'")
            return
        
        print(f"\n=== SỰ KIỆN TẠI '{location_filter}' ===")
        self.display_events_table(filtered_events)
    
    def show_events_summary(self):
        """Hiển thị tóm tắt tất cả sự kiện"""
        if not self.system.events:
            print("Không có sự kiện nào")
            return
        
        print(f"\nTÓM TẮT SỰ KIỆN")
        print("="*40)
        
        total_events = len(self.system.events)
        total_capacity = sum(e.max_capacity for e in self.system.events.values())
        total_registered = sum(len(e.attendees) for e in self.system.events.values())
        
        print(f"Tổng số sự kiện: {total_events}")
        print(f"Tổng sức chứa: {total_capacity}")
        print(f"Đã đăng ký: {total_registered}")
        print(f"Còn trống: {total_capacity - total_registered}")
        
        if total_capacity > 0:
            fill_rate = (total_registered / total_capacity) * 100
            print(f"Tỷ lệ lấp đầy: {fill_rate:.1f}%")
        
        # Top 3 sự kiện nhiều người đăng ký nhất
        events_by_attendance = sorted(
            self.system.events.values(), 
            key=lambda e: len(e.attendees), 
            reverse=True
        )
        
        print(f"\nTOP 3 SỰ KIỆN PHỔ BIẾN:")
        for i, event in enumerate(events_by_attendance[:3], 1):
            attendance = len(event.attendees)
            print(f"   {i}. {event.name} - {attendance} người")
        
        # Sự kiện sắp diễn ra
        from datetime import date
        upcoming_events = [e for e in self.system.events.values() if e.date >= date.today()]
        upcoming_events.sort(key=lambda e: e.date)
        
        if upcoming_events:
            print(f"\nSỰ KIỆN SẮP DIỄN RA:")
            for event in upcoming_events[:3]:
                days_left = (event.date - date.today()).days
                print(f"   - {event.name} - {event.date} (còn {days_left} ngày)")
    
    def display_events_calendar_view(self):
        """Hiển thị sự kiện dạng calendar (đơn giản)"""
        from datetime import date, timedelta
        from collections import defaultdict
        
        # Nhóm events theo ngày
        events_by_date = defaultdict(list)
        for event in self.system.events.values():
            events_by_date[event.date].append(event)
        
        # Hiển thị 7 ngày tới
        print(f"\nLỊCH SỰ KIỆN 7 NGÀY TỚI")
        print("="*50)
        
        today = date.today()
        for i in range(7):
            current_date = today + timedelta(days=i)
            day_name = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "CN"][current_date.weekday()]
            
            print(f"\n{day_name} - {current_date}")
            print("-" * 30)
            
            if current_date in events_by_date:
                for event in events_by_date[current_date]:
                    attendance = f"{len(event.attendees)}/{event.max_capacity}"
                    print(f"   {event.time} - {event.name}")
                    print(f"      {event.location} | {attendance}")
            else:
                print("   Không có sự kiện")
    
    def show_event_search_results(self, search_term=""):
        """Hiển thị kết quả tìm kiếm sự kiện"""
        if not search_term:
            print("Cần nhập từ khóa tìm kiếm")
            return
        
        search_term = search_term.lower()
        found_events = []
        
        for event in self.system.events.values():
            # Tìm trong tên, mô tả, địa điểm
            if (search_term in event.name.lower() or 
                search_term in event.description.lower() or 
                search_term in event.location.lower()):
                found_events.append(event)
        
        if not found_events:
            print(f"Không tìm thấy sự kiện nào với từ khóa '{search_term}'")
            return
        
        print(f"\nKẾT QUẢ TÌM KIẾM: '{search_term}'")
        print(f"Tìm thấy {len(found_events)} sự kiện")
        print("="*50)
        
        self.display_events_table(found_events)
        
        # Cho phép xem chi tiết
        detail = input("\nXem chi tiết sự kiện nào? (Event ID hoặc Enter): ").strip()
        if detail and detail in self.system.events:
            if self.system.events[detail] in found_events:
                self.show_event_details(self.system.events[detail])
            else:
                print("Event ID không có trong kết quả tìm kiếm")
    
    def show_available_events_for_registration(self):
        """Hiển thị sự kiện có thể đăng ký"""
        if self.system.current_role not in ["Student", "Visitor"]:
            print("Chỉ Student/Visitor mới có thể đăng ký")
            return
        
        available_events = []
        for event in self.system.events.values():
            # Kiểm tra chưa đăng ký và còn chỗ
            if (self.system.current_user.user_id not in event.attendees and 
                len(event.attendees) < event.max_capacity):
                available_events.append(event)
        
        if not available_events:
            print("Không có sự kiện nào để đăng ký")
            print("Có thể bạn đã đăng ký hết hoặc các sự kiện đã đầy")
            return
        
        print(f"\nSỰ KIỆN CÓ THỂ ĐĂNG KÝ")
        print(f"Có {len(available_events)} sự kiện")
        print("="*50)
        
        self.display_events_table(available_events)
        return available_events
    
    def show_my_registered_events(self):
        """Hiển thị sự kiện đã đăng ký"""
        if self.system.current_role not in ["Student", "Visitor"]:
            print("Chỉ Student/Visitor mới có lịch sử đăng ký")
            return
        
        my_events = []
        for event in self.system.events.values():
            if self.system.current_user.user_id in event.attendees:
                my_events.append(event)
        
        if not my_events:
            print("Bạn chưa đăng ký sự kiện nào")
            return
        
        print(f"\nSỰ KIỆN ĐÃ ĐĂNG KÝ")
        print(f"Bạn đã đăng ký {len(my_events)} sự kiện")
        print("="*50)
        
        self.display_events_table(my_events)
        
        # Cho phép xem chi tiết
        detail = input("\nXem chi tiết sự kiện nào? (Event ID hoặc Enter): ").strip()
        if detail and detail in self.system.events:
            event = self.system.events[detail]
            if self.system.current_user.user_id in event.attendees:
                self.show_event_details(event)
            else:
                print("Bạn chưa đăng ký sự kiện này")
    
    def show_events_by_organizer(self, organizer_id=None):
        """Hiển thị sự kiện theo organizer"""
        if not organizer_id:
            organizer_id = self.system.current_user.user_id
        
        organizer_events = [e for e in self.system.events.values() 
                           if e.organizer_id == organizer_id]
        
        if not organizer_events:
            print("Không có sự kiện nào")
            return
        
        # Lấy tên organizer
        organizer_name = "Unknown"
        if organizer_id in self.system.users:
            organizer_name = self.system.users[organizer_id].full_name
        
        print(f"\nSỰ KIỆN CỦA {organizer_name}")
        print(f"Tổng cộng: {len(organizer_events)} sự kiện")
        print("="*50)
        
        self.display_events_table(organizer_events)
    
    def show_events_statistics_summary(self):
        """Hiển thị tóm tắt thống kê nhanh"""
        if not self.system.events:
            print("Không có dữ liệu để thống kê")
            return
        
        print(f"\nTHỐNG KÊ NHANH")
        print("="*30)
        
        # Thống kê cơ bản
        total_events = len(self.system.events)
        total_registered = sum(len(e.attendees) for e in self.system.events.values())
        
        print(f"Tổng sự kiện: {total_events}")
        print(f"Lượt đăng ký: {total_registered}")
        
        if total_events > 0:
            avg_attendance = total_registered / total_events
            print(f"TB/sự kiện: {avg_attendance:.1f} người")
        
        # Sự kiện hot nhất
        if self.system.events:
            hottest_event = max(self.system.events.values(), key=lambda e: len(e.attendees))
            print(f"Sự kiện hot: {hottest_event.name} ({len(hottest_event.attendees)} người)")
        
        # Tình trạng đăng ký
        full_events = sum(1 for e in self.system.events.values() 
                         if len(e.attendees) >= e.max_capacity)
        print(f"Sự kiện đầy: {full_events}/{total_events}")
        
        empty_events = sum(1 for e in self.system.events.values() 
                          if len(e.attendees) == 0)
        print(f"Chưa có đăng ký: {empty_events}/{total_events}")
    
    def display_compact_events_list(self, events, show_details=False):
        """Hiển thị danh sách sự kiện dạng compact"""
        if not events:
            print("Không có sự kiện nào")
            return
        
        print(f"\nDANH SÁCH SỰ KIỆN ({len(events)} sự kiện)")
        print("-" * 60)
        
        for i, event in enumerate(events, 1):
            attendance = len(event.attendees)
            capacity = event.max_capacity
            status = "FULL" if attendance >= capacity else "OPEN" if attendance < capacity * 0.8 else "NEAR_FULL"
            
            print(f"{i:2}. {status} {event.name}")
            print(f"     {event.date} | {event.location}")
            print(f"     {attendance}/{capacity} | ID: {event.event_id}")
            
            if show_details:
                print(f"     {event.description[:50]}...")
            
            print()  # Empty line between events