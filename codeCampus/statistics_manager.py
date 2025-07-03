# statistics_manager.py - Quản lý thống kê và báo cáo

import csv
from datetime import datetime

class StatisticsManager:
    """Class quản lý thống kê và báo cáo"""
    
    def __init__(self, system):
        self.system = system
    
    def show_statistics(self):
        """Hiển thị thống kê tổng quan (Admin)"""
        if self.system.current_role != "Admin":
            print("Chỉ Admin mới có quyền xem thống kê tổng quan")
            return
        
        total_events = len(self.system.events)
        total_attendees = sum(len(event.attendees) for event in self.system.events.values())
        
        if total_events == 0:
            print("Chưa có sự kiện nào")
            return
        
        average_attendees = total_attendees / total_events
        
        # Tìm sự kiện có attendance cao nhất và thấp nhất
        events_list = list(self.system.events.values())
        max_event = max(events_list, key=lambda e: len(e.attendees))
        min_event = min(events_list, key=lambda e: len(e.attendees))
        
        print("\n" + "="*50)
        print("THỐNG KÊ TỔNG QUAN HỆ THỐNG")
        print("="*50)
        
        print(f"Tổng số sự kiện: {total_events}")
        print(f"Tổng số người tham dự: {total_attendees}")
        print(f"Trung bình người tham dự/sự kiện: {average_attendees:.1f}")
        
        # Thống kê sức chứa
        total_capacity = sum(e.max_capacity for e in self.system.events.values())
        fill_rate = (total_attendees / total_capacity) * 100 if total_capacity > 0 else 0
        print(f"Tổng sức chứa: {total_capacity}")
        print(f"Tỷ lệ lấp đầy: {fill_rate:.1f}%")
        
        print(f"\nSự kiện phổ biến nhất:")
        print(f"   {max_event.name} - {len(max_event.attendees)} người")
        
        print(f"\nSự kiện ít quan tâm nhất:")
        print(f"   {min_event.name} - {len(min_event.attendees)} người")
        
        # Thống kê theo vai trò
        self._show_role_statistics()
        
        # Thống kê theo organizer
        self._show_organizer_statistics()
        
        # Thống kê trạng thái sự kiện
        self._show_event_status_statistics()
        
        # Menu xuất báo cáo
        self._show_export_menu()
    
    def show_my_event_statistics(self):
        """Thống kê sự kiện của organizer"""
        if self.system.current_role != "EventOrganizer":
            print("Chỉ Event Organizer mới có thể xem thống kê sự kiện của mình")
            return
        
        my_events = [e for e in self.system.events.values() 
                    if e.organizer_id == self.system.current_user.user_id]
        
        if not my_events:
            print("Bạn chưa được phân công tổ chức sự kiện nào")
            return
        
        total_events = len(my_events)
        total_attendees = sum(len(event.attendees) for event in my_events)
        average_attendees = total_attendees / total_events if total_events > 0 else 0
        
        print(f"\nTHỐNG KÊ SỰ KIỆN CỦA {self.system.current_user.full_name}")
        print("="*50)
        
        print(f"Số sự kiện tổ chức: {total_events}")
        print(f"Tổng người tham dự: {total_attendees}")
        print(f"Trung bình/sự kiện: {average_attendees:.1f} người")
        
        if my_events:
            # Sự kiện thành công nhất
            best_event = max(my_events, key=lambda e: len(e.attendees))
            print(f"\nSự kiện thành công nhất:")
            print(f"   {best_event.name} - {len(best_event.attendees)} người")
            
            # Tỷ lệ lấp đầy trung bình
            total_capacity = sum(e.max_capacity for e in my_events)
            avg_fill_rate = (total_attendees / total_capacity) * 100 if total_capacity > 0 else 0
            print(f"\nTỷ lệ lấp đầy TB: {avg_fill_rate:.1f}%")
            
            # Chi tiết từng sự kiện
            print(f"\nCHI TIẾT TỪNG SỰ KIỆN:")
            print(f"{'Tên sự kiện':<30} {'Ngày':<12} {'Đăng ký':<10} {'Tỷ lệ':<8}")
            print("-" * 70)
            
            for event in my_events:
                fill_rate = (len(event.attendees) / event.max_capacity) * 100
                attendance = f"{len(event.attendees)}/{event.max_capacity}"
                print(f"{event.name[:29]:<30} {event.date:<12} {attendance:<10} {fill_rate:.1f}%")
        
        # Xuất báo cáo cá nhân
        export = input("\nXuất báo cáo cá nhân? (y/n): ").lower()
        if export == 'y':
            self._export_personal_report(my_events)
    
    def _show_role_statistics(self):
        """Thống kê theo vai trò người tham dự"""
        print(f"\nTHỐNG KÊ THEO VAI TRÒ:")
        
        role_stats = {}
        for event in self.system.events.values():
            for user_id in event.attendees:
                if user_id in self.system.users:
                    role = self.system.users[user_id].role
                    role_stats[role] = role_stats.get(role, 0) + 1
        
        if role_stats:
            total_registrations = sum(role_stats.values())
            for role, count in role_stats.items():
                percentage = (count / total_registrations) * 100 if total_registrations > 0 else 0
                print(f"   {role}: {count} lượt ({percentage:.1f}%)")
        else:
            print("   Chưa có đăng ký nào")
    
    def _show_organizer_statistics(self):
        """Thống kê theo organizer"""
        print(f"\nTHỐNG KÊ THEO ORGANIZER:")
        
        organizer_stats = {}
        for event in self.system.events.values():
            org_id = event.organizer_id
            if org_id not in organizer_stats:
                organizer_stats[org_id] = {
                    'events': 0,
                    'attendees': 0,
                    'name': 'Unknown'
                }
            
            if org_id in self.system.users:
                organizer_stats[org_id]['name'] = self.system.users[org_id].full_name
            
            organizer_stats[org_id]['events'] += 1
            organizer_stats[org_id]['attendees'] += len(event.attendees)
        
        # Sắp xếp theo số người tham dự
        sorted_orgs = sorted(organizer_stats.items(), 
                           key=lambda x: x[1]['attendees'], 
                           reverse=True)
        
        for org_id, stats in sorted_orgs:
            avg = stats['attendees'] / stats['events'] if stats['events'] > 0 else 0
            print(f"   {stats['name']}: {stats['events']} sự kiện, {stats['attendees']} người (TB: {avg:.1f})")
    
    def _show_event_status_statistics(self):
        """Thống kê trạng thái sự kiện"""
        print(f"\nTHỐNG KÊ TRẠNG THÁI SỰ KIỆN:")
        
        full_events = 0     # Đầy 100%
        high_events = 0     # 80-99%
        medium_events = 0   # 50-79%
        low_events = 0      # 1-49%
        empty_events = 0    # 0%
        
        for event in self.system.events.values():
            fill_rate = len(event.attendees) / event.max_capacity if event.max_capacity > 0 else 0
            
            if fill_rate >= 1.0:
                full_events += 1
            elif fill_rate >= 0.8:
                high_events += 1
            elif fill_rate >= 0.5:
                medium_events += 1
            elif fill_rate > 0:
                low_events += 1
            else:
                empty_events += 1
        
        total = len(self.system.events)
        print(f"   Đầy (100%): {full_events}/{total} sự kiện")
        print(f"   Gần đầy (80-99%): {high_events}/{total} sự kiện")
        print(f"   Khá tốt (50-79%): {medium_events}/{total} sự kiện")
        print(f"   Còn ít (1-49%): {low_events}/{total} sự kiện")
        print(f"   Chưa có (0%): {empty_events}/{total} sự kiện")
    
    def _show_export_menu(self):
        """Menu xuất báo cáo"""
        print(f"\nXUẤT BÁO CÁO:")
        print("1. Báo cáo Excel (UTF-8 with BOM)")
        print("2. Báo cáo WPS (UTF-8 thuần)")
        print("3. Báo cáo đầy đủ (cả 2 format)")
        print("4. Báo cáo chi tiết người tham dự")
        print("0. Không xuất")
        
        choice = input("\nChọn (0-4): ").strip()
        
        if choice == '1':
            self._export_excel_report()
        elif choice == '2':
            self._export_wps_report()
        elif choice == '3':
            self._export_full_report()
        elif choice == '4':
            self._export_detailed_attendee_report()
        elif choice == '0':
            print("Không xuất báo cáo")
        else:
            print("Lựa chọn không hợp lệ")
    
    def _export_excel_report(self):
        """Xuất báo cáo Excel format"""
        try:
            filename = f"statistics_Excel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=',')
                
                # Header thông tin
                writer.writerow(['CAMPUS EVENT MANAGEMENT SYSTEM'])
                writer.writerow(['STATISTICS REPORT'])
                writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow([])
                
                # Thống kê tổng quan
                total_events = len(self.system.events)
                total_attendees = sum(len(e.attendees) for e in self.system.events.values())
                average = total_attendees / total_events if total_events > 0 else 0
                
                writer.writerow(['SUMMARY STATISTICS'])
                writer.writerow(['Total Events', str(total_events)])
                writer.writerow(['Total Attendees', str(total_attendees)])
                writer.writerow(['Average per Event', f"{average:.2f}"])
                writer.writerow([])
                
                # Chi tiết sự kiện
                writer.writerow(['EVENT DETAILS'])
                writer.writerow(['ID', 'Event Name', 'Date', 'Location', 'Registered', 'Capacity', 'Fill Rate (%)'])
                
                for event in self.system.events.values():
                    fill_rate = (len(event.attendees) / event.max_capacity) * 100
                    writer.writerow([
                        event.event_id, event.name, str(event.date), event.location,
                        str(len(event.attendees)), str(event.max_capacity), f"{fill_rate:.1f}"
                    ])
            
            print(f"Đã xuất báo cáo Excel: {filename}")
            return filename
            
        except Exception as e:
            print(f"Lỗi xuất báo cáo Excel: {e}")
            return None
    
    def _export_wps_report(self):
        """Xuất báo cáo WPS format"""
        try:
            filename = f"statistics_WPS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=',')
                
                # Header tiếng Việt
                writer.writerow(['HE THONG QUAN LY SU KIEN CAMPUS'])
                writer.writerow(['BAO CAO THONG KE'])
                writer.writerow(['Tao ngay:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow([])
                
                # Thống kê
                total_events = len(self.system.events)
                total_attendees = sum(len(e.attendees) for e in self.system.events.values())
                average = total_attendees / total_events if total_events > 0 else 0
                
                writer.writerow(['THONG KE TONG QUAN'])
                writer.writerow(['Tong so su kien', str(total_events)])
                writer.writerow(['Tong so nguoi tham du', str(total_attendees)])
                writer.writerow(['Trung binh moi su kien', f"{average:.2f}"])
                writer.writerow([])
                
                # Chi tiết
                writer.writerow(['CHI TIET SU KIEN'])
                writer.writerow(['ID', 'Ten su kien', 'Ngay', 'Dia diem', 'Da dang ky', 'Suc chua', 'Ty le (%)'])
                
                for event in self.system.events.values():
                    fill_rate = (len(event.attendees) / event.max_capacity) * 100
                    writer.writerow([
                        event.event_id, event.name, str(event.date), event.location,
                        str(len(event.attendees)), str(event.max_capacity), f"{fill_rate:.1f}"
                    ])
            
            print(f"Đã xuất báo cáo WPS: {filename}")
            return filename
            
        except Exception as e:
            print(f"Lỗi xuất báo cáo WPS: {e}")
            return None
    
    def _export_full_report(self):
        """Xuất báo cáo đầy đủ cả 2 format"""
        excel_file = self._export_excel_report()
        wps_file = self._export_wps_report()
        
        if excel_file and wps_file:
            print(f"Đã xuất báo cáo đầy đủ:")
            print(f"   - Excel: {excel_file}")
            print(f"   - WPS: {wps_file}")
    
    def _export_detailed_attendee_report(self):
        """Xuất báo cáo chi tiết người tham dự"""
        try:
            filename = f"attendee_details_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow(['DETAILED ATTENDEE REPORT'])
                writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow([])
                
                # Mỗi sự kiện một section
                for event in self.system.events.values():
                    writer.writerow([f'EVENT: {event.name}'])
                    writer.writerow(['Date:', str(event.date)])
                    writer.writerow(['Location:', event.location])
                    writer.writerow(['Registered:', f"{len(event.attendees)}/{event.max_capacity}"])
                    writer.writerow([])
                    
                    if event.attendees:
                        writer.writerow(['STT', 'Full Name', 'Email', 'Role'])
                        for i, user_id in enumerate(event.attendees, 1):
                            if user_id in self.system.users:
                                user = self.system.users[user_id]
                                writer.writerow([i, user.full_name, user.email, user.role])
                            else:
                                writer.writerow([i, 'Unknown User', 'N/A', 'Unknown'])
                    else:
                        writer.writerow(['No attendees yet'])
                    
                    writer.writerow([])  # Empty line between events
            
            print(f"Đã xuất báo cáo chi tiết: {filename}")
            return filename
            
        except Exception as e:
            print(f"Lỗi xuất báo cáo chi tiết: {e}")
            return None
    
    def _export_personal_report(self, my_events):
        """Xuất báo cáo cá nhân cho organizer"""
        try:
            user_name = self.system.current_user.full_name.replace(' ', '_')
            filename = f"my_events_{user_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow([f'PERSONAL EVENT REPORT - {self.system.current_user.full_name}'])
                writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow([])
                
                # Thống kê cá nhân
                total_events = len(my_events)
                total_attendees = sum(len(e.attendees) for e in my_events)
                avg_attendees = total_attendees / total_events if total_events > 0 else 0
                
                writer.writerow(['PERSONAL STATISTICS'])
                writer.writerow(['Total Events Organized', str(total_events)])
                writer.writerow(['Total Attendees', str(total_attendees)])
                writer.writerow(['Average per Event', f"{avg_attendees:.2f}"])
                writer.writerow([])
                
                # Chi tiết sự kiện
                writer.writerow(['MY EVENT DETAILS'])
                writer.writerow(['Event ID', 'Event Name', 'Date', 'Location', 'Attendees', 'Capacity', 'Fill Rate'])
                
                for event in my_events:
                    fill_rate = (len(event.attendees) / event.max_capacity) * 100
                    writer.writerow([
                        event.event_id, event.name, str(event.date), event.location,
                        str(len(event.attendees)), str(event.max_capacity), f"{fill_rate:.1f}%"
                    ])
            
            print(f"Đã xuất báo cáo cá nhân: {filename}")
            return filename
            
        except Exception as e:
            print(f"Lỗi xuất báo cáo cá nhân: {e}")
            return None