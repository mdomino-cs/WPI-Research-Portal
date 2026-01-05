from app.student import student_bp
from app.decorators import role_required
from flask import render_template
from app.main.models import Position
from app import db
import sqlalchemy as sqla

@student_bp.route('/positions', methods=['GET'])
@role_required('student')
def positions():
    query = sqla.select(Position)
    positions = db.session.scalars(query).all()
    return render_template('positions.html', positions=positions)