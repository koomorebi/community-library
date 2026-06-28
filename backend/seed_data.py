"""
社区图书馆借阅管理系统 - 示例数据生成脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from app.database import SessionLocal, engine, Base
from app.models.book import Book
from app.models.category import Category
from app.models.book_copy import BookCopy
from app.models.member import Member
from app.models.borrow import Borrow
from app.models.admin import Admin
import bcrypt

def create_sample_data():
    """生成示例数据"""
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        if db.query(Category).count() > 0:
            print("  ⚠️  数据库已有数据，跳过示例数据生成")
            return
        
        print("  📦 生成示例数据...")
        
        # 1. 创建管理员
        admin = Admin(
            username="admin",
            password_hash=bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            name="系统管理员"
        )
        db.add(admin)
        
        # 2. 创建分类
        categories_data = [
            ("文学小说", "中外文学经典及当代小说"),
            ("科技计算机", "计算机技术、编程、人工智能等"),
            ("历史传记", "历史著作、人物传记"),
            ("生活百科", "健康、美食、旅游、家庭教育"),
            ("少儿读物", "适合青少年阅读的书籍"),
            ("经济管理", "经济学、管理学、投资理财"),
            ("艺术设计", "绘画、摄影、音乐、设计"),
            ("自然科学", "物理、化学、生物、天文"),
        ]
        
        categories = []
        for name, desc in categories_data:
            cat = Category(name=name, description=desc)
            db.add(cat)
            categories.append(cat)
        db.flush()
        
        # 3. 创建图书
        books_data = [
            # 文学小说
            ("活着", "余华", "978-7-5063-6058-9", 0, 29.90, 3),
            ("百年孤独", "加西亚·马尔克斯", "978-7-5442-4528-9", 0, 39.50, 2),
            ("红楼梦", "曹雪芹", "978-7-0200-0220-8", 0, 59.80, 2),
            ("三体", "刘慈欣", "978-7-5366-9293-0", 0, 36.00, 3),
            ("围城", "钱钟书", "978-7-0200-2406-8", 0, 28.00, 2),
            
            # 科技计算机
            ("Python编程：从入门到实践", "Eric Matthes", "978-7-1154-2533-6", 1, 89.00, 3),
            ("深入理解计算机系统", "Randal E. Bryant", "978-7-1115-4105-0", 1, 139.00, 2),
            ("算法导论", "Thomas H. Cormen", "978-7-1114-0054-8", 1, 128.00, 2),
            ("JavaScript高级程序设计", "Matt Frisbie", "978-7-1155-4537-2", 1, 99.00, 2),
            
            # 历史传记
            ("史记", "司马迁", "978-7-1010-0314-2", 2, 68.00, 2),
            ("人类简史", "尤瓦尔·赫拉利", "978-7-5086-4675-0", 2, 49.80, 3),
            ("万历十五年", "黄仁宇", "978-7-1080-0491-3", 2, 28.00, 2),
            
            # 生活百科
            ("活着为了讲述", "加西亚·马尔克斯", "978-7-5442-7061-2", 3, 35.00, 2),
            ("饮食术", "牧田善二", "978-7-5086-8745-3", 3, 42.00, 2),
            
            # 少儿读物
            ("小王子", "安托万·德·圣-埃克苏佩里", "978-7-0201-0687-5", 4, 22.00, 3),
            ("哈利·波特与魔法石", "J.K.罗琳", "978-7-0201-0330-0", 4, 35.00, 2),
            
            # 经济管理
            ("经济学原理", "曼昆", "978-7-3012-5630-5", 5, 88.00, 2),
            ("从零到一", "彼得·蒂尔", "978-7-5086-5169-9", 5, 39.80, 2),
            
            # 艺术设计
            ("设计中的设计", "原研哉", "978-7-5495-1245-6", 6, 48.00, 2),
            
            # 自然科学
            ("时间简史", "斯蒂芬·霍金", "978-7-5357-1870-5", 7, 38.00, 2),
        ]
        
        books = []
        for title, author, isbn, cat_idx, price, copies in books_data:
            book = Book(
                title=title,
                author=author,
                isbn=isbn,
                category_id=categories[cat_idx].id,
                price=price,
                description=f"《{title}》是{author}的经典之作"
            )
            db.add(book)
            db.flush()
            
            # 创建副本
            for i in range(copies):
                copy = BookCopy(
                    book_id=book.id,
                    copy_code=f"{book.id:03d}-{i+1:02d}",
                    status="available"
                )
                db.add(copy)
            
            books.append(book)
        
        # 4. 创建会员
        members_data = [
            ("张三", "13800138001", "北京市朝阳区建国路88号", "zhangsan@email.com"),
            ("李四", "13900139002", "北京市海淀区中关村大街1号", "lisi@email.com"),
            ("王五", "13700137003", "北京市西城区西单北大街1号", "wangwu@email.com"),
            ("赵六", "13600136004", "北京市东城区东单北大街1号", "zhaoliu@email.com"),
            ("孙七", "13500135005", "北京市丰台区丰台路1号", "sunqi@email.com"),
            ("周八", "13400134006", "北京市石景山区石景山路1号", "zhouba@email.com"),
            ("吴九", "13300133007", "北京市通州区新华大街1号", "wujiu@email.com"),
            ("郑十", "13200132008", "北京市大兴区兴丰大街1号", "zhengshi@email.com"),
            ("钱十一", "13100131009", "北京市顺义区府前街1号", "qian11@email.com"),
            ("陈十二", "13000130010", "北京市昌平区政府街1号", "chen12@email.com"),
        ]
        
        members = []
        for name, phone, address, email in members_data:
            member = Member(
                name=name,
                phone=phone,
                address=address,
                email=email,
                member_type="regular"
            )
            db.add(member)
            members.append(member)
        db.flush()
        
        # 5. 创建借阅记录
        now = datetime.now()
        
        # 获取所有可用副本
        available_copies = db.query(BookCopy).filter(BookCopy.status == "available").all()
        copy_idx = 0
        
        # 已归还的记录 (7条)
        for i in range(7):
            if copy_idx >= len(available_copies):
                break
            copy = available_copies[copy_idx]
            member = members[i % len(members)]
            borrow_date = now - timedelta(days=30 - i*3)
            due_date = borrow_date + timedelta(days=30)
            return_date = borrow_date + timedelta(days=10 + i*2)
            
            borrow = Borrow(
                book_copy_id=copy.id,
                member_id=member.id,
                borrow_date=borrow_date,
                due_date=due_date,
                return_date=return_date,
                status="returned"
            )
            db.add(borrow)
            copy_idx += 1
        
        # 借阅中的记录 (5条)
        for i in range(5):
            if copy_idx >= len(available_copies):
                break
            copy = available_copies[copy_idx]
            member = members[(i + 3) % len(members)]
            borrow_date = now - timedelta(days=15 - i*2)
            due_date = borrow_date + timedelta(days=30)
            
            borrow = Borrow(
                book_copy_id=copy.id,
                member_id=member.id,
                borrow_date=borrow_date,
                due_date=due_date,
                status="borrowed"
            )
            db.add(borrow)
            copy.status = "borrowed"
            copy_idx += 1
        
        # 逾期的记录 (3条)
        for i in range(3):
            if copy_idx >= len(available_copies):
                break
            copy = available_copies[copy_idx]
            member = members[(i + 7) % len(members)]
            borrow_date = now - timedelta(days=45 + i*5)
            due_date = borrow_date + timedelta(days=30)
            
            borrow = Borrow(
                book_copy_id=copy.id,
                member_id=member.id,
                borrow_date=borrow_date,
                due_date=due_date,
                status="overdue"
            )
            db.add(borrow)
            copy.status = "borrowed"
            copy_idx += 1
        
        db.commit()
        
        print(f"  ✅ 生成完成：")
        print(f"     - 1 个管理员 (admin/admin123)")
        print(f"     - {len(categories)} 个分类")
        print(f"     - {len(books)} 本图书")
        print(f"     - {len(members)} 个会员")
        print(f"     - 15 条借阅记录")
        
    except Exception as e:
        db.rollback()
        print(f"  ❌ 生成失败：{e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
