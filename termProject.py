from config import Config

from app import create_app, db
import sqlalchemy as sqla

from app.main.models import Major, User

app = create_app(Config)


def seed_data():
    """Create tables (for local dev) and seed majors and faculty users if absent."""
    with app.app_context():
        # Create tables for local development. In production use migrations instead.
        db.create_all()

        # Seed majors
        if db.session.scalars(sqla.select(Major)).first() is None:
            majors = ['CS', 'RBE', 'ME', 'ECE', 'DS']
            db.session.add_all([Major(name=m) for m in majors])

        # Seed a couple of faculty users if no users exist
        if db.session.scalars(sqla.select(User)).first() is None:
            faculty = [
                {
                    'first_name': 'Mike',
                    'last_name': 'Domino',
                    'email': 'mfdomino@wpi.edu',
                    'username': 'mike_faculty',
                    'password': 'password123',
                },
                {
                    'first_name': 'Chris',
                    'last_name': 'Luigi',
                    'email': 'chris@example.com',
                    'username': 'chris_faculty',
                    'password': 'password123',
                }
            ]
            for f in faculty:
                u = User(
                    username=f['username'],
                    first_name=f['first_name'],
                    last_name=f['last_name'],
                    email=f['email'],
                    type='faculty'
                )
                u.set_password(f['password'])
                db.session.add(u)

        db.session.commit()


@app.cli.command('seed')
def seed_cmd():
    """Flask CLI command: `flask seed` to populate initial data."""
    seed_data()
    print('Seeding finished.')


if __name__ == "__main__":
    seed_data()
    app.run(debug=True)