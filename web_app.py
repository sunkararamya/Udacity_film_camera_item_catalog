from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Model_Data_Setup import  Base,Filmy_Camera_type,Filmy_cam_Name,Google_Mail_user
from flask import session as signin_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime
#creating database in sqlite
engine_1 = create_engine('sqlite:///filmcameras.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine_1)
DBSession = sessionmaker(bind=engine_1)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Film Camera Hub"

DBSession = sessionmaker(bind=engine_1)
session = DBSession()
#  It is for Creating anti-forgery state token
fct_tcs = session.query(Filmy_Camera_type).all()


#gmail user signin
@app.route('/signin')
def displaysignin():
    
    cur_state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    signin_session['cur_state'] = cur_state
    # return "The current session state is %s" % signin_session['cur_state']
    fct_tcs = session.query(Filmy_Camera_type).all()
    fctes = session.query(Filmy_cam_Name).all()
    return render_template('signin.html',
                           STATE=cur_state, fct_tcs=fct_tcs, fctes=fctes)
    # return render_template('myhome.html', STATE=cur_state
    # fct_tcs=fct_tcs,fctes=fctes)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # state token validating
    if request.args.get('cur_state') != signin_session['cur_state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtaining authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Checking that the access token is valid or not.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If access token info is invalid, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify if that the access token is used for the intended user or not.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verifying that the access token is valid or not for this itemapp.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client  ID is does not matching app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = signin_session.get('access_token')
    stored_gplus_id = signin_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user was already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    signin_session['access_token'] = credentials.access_token
    signin_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    signin_session['username'] = data['name']
    signin_session['picture'] = data['picture']
    signin_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(signin_session['email'])
    if not user_id:
        user_id = createUser(signin_session)
    signin_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += signin_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += signin_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % signin_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(signin_session):
    User1 = Google_Mail_user(name=signin_session['username'], email=signin_session[
                   'email'], picture=signin_session['picture'])
    session.add(User1)
    session.commit()
    user = session.query(Google_Mail_user).filter_by(email=signin_session['email']).one()
    return user.r_id


def getUserInfo(user_id):
    user = session.query(Google_Mail_user).filter_by(r_id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(Google_Mail_user).filter_by(email=email).one()
        return user.r_id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their signin_session
# connecting to Home
@app.route('/')
@app.route('/home')
def home():
    fct_tcs = session.query(Filmy_Camera_type).all()
    return render_template('myhome.html', fct_tcs=fct_tcs)


# camera hub  for admins
@app.route('/CameraHub')
def CameraHub():
    try:
        if signin_session['username']:
            name = signin_session['username']
            fct_tcs = session.query(Filmy_Camera_type).all()
            fcts = session.query(Filmy_Camera_type).all()
            fctes = session.query(Filmy_cam_Name).all()
            return render_template('myhome.html', fct_tcs=fct_tcs,
                                   fcts=fcts, fctes=fctes, uname=name)
    except:
        return redirect(url_for('displaysignin'))

######
# Showing film_cameras based on Camera category
@app.route('/CameraHub/<int:fctid>/AllCompanys')
def displayCameras(fctid):
    fct_tcs = session.query(Filmy_Camera_type).all()
    fcts = session.query(Filmy_Camera_type).filter_by(r_id=fctid).one()
    fctes = session.query(Filmy_cam_Name).filter_by(filmcameratypeid=fctid).all()
    try:
        if signin_session['username']:
            return render_template('displayCameras.html', fct_tcs=fct_tcs,
                                   fcts=fcts, fctes=fctes,
                                   uname=signin_session['username'])
    except:
        return render_template('displayCameras.html',
                               fct_tcs=fct_tcs, fcts=fcts, fctes=fctes)


# Add New Camera Name
@app.route('/CameraHub/addCameraType', methods=['POST', 'GET'])
def addCameraType():
    if request.method == 'POST':
        company = Filmy_Camera_type(name=request.form['name'],
                           user_id=signin_session['user_id'])
        session.add(company)
        session.commit()
        return redirect(url_for('CameraHub'))
    else:
        return render_template('addCameraType.html', fct_tcs=fct_tcs)

########
# edit camera names
@app.route('/CameraHub/<int:fctid>/edit', methods=['POST', 'GET'])
def editCameraCategory(fctid):
    editCamera = session.query(Filmy_Camera_type).filter_by(r_id=fctid).one()
    creator = getUserInfo(editCamera.user_id)
    user = getUserInfo(signin_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.r_id != signin_session['user_id']:
        flash("You cannot edit this Film Camera Type."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('CameraHub'))
    if request.method == "POST":
        if request.form['name']:
            editCamera.name = request.form['name']
        session.add(editCamera)
        session.commit()
        flash("Film Camera Type is edited successfully ")
        return redirect(url_for('CameraHub'))
    else:
        # fct_tcs is a globla variable we can use this 
        return render_template('editCameraCategory.html',
                               fct=editCamera, fct_tcs=fct_tcs)


# Deleting Camera Category
@app.route('/CameraHub/<int:fctid>/delete', methods=['POST', 'GET'])
def deleteCameraCategory(fctid):
    fct = session.query(Filmy_Camera_type).filter_by(r_id=fctid).one()
    creator = getUserInfo(fct.user_id)
    user = getUserInfo(signin_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.r_id != signin_session['user_id']:
        flash("You cannot Delete this Film Camera Type."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('CameraHub'))
    if request.method == "POST":
        session.delete(fct)
        session.commit()
        flash("Film Camera Type is deleted successfully")
        return redirect(url_for('CameraHub'))
    else:
        return render_template('deleteCameraCategory.html', fct=fct, fct_tcs=fct_tcs)

# Add New Camera Details
@app.route('/CameraHub/addCompany/addCameraDetails/<string:fctname>/add',
           methods=['GET', 'POST'])
def addCameraDetails(fctname):
    fcts = session.query(Filmy_Camera_type).filter_by(name=fctname).one()
    # See if the logged in user is not the owner of camera
    creator = getUserInfo(fcts.user_id)
    user = getUserInfo(signin_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.r_id != signin_session['user_id']:
        flash("You cannot add new camera details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('displayCameras', fctid=fcts.r_id))
    if request.method == 'POST':
        name = request.form['name']
        cam_Model = request.form['cam_Model']
        Dimension  = request.form['Dimension']
        Batteries = request.form['Batteries']
        resolution= request.form['resolution']
        screen_size = request.form['screen_size']
        conector_type = request.form['conector_type']
        camera_cost = request.form['camera_cost']
        voltage = request.form['voltage']
        cameraDetails = Filmy_cam_Name(name=name, cam_Model=cam_Model,
                              Dimension=Dimension, Batteries=Batteries,
                              resolution=resolution,
                              screen_size=screen_size,
		              conector_type=conector_type,
			      camera_cost=camera_cost,
                              voltage=voltage,
                              date=datetime.datetime.now(),
                              filmcameratypeid=fcts.r_id,
                              user_id=signin_session['user_id'])
        session.add(cameraDetails)
        session.commit()
        return redirect(url_for('displayCameras', fctid=fcts.r_id))
    else:
        return render_template('addCameraDetails.html',
                               fctname=fcts.name, fct_tcs=fct_tcs)

######
# Edit camera details
@app.route('/CameraHub/<int:fctid>/<string:fctename>/edit',
           methods=['GET', 'POST'])
def editCameradetails(fctid, fctename):
    fct = session.query(Filmy_Camera_type).filter_by(r_id=fctid).one()
    cameraDetails = session.query(Filmy_cam_Name).filter_by(name=fctename).one()
    # See if the logged in user is not the owner of camera
    creator = getUserInfo(fct.user_id)
    user = getUserInfo(signin_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.r_id != signin_session['user_id']:
        flash("You can't edit camera details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('displayCameras', fctid=fct.id))
    # POST methods
    if request.method == 'POST':
        cameraDetails.name=request.form['name']
        cameraDetails.cam_Model=request.form['cam_Model']
        cameraDetails.Dimension=request.form['Dimension']
        cameraDetails.Batteries=request.form['Batteries']
        cameraDetails.resolution=request.form['resolution']
        cameraDetails.screen_size=request.form['screen_size']
        cameraDetails.conector_type=request.form['conector_type']
        cameraDetails.camera_cost=request.form['camera_cost']
        cameraDetails.voltage =request.form['voltage']
        cameraDetails.date = datetime.datetime.now()
        session.add(cameraDetails)
        session.commit()
        flash("film_camera Edited Successfully")
        return redirect(url_for('displayCameras', fctid=fctid))
    else:
        return render_template('editCameradetails.html',
                               fctid=fctid, cameraDetails=cameraDetails, fct_tcs=fct_tcs)

#####
# Delte camera Edit
@app.route('/CameraHub/<int:fctid>/<string:fctename>/delete',
           methods=['GET', 'POST'])
def deleteCameradetails(fctid, fctename):
    fct = session.query(Filmy_Camera_type).filter_by(r_id=fctid).one()
    cameraDetails = session.query(Filmy_cam_Name).filter_by(name=fctename).one()
    # See if the logged in user is not the owner of camera
    creator = getUserInfo(fct.user_id)
    user = getUserInfo(signin_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.r_id != signin_session['user_id']:
        flash("You can't delete Camera details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('displayCameras', fctid=fct.r_id))
    if request.method == "POST":
        session.delete(cameraDetails)
        session.commit()
        flash("Camera details deleted Successfully")
        return redirect(url_for('displayCameras', fctid=fctid))
    else:
        return render_template('deleteCameradetails.html',
                               fctid=fctid, cameraDetails=cameraDetails, fct_tcs=fct_tcs)

####
# Logout from current user
@app.route('/logout')
def logout():
    access_token = signin_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (signin_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = signin_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type': 'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del signin_session['access_token']
        del signin_session['gplus_id']
        del signin_session['username']
        del signin_session['email']
        del signin_session['picture']
        response = make_response(json.dumps('Successfully disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('displaysignin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#####
# Json
@app.route('/CameraHub/JSON')
def allfilm_camerasJSON():
    cameracategories = session.query(Filmy_Camera_type).all()
    category_dict = [c.serialize for c in cameracategories]
    for c in range(len(category_dict)):
        film_cameras = [i.serialize for i in session.query(
                 Filmy_cam_Name).filter_by(filmcameratypeid=category_dict[c]["r_id"]).all()]
        if film_cameras:
            category_dict[c]["film_camera"] = film_cameras
    return jsonify(Filmy_Camera_type=category_dict)

####
@app.route('/film_camerastore/cameracategories/JSON')
def categoriesJSON():
    film_cameras = session.query(Filmy_Camera_type).all()
    return jsonify(cameracategories=[c.serialize for c in film_cameras])

####
@app.route('/film_camerastore/film_cameras/JSON')
def itemsJSON():
    items = session.query(Filmy_cam_Name).all()
    return jsonify(film_cameras=[i.serialize for i in items])

#####
@app.route('/camerastore/<path:film_camera_name>/film_cameras/JSON')
def categoryItemsJSON(film_camera_name):
    film_cameraCategory = session.query(Filmy_Camera_type).filter_by(name=film_camera_name).one()
    film_cameras = session.query(Filmy_cam_Name).filter_by(filmycamname=film_cameraCategory).all()
    return jsonify(film_cameramodel=[i.serialize for i in film_cameras])

#####
@app.route('/camerastore/<path:film_camera_name>/<path:model_name>/JSON')
def ItemJSON(film_camera_name, model_name):
    film_cameraCategory = session.query(Filmy_Camera_type).filter_by(name=film_camera_name).one()
    film_cameramodel = session.query(Filmy_cam_Name).filter_by(
           name=model_name,filmycamname=film_cameraCategory).one()
    return jsonify(film_cameramodel=[film_cameramodel.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
