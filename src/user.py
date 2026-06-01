from auth import hash_password, is_correct_password
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    username = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fornavn = db.Column(db.String(100), nullable=False)
    etternavn = db.Column(db.String(100), nullable=False)

    def __init__(self, username: str, password: str, fornavn: str, etternavn: str):
        self.username = username.lower()
        self.password = hash_password(password, self.username)
        self.fornavn = fornavn
        self.etternavn = etternavn

    def check_password(self, password: str) -> bool:
        return is_correct_password(password, self.username, self.password)

    @property
    def fullt_navn(self):
        return f"{self.fornavn} {self.etternavn}"

    def save_to_db(self):
        """Add user to database session and commit"""
        db.session.add(self)
        db.session.commit()

def get_all() -> dict[str, User]:
    """Fetch all users and return as dictionary"""
    users = User.query.all()
    return {user.username: user for user in users}

def get(username: str):
    """Get a specific user by username"""
    user = User.query.filter_by(username=username.lower()).first()
    if not user:
        raise ValueError(f"User {username} not found")
    return user

def init_db():
    """Initialize database tables"""
    db.create_all()
    print("Database tables created/verified")
