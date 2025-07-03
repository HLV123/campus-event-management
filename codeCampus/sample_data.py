# sample_data.py - Simplified Sample Data (4 Events Ready)

from models import Admin, EventOrganizer, Student, Visitor, Event
from datetime import date, time
import uuid

def generate_id():
    """Tạo unique ID"""
    return str(uuid.uuid4())[:8]

def create_sample_users():
    """Tạo dữ liệu người dùng mẫu - không cần password"""
    users = {}
    
    # 1. ADMIN
    admin = Admin(
        user_id=generate_id(),
        username="admin",
        full_name="Quản trị viên Hệ thống",
        email="admin@campus.edu.vn"
    )
    users[admin.user_id] = admin
    
    # 2. EVENT ORGANIZERS (3 người)
    organizers_data = [
        {
            "username": "organizer1",
            "full_name": "Nguyễn Văn Tổ Chức",
            "email": "organizer1@campus.edu.vn"
        },
        {
            "username": "organizer2",
            "full_name": "Trần Thị Sự Kiện",
            "email": "organizer2@campus.edu.vn"
        },
        {
            "username": "organizer3",
            "full_name": "Lê Minh Hoạt Động",
            "email": "organizer3@campus.edu.vn"
        }
    ]
    
    for org_data in organizers_data:
        organizer = EventOrganizer(
            user_id=generate_id(),
            username=org_data["username"],
            full_name=org_data["full_name"],
            email=org_data["email"]
        )
        users[organizer.user_id] = organizer
    
    # 3. STUDENTS (3 người)
    students_data = [
        {
            "username": "student1",
            "full_name": "Phạm Văn Học",
            "email": "student1@campus.edu.vn"
        },
        {
            "username": "student2",
            "full_name": "Hoàng Thị Sinh Viên",
            "email": "student2@campus.edu.vn"
        },
        {
            "username": "student3",
            "full_name": "Vũ Minh Campus",
            "email": "student3@campus.edu.vn"
        }
    ]
    
    for std_data in students_data:
        student = Student(
            user_id=generate_id(),
            username=std_data["username"],
            full_name=std_data["full_name"],
            email=std_data["email"]
        )
        users[student.user_id] = student
    
    # 4. VISITORS (2 người)
    visitors_data = [
        {
            "username": "visitor1",
            "full_name": "Đặng Thị Khách Mời",
            "email": "visitor1@company.com"
        },
        {
            "username": "visitor2",
            "full_name": "Bùi Văn Doanh Nghiệp",
            "email": "visitor2@enterprise.vn"
        }
    ]
    
    for vis_data in visitors_data:
        visitor = Visitor(
            user_id=generate_id(),
            username=vis_data["username"],
            full_name=vis_data["full_name"],
            email=vis_data["email"]
        )
        users[visitor.user_id] = visitor
    
    return users

def create_4_sample_events(users):
    """Tạo 4 sự kiện mẫu có sẵn"""
    events = {}
    
    # Lấy organizer IDs
    organizer_ids = [user_id for user_id, user in users.items() 
                    if user.role == "EventOrganizer"]
    
    # 4 sự kiện mẫu
    events_data = [
        {
            "name": "Hội thảo Công nghệ AI 2025",
            "description": "Hội thảo về xu hướng phát triển trí tuệ nhân tạo trong năm 2025, chia sẻ kinh nghiệm từ các chuyên gia hàng đầu",
            "date": date(2025, 7, 15),
            "time": time(14, 0),
            "location": "Hội trường A - Tòa nhà Khoa học",
            "max_capacity": 100,
            "organizer_id": organizer_ids[0] if organizer_ids else generate_id()
        },
        {
            "name": "Workshop Lập trình Python",
            "description": "Workshop thực hành lập trình Python từ cơ bản đến nâng cao, phù hợp cho người mới bắt đầu",
            "date": date(2025, 7, 20),
            "time": time(9, 0),
            "location": "Phòng Lab 201 - Tòa nhà Công nghệ",
            "max_capacity": 30,
            "organizer_id": organizer_ids[1] if len(organizer_ids) > 1 else generate_id()
        },
        {
            "name": "Ngày hội Khởi nghiệp 2025",
            "description": "Sự kiện giao lưu, chia sẻ kinh nghiệm khởi nghiệp cho sinh viên với sự tham gia của các doanh nhân thành công",
            "date": date(2025, 7, 25),
            "time": time(8, 30),
            "location": "Sân vận động trường",
            "max_capacity": 200,
            "organizer_id": organizer_ids[2] if len(organizer_ids) > 2 else generate_id()
        },
        {
            "name": "Seminar Phát triển Nghề nghiệp",
            "description": "Hướng dẫn phát triển kỹ năng mềm, viết CV và phỏng vấn xin việc cho sinh viên sắp ra trường",
            "date": date(2025, 7, 10),
            "time": time(15, 30),
            "location": "Phòng hội thảo B - Tòa nhà Hành chính",
            "max_capacity": 80,
            "organizer_id": organizer_ids[0] if organizer_ids else generate_id()
        }
    ]
    
    # Tạo 4 events
    for event_data in events_data:
        event_id = generate_id()
        event = Event(
            event_id=event_id,
            name=event_data["name"],
            description=event_data["description"],
            date=event_data["date"],
            time=event_data["time"],
            location=event_data["location"],
            max_capacity=event_data["max_capacity"],
            organizer_id=event_data["organizer_id"]
        )
        events[event_id] = event
    
    return events

def create_sample_registrations(users, events):
    """Tạo một số registrations mẫu để demo"""
    # Lấy student và visitor IDs
    attendee_ids = [user_id for user_id, user in users.items() 
                   if user.role in ["Student", "Visitor"]]
    
    if not attendee_ids or not events:
        print("Không có attendees hoặc events để tạo registrations")
        return
    
    event_list = list(events.values())
    
    # Tạo sample registrations cho 4 events
    registrations_made = 0
    
    # Event 1 - đăng ký nhiều người (test highest attendance)
    for user_id in attendee_ids[:4]:  # Đăng ký 4/5 người
        try:
            event_list[0].add_attendee(user_id)
            registrations_made += 1
        except ValueError:
            pass
    
    # Event 2 - đăng ký ít người (test lowest attendance)
    try:
        event_list[1].add_attendee(attendee_ids[0])
        registrations_made += 1
    except ValueError:
        pass
    
    # Event 3 - đăng ký vừa phải (3 người)
    for user_id in attendee_ids[:3]:
        try:
            event_list[2].add_attendee(user_id)
            registrations_made += 1
        except ValueError:
            pass
    
    # Event 4 - đăng ký 2 người
    for user_id in attendee_ids[:2]:
        try:
            event_list[3].add_attendee(user_id)
            registrations_made += 1
        except ValueError:
            pass
    
    print(f"Đã tạo {registrations_made} registrations mẫu")

def initialize_sample_data():
    """Khởi tạo toàn bộ dữ liệu mẫu với 4 sự kiện có sẵn"""
    print("Đang tạo dữ liệu mẫu...")
    
    # Tạo users
    users = create_sample_users()
    print(f"Đã tạo {len(users)} users mẫu")
    
    # Tạo 4 events có sẵn
    events = create_4_sample_events(users)
    print(f"Đã tạo {len(events)} events có sẵn")
    
    # Tạo registrations mẫu
    create_sample_registrations(users, events)
    
    print("\nTóm tắt dữ liệu mẫu:")
    print(f"Users: {len(users)} (1 Admin, 3 Organizers, 3 Students, 2 Visitors)")
    print(f"Events: {len(events)} sự kiện có sẵn")
    
    total_attendees = sum(len(e.attendees) for e in events.values())
    print(f"Registrations: {total_attendees} lượt đăng ký")
    
    print("\nHệ thống đã sẵn sàng - không cần đăng nhập!")
    
    return users, events