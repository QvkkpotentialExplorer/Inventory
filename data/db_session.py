import sqlalchemy as sa
import sqlalchemy.orm as orm

from data.data import Base as SqlAlchemyBase

__factory = None

def create_engine_and_session(db_file):
    """
    Создает подключение к базе данных и возвращает сессию.
    """
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    # Импортируем все модели для регистрации таблиц
    from . import __all_models

    # Создание таблиц вручную
    SqlAlchemyBase.metadata.create_all(engine)

    # Возвращаем сессию
    session = __factory()
    return session

db_sess =create_engine_and_session('./db/inventory_crm.db')