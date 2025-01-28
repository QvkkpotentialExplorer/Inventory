from flask_login import UserMixin
from sqlalchemy import Column, String, CheckConstraint, Integer, orm
from werkzeug.security import generate_password_hash, check_password_hash

from data.data import Base


class User(Base,UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False,default='user')
    full_name = Column(String, nullable= True)
    email = Column(String)

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'user')", name="check_user_role"),
    )



    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)