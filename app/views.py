import os
from flask import make_response, jsonify, request, redirect, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from app.forms import UserForm, LoginForm, ContestantForm, PrelimScoringForm, QandAScoreForm

from app.models import User, Contestant, PrelimScoring, TopFiveScoring, TopThreeScoring, Section
from app import app, db, login_manager
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import jwt

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if request.method=="POST":
        try:
            data = LoginForm()
            username = data.username.data
            password = data.password.data
            user = db.session.query(User).filter_by(username=username).first()
            print(user)
            if user is not None and user.active and check_password_hash(user.password, password):
                if login_user(user):
                    token = generate_token()
                    load_user(str(user.id))
                    return jsonify(status='success', message = 'User successfully logged in.', id=user.id, username=username, role=user.role, token=token)
            return jsonify(status="error", message="Invalid login credentials or user is not active!")
        except Exception as e:
            print(e)
            return jsonify(errors='An error occurred while processing your request'), 500
    return jsonify(errors='Invalid request method'), 405


@login_manager.user_loader
def load_user(id):
    user = db.session.execute(db.select(User).filter_by(id=id)).scalar()
    return user


@app.route('/api/v1/auth/logout', methods = ['POST','GET'])
@login_required
def logout():
    token = request.headers.get('Authorization', None).split(" ")
    try:
        if user_authorized() and len(token) == 2 and token[0].lower() == "bearer":
            logout_user()
        return jsonify(status="success", message = "User sucessfully logged out."), 200
    except Exception as e:
        print(e)
        return jsonify(errors='An error occurred while processing your request'), 500


@app.route("/api/v1/auth/register", methods=['POST'])
def register():
    form = UserForm()
    if request.method=="POST":
        user = User(form.username.data, form.password.data, form.role.data, form.name.data, form.email.data, form.region.data)
        if not user:
            return jsonify(status="error", message="Unable to register user/judge.")
        return make_response({'status':'success', 'id':user.id})
        
    
@app.route("/api/v1/generate-token")
@login_required
def generate_token():
    timestamp = datetime.utcnow()
    if current_user is not None:
        payload = {
            "id": current_user.id,
            "role": current_user.role,
            "username": current_user.username,
            "iat": timestamp,
            "exp": timestamp + timedelta(days=7)
        }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
    return token


@app.route("/api/v1/sections")
def get_sections():
    response = {
        "status":"error"
    }
    data = []
    try:
        payload = get_request_payload()
        if payload and (payload['role']=='admin' or payload['role']=='chief'):
            uid = payload['id']
            load_user(str(uid))
            sections = db.session.query(Section).all()
            for section in sections:  
                data.append({
                    "id":section.id,
                    "round":section.round,
                    "section":section.section,
                    "active":section.active
                })
                response['status']="success"
                response['data']=data
        else:
            response['message'] = "Unauthorized access"
    except Exception as e:
        print(e)
        response['message']="Unable to get pageant sections at this time."
    return make_response(response)

@app.route("/api/v1/contestants/<int:year>")
# @login_required
def get_contestant(year):
    if request.method=="GET":
        result = {"status": "error"}
        try:
            result['status'], result['data'] = Contestant.get_contestants()
        except Exception as e:
            print(e)
            
        return make_response(result)


@app.route("/api/v1/contestants/<int:year>", methods=['POST'])
# @login_required
def add_contestant(year):
    if request.method=="POST":
        form = ContestantForm()
        try:
            photo = request.files['photo']
            filename=secure_filename(photo.filename) 
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #
            if isAPhoto(filename):
                lady= Contestant(year, form.contestant_no.data, form.title.data, form.name.data, filename)
                db.session.add(lady)
                db.session.commit()
                db.session.refresh(lady)
                return jsonify(status="success", message="Contestant successfully added!", id=lady.id)
        except Exception as e:
            print(e)
            return jsonify(status="error", message="Could not add new contestant")
    return jsonify(status="error", message="invalid request"), 401
    
        
@app.route("/api/v1/prelim/interview", methods=['POST']) 
# @login_required
def prelim_interview():
    # get form data
    response = {'status':'error'}
    form = PrelimScoringForm()
    if request.method=='POST':
        # get and decode token into payload
        try:
            payload = get_request_payload()
            if payload:
                # if role is judge or chief, update the prelim counter for interview for that contestant, judge, year
                uid = payload['id']
                load_user(str(uid))
                judge = payload['username']
                response['status'], response['data'] = PrelimScoring.score_interview(judge, form.contestant_no.data, form.interview.data, form.year.data)
        except Exception as e:
            print(e)
    return make_response(response)
            

@app.route("/api/v1/section/<int:round>/<section>", methods=['POST'])
# @login_required
def add_section(round, section):
    response = {
        'status':'error',
        'message':'unable to add new section.'
    }
    try:
        payload = get_request_payload()
        if payload:
            uid = payload['id']
            load_user(str(uid))
            if current_user.role == "chief" or current_user.role == "admin":
                sect = Section(round, section.lower())
                db.session.add(sect)
                db.session.commit()
                db.session.refresh(sect)
                response = {
                    'status':'success',
                    'data': {
                        'id':sect.id
                    }
                }
    except Exception as e:
        print(e)
        db.session.rollback()
    return make_response(response)
        
        
@app.route("/api/v1/prelim/swimsuit", methods=['POST']) 
# @login_required
def prelim_swimsuit():
    # get form data
    response = {'status':'error'}
    form = PrelimScoringForm()
    if request.method=='POST':
        # get and decode token into payload
        try:
            payload = get_request_payload()  
            if payload:
                # if role is judge or chief, update the prelim counter for interview for that contestant, judge, year
                uid = payload['id']
                load_user(str(uid))
                judge = payload['username']
                response['status'], response['data'] = PrelimScoring.score_swimsuit(judge, form.contestant_no.data, form.swimsuit.data, form.year.data)
        except Exception as e:
            print(e)
    return make_response(response)

    
@app.route("/api/v1/prelim/ballroom", methods=['POST']) 
# @login_required
def prelim_ballroom():
     # get form data
    response = {'status':'error'}
    form = PrelimScoringForm()
    if request.method=='POST':
        # get and decode token into payload
        try:
            payload = get_request_payload()  
            if payload:
                # if role is judge or chief, update the prelim counter for interview for that contestant, judge, year
                uid = payload['id']
                load_user(str(uid))
                judge = payload['username']
                response['status'], response['data'] = PrelimScoring.score_ballroom(judge, form.contestant_no.data, form.ballroom.data, form.year.data)
        except Exception as e:
            print(e)
    return make_response(response)


@app.route("/api/v1/round/<int:round>/close", methods=['POST'])
def close_round(round):
    response = { 'status':'error'}
    try:
        payload = get_request_payload()
        uid = payload['id']
        load_user(str(uid))
        if current_user.role == 'admin' or current_user.role == 'chief':
            # close all sections in this round
            sections = db.session.query(Section).filter_by(round=round).all()
            for sect in sections:
                sect.close()
            db.session.commit()
            response = {'status':'success'}
    except Exception as e:
        print(e)
        db.session.rollback()
        response['message']='could not close sections of this round.'
    return make_response(response)


@app.route("/api/v1/round/<int:round>/open", methods=['POST'])
def open_round(round):
    response = { 'status':'error'}
    try:
        payload = get_request_payload()
        uid = payload['id']
        load_user(str(uid))
        if current_user.role == 'admin' or current_user.role == 'chief':
            # close all sections in this round
            sections = db.session.query(Section).filter_by(round=round).all()
            for sect in sections:
                sect.open()
            db.session.commit()
            response = {'status':'success'}
    except Exception as e:
        print(e)
        db.session.rollback()
        response['message']='could not open sections of this round.'
    return make_response(response)


@app.route("/api/v1/prelims/top10", methods=['GET']) 
def get_top_ten():
    
    response = {'status':'error'}
    try:
        payload = get_request_payload()
        uid = payload['id']
        load_user(str(uid))
        if current_user.role == 'chief' or current_user.role == 'admin':
            response['data'] = PrelimScoring.get_top_ten()
            if not len(response['data']):
                response['status']='error'
            else:
                response['status'] = 'success'
        else: 
            response['message'] = "You are not authorized to view this resource."
    except Exception as e:
        print(e)
        response['message']='unable to retrieve top 10 at this time'
    return make_response(response)


@app.route("/api/v1/prelims/best_swimsuit", methods=['GET']) 
def best_swimsuit():
    
    response = {'status':'error'}
    try:
        payload = get_request_payload()
        uid = payload['id']
        load_user(str(uid))
        if current_user.role == 'chief' or current_user.role == 'admin':
            response['data'] = PrelimScoring.best_swimsuit_score()
            if not len(response['data']):
                response['status']='error'
            else:
                response['status'] = 'success'
        else: 
            response['message'] = "You are not authorized to view this resource."
    except Exception as e:
        print(e)
        response['message']='unable to retrieve top 10 at this time'
    return make_response(response)

@app.route("/api/v1/prelims/best_evening", methods=['GET']) 
def best_evening():
    
    response = {'status':'error'}
    try:
        payload = get_request_payload()
        uid = payload['id']
        load_user(str(uid))
        if current_user.role == 'chief' or current_user.role == 'admin':
            response['data'] = PrelimScoring.best_evening_score()
            if not len(response['data']):
                response['status']='error'
            else:
                response['status'] = 'success'
        else: 
            response['message'] = "You are not authorized to view this resource."
    except Exception as e:
        print(e)
        response['message']='unable to retrieve top 10 at this time'
    return make_response(response)
        
    
@app.route("/api/v1/prelims/top5", methods=['GET'])     
def get_top_five():
    response = {'status':'error'}
    try:
        payload = get_request_payload()
        uid = payload['id']
        load_user(str(uid))
        if current_user.role:
            response['data'] = PrelimScoring.get_top_five()
            if not len(response['data']):
                response['status']='error'
                response['message'] = "The Top 5 has not yet been selected. Prelim Round is not yet closed..."
            else:
                response['status'] = 'success'
        else: 
            response['message'] = "You are not authorized to view this resource."
    except Exception as e:
        print(e)
        response['message']='unable to retrieve top 5 at this time'
    return response

   
@app.route("/api/v1/top5", methods=['POST']) 
@login_required
def top5_vote():
    # get form data
    response = {'status':'error'}
    form = QandAScoreForm()
    if request.method=='POST':
        # get and decode token into payload
        try:
            payload = get_request_payload()  
            if payload:
                # if role is judge or chief, update the prelim counter for interview for that contestant, judge, year
                uid = payload['id']
                load_user(str(uid))
                judge = payload['username']
                response['status'], response['data'] = TopFiveScoring.score_contestant(judge, form.contestant_no.data, form.q_and_a.data, form.year.data)
        except Exception as e:
            print(e)
    return make_response(response)

     
@app.route("/api/v1/top5/top3", methods=['GET'])
def get_top_three():
    response = {'status':'error'}
    try:
        payload = get_request_payload()
        uid = payload['id']
        load_user(str(uid))
        if current_user.role:
            response['data'] = TopFiveScoring.get_top_three()
            if not len(response['data']):
                response['status']='error'
                response['message'] = "The Top 3 has not yet been selected. Top 5 Round is not yet closed..."
            else:
                response['status'] = 'success'
        else: 
            response['message'] = "You are not authorized to view this resource."
    except Exception as e:
        print(e)
        response['message']='unable to retrieve top 5 at this time'
    return response   


@app.route("/api/v1/top3", methods=['POST']) 
@login_required
def top3_vote():
    # get form data
    response = {'status':'error'}
    form = QandAScoreForm()
    if request.method=='POST':
        # get and decode token into payload
        try:
            payload = get_request_payload()  
            if payload:
                # if role is judge or chief, update the prelim counter for interview for that contestant, judge, year
                uid = payload['id']
                load_user(str(uid))
                judge = payload['username']
                response['status'], response['data'] = TopThreeScoring.score_contestant(judge, form.contestant_no.data, form.q_and_a.data, form.year.data)
        except Exception as e:
            print(e)
    return make_response(response)


@app.route("/api/v1/top3/scores", methods=['GET'])
def get_final_scores():
    response = {'status':'error'}
    try:
        payload = get_request_payload()
        uid = payload['id']
        load_user(str(uid))
        if current_user.role == 'chief' or current_user.role == 'admin':
            response['data'] = TopThreeScoring.get_top_three()
            if not len(response['data']):
                response['status']='error'
            else:
                response['status'] = 'success'
        else: 
            response['message'] = "You are not authorized to view this resource."
    except Exception as e:
        print(e)
        response['message']='unable to retrieve top 5 at this time'
    return response 

# @app.route('/api/v1/contestants/<int:year>/<int:n>')
# @login_required
# def get_top_n(year, n):
#     response = {
#         'status':'error',
#         'message':'Judging is not yet complete'
#     }
#     if n == 10:
#         if Section.round_closed(1):
#             response = {
#                 'status':'success',
#                 'data':PrelimScoring.get_top_ten()
#             }
                
#     elif n == 5:
        
#         if Section.round_closed(1):
#             response = {
#                 'status':'success',
#                 'data':PrelimScoring.get_top_five()
#             }
#     elif n == 3:
#         if Section.round_closed(2):
#             response = {
#                 'status':'success',
#                 'data':TopFiveScoring.get_top_three()
#             }
#     elif n == 1:
#         if Section.round_closed(3):
#             response = {
#                 'status':'success',
#                 'data':{
#                     'first':TopThreeScoring.get_first_place(),
#                     'second':TopThreeScoring.get_second_place(),
#                     'third':TopThreeScoring.get_third_place(),
#                     'ranks':TopThreeScoring.get_final_scores()
#                     }
#             }
#     else:
#         response['status'], response['data'] = Contestant.get_contestants()
        
#     return make_response(response)


# -- helper functions -- 

def isAPhoto(filename):
    #Checks if a file is a photo
    # if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpg"):
    return filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.png') or filename.lower().endswith('.gif')


def get_request_payload():
    token = request.headers.get('Authorization', None)
    parts = []
    payload = {}
    if token is not None: parts = token.split()
    if len(parts)==2 and parts[0].lower()=="bearer":
        payload = jwt.decode(parts[1], app.config['SECRET_KEY'], algorithms=["HS256"])
    return payload
        

def user_authorized():
    payload = get_request_payload()
    role = payload['role']
    if not current_user.is_authenticated:
        if role==current_user.role and (current_user.role=="judge" or current_user.role=="chief" or current_user.role=="admin"):
            return True
    return False