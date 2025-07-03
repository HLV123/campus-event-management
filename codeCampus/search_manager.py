# search_manager.py - Quản lý tìm kiếm và lọc sự kiện

from datetime import datetime, date

class SearchManager:
    """Class quản lý tìm kiếm và lọc sự kiện"""
    
    def __init__(self, system):
        self.system = system
    
    def search_events(self):
        """Menu tìm kiếm sự kiện với nhiều tiêu chí"""
        print("\nTÌM KIẾM SỰ KIỆN")
        print("="*30)
        print("1. Tìm theo tên sự kiện")
        print("2. Tìm theo địa điểm")
        print("3. Tìm theo ngày")
        print("4. Tìm theo organizer")
        print("5. Lọc theo tình trạng đăng ký")
        print("6. Tìm kiếm nâng cao")
        print("0. Quay lại")
        
        choice = input("\nChọn cách tìm kiếm (0-6): ").strip()
        
        if choice == '1':
            self.search_by_name()
        elif choice == '2':
            self.search_by_location()
        elif choice == '3':
            self.search_by_date()
        elif choice == '4':
            self.search_by_organizer()
        elif choice == '5':
            self.filter_by_registration_status()
        elif choice == '6':
            self.advanced_search()
        elif choice == '0':
            return
        else:
            print("Lựa chọn không hợp lệ")
    
    def search_by_name(self):
        """Tìm kiếm theo tên sự kiện"""
        search_term = input("\nNhập tên sự kiện cần tìm: ").strip()
        
        if not search_term:
            print("Vui lòng nhập từ khóa tìm kiếm")
            return
        
        found_events = []
        search_term_lower = search_term.lower()
        
        for event in self.system.events.values():
            if search_term_lower in event.name.lower():
                found_events.append(event)
        
        self._display_search_results(found_events, f"tên chứa '{search_term}'")
    
    def search_by_location(self):
        """Tìm kiếm theo địa điểm"""
        # Hiển thị các địa điểm có sẵn
        locations = set(event.location for event in self.system.events.values())
        
        print(f"\nCÁC ĐỊA ĐIỂM CÓ SẴN:")
        for i, location in enumerate(sorted(locations), 1):
            print(f"{i}. {location}")
        
        search_term = input(f"\nNhập địa điểm cần tìm (hoặc từ khóa): ").strip()
        
        if not search_term:
            print("Vui lòng nhập địa điểm")
            return
        
        found_events = []
        search_term_lower = search_term.lower()
        
        for event in self.system.events.values():
            if search_term_lower in event.location.lower():
                found_events.append(event)
        
        self._display_search_results(found_events, f"địa điểm chứa '{search_term}'")
    
    def search_by_date(self):
        """Tìm kiếm theo ngày"""
        print(f"\nTÌM KIẾM THEO NGÀY:")
        print("1. Sự kiện hôm nay")
        print("2. Sự kiện tuần này")
        print("3. Sự kiện tháng này")
        print("4. Chọn ngày cụ thể")
        print("5. Chọn khoảng thời gian")
        
        choice = input("\nChọn (1-5): ").strip()
        
        today = date.today()
        found_events = []
        search_description = ""
        
        if choice == '1':
            # Sự kiện hôm nay
            found_events = [e for e in self.system.events.values() if e.date == today]
            search_description = "hôm nay"
            
        elif choice == '2':
            # Sự kiện tuần này
            from datetime import timedelta
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            
            found_events = [e for e in self.system.events.values() 
                          if week_start <= e.date <= week_end]
            search_description = "tuần này"
            
        elif choice == '3':
            # Sự kiện tháng này
            month_start = today.replace(day=1)
            if today.month == 12:
                month_end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                month_end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
            
            found_events = [e for e in self.system.events.values() 
                          if month_start <= e.date <= month_end]
            search_description = "tháng này"
            
        elif choice == '4':
            # Ngày cụ thể
            date_str = input("Nhập ngày (YYYY-MM-DD): ").strip()
            try:
                search_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                found_events = [e for e in self.system.events.values() if e.date == search_date]
                search_description = f"ngày {search_date}"
            except ValueError:
                print("Format ngày không đúng")
                return
                
        elif choice == '5':
            # Khoảng thời gian
            try:
                start_str = input("Từ ngày (YYYY-MM-DD): ").strip()
                end_str = input("Đến ngày (YYYY-MM-DD): ").strip()
                
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
                
                if start_date > end_date:
                    print("Ngày bắt đầu phải trước ngày kết thúc")
                    return
                
                found_events = [e for e in self.system.events.values() 
                              if start_date <= e.date <= end_date]
                search_description = f"từ {start_date} đến {end_date}"
                
            except ValueError:
                print("Format ngày không đúng")
                return
        else:
            print("Lựa chọn không hợp lệ")
            return
        
        self._display_search_results(found_events, search_description)
    
    def search_by_organizer(self):
        """Tìm kiếm theo organizer"""
        # Hiển thị danh sách organizers
        organizers = {}
        for event in self.system.events.values():
            if event.organizer_id in self.system.users:
                organizer = self.system.users[event.organizer_id]
                if organizer.user_id not in organizers:
                    organizers[organizer.user_id] = {
                        'name': organizer.full_name,
                        'events': []
                    }
                organizers[organizer.user_id]['events'].append(event)
        
        if not organizers:
            print("Không có organizer nào")
            return
        
        print(f"\nDANH SÁCH ORGANIZERS:")
        org_list = list(organizers.items())
        for i, (org_id, org_info) in enumerate(org_list, 1):
            event_count = len(org_info['events'])
            print(f"{i}. {org_info['name']} ({event_count} sự kiện)")
        
        try:
            choice = int(input(f"\nChọn organizer (1-{len(org_list)}): ")) - 1
            selected_org_id, selected_org_info = org_list[choice]
            
            found_events = selected_org_info['events']
            search_description = f"organizer '{selected_org_info['name']}'"
            
            self._display_search_results(found_events, search_description)
            
        except (ValueError, IndexError):
            print("Lựa chọn không hợp lệ")
    
    def filter_by_registration_status(self):
        """Lọc theo tình trạng đăng ký"""
        print(f"\nLỌC THEO TÌNH TRẠNG ĐĂNG KÝ:")
        print("1. Sự kiện đã đầy (100%)")
        print("2. Sự kiện gần đầy (80-99%)")
        print("3. Sự kiện còn nhiều chỗ (dưới 50%)")
        print("4. Sự kiện chưa có ai đăng ký")
        print("5. Sự kiện còn chỗ (có thể đăng ký)")
        
        choice = input("\nChọn (1-5): ").strip()
        
        found_events = []
        search_description = ""
        
        for event in self.system.events.values():
            fill_rate = len(event.attendees) / event.max_capacity if event.max_capacity > 0 else 0
            
            if choice == '1' and fill_rate >= 1.0:
                found_events.append(event)
                search_description = "đã đầy"
            elif choice == '2' and 0.8 <= fill_rate < 1.0:
                found_events.append(event)
                search_description = "gần đầy (80-99%)"
            elif choice == '3' and fill_rate < 0.5:
                found_events.append(event)
                search_description = "còn nhiều chỗ"
            elif choice == '4' and fill_rate == 0:
                found_events.append(event)
                search_description = "chưa có đăng ký"
            elif choice == '5' and fill_rate < 1.0:
                found_events.append(event)
                search_description = "còn chỗ"
        
        if choice in ['1', '2', '3', '4', '5']:
            self._display_search_results(found_events, search_description)
        else:
            print("Lựa chọn không hợp lệ")
    
    def advanced_search(self):
        """Tìm kiếm nâng cao với nhiều tiêu chí"""
        print(f"\nTÌM KIẾM NÂNG CAO")
        print("Có thể để trống các tiêu chí không muốn lọc")
        print("-" * 40)
        
        # Thu thập tiêu chí tìm kiếm
        criteria = {}
        
        # Tên sự kiện
        name_keyword = input("Từ khóa trong tên (Enter để bỏ qua): ").strip()
        if name_keyword:
            criteria['name'] = name_keyword.lower()
        
        # Địa điểm
        location_keyword = input("Từ khóa địa điểm (Enter để bỏ qua): ").strip()
        if location_keyword:
            criteria['location'] = location_keyword.lower()
        
        # Khoảng ngày
        date_filter = input("Lọc theo ngày? (y/n): ").lower()
        if date_filter == 'y':
            try:
                start_str = input("Từ ngày (YYYY-MM-DD, Enter = hôm nay): ").strip()
                end_str = input("Đến ngày (YYYY-MM-DD, Enter = cuối năm): ").strip()
                
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else date.today()
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else date(2025, 12, 31)
                
                criteria['date_range'] = (start_date, end_date)
            except ValueError:
                print("Format ngày không đúng, bỏ qua tiêu chí ngày")
        
        # Tình trạng đăng ký
        status_filter = input("Lọc theo tình trạng? (full/available/empty/Enter để bỏ qua): ").strip().lower()
        if status_filter in ['full', 'available', 'empty']:
            criteria['status'] = status_filter
        
        # Số lượng người tham dự
        attendee_filter = input("Lọc theo số người đăng ký? (y/n): ").lower()
        if attendee_filter == 'y':
            try:
                min_attendees = input("Tối thiểu (Enter = 0): ").strip()
                max_attendees = input("Tối đa (Enter = không giới hạn): ").strip()
                
                min_val = int(min_attendees) if min_attendees else 0
                max_val = int(max_attendees) if max_attendees else float('inf')
                
                criteria['attendee_range'] = (min_val, max_val)
            except ValueError:
                print("Số không hợp lệ, bỏ qua tiêu chí số lượng")
        
        # Thực hiện tìm kiếm
        found_events = self._apply_advanced_criteria(criteria)
        
        # Hiển thị kết quả
        criteria_desc = self._build_criteria_description(criteria)
        self._display_search_results(found_events, criteria_desc)
    
    def _apply_advanced_criteria(self, criteria):
        """Áp dụng các tiêu chí tìm kiếm nâng cao"""
        found_events = []
        
        for event in self.system.events.values():
            match = True
            
            # Kiểm tra tên
            if 'name' in criteria:
                if criteria['name'] not in event.name.lower():
                    match = False
            
            # Kiểm tra địa điểm
            if 'location' in criteria and match:
                if criteria['location'] not in event.location.lower():
                    match = False
            
            # Kiểm tra ngày
            if 'date_range' in criteria and match:
                start_date, end_date = criteria['date_range']
                if not (start_date <= event.date <= end_date):
                    match = False
            
            # Kiểm tra tình trạng
            if 'status' in criteria and match:
                fill_rate = len(event.attendees) / event.max_capacity if event.max_capacity > 0 else 0
                
                if criteria['status'] == 'full' and fill_rate < 1.0:
                    match = False
                elif criteria['status'] == 'available' and fill_rate >= 1.0:
                    match = False
                elif criteria['status'] == 'empty' and len(event.attendees) > 0:
                    match = False
            
            # Kiểm tra số lượng người tham dự
            if 'attendee_range' in criteria and match:
                min_val, max_val = criteria['attendee_range']
                attendee_count = len(event.attendees)
                if not (min_val <= attendee_count <= max_val):
                    match = False
            
            if match:
                found_events.append(event)
        
        return found_events
    
    def _build_criteria_description(self, criteria):
        """Tạo mô tả tiêu chí tìm kiếm"""
        descriptions = []
        
        if 'name' in criteria:
            descriptions.append(f"tên chứa '{criteria['name']}'")
        
        if 'location' in criteria:
            descriptions.append(f"địa điểm chứa '{criteria['location']}'")
        
        if 'date_range' in criteria:
            start, end = criteria['date_range']
            descriptions.append(f"từ {start} đến {end}")
        
        if 'status' in criteria:
            status_map = {
                'full': 'đã đầy',
                'available': 'còn chỗ',
                'empty': 'chưa có đăng ký'
            }
            descriptions.append(f"tình trạng {status_map[criteria['status']]}")
        
        if 'attendee_range' in criteria:
            min_val, max_val = criteria['attendee_range']
            if max_val == float('inf'):
                descriptions.append(f"ít nhất {min_val} người")
            else:
                descriptions.append(f"từ {min_val} đến {max_val} người")
        
        return " và ".join(descriptions) if descriptions else "không có tiêu chí"
    
    def _display_search_results(self, found_events, search_description):
        """Hiển thị kết quả tìm kiếm"""
        if not found_events:
            print(f"\nKhông tìm thấy sự kiện nào với tiêu chí: {search_description}")
            return
        
        print(f"\nTÌM THẤY {len(found_events)} SỰ KIỆN")
        print(f"Tiêu chí: {search_description}")
        print("="*60)
        
        # Hiển thị kết quả dạng bảng
        print(f"{'ID':<8} {'Tên sự kiện':<30} {'Ngày':<12} {'Đăng ký':<10}")
        print("-" * 70)
        
        for event in sorted(found_events, key=lambda e: e.date):
            attendance = f"{len(event.attendees)}/{event.max_capacity}"
            print(f"{event.event_id:<8} {event.name[:29]:<30} {event.date:<12} {attendance:<10}")
        
        # Menu hành động với kết quả
        print(f"\nHÀNH ĐỘNG VỚI KẾT QUẢ:")
        print("1. Xem chi tiết sự kiện")
        print("2. Đăng ký sự kiện (nếu là Student/Visitor)")
        print("3. Xuất kết quả ra file")
        print("0. Quay lại")
        
        choice = input("\nChọn (0-3): ").strip()
        
        if choice == '1':
            self._view_search_result_details(found_events)
        elif choice == '2':
            self._register_from_search_results(found_events)
        elif choice == '3':
            self._export_search_results(found_events, search_description)
        elif choice == '0':
            return
        else:
            print("Lựa chọn không hợp lệ")
    
    def _view_search_result_details(self, events):
        """Xem chi tiết từ kết quả tìm kiếm"""
        event_id = input("Nhập ID sự kiện để xem chi tiết: ").strip()
        
        target_event = None
        for event in events:
            if event.event_id == event_id:
                target_event = event
                break
        
        if target_event:
            self.system.view_ops.show_event_details(target_event)
        else:
            print("Event ID không có trong kết quả tìm kiếm")
    
    def _register_from_search_results(self, events):
        """Đăng ký sự kiện từ kết quả tìm kiếm"""
        if self.system.current_role not in ["Student", "Visitor"]:
            print("Chỉ Student/Visitor mới có thể đăng ký")
            return
        
        # Lọc events có thể đăng ký
        available_events = []
        for event in events:
            if (self.system.current_user.user_id not in event.attendees and 
                len(event.attendees) < event.max_capacity):
                available_events.append(event)
        
        if not available_events:
            print("Không có sự kiện nào trong kết quả để đăng ký")
            return
        
        print(f"\nSỰ KIỆN CÓ THỂ ĐĂNG KÝ TRONG KẾT QUẢ:")
        for event in available_events:
            attendance = f"{len(event.attendees)}/{event.max_capacity}"
            print(f"   {event.event_id} - {event.name} ({attendance})")
        
        event_id = input("\nNhập ID sự kiện để đăng ký: ").strip()
        
        target_event = None
        for event in available_events:
            if event.event_id == event_id:
                target_event = event
                break
        
        if target_event:
            try:
                target_event.add_attendee(self.system.current_user.user_id)
                print(f"Đăng ký thành công: {target_event.name}")
                remaining = target_event.max_capacity - len(target_event.attendees)
                print(f"Còn lại: {remaining} chỗ")
            except ValueError as e:
                print(f"Lỗi: {e}")
        else:
            print("Event ID không hợp lệ hoặc không thể đăng ký")
    
    def _export_search_results(self, events, search_description):
        """Xuất kết quả tìm kiếm ra file"""
        try:
            import csv
            filename = f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow(['SEARCH RESULTS'])
                writer.writerow(['Search Criteria:', search_description])
                writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow(['Total Results:', len(events)])
                writer.writerow([])
                
                # Results
                writer.writerow(['Event ID', 'Event Name', 'Date', 'Time', 'Location', 'Registered', 'Capacity', 'Fill Rate'])
                
                for event in sorted(events, key=lambda e: e.date):
                    fill_rate = f"{(len(event.attendees) / event.max_capacity) * 100:.1f}%"
                    writer.writerow([
                        event.event_id, event.name, str(event.date), str(event.time),
                        event.location, len(event.attendees), event.max_capacity, fill_rate
                    ])
            
            print(f"Đã xuất kết quả tìm kiếm: {filename}")
            
        except Exception as e:
            print(f"Lỗi xuất file: {e}")