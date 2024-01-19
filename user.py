from flask_login import UserMixin

from db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    def increment_asked(self):
        db = get_db()
        try:
            db.execute(
                f"""
                UPDATE [dbo].[user]
                SET questions_asked = questions_asked + 1 WHERE id = \'{self.id}\'
                """
            )
            db.commit()
        except Exception as e:
            # Handle the exception, print an error message, or take appropriate action
            print(f"Error: {e}")
            # Rollback the transaction to undo any changes made before the exception occurred
            db.rollback()
        finally:
            # Optionally close the connection
            db.close()

    def increment_correct(self):
        db = get_db()
        try:
            db.execute(
                f"""
                UPDATE [dbo].[user]
                SET questions_correct = questions_correct + 1 WHERE id = \'{self.id}\'
                """
            )
            db.commit()
        except Exception as e:
            # Handle the exception, print an error message, or take appropriate action
            print(f"Error: {e}")
            # Rollback the transaction to undo any changes made before the exception occurred
            db.rollback()
        finally:
            # Optionally close the connection
            db.close()

    def increment_incorrect(self):
        db = get_db()
        try:
            db.execute(
                f"""
                UPDATE [dbo].[user]
                SET questions_incorrect = questions_incorrect + 1 WHERE id = \'{self.id}\'
                """
            )
            db.commit()
        except Exception as e:
            # Handle the exception, print an error message, or take appropriate action
            print(f"Error: {e}")
            # Rollback the transaction to undo any changes made before the exception occurred
            db.rollback()
        finally:
            # Optionally close the connection
            db.close()

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            f"SELECT * FROM [dbo].[user] WHERE id = \'{user_id}\'"
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        try:
            db.execute(
                "INSERT INTO [dbo].[user] (id, name, email, profile_pic) "
                "VALUES (?, ?, ?, ?)",
                (id_, name, email, profile_pic),
            )
            db.commit()
        except Exception as e:
            # Handle the exception, print an error message, or take appropriate action
            print(f"Error: {e}")
            # Rollback the transaction to undo any changes made before the exception occurred
            db.rollback()
        finally:
            # Optionally close the connection
            db.close()