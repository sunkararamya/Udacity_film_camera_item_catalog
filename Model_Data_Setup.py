import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String,VARCHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class Google_Mail_user(Base):
    __tablename__ = 'google_mail_user'
    r_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(246), nullable=False)
    picture=Column(String(250))
class Filmy_Camera_type(Base):
    __tablename__ = 'filmcameratype'
    r_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('google_mail_user.r_id'))
    user = relationship(Google_Mail_user, backref="filmcameratype")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'r_id': self.r_id
        }


class Filmy_cam_Name(Base):
    __tablename__ = 'filmycamname'
    r_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(350), nullable=False)
    cam_Model = Column(VARCHAR(150))
    Dimension = Column(VARCHAR(150))
    Batteries= Column(VARCHAR(150))
    resolution = Column(VARCHAR(10))
    screen_size= Column(VARCHAR(250))
    conector_type=Column(VARCHAR(250))
    camera_cost=Column(VARCHAR(250))
    voltage=Column(VARCHAR(250))
    date = Column(DateTime, nullable=False)
    filmcameratypeid = Column(Integer, ForeignKey('filmcameratype.r_id'))
    filmcameratype = relationship(
        Filmy_Camera_type, backref=backref('filmycamname', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('google_mail_user.r_id'))
    user = relationship(Google_Mail_user, backref="filmycamname")

    @property
    def serialize(self):
        """ This method is used to return objects data in easily serializeable formats"""
        return {
            'name': self.name ,
            'cam_Model': self. cam_Model,
            'Dimension': self. Dimension,
            'Batteries': self. Batteries,
            'resolution': self. resolution,
            'screen_size': self. screen_size,
            'conector_type':self.conector_type,
            'camera_cost':self.camera_cost,
            'voltage':self.voltage,
            'date': self. date,
            'r_id': self.r_id
        }
engine_1 = create_engine('sqlite:///filmcameras.db')
Base.metadata.create_all(engine_1)
