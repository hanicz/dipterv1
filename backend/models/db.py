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
    path = Column(String(250), nullable=False, unique=True)
    created = Column(DateTime, nullable=False)

    def __repr__(self):
        return "File: (id='%i', user_id='%i', file_name='%s', path='%s', created='%s')" \
               % (self.id, self.user_id, self.file_name, self.path,  str(self.created))


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


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)
    token = Column(String(250), nullable=False, unique=True)
    valid = Column(DateTime, nullable=False)

    def __repr__(self):
        return "Token: (id='%i', user_id='%i', token='%s', valid='%s')" \
               % (self.id, self.user_id, self.token,  str(self.valid))


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)
    content = Column(TEXT, nullable=False)
    created = Column(DateTime, nullable=False)

    def __repr__(self):
        return "Note: (id='%i', user_id='%i', content='%s', created='%s')" \
               % (self.id, self.user_id, self.content,  str(self.created))


class PublicLink(Base):
    __tablename__ = 'public_links'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    file = relationship(File)
    link = Column(String(250), nullable=False, unique=True)
    created = Column(DateTime, nullable=False)

    def __repr__(self):
        return "Public Link: (id='%i', file_id='%i', link='%s', created='%s')" \
               % (self.id, self.file_id, self.link,  str(self.created))


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)

    def __repr__(self):
        return "Role: (id='%i', name='%s')" \
                % (self.id, self.name)


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
    user = Column(String(250), nullable=False)
    code = Column(String(250), nullable=False)

    def __repr__(self):
        return "Credential Store: (id='%i', environment='%s', code='%s')" \
                % (self.id, self.environment, self.code)


def init_db():
    Base.metadata.create_all(engine)
