from sqlmodel import SQLModel, create_engine, Session

# 1. Nombre del archivo físico
sqlite_file_name = "billetera_v2.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 2. El Motor (Engine)
engine = create_engine(sqlite_url)

def create_all_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
