from sqlalchemy import Column, Integer, String, DateTime, BLOB, ForeignKey, TEXT, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///test.db', echo=True)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    email = Column(String(250), nullable=False, unique=True)
    password_hash = Column(String(250), nullable=False)
    activation_link = Column(String(250), nullable=True, unique=True)
    created = Column(DateTime, nullable=False)
    failed_attempts = Column(Integer, nullable=False, default=0)

    files = relationship("File", cascade="all, delete-orphan")
    logs = relationship("Log", cascade="all, delete-orphan")
    fileShares = relationship("FileShare", cascade="all, delete-orphan")

    def __repr__(self):
        return "User: (id='%i', name='%s', email='%s', password_hash='%s', created='%s')" \
               % (self.id, self.name, self.email, self.password_hash, str(self.created))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)
    file_name = Column(String(250), nullable=False)
    path = Column(String(250), nullable=False)
    created = Column(DateTime, nullable=False)
    public_link = Column(String(250), nullable=True, unique=True)
    content = Column(TEXT, nullable=True)
    folder = Column(Integer, nullable=False)
    delete_date = Column(DateTime, nullable=True)

    fileShares = relationship("FileShare", cascade="all, delete-orphan")

    def __repr__(self):
        return "File: (id='%i', user_id='%i', file_name='%s', path='%s', created='%s', public_link='%s', content='%s', folder='%i', delete_date='%s')" \
               % (self.id, self.user_id, self.file_name, self.path,  str(self.created), self.public_link, self.content, self.folder, str(self.delete_date))

    def serialize(self):
        return{
            'id': self.id,
            'fileName': self.file_name,
            'created': self.created,
            'folder:': self.folder
        }


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    priority = Column(Integer, nullable=False)

    fileShares = relationship("FileShare", cascade="all, delete-orphan")

    def __repr__(self):
        return "Role: (id='%i', name='%s,', priority='%i')" \
                % (self.id, self.name, self.priority)

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name
        }


class Log(Base):
    __tablename__ = 'my_logger'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)
    trace = Column(TEXT, nullable=False)
    created = Column(DateTime, nullable=False)

    def __repr__(self):
        return "Log: (id='%i', user_id='%i', text='%s', created='%s')" \
               % (self.id, self.user_id, self.text,  str(self.created))


class FileShare(Base):
    __tablename__ = 'file_share'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    file = relationship(File)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship(Role)
    created = Column(DateTime, nullable=False)

    def __repr__(self):
        return "Note: (id='%i', user_id='%i', file_id='%i', role_id='%i', created='%s')" \
               % (self.id, self.user_id, self.file_id, self.role_id,str(self.created))


class CredentialStore(Base):
    __tablename__ = 'credential_store'

    id = Column(Integer, primary_key=True)
    environment = Column(String(250), nullable=False, unique=True)
    code = Column(String(250), nullable=False)

    def __repr__(self):
        return "Credential Store: (id='%i', environment='%s', code='%s')" \
                % (self.id, self.environment, self.code)


def init_db():
    Base.metadata.create_all(engine)
