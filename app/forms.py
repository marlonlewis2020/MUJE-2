from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileSize
from wtforms import FileField, StringField, SelectField, IntegerField, EmailField, TelField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Length


class UserForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=3, max=50)])
    email = EmailField("Email", validators=[InputRequired(), Length(min=3, max=30)])
    role = SelectField("Role", choices=[('judge','Judge'), ('chief','Chief Judge'), ('admin','Admin')], validators=[InputRequired(), Length(min=3, max=30)])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    region = StringField("Region", validators=[InputRequired()])
    
    
class LoginForm (FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=80)])
    

class ContestantForm(FlaskForm):
    __tablename__="contestants"
    contestant_no = IntegerField("Contestant No.", validators=[InputRequired()])
    year = IntegerField("Year", validators=[InputRequired()], name="year", id="year")
    title = StringField("Contestant Name", validators=[InputRequired()], id="title", name="title")
    name = StringField("Contestant Name", validators=[InputRequired()], name="name", id="name")
    photo = FileField("Photo", validators=[FileRequired(), FileSize(max_size=4000000), FileAllowed(["jpg", "png", "jpeg"], message="Image Files Only!")])

class PrelimScoringForm(FlaskForm):
    judge = SelectField("Judge", choices=[('','')], validators=[InputRequired()])
    contestant_no = SelectField("Contestant Number", choices=[('1','1'), 
                                                              ('2','2'),
                                                              ('3','3'),
                                                              ('4','4'),
                                                              ('5','5'),
                                                              ('6','6'),
                                                              ('7','7'),
                                                              ('8','8'),
                                                              ('9','9'),
                                                              ('10','10'),
                                                              ('11','11'),
                                                              ('12','12'),
                                                              ('13','13'),
                                                              ('14','14'),
                                                              ('15','15')
                                                              ], validators=[InputRequired()])
    interview = IntegerField("Interview Score", validators=[InputRequired()])
    swimsuit = IntegerField("Swimsuit Score", validators=[InputRequired()])
    ballroom = IntegerField("Ballroom Score", validators=[InputRequired()])
    year = IntegerField("Year.", validators=[InputRequired()], name="year", id="year")
    

class QandAScoreForm(FlaskForm):
    judge = SelectField("Judge", choices=[('','')], validators=[InputRequired()])
    contestant_no = SelectField("Contestant Number", choices=[('1','1'), 
                                                              ('2','2'),
                                                              ('3','3'),
                                                              ('4','4'),
                                                              ('5','5'),
                                                              ('6','6'),
                                                              ('7','7'),
                                                              ('8','8'),
                                                              ('9','9'),
                                                              ('10','10'),
                                                              ('11','11'),
                                                              ('12','12'),
                                                              ('13','13'),
                                                              ('14','14'),
                                                              ('15','15')
                                                              ], validators=[InputRequired()])
    q_and_a = IntegerField("Interview Score", validators=[InputRequired()])
    year = IntegerField("Year.", validators=[InputRequired()], name="year", id="year")