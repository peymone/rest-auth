from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, Session, Mapped, mapped_column


# Configurate data base
DATABASE_URL = 'sqlite:///users.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()
session = Session(engine)


class User(Base):
    """User table model"""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


def init_db() -> None:
    """Create Data Base"""

    Base.metadata.create_all(engine)


def add_user(name: str, email: str, hashed_password: str) -> bool:
    """Insert new User to Data Base

    Args: 
        email (str): user email
        name (str): user name
        password (str): hashed user password

    Returns:
        bool: return True if data successfully added
    """

    user = User(name=name, email=email, password=hashed_password)
    result = True

    try:
        session.add(user)
        session.commit()

    except Exception as e:

        session.rollback()
        session.flush()
        result = False

    return result


def get_password(email: str) -> tuple[str, str]:
    statement = select(User.password).where(User.email == email)
    user = session.execute(statement).first()

    return user


if __name__ == '__main__':
    init_db()
