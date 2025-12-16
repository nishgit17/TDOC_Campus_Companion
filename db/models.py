"""
╔══════════════════════════════════════════════════════════════════════════╗
║                       DATABASE MODELS                                    ║
║                  Table Definitions Using SQLModel                        ║
╚══════════════════════════════════════════════════════════════════════════╝

📁 FILE ROLE IN PROJECT:
─────────────────────────────────────────────────────────────────────────
This file defines the DATABASE SCHEMA for the Campus Companion system.
Each class represents a table, and each class attribute represents a column.
SQLModel automatically converts these Python classes into SQL tables.

🔗 HOW IT FITS IN THE ARCHITECTURE:
─────────────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  [1] MODELS (THIS FILE) ← Database Structure                        │
│      • Defines what data can be stored                              │
│      • Defines relationships between tables                         │
│       ↓                                                             │
│  [2] SESSION (db/session.py)                                        │
│      • Reads these models                                           │
│      • Creates actual tables in SQLite                              │
│       ↓                                                             │
│  [3] API ROUTES (api/routers/chat.py)                               │
│      • Uses these models to query database                          │
│      • Example: session.query(Faculty).filter(...)                  │
│       ↓                                                             │
│  [4] DATABASE FILE (campus_companion.db)                            │
│      • Physical SQLite file with actual data                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

🎯 WHAT THIS FILE DOES:
─────────────────────────────────────────────────────────────────────────
1. Defines 10 database tables for campus data
2. Specifies columns, types, and constraints for each table
3. Provides type hints for better code completion and error checking
4. Auto-generates SQL CREATE TABLE statements via SQLModel

📊 DATABASE TABLES DEFINED HERE:
─────────────────────────────────────────────────────────────────────────
1. User         - Student/admin accounts
2. Faculty      - Professor information
3. Canteen      - Campus food outlet contacts
4. Warden       - Hostel warden information
5. Building     - Campus building data
6. Room         - Individual room locations
7. MessMenu     - Daily hostel food schedules
8. Document     - Uploaded PDFs and files
9. Notice       - Campus announcements
10. Embedding   - AI vector embeddings (for RAG)

🔑 KEY CONCEPTS:
─────────────────────────────────────────────────────────────────────────
SQLModel = Pydantic + SQLAlchemy
  • Type validation (ensures correct data types)
  • Auto-generates database tables
  • Works with FastAPI seamlessly

Field Types:
  • Optional[int] = Can be None (nullable column)
  • str = Required string (NOT NULL)
  • datetime = Timestamp with date + time
  • date = Date only (no time)
  • dict = JSON object stored in database

Field() Parameters:
  • default=None: Column can be empty
  • primary_key=True: Unique identifier for each row
  • default_factory=datetime.utcnow: Auto-set to current time

💡 EXAMPLE USAGE:
─────────────────────────────────────────────────────────────────────────
Creating a new faculty record:

    from db.models import Faculty
    from db.session import SessionLocal
    
    # Create a new faculty entry
    new_faculty = Faculty(
        name="Dr. John Doe",
        department="Computer Science",
        office_location="AB-301",
        email="john.doe@nitdgp.ac.in",
        phone="+91-9876543210"
    )
    
    # Save to database
    session = SessionLocal()
    session.add(new_faculty)
    session.commit()

Querying faculty:

    from sqlmodel import select
    
    # Find all CS department faculty
    statement = select(Faculty).where(Faculty.department == "Computer Science")
    results = session.exec(statement).all()

🔧 HOW TO MODIFY:
─────────────────────────────────────────────────────────────────────────
Adding a new table:
1. Create a new class inheriting from SQLModel
2. Add table=True parameter
3. Define columns as class attributes
4. Run init_db() to create the table

Example:
    class Student(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        roll_no: str
        name: str
        email: str

Adding a column to existing table:
1. Add attribute to the class
2. Drop old table or use Alembic migrations
3. Re-run init_db()

📝 IMPORTANT NOTES:
─────────────────────────────────────────────────────────────────────────
• These are just DEFINITIONS - no data stored here
• Actual data lives in campus_companion.db file
• Changes here require database re-initialization
• Use Optional[] for nullable columns, plain type for required
"""




# IMPORTING REQUIRED MODULES








# WE WILL START CREATING DATABASE TABLES NOW

# ============================================================================
# USER MODEL
# ============================================================================







# ============================================================================
# FACULTY MODEL
# ============================================================================







# ============================================================================
# CANTEEN MODEL
# ============================================================================







# ============================================================================
# WARDEN MODEL
# ============================================================================








# ============================================================================
# BUILDING MODEL
# ============================================================================








# ============================================================================
# ROOM MODEL
# ============================================================================








# ============================================================================
# DOCUMENT MODEL
# ============================================================================







# ============================================================================
# NOTICE MODEL
# ============================================================================









# ============================================================================
# EMBEDDING MODEL
# ============================================================================









