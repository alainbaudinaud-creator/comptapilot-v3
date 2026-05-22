from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    users = relationship("User", back_populates="company")

    clients = relationship("Client", back_populates="company")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True)

    password = Column(String)

    role = Column(String, default="client")

    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="users")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    email = Column(String)

    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="clients")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    filename = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class SchedulerJob(Base):
    __tablename__ = "scheduler_jobs"

    id = Column(Integer, primary_key=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
