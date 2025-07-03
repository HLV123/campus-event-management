# menu_manager.py - Quản lý giao diện menu

class MenuManager:
    """Class quản lý các menu giao diện"""
    
    def __init__(self, system):
        self.system = system
    
    # ====================== ROLE SELECTION ======================
    
    def select_role(self):
        """Chọn vai trò để sử dụng hệ thống"""
        print("\n" + "="*50)
        print("CHỌN VAI TRÒ SỬ DỤNG HỆ THỐNG")
        print("="*50)
        print("1. Admin - Quản trị viên")
        print("2. Event Organizer - Người tổ chức sự kiện")
        print("3. Student - Sinh viên")
        print("4. Visitor - Khách mời")
        print("5. Xem thông tin hệ thống")
        print("0. Thoát")
        
        choice = input("\nChọn vai trò (0-5): ").strip()
        
        if choice == '1':
            self.system.current_role = "Admin"
            admin_users = [u for u in self.system.users.values() if u.role == "Admin"]
            self.system.current_user = admin_users[0] if admin_users else None
            return "Admin"
        elif choice == '2':
            self.system.current_role = "EventOrganizer"
            self.select_organizer()
            return "EventOrganizer"
        elif choice == '3':
            self.system.current_role = "Student"
            self.select_student()
            return "Student"
        elif choice == '4':
            self.system.current_role = "Visitor"
            self.select_visitor()
            return "Visitor"
        elif choice == '5':
            self.show_system_info()
            return None
        elif choice == '0':
            return "Exit"
        else:
            print("Lựa chọn không hợp lệ")
            return None
    
    def select_organizer(self):
        """Chọn organizer cụ thể"""
        organizers = [u for u in self.system.users.values() if u.role == "EventOrganizer"]
        if not organizers:
            print("Không có organizer nào")
            return
        
        print("\nChọn Organizer:")
        for i, org in enumerate(organizers, 1):
            print(f"{i}. {org.full_name} ({org.username})")
        
        try:
            choice = int(input("\nChọn organizer (số): ")) - 1
            self.system.current_user = organizers[choice]
            print(f"Đã chọn: {self.system.current_user.full_name}")
        except (ValueError, IndexError):
            print("Lựa chọn không hợp lệ")
            self.system.current_user = organizers[0]  # Default first organizer
    
    def select_student(self):
        """Chọn student cụ thể"""
        students = [u for u in self.system.users.values() if u.role == "Student"]
        if not students:
            print("Không có student nào")
            return
        
        print("\nChọn Student:")
        for i, student in enumerate(students, 1):
            print(f"{i}. {student.full_name} ({student.username})")
        
        try:
            choice = int(input("\nChọn student (số): ")) - 1
            self.system.current_user = students[choice]
            print(f"Đã chọn: {self.system.current_user.full_name}")
        except (ValueError, IndexError):
            print("Lựa chọn không hợp lệ")
            self.system.current_user = students[0]  # Default first student
    
    def select_visitor(self):
        """Chọn visitor cụ thể"""
        visitors = [u for u in self.system.users.values() if u.role == "Visitor"]
        if not visitors:
            print("Không có visitor nào")
            return
        
        print("\nChọn Visitor:")
        for i, visitor in enumerate(visitors, 1):
            print(f"{i}. {visitor.full_name} ({visitor.username})")
        
        try:
            choice = int(input("\nChọn visitor (số): ")) - 1
            self.system.current_user = visitors[choice]
            print(f"Đã chọn: {self.system.current_user.full_name}")
        except (ValueError, IndexError):
            print("Lựa chọn không hợp lệ")
            self.system.current_user = visitors[0]  # Default first visitor
    
    # ====================== MAIN MENUS ======================
    
    def admin_menu(self):
        """Menu cho Admin"""
        while True:
            print(f"\nADMIN DASHBOARD - {self.system.current_user.full_name}")
            print("="*40)
            print("1. Tạo sự kiện")
            print("2. Cập nhật sự kiện")
            print("3. Xóa sự kiện")
            print("4. Xem tất cả sự kiện")
            print("5. Xem tất cả người tham dự")
            print("6. Thống kê và báo cáo")
            print("7. Lưu dữ liệu")
            print("0. Quay lại")
            
            choice = input("\nChọn (0-7): ").strip()
            
            if choice == '1':
                self.system.event_ops.create_event()
            elif choice == '2':
                self.system.event_ops.update_event()
            elif choice == '3':
                self.system.event_ops.delete_event()
            elif choice == '4':
                self.system.view_ops.view_all_events()
            elif choice == '5':
                self.system.registration_mgr.view_all_attendees()
            elif choice == '6':
                self.system.stats_mgr.show_statistics()
            elif choice == '7':
                self.system.save_data()
            elif choice == '0':
                break
            else:
                print("Lựa chọn không hợp lệ")
    
    def organizer_menu(self):
        """Menu cho Event Organizer"""
        while True:
            print(f"\nORGANIZER DASHBOARD - {self.system.current_user.full_name}")
            print("="*40)
            print("1. Xem sự kiện của tôi")
            print("2. Quản lý đăng ký")
            print("3. Xem tất cả sự kiện")
            print("4. Thống kê sự kiện của tôi")
            print("0. Quay lại")
            
            choice = input("\nChọn (0-4): ").strip()
            
            if choice == '1':
                self.system.view_ops.view_my_events()
            elif choice == '2':
                self.system.registration_mgr.manage_registrations()
            elif choice == '3':
                self.system.view_ops.view_all_events()
            elif choice == '4':
                self.system.stats_mgr.show_my_event_statistics()
            elif choice == '0':
                break
            else:
                print("Lựa chọn không hợp lệ")
    
    def student_visitor_menu(self):
        """Menu cho Student/Visitor"""
        role_name = "STUDENT" if self.system.current_role == "Student" else "VISITOR"
        
        while True:
            print(f"\n{role_name} DASHBOARD - {self.system.current_user.full_name}")
            print("="*40)
            print("1. Xem sự kiện")
            print("2. Đăng ký sự kiện")
            print("3. Xem sự kiện đã đăng ký")
            print("4. Tìm kiếm sự kiện")
            print("0. Quay lại")
            
            choice = input("\nChọn (0-4): ").strip()
            
            if choice == '1':
                self.system.view_ops.view_all_events()
            elif choice == '2':
                self.system.registration_mgr.register_for_event()
            elif choice == '3':
                self.system.registration_mgr.view_my_registrations()
            elif choice == '4':
                self.system.search_mgr.search_events()
            elif choice == '0':
                break
            else:
                print("Lựa chọn không hợp lệ")
    
    # ====================== SYSTEM INFO ======================
    
    def show_system_info(self):
        """Hiển thị thông tin hệ thống"""
        print("\nTHÔNG TIN HỆ THỐNG")
        print("="*40)
        
        # Thống kê users theo role
        user_stats = {}
        for user in self.system.users.values():
            role = user.role
            user_stats[role] = user_stats.get(role, 0) + 1
        
        print("NGƯỜI DÙNG:")
        for role, count in user_stats.items():
            print(f"   {role}: {count} người")
        
        print(f"\nSỰ KIỆN: {len(self.system.events)} sự kiện có sẵn")
        
        total_attendees = sum(len(e.attendees) for e in self.system.events.values())
        print(f"ĐĂNG KÝ: {total_attendees} lượt tham gia")
        
        print("\nĐẶC ĐIỂM HỆ THỐNG:")
        print("- Không cần đăng nhập phức tạp")
        print("- 4 sự kiện có sẵn để demo")
        print("- Chọn vai trò trực tiếp để sử dụng")
        print("- Dữ liệu mẫu đầy đủ cho thử nghiệm")
        print("- Quản lý đầy đủ: Tạo, Cập nhật, Xóa sự kiện")
        print("- Báo cáo và thống kê chi tiết")
        
        print("\nPHÂN QUYỀN CHI TIẾT:")
        print("Admin:")
        print("   - Tạo, cập nhật, xóa sự kiện")
        print("   - Xem tất cả sự kiện và người tham dự")
        print("   - Thống kê và báo cáo toàn hệ thống")
        
        print("Event Organizer:")
        print("   - Xem sự kiện được phân công")
        print("   - Quản lý đăng ký cho sự kiện của mình")
        print("   - Thống kê sự kiện của mình")
        
        print("Student/Visitor:")
        print("   - Xem và tìm kiếm sự kiện")
        print("   - Đăng ký tham gia sự kiện")
        print("   - Xem lịch sử đăng ký")
        
        input("\nNhấn Enter để tiếp tục...")