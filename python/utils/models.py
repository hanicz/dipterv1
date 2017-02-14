from sqlalchemy import Column, Integer, String, DateTime, BLOB, ForeignKey, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password_hash = Column(BLOB, nullable=False)
    created = Column(DateTime, nullable=False)

    def __repr__(self):
        return "User: (id='%i', name='%s', email='%s', password_hash='%s', created='%s')" \
               % (self.id, self.name, self.email, self.password_hash, str(self.created))


class InactiveUser(Base):
    __tablename__ = 'inactive_users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password_hash = Column(BLOB, nullable=False)
    activation_link = Column(BLOB, nullable=False)
    created = Column(DateTime, nullable=False)

    def __repr__(self):
        return "Inactive User: (id='%i', name='%s', email='%s', activation_link='%s' password_hash='%s', created='%s')" \
               % (self.id, self.name, self.email, self.activation_link, self.password_hash, str(self.created))


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)
    file_name = Column(String(250), nullable=False)
    path = Column(String(250), nullable=False)
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
    token = Column(String(250), nullable=False)
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
    link = Column(String(250), nullable=False)
    created = Column(DateTime, nullable=False)

    def __repr__(self):
        return "Public Link: (id='%i', file_id='%i', link='%s', created='%s')" \
               % (self.id, self.file_id, self.link,  str(self.created))


class FileShare(Base):
    __tablename__ = 'file_share'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    file = relationship(File)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)
    created = Column(DateTime, nullable=False)

    def __repr__(self):
        return "Note: (id='%i', user_id='%i', file_id='%i', created='%s')" \
               % (self.id, self.user_id, self.file_id, str(self.created))

'''    engine = create_engine('sqlite:///test.db', echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    asd23 = User(name='asd', email='asd', password_hash='asd', created=datetime.datetime.now())
    session.add(asd23)
    session.commit()

    q = session.query(User).all()

    for user in q:
        print user'''