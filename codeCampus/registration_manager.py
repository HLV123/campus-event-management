# registration_manager.py - Quản lý đăng ký sự kiện

class RegistrationManager:
    """Class quản lý đăng ký sự kiện"""
    
    def __init__(self, system):
        self.system = system
    
    def register_for_event(self):
        """Đăng ký sự kiện (Student/Visitor)"""
        if self.system.current_role not in ["Student", "Visitor"]:
            print("Chỉ sinh viên và khách mời mới có thể đăng ký")
            return
        
        # Hiển thị events chưa đăng ký
        available_events = []
        for event in self.system.events.values():
            if self.system.current_user.user_id not in event.attendees:
                available_events.append(event)
        
        if not available_events:
            print("Không có sự kiện nào để đăng ký")
            return
        
        print("\n=== SỰ KIỆN CÓ THỂ ĐĂNG KÝ ===")
        self._display_events_table(available_events)
        
        event_id = input("\nNhập ID sự kiện: ").strip()
        
        if event_id not in self.system.events:
            print("Không tìm thấy sự kiện")
            return
        
        event = self.system.events[event_id]
        
        try:
            event.add_attendee(self.system.current_user.user_id)
            print(f"Đăng ký thành công sự kiện: {event.name}")
            available_spots = event.max_capacity - len(event.attendees)
            print(f"Còn lại: {available_spots} chỗ")
        except ValueError as e:
            print(f"Lỗi: {e}")
    
    def view_my_registrations(self):
        """Xem sự kiện đã đăng ký (Student/Visitor)"""
        my_events = []
        for event in self.system.events.values():
            if self.system.current_user.user_id in event.attendees:
                my_events.append(event)
        
        if not my_events:
            print("Bạn chưa đăng ký sự kiện nào")
            return
        
        print("\n=== SỰ KIỆN ĐÃ ĐĂNG KÝ ===")
        self._display_events_table(my_events)
        
        # Xem chi tiết
        detail = input("\nXem chi tiết sự kiện nào? (Event ID hoặc Enter): ").strip()
        if detail and detail in self.system.events:
            event = self.system.events[detail]
            if self.system.current_user.user_id in event.attendees:
                self._show_event_details(event)
    
    def manage_registrations(self):
        """Quản lý đăng ký sự kiện (Organizer)"""
        # Hiển thị sự kiện của organizer
        my_events = [e for e in self.system.events.values() 
                    if e.organizer_id == self.system.current_user.user_id]
        
        if not my_events:
            print("Bạn chưa có sự kiện nào")
            return
        
        print("\n=== SỰ KIỆN CỦA TÔI ===")
        self._display_events_table(my_events)
        
        event_id = input("\nNhập ID sự kiện: ").strip()
        if event_id not in self.system.events:
            print("Không tìm thấy sự kiện")
            return
        
        event = self.system.events[event_id]
        if event.organizer_id != self.system.current_user.user_id:
            print("Bạn chỉ có thể quản lý sự kiện của mình")
            return
        
        print(f"\n=== ĐĂNG KÝ CHO: {event.name} ===")
        print(f"Số người đăng ký: {len(event.attendees)}/{event.max_capacity}")
        
        if event.attendees:
            print("\nDanh sách người đăng ký:")
            for i, user_id in enumerate(event.attendees, 1):
                if user_id in self.system.users:
                    attendee = self.system.users[user_id]
                    print(f"{i}. {attendee.full_name} ({attendee.email}) - {attendee.role}")
                else:
                    print(f"{i}. Unknown User (ID: {user_id})")
        else:
            print("Chưa có người đăng ký")
        
        # Menu quản lý đăng ký
        print(f"\n=== QUẢN LÝ ĐĂNG KÝ ===")
        print("1. Xem chi tiết danh sách")
        print("2. Xuất danh sách ra file")
        print("3. Thống kê đăng ký")
        print("0. Quay lại")
        
        choice = input("\nChọn (0-3): ").strip()
        
        if choice == '1':
            self._show_detailed_attendee_list(event)
        elif choice == '2':
            self._export_attendee_list(event)
        elif choice == '3':
            self._show_registration_statistics(event)
        elif choice == '0':
            return
        else:
            print("Lựa chọn không hợp lệ")
    
    def view_all_attendees(self):
        """Xem tất cả người tham dự (Admin)"""
        print("\n=== TẤT CẢ NGƯỜI THAM DỰ ===")
        for event in self.system.events.values():
            if event.attendees:
                print(f"\n{event.name} ({event.date})")
                print(f"   Số người: {len(event.attendees)}/{event.max_capacity}")
                
                for user_id in event.attendees:
                    if user_id in self.system.users:
                        attendee = self.system.users[user_id]
                        print(f"   - {attendee.full_name} ({attendee.role})")
                    else:
                        print(f"   - Unknown User (ID: {user_id})")
            else:
                print(f"\n{event.name} - Chưa có người đăng ký")
    
    # ====================== HELPER METHODS ======================
    
    def _display_events_table(self, events):
        """Hiển thị danh sách events dạng table"""
        print(f"{'ID':<8} {'Tên sự kiện':<30} {'Ngày':<12} {'Đăng ký':<10}")
        print("-" * 70)
        
        for event in events:
            attendance = f"{len(event.attendees)}/{event.max_capacity}"
            print(f"{event.event_id:<8} {event.name[:29]:<30} {event.date:<12} {attendance:<10}")
    
    def _show_event_details(self, event):
        """Hiển thị chi tiết sự kiện"""
        print(f"\n=== CHI TIẾT SỰ KIỆN ===")
        print(f"Tên: {event.name}")
        print(f"Mô tả: {event.description}")
        print(f"Ngày: {event.date}")
        print(f"Giờ: {event.time}")
        print(f"Địa điểm: {event.location}")
        print(f"Đăng ký: {len(event.attendees)}/{event.max_capacity}")
        print(f"ID: {event.event_id}")
        
        # Hiển thị organizer
        if event.organizer_id in self.system.users:
            organizer = self.system.users[event.organizer_id]
            print(f"Người tổ chức: {organizer.full_name}")
    
    def _show_detailed_attendee_list(self, event):
        """Hiển thị danh sách chi tiết người tham dự"""
        print(f"\n=== DANH SÁCH CHI TIẾT - {event.name} ===")
        
        if not event.attendees:
            print("Chưa có người đăng ký")
            return
        
        print(f"{'STT':<3} {'Họ tên':<25} {'Email':<30} {'Vai trò':<15}")
        print("-" * 80)
        
        for i, user_id in enumerate(event.attendees, 1):
            if user_id in self.system.users:
                attendee = self.system.users[user_id]
                print(f"{i:<3} {attendee.full_name:<25} {attendee.email:<30} {attendee.role:<15}")
            else:
                print(f"{i:<3} {'Unknown User':<25} {'N/A':<30} {'Unknown':<15}")
        
        print(f"\nTổng cộng: {len(event.attendees)} người")
    
    def _export_attendee_list(self, event):
        """Xuất danh sách người tham dự ra file"""
        if not event.attendees:
            print("Chưa có người đăng ký để xuất")
            return
        
        try:
            import csv
            from datetime import datetime
            
            filename = f"attendees_{event.event_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow([
                    'STT', 'Họ tên', 'Email', 'Vai trò', 'Ngày đăng ký'
                ])
                
                # Event info
                writer.writerow([])
                writer.writerow(['THÔNG TIN SỰ KIỆN'])
                writer.writerow(['Tên sự kiện', event.name])
                writer.writerow(['Ngày', str(event.date)])
                writer.writerow(['Địa điểm', event.location])
                writer.writerow(['Tổng đăng ký', len(event.attendees)])
                writer.writerow([])
                
                # Attendee data
                writer.writerow(['DANH SÁCH NGƯỜI THAM DỰ'])
                writer.writerow(['STT', 'Họ tên', 'Email', 'Vai trò'])
                
                for i, user_id in enumerate(event.attendees, 1):
                    if user_id in self.system.users:
                        attendee = self.system.users[user_id]
                        writer.writerow([
                            i, attendee.full_name, attendee.email, attendee.role
                        ])
                    else:
                        writer.writerow([
                            i, 'Unknown User', 'N/A', 'Unknown'
                        ])
            
            print(f"Đã xuất danh sách: {filename}")
            
        except Exception as e:
            print(f"Lỗi xuất file: {e}")
    
    def _show_registration_statistics(self, event):
        """Hiển thị thống kê đăng ký"""
        total_capacity = event.max_capacity
        registered = len(event.attendees)
        available = total_capacity - registered
        fill_rate = (registered / total_capacity) * 100 if total_capacity > 0 else 0
        
        print(f"\n=== THỐNG KÊ ĐĂNG KÝ - {event.name} ===")
        print(f"Tổng sức chứa: {total_capacity}")
        print(f"Đã đăng ký: {registered}")
        print(f"Còn trống: {available}")
        print(f"Tỷ lệ lấp đầy: {fill_rate:.1f}%")
        
        # Thống kê theo vai trò
        role_stats = {}
        for user_id in event.attendees:
            if user_id in self.system.users:
                role = self.system.users[user_id].role
                role_stats[role] = role_stats.get(role, 0) + 1
        
        if role_stats:
            print(f"\nThống kê theo vai trò:")
            for role, count in role_stats.items():
                print(f"   {role}: {count} người")
        
        # Cảnh báo nếu gần đầy
        if fill_rate >= 90:
            print(f"\nCảnh báo: Sự kiện sắp đầy!")
        elif fill_rate >= 75:
            print(f"\nLưu ý: Sự kiện đã đăng ký {fill_rate:.1f}%")