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
    name: Mapped[str] = mapped_column(unique=True)
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
    user_id = None

    try:
        session.add(user)
        session.commit()
        user_id = user.id

    except Exception as e:

        session.rollback()
        session.flush()

    return user_id


def get_user_by_name(name: str) -> tuple[int, str, str]:
    """Get User data from DB by name

    Args:
        name (str): user name

    Returns:
        tuple[int, str, str]: user_id, user_email, user_password
    """

    statement = select(User.id, User.email, User.password).where(User.name == name)
    user = session.execute(statement).first()

    return user


def get_user_by_id(id: int) -> tuple[str, str, str]:
    """Get User data from DB by id

    Args:
        id (int): user id

    Returns:
        tuple[str, str]: user_name, user_email, user_password
    """

    statement = select(User.name, User.email, User.password).where(User.id == id)
    user = session.execute(statement).first()

    return user


if __name__ == '__main__':
    init_db()
