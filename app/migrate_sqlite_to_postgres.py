from app import create_app, db as postgres_db
from main.models import User, OtherModel  # import all your models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite connection
sqlite_engine = create_engine('sqlite:////home/ec2-user/team-pypartners/app.db')
SQLiteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SQLiteSession()

# Postgres (RDS) connection
app = create_app()
app.app_context().push()
postgres_session = postgres_db.session

# Example: migrate users
for user in sqlite_session.query(User).all():
    postgres_session.add(User(
        id=user.id,
        name=user.name,
        email=user.email,
        # add all relevant fields
    ))

postgres_session.commit()
print("Users migrated!")

# Repeat for other tables/models
