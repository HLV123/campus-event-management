# file_manager.py - File Operations

import csv
import json
from datetime import datetime

class FileManager:
    """Quản lý file operations"""
    
    def save_events_to_csv(self, events):
        """Lưu events data vào CSV file với encoding đúng"""
        try:
            with open('events.csv', 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                
                # Header
                writer.writerow([
                    'event_id', 'name', 'description', 'date', 'time', 
                    'location', 'max_capacity', 'organizer_id', 'attendees'
                ])
                
                # Data rows
                for event in events.values():
                    attendees_str = ';'.join(event.attendees) if event.attendees else ''
                    writer.writerow([
                        event.event_id, 
                        event.name, 
                        event.description,
                        str(event.date), 
                        str(event.time), 
                        event.location,
                        event.max_capacity, 
                        event.organizer_id, 
                        attendees_str
                    ])
            
            print(f"Đã lưu {len(events)} events vào events.csv")
            return True
            
        except Exception as e:
            print(f"Lỗi lưu events: {e}")
            return False
    
    def save_users_to_csv(self, users):
        """Lưu users data vào CSV file với encoding đúng"""
        try:
            with open('users.csv', 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                
                # Header
                writer.writerow(['user_id', 'username', 'full_name', 'email', 'role'])
                
                # Data rows
                for user in users.values():
                    writer.writerow([
                        user.user_id, 
                        user.username, 
                        user.full_name,
                        user.email, 
                        user.role
                    ])
            
            print(f"Đã lưu {len(users)} users vào users.csv")
            return True
            
        except Exception as e:
            print(f"Lỗi lưu users: {e}")
            return False
    
    def export_statistics_csv(self, events):
        """Xuất báo cáo thống kê ra CSV tương thích Excel và WPS"""
        try:
            filename = f"statistics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Tạo 2 phiên bản: Excel và WPS
            # Phiên bản cho Excel (UTF-8 with BOM)
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                
                # Tính toán thống kê
                total_events = len(events)
                total_attendees = sum(len(event.attendees) for event in events.values())
                average = total_attendees / total_events if total_events > 0 else 0
                
                # Thống kê tổng quan (tiếng Anh cho Excel)
                writer.writerow(['STATISTICS SUMMARY'])
                writer.writerow(['Total Events', str(total_events)])
                writer.writerow(['Total Attendees', str(total_attendees)])
                writer.writerow(['Average Attendees per Event', f"{average:.2f}"])
                writer.writerow([''])
                
                # Tìm sự kiện có attendance cao nhất và thấp nhất
                if events:
                    max_event = max(events.values(), key=lambda e: len(e.attendees))
                    min_event = min(events.values(), key=lambda e: len(e.attendees))
                    
                    writer.writerow(['MOST POPULAR EVENT'])
                    writer.writerow(['Event Name', max_event.name])
                    writer.writerow(['Attendees', str(len(max_event.attendees))])
                    writer.writerow([''])
                    
                    writer.writerow(['LEAST POPULAR EVENT'])
                    writer.writerow(['Event Name', min_event.name])
                    writer.writerow(['Attendees', str(len(min_event.attendees))])
                    writer.writerow([''])
                
                # Chi tiết từng sự kiện
                writer.writerow(['EVENT DETAILS'])
                writer.writerow([
                    'ID', 'Event Name', 'Date', 'Registered', 
                    'Capacity', 'Fill Rate (%)'
                ])
                
                for event in events.values():
                    fill_rate = (len(event.attendees) / event.max_capacity) * 100
                    writer.writerow([
                        event.event_id, 
                        event.name, 
                        str(event.date),
                        str(len(event.attendees)), 
                        str(event.max_capacity), 
                        f"{fill_rate:.1f}"
                    ])
            
            # Tạo phiên bản WPS (UTF-8 thuần)
            filename_wps = f"statistics_report_WPS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename_wps, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=',')
                
                # Thống kê tổng quan (tiếng Việt cho WPS)
                writer.writerow(['THONG KE TONG QUAN'])
                writer.writerow(['Tong so su kien', str(total_events)])
                writer.writerow(['Tong so nguoi tham du', str(total_attendees)])
                writer.writerow(['Trung binh nguoi/su kien', f"{average:.2f}"])
                writer.writerow([''])
                
                if events:
                    max_event = max(events.values(), key=lambda e: len(e.attendees))
                    min_event = min(events.values(), key=lambda e: len(e.attendees))
                    
                    writer.writerow(['SU KIEN PHO BIEN NHAT'])
                    writer.writerow(['Ten su kien', max_event.name])
                    writer.writerow(['So nguoi tham du', str(len(max_event.attendees))])
                    writer.writerow([''])
                    
                    writer.writerow(['SU KIEN IT QUAN TAM NHAT'])
                    writer.writerow(['Ten su kien', min_event.name])
                    writer.writerow(['So nguoi tham du', str(len(min_event.attendees))])
                    writer.writerow([''])
                
                # Chi tiết từng sự kiện
                writer.writerow(['CHI TIET TUNG SU KIEN'])
                writer.writerow([
                    'ID', 'Ten su kien', 'Ngay', 'Da dang ky', 
                    'Suc chua', 'Ty le (%)'
                ])
                
                for event in events.values():
                    fill_rate = (len(event.attendees) / event.max_capacity) * 100
                    writer.writerow([
                        event.event_id, 
                        event.name, 
                        str(event.date),
                        str(len(event.attendees)), 
                        str(event.max_capacity), 
                        f"{fill_rate:.1f}"
                    ])
            
            print(f"Đã xuất báo cáo:")
            print(f"   - Cho Excel: {filename}")
            print(f"   - Cho WPS: {filename_wps}")
            return filename
            
        except Exception as e:
            print(f"Lỗi xuất báo cáo: {e}")
            return None
    
    def save_all_data(self, users, events):
        """Lưu tất cả dữ liệu"""
        success = True
        
        if not self.save_users_to_csv(users):
            success = False
        
        if not self.save_events_to_csv(events):
            success = False
        
        if success:
            print("Đã lưu tất cả dữ liệu thành công")
        else:
            print("Có lỗi khi lưu dữ liệu")
        
        return success