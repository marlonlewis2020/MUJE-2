from . import db, app
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import desc, text

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    muje_region = db.Column(db.String(200), default="East")
    name = db.Column(db.String(80))
    email = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    joined_on = db.Column(db.DateTime, default = datetime.now)
    

    def __init__(self, username, password, role, name, email, region):
        self.username = username
        self.password = generate_password_hash(password, method="pbkdf2:sha256")
        self.role = role
        self.name = name
        self.email = email
        self.region = region
        try:
            db.session.add(self)
            db.session.commit()
            db.session.refresh(self)
        except Exception as e:
            print(e)
            db.session.rollback()

        
    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self, id) #python 2 support
        except NameError:
            return str(self.id) #python 3 support
        
    def __repr__(self):
        return f'<User {self.id} - {self.username}>'
    
    
class Contestant(db.Model):
    __tablename__ = 'contestants'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer)
    contestant_no = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(256))
    photo = db.Column(db.String(80))
    muje_region = db.Column(db.String(200), default="Eastern")
    joined_on = db.Column(db.DateTime, default = datetime.now)
    

    def __init__(self, year, contestant_no, title, name, photo):
        self.year = year
        self.contestant_no = contestant_no
        self.title = "Miss " + title.strip()
        self.name = name.strip()
        self.photo = photo.strip()
        self.muje_region = "East"
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
        
    @staticmethod
    def load_prelims():
        try:
            this_year = db.session.query(func.max(Contestant.year)).scalar()
            ladies = db.session.query(Contestant).filter_by(year=this_year).all()
            judges = db.session.query(User).filter((User.role=="judge") & (User.active==True)).all()
            for lady in ladies:
                for judge in judges:
                    miss = PrelimScoring(judge.username, lady.contestant_no, this_year)
                    db.session.add(miss)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            
            
    @staticmethod
    def get_contestants():
        data = []
        try:
            this_year = db.session.query(func.max(Contestant.year)).scalar()
            ladies = db.session.query(Contestant).filter_by(year=this_year).all()
            for lady in ladies:
                data.append({
                    'year':lady.year,
                    'contestant_no':lady.contestant_no,
                    'title':lady.title,
                    'name':lady.name,
                    'photo':lady.photo_path(),
                    'muje_region':lady.muje_region
                })
        except Exception as e:
            print(e)
            return "error", data
        return "success", data
    

    def photo_path(self):
        if self.photo:
            return f'{app.config["UPLOAD_FOLDER"]}/{self.photo}'
        else:
            return None
  
        
class Section(db.Model):
    __tablename__="sections"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    round = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(80), nullable=False, unique=True)
    active = db.Column(db.Boolean(), default=True) # open or close
    
    def __init__(self, round, section):
        self.round = round
        self.section = section
        self.active = True
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
    
    def close(self):
        self.active=False
        try:
            db.session.commit()
            return "success", True
        except Exception as e:
            print(e)
            return "error", False
    
    def open(self):
        self.active=True
        try:
            db.session.commit()
            return "success", True
        except Exception as e:
            print(e)
            return "error", False
        
    def is_open(self):
        return self.active==True
    
    @staticmethod
    def round_closed(round):
        closed = True
        sections = db.session.query(Section).filter_by(round=round).all()
        for sec in sections:
            if sec.is_open():
                closed = False
                break
        return closed
      
        
class PrelimScoring(db.Model):
    __tablename__="prelimscoring"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    judge = db.Column(db.String(80))
    contestant_no = db.Column(db.Integer())
    interview = db.Column(db.Integer(), default=0)
    swimsuit = db.Column(db.Integer(), default=0)
    ballroom = db.Column(db.Integer(), default=0)
    year = db.Column(db.Integer())
    
    def __init__(self, judge:str, contestant_no:int, year:int):
        self.judge = judge
        self.contestant_no = contestant_no
        self.year = year 
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
        
    @staticmethod
    def select_prelim_contestant_for_judge_to_score(judge:str, contestant_no:int, year:int):
        prelim_contestant_score = db.session.query(PrelimScoring).filter((PrelimScoring.judge==judge) & (PrelimScoring.contestant_no==contestant_no) & (PrelimScoring.year==year)).scalar()
        if prelim_contestant_score is None:
            try:
                contestant = db.session.query(Contestant).filter((Contestant.contestant_no==contestant_no) & (Contestant.year==year)).first()
                if contestant is not None:
                    prelim_contestant_score = PrelimScoring(judge, contestant_no, year)
                    db.session.add(prelim_contestant_score)
                    db.session.commit()
                    db.session.refresh(prelim_contestant_score)
            except Exception as e:
                print(e)
                return "error", None
        return "success", prelim_contestant_score
        
    @staticmethod
    def score_interview(judge:str, contestant_no:int, score:int, year:int):
        section = db.session.query(Section).filter_by(section="interview").scalar()
        status, girl = PrelimScoring.select_prelim_contestant_for_judge_to_score(judge, contestant_no, year)
        if status == "success" and section and section.active:
            girl.interview = score
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return "error", False
            return "success", True
        return "error", False
    
    @staticmethod
    def score_swimsuit(judge:str, contestant_no:int, score:int, year:int):
        section = db.session.query(Section).filter_by(section="swimwear").scalar()
        status, girl = PrelimScoring.select_prelim_contestant_for_judge_to_score(judge, contestant_no, year)
        if status == "success" and section and section.active:
            girl.swimsuit = score
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return "error", False
            return "success", True
        return "error", False
    
    @staticmethod
    def score_ballroom(judge:str, contestant_no:int, score:int, year:int):
        section = db.session.query(Section).filter_by(section="ballroom").scalar()
        status, girl = PrelimScoring.select_prelim_contestant_for_judge_to_score(judge, contestant_no, year)
        if status == "success" and section and section.active:
            girl.ballroom = score
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return "error", False
            return "success", True
        return "error", False
    
    def avg_interview_scores(self):
        avg_interviews = db.session.query(PrelimScoring.contestant_no, func.avg(PrelimScoring.interview).label('interview_average')).all()
        return avg_interviews
    
    def avg_swimsuit_scores(self):    
        avg_swimsuit = db.session.query(PrelimScoring.contestant_no, func.avg(PrelimScoring.swimsuit).label('swimsuit_average')).all()
        return avg_swimsuit

    def avg_ballroom_scores(self):
        avg_ballroom = db.session.query(PrelimScoring.contestant_no, func.avg(PrelimScoring.ballroom).label('average')).all()
        return avg_ballroom

            
    @staticmethod
    def get_final_scores():
        scores = []
        if Section.round_closed(1):
            scores = db.session.execute(text("SELECT p.contestant_no, c.name, c.title, ROUND(SUM(p.interview + p.swimsuit + p.ballroom) / COUNT(p.judge)) as average, c.photo FROM prelimscoring as p JOIN contestants as c ON p.contestant_no=c.contestant_no GROUP BY p.contestant_no ORDER BY average DESC")).all()
        return scores
        
    @staticmethod
    def get_top_ten():
        scores = []
        if Section.round_closed(1):
            try:
                sc_data = PrelimScoring.get_final_scores()[0:10]
                for data in sc_data:
                    scores.append({'contestant_no':data[0], 'name':data[1], 'title':data[2], 'score':int(data[3]), 'photo':f'{app.config["UPLOAD_FOLDER"]}/{data[4]}'})
            except Exception as e:
                print(e)
                scores = []
        return scores
    
    @staticmethod
    def get_top_five():
        scores = []
        if Section.round_closed(1):
            try:
                sc_data = PrelimScoring.get_final_scores()[0:5]
                for data in sc_data:
                    scores.append({'contestant_no':data[0], 'name':data[1], 'title':data[2], 'score':int(data[3]), 'photo':f'{app.config["UPLOAD_FOLDER"]}/{data[4]}'})
            except Exception as e:
                print(e)
                scores = []
        return scores
        
    
    @staticmethod
    def load_top5():
        try:
            this_year = db.session.query(func.max(Contestant.year)).scalar()
            ladies = PrelimScoring.get_top_five()
            if Section.round_closed(1) and len(ladies):
                judges = db.session.query(User).filter((User.role=="judge") & (User.active==True)).all()
                for lady in ladies:
                    for judge in judges:
                        miss = TopFiveScoring(judge.username, lady.contestant_no, this_year)
                        db.session.add(miss)
                db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
    
    
class TopFiveScoring(db.Model):
    __tablename__="topfivescoring"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    judge = db.Column(db.String(80))
    contestant_no = db.Column(db.Integer())
    year = db.Column(db.Integer())
    q_and_a = db.Column(db.Integer())
    
    def __init__(self, judge:str, contestant_no:int, year:int):
        self.judge = judge
        self.contestant_no = contestant_no
        self.year = year 
        self.q_and_a = 0 
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
    
    @staticmethod
    def select_top5_contestant_for_judge_to_score(judge:str, contestant_no:int, year:int):
        top5_contestant_score = db.session.query(TopFiveScoring).filter((TopFiveScoring.judge==judge) & (TopFiveScoring.contestant_no==contestant_no) & (TopFiveScoring.year==year)).scalar()
        if top5_contestant_score is None:
            try:
                contestant = db.session.query(Contestant).filter((Contestant.contestant_no==contestant_no) & (Contestant.year==year)).first()
                if contestant is not None:
                    top5_contestant_score = TopFiveScoring(judge, contestant_no, year)
                    db.session.add(top5_contestant_score)
                    db.session.commit()
                    db.session.refresh(top5_contestant_score)
            except Exception as e:
                print(e)
                return "error", None
        return "success", top5_contestant_score
    
    @staticmethod
    def score_contestant(judge:str, contestant_no:int, score:int, year:int):
        section = db.session.query(Section).filter_by(section="qa1").scalar()
        status, girl = TopFiveScoring.select_top5_contestant_for_judge_to_score(judge, contestant_no, year)
        if status == "success" and section and section.active:
            girl.q_and_a = score
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return "error", False
            return "success", True
        return "error", False
    
    @staticmethod
    def get_final_scores():
        scores = []
        if Section.round_closed(2):
            scores = db.session.execute(text("SELECT p.contestant_no, c.name, c.title, ROUND(SUM(p.q_and_a) / COUNT(p.judge)) as average, c.photo FROM topfivescoring as p JOIN contestants as c ON p.contestant_no=c.contestant_no GROUP BY p.contestant_no ORDER BY average DESC")).all()
        return scores
    
    @staticmethod
    def get_top_three():
        scores = []
        if Section.round_closed(2):
            try:
                sc_data = TopFiveScoring.get_final_scores()[0:3]
                for data in sc_data:
                    scores.append({'contestant_no':data[0], 'name':data[1], 'title':data[2], 'score':int(data[3]), 'photo':f'{app.config["UPLOAD_FOLDER"]}/{data[4]}'})
            except Exception as e:
                print(e)
                scores = []
        return scores
    
    @staticmethod
    def load_top3():
        try:
            this_year = db.session.query(func.max(Contestant.year)).scalar()
            ladies = TopFiveScoring.get_top_three()
            judges = db.session.query(User).filter((User.role=="judge") & (User.active==True)).all()
            if Section.round_closed(2) and len(ladies):
                for lady in ladies:
                    for judge in judges:
                        miss = TopThreeScoring(judge.username, lady.contestant_no, this_year)
                        db.session.add(miss)
                db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
    
    
class TopThreeScoring(db.Model):
    __tablename__="topthreescoring"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    judge = db.Column(db.String(80))
    contestant_no = db.Column(db.Integer())
    year = db.Column(db.Integer())
    q_and_a = db.Column(db.Integer())
    
    def __init__(self, judge:str, contestant_no:int, year:int):
        self.judge = judge
        self.contestant_no = contestant_no
        self.year = year 
        self.q_and_a = 0 
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
    
    @staticmethod
    def select_top3_contestant_for_judge_to_score(judge:str, contestant_no:int, year:int):
        top3_contestant_score = db.session.query(TopThreeScoring).filter((TopThreeScoring.judge==judge) & (TopThreeScoring.contestant_no==contestant_no) & (TopThreeScoring.year==year)).scalar()
        if top3_contestant_score is None:
            try:
                contestant = db.session.query(Contestant).filter((Contestant.contestant_no==contestant_no) & (Contestant.year==year)).first()
                if contestant is not None:
                    top3_contestant_score = TopThreeScoring(judge, contestant_no, year)
                    db.session.add(top3_contestant_score)
                    db.session.commit()
                    db.session.refresh(top3_contestant_score)
            except Exception as e:
                print(e)
                return "error", None
        return "success", top3_contestant_score
    
    @staticmethod
    def score_contestant(judge:str, contestant_no:int, score:int, year:int):
        section = db.session.query(Section).filter_by(section="qa2").scalar()
        status, girl = TopThreeScoring.select_top3_contestant_for_judge_to_score(judge, contestant_no, year)
        if status == "success" and section and section.active:
            girl.q_and_a = score
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                return "error", False
            return "success", True
        return "error", False
    
    @staticmethod
    def get_final_scores():
        scores = []
        if Section.round_closed(3):
            scores = db.session.execute(text("SELECT p.contestant_no, c.name, c.title, ROUND(SUM(p.q_and_a) / COUNT(p.judge)) as average, c.photo FROM topthreescoring as p JOIN contestants as c ON p.contestant_no=c.contestant_no GROUP BY p.contestant_no ORDER BY average DESC")).all()
        return scores
    
    @staticmethod
    def get_top_three():
        scores = []
        if Section.round_closed(3):
            try:
                sc_data = TopThreeScoring.get_final_scores()[0:3]
                for data in sc_data:
                    scores.append({'contestant_no':data[0], 'name':data[1], 'title':data[2], 'score':int(data[3]), 'photo':f'{app.config["UPLOAD_FOLDER"]}/{data[4]}'})
            except Exception as e:
                print(e)
                scores = []
        return scores
    
    @staticmethod
    def get_third_place(self):
        scores = []
        if Section.round_closed(3):
            scores = TopThreeScoring.get_final_scores()[2]
        return scores
    
    @staticmethod
    def get_second_place(self):
        scores = []
        if Section.round_closed(3):
            scores = TopThreeScoring.get_final_scores()[1]
        return scores
    
    @staticmethod
    def get_first_place(self):
        scores = []
        if Section.round_closed(3):
            scores = TopThreeScoring.get_final_scores()[0]
        return scores