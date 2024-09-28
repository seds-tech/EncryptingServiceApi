import random
import threading
import time
from app import db

class User(db.Document):
    publicKey = db.StringField(required=True, unique=True)
    addingToken = db.IntField(min_value=0, default=111111)  # Default to 111111
    deactivateState = db.BooleanField(default=False)  # Default to False

    @classmethod
    def create_user(cls, publicKey, addingToken=0, deactivateState=False):
        user = cls(publicKey=publicKey, addingToken=addingToken, deactivateState=deactivateState)
        user.save()
        return str(user.id)
    
    @classmethod
    def check_deactivate_state(cls, user_id):
        try:
            user = cls.objects.get(id=user_id)
            return {
                'id': str(user.id),
                'deactivateState': user.deactivateState
            }
        except cls.DoesNotExist:
            return None
        
    @classmethod
    def update_deactivate_state(cls, user_id, deactivateState):
        try:
            user = cls.objects.get(id=user_id)
            user.deactivateState = deactivateState  # Update the deactivateState
            user.save()  # Save the changes to the database
            return {
                'id': str(user.id),
                'deactivateState': user.deactivateState
            }
        except cls.DoesNotExist:
            return None
        
   

    @classmethod
    def update_adding_token(cls, user_id):
        try:
            user = cls.objects.get(id=user_id)

            # Check if the addingToken is 111111, only then update it
            if user.addingToken == 111111:
                # Generate a random six-digit number that isn't 111111
                new_token = 111111
                while new_token == 111111:
                    new_token = random.randint(100000, 999999)

                user.addingToken = new_token
                user.save()

                # Schedule a change back to 111111 after 2 minutes (120 seconds)
                def reset_adding_token():
                    time.sleep(120)
                    user.addingToken = 111111
                    user.save()

                threading.Thread(target=reset_adding_token).start()

                return user.addingToken
            else:
                # Return None if the token is not 111111 (indicating no update)
                return None
        except cls.DoesNotExist:
            return None
    @classmethod
    def get_user_by_adding_token(cls, addingToken):
        try:
            # Check if the addingToken is 111111
            if addingToken == 111111:
                return {'error': 'User lookup by addingToken is not possible when addingToken is 111111'}

            # Find the user with the given addingToken
            user = cls.objects.get(addingToken=addingToken)
            return {'publicKey': user.publicKey}
        except cls.DoesNotExist:
            return {'error': 'User not found'}


