from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Model_Data_Setup import *

engine = create_engine('sqlite:///filmcameras.db')
''' Bind the engine to the metadata of the Base class so that the
 declaratives can be accessed through a DBSession instance'''
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete Filmy_Camera_type if exisitng.
session.query(Filmy_Camera_type).delete()
# Delete Filmy_cam_Name if exisitng.
session.query(Filmy_cam_Name).delete()
# Delete Google_Mail_user if exisitng.
session.query(Google_Mail_user).delete()

# Create sample users data
User1 = Google_Mail_user(name="ramya reddy",
                 email="ramyasunkara52@gmail.com",
                 picture='http://www.enchanting-costarica.com/wp-content/'
                 'uploads/2018/02/jcarvaja17-min.jpg')
session.add(User1)
session.commit()
print ("user successfully added")
# Create sample camera types
Cam_type1 = Filmy_Camera_type(name="SingleLensReflex Camera",
                     user_id=1)
session.add(Cam_type1)
session.commit()

Cam_type2 = Filmy_Camera_type(name="Range-Finder",
                     user_id=1)
session.add(Cam_type2)
session.commit

Cam_type3  = Filmy_Camera_type(name="TwinLens Reflex",
                     user_id=1)
session.add(Cam_type3)
session.commit()
Cam_type4 = Filmy_Camera_type(name="Stereo Cameras",
                     user_id=1)
session.add(Cam_type4)
session.commit()

Cam_type5 = Filmy_Camera_type(name="Instant Cameras",
                     user_id=1)
session.add(Cam_type5)
session.commit()
Cam_type6 = Filmy_Camera_type(name="Panoramic Cameras",
                     user_id=1)
session.add(Cam_type6)
session.commit()
Cam_type7  = Filmy_Camera_type(name="Folding Cameras",
                     user_id=1)
session.add(Cam_type7)
session.commit()
Cam_type8 = Filmy_Camera_type(name="Large Format Cameras",
                     user_id=1)
session.add(Cam_type8)
session.commit()

# Populare a  with models for testing
# Using different users for  names year also
Cam1 = Filmy_cam_Name(name="Canon",
                       cam_Model="EOS 1300D",
                       Dimension="7.8 x 12.9 x 10.1 cm",
                       Batteries="1 Lithium batteries required",
                       resolution="18",
                       screen_size="3 Inches",
                       conector_type="Wi-Fi,NFC",
                       camera_cost="40,000Rs",
                       voltage="7.4 Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=1,
                       user_id=1)
session.add(Cam1)
session.commit()
Cam2 = Filmy_cam_Name(name="Nikon",
                       cam_Model="Nik_D5300_18_55",
                       Dimension="7.6 x 12.5 x 9.8 cm",
                       Batteries="1 Lithium ion batteries required",
                       resolution="24.2 Megapixels",
                       screen_size="3.2 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="42,798Rs",
                       voltage="7.6 Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=1,
                       user_id=1)
session.add(Cam2)
session.commit()
Cam3 = Filmy_cam_Name(name="Sony",
                       cam_Model="DSC-H300B",
                       Dimension="9.2 x 12.8 x 8.9 cm",
                       Batteries="2 AA batteries required",
                       resolution="20.1 megapixels",
                       screen_size="3 Inches",
                       conector_type="usb",
                       camera_cost="14,400Rs",
                       voltage="7.2 Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=1,
                       user_id=1)
session.add(Cam3)
session.commit()
Cam4 = Filmy_cam_Name(name="Nikon",
                       cam_Model="BKA130YA",
                       Dimension="11 x 13 x 8 cm",
                       Batteries="1 CR2 batteries required. (included)",
                       resolution="18.1 megapixels",
                       screen_size="3.1Inches",
                       conector_type="Wi-fi",
                       camera_cost="17,987Rs",
                       voltage="7.4 Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=2,
                       user_id=1)
session.add(Cam4)
session.commit()
Cam5 = Filmy_cam_Name(name="Xummy",
                       cam_Model="198160",
                       Dimension="7.9 x 12.9 x 10.2 cm",
                       Batteries="1 Lithium ion batteries required",
                       resolution="19.2 megapixels",
                       screen_size="3 Inches",
                       conector_type="usb",
                       camera_cost="20,000Rs",
                       voltage="7.4 Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=2,
                       user_id=1)
session.add(Cam1)
session.commit()
Cam6 = Filmy_cam_Name(name="Fotodiox",
                       cam_Model="B-III-Cap-zetal",
                       Dimension="5 x 5 x 2.5 cm",
                       Batteries="No batteries required",
                       resolution="18.1mega pixels",
                       screen_size="3 Inches",
                       conector_type="Wi-fi",
                       camera_cost="16,000Rs",
                       voltage="7.4 Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=3,
                       user_id=1)
session.add(Cam6)
session.commit()
Cam7 = Filmy_cam_Name(name="Superheadz Blackbird",
                       cam_Model="Sundome Camera",
                       Dimension="18.2 x 13 x 12.2 cm",
                       Batteries="No batteries required",
                       resolution="21.1 megapixels",
                       screen_size="3.2 Inches",
                       conector_type="no connector",
                       camera_cost="33,345Rs",
                       voltage="7.3 Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=3,
                       user_id=1)
session.add(Cam7)
session.commit()
Cam8 = Filmy_cam_Name(name="myTVS",
                       cam_Model="TAV-40 + Sensor",
                       Dimension="25 x 21 x 18 cm",
                       Batteries="No batteries required",
                       resolution="18",
                       screen_size="3 Inches",
                       conector_type="Wi-Fi,NFC",
                       camera_cost="7,986Rs",
                       voltage="7.4 Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=4,
                       user_id=1)
session.add(Cam8)
session.commit()
Cam9 = Filmy_cam_Name(name="DULCET",
                       cam_Model="DC-9911TC",
                       Dimension="21.5 x 16.5 x 9.5 cm",
                       Batteries="No ion batteries required",
                       resolution="18",
                       screen_size="3 Inches",
                       conector_type="Wi-Fi,NFC",
                       camera_cost="5,568Rs",
                       voltage="7.4 Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=4,
                       user_id=1)
session.add(Cam9)
session.commit()
Cam10 = Filmy_cam_Name(name="Woodman",
                       cam_Model="S1",
                       Dimension="45.7 x 30.5 x 25 cm",
                       Batteries="No ion batteries required",
                       resolution="720p HD Ready Megapixels",
                       screen_size="7 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="10,000Rs",
                       voltage="7.2Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=4,
                       user_id=1)
session.add(Cam10)
session.commit()
Cam11 = Filmy_cam_Name(name="V.T.I.",
                       cam_Model="VTI002",
                       Dimension="20 x 20 x 8 cm",
                       Batteries="No batteries required",
                       resolution="1080p Full HD",
                       screen_size="3.1 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="4,678Rs",
                       voltage="7.4 Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=5,
                       user_id=1)
session.add(Cam11)
session.commit()
Cam12 = Filmy_cam_Name(name="Fuji",
                       cam_Model="Instax Square SQ6 Blush Gold",
                       Dimension="15.5x15.5x10.4cm",
                       Batteries="2 CR2batteries required",
                       resolution="21megapixels",
                       screen_size="3.1 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="7,490Rs",
                       voltage="7.2Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=5,
                       user_id=1)
session.add(Cam12)
session.commit()
Cam13 = Filmy_cam_Name(name="YAOJIN",
                       cam_Model="YAOJINJAS130-F01",
                       Dimension="19.2 x 19.2 x 9.4 cm",
                       Batteries="No batteries required",
                       resolution="21megapixels",
                       screen_size="3.1 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="7,490Rs",
                       voltage="7.2Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=6,
                       user_id=1)
session.add(Cam13)
session.commit()
Cam14 = Filmy_cam_Name(name="MSE",
                       cam_Model="DigitalCameraBinocular-A2",
                       Dimension="19.2 x 19.2 x 9.4 cm",
                       Batteries="No batteries required",
                       resolution="21megapixels",
                       screen_size="3.1 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="8,890Rs",
                       voltage="7.1Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=7,
                       user_id=1)
session.add(Cam14)
session.commit()
Cam15 = Filmy_cam_Name(name="HOLGA",
                       cam_Model="120N",
                       Dimension="25.4x21.3x15.7cm",
                       Batteries="No batteries required",
                       resolution="19megapixels",
                       screen_size="3.1 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="8,890Rs",
                       voltage="7.1Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=7,
                       user_id=1)
session.add(Cam15)
session.commit()
Cam16 = Filmy_cam_Name(name="Fuji",
                       cam_Model="120N",
                       Dimension="20.1x16.8x14.1 cm",
                       Batteries="No batteries required",
                       resolution="19megapixels",
                       screen_size="3.1 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="8,890Rs",
                       voltage="7.1Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=8,
                       user_id=1)
session.add(Cam16)
session.commit()
Cam16 = Filmy_cam_Name(name="Fuji",
                       cam_Model="120N",
                       Dimension="20.1x16.8x14.1 cm",
                       Batteries="No batteries required",
                       resolution="19megapixels",
                       screen_size="3.1 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="8,890Rs",
                       voltage="7.2Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=8,
                       user_id=1)
session.add(Cam16)
session.commit()

print("Your films database has been inserted!")
