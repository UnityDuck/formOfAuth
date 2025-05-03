from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class AddWorkForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    team_leader_id = IntegerField('Team Leader ID', validators=[DataRequired()])
    work_size = IntegerField('Work Size (hours)', validators=[DataRequired()])
    collaborators = StringField('Collaborators (IDs)', validators=[DataRequired()])
    is_job_finished = BooleanField('Is job finished?', default=False)
    submit = SubmitField('Add Work')
