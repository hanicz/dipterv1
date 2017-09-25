from sqlalchemy import Column, Integer, String, DateTime, BLOB, ForeignKey, TEXT, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///test.db', echo=True)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    email = Column(String(250), nullable=False, unique=True)
    password_hash = Column(String(250), nullable=False)
    activation_link = Column(String(250), nullable=True, unique=True)
    created = Column(DateTime, nullable=False)
    failed_attempts = Column(Integer, nullable=False, default=0)
    dropbox_auth = Column(String(250), nullable=True)
    main_folder = Column(Integer, nullable=True)


    files = relationship("File", cascade="all, delete-orphan")
    logs = relationship("Log", cascade="all, delete-orphan")
    fileShares = relationship("FileShare", cascade="all, delete-orphan")
    folders = relationship("Folder", cascade="all, delete-orphan")

    def __repr__(self):
        return "User: (id='%i', name='%s', email='%s', password_hash='%s', created='%s')" \
               % (self.id, self.name, self.email, self.password_hash, str(self.created))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'folder': self.main_folder
        }


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    file_name = Column(String(250), nullable=True)
    system_file_name = Column(String(250), nullable=True)
    created = Column(DateTime, nullable=False)
    public_link = Column(String(250), nullable=True, unique=True)
    content = Column(TEXT, nullable=True)
    folder_id = Column(Integer, ForeignKey('folder.id'))
    delete_date = Column(DateTime, nullable=True)
    version = Column(Integer, nullable=False)

    fileShares = relationship("FileShare", cascade="all, delete-orphan")
    logs = relationship("Log", cascade="all, delete-orphan")

    '''def __repr__(self):
        return "File: (id='%i', user_id='%i', file_name='%s', created='%s', public_link='%s', " \
               "content='%s', folder='%i', delete_date='%s', system_file_name='%s')" \
               % (int(self.id), int(self.user_id), self.file_name, str(self.created), self.public_link, self.content,
                  self.folder, str(self.delete_date), self.system_file_name)'''

    def serialize(self):
        return{
            'id': self.id,
            'fileName': self.file_name,
            'created': self.created,
            'folder': self.folder_id,
            'content': self.content,
            'deleted': self.delete_date,
            'version': self.version,
            'publicLink': self.public_link
        }


class Folder(Base):
    __tablename__ = 'folder'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    parent_folder = Column(Integer, ForeignKey('folder.id'))
    folder = relationship('Folder', remote_side=[id])
    folder_name = Column(String(250), nullable=True)
    path = Column(String(250), nullable=True)
    created = Column(DateTime, nullable=False)
    delete_date = Column(DateTime, nullable=True)

    files = relationship("File", cascade="all, delete-orphan")
    logs = relationship("Log", cascade="all, delete-orphan")
    folders = relationship("Folder", cascade="all, delete-orphan")

    '''def __repr__(self):
        return "Folder: (id='%i', user_id='%i', parent_folder='%i', path='%s', created='%s', folder_name='%s', " \
               "delete_date='%s')" \
               % (int(self.id), int(self.user_id), int(self.parent_folder), self.path,  str(self.created), self.folder_name,
                  str(self.delete_date))'''

    def serialize(self):
        return{
            'id': self.id,
            'created': self.created,
            'folderName': self.folder_name,
            'parent': self.parent_folder
        }


class Role(Base):
    __tablename__ = 'role'

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
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    message = Column(TEXT, nullable=False)
    file_id = Column(Integer, ForeignKey('file.id'))
    file = relationship(File)
    folder_id = Column(Integer, ForeignKey('folder.id'))
    folder = relationship(Folder)
    created = Column(DateTime, nullable=False)

    def __repr__(self):
        return "Log: (id='%i', user_id='%i', text='%s', created='%s')" \
               % (self.id, self.user_id, self.text,  str(self.created))

    def serialize(self):
        return{
            'user': self.user_id,
            'message': self.message,
            'file': self.file_id,
            'folder': self.folder_id,
            'created': self.created
        }


class FileShare(Base):
    __tablename__ = 'file_share'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('file.id'))
    file = relationship(File)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    role_id = Column(Integer, ForeignKey('role.id'))
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
