
from app.models.user import User as UserModel
from app.schema.user import UserBase, UserInDB
from typing import List, Optional
from mongoengine import QuerySet, DoesNotExist

class UserRepository:
    def __init__(self):
        pass

    def create(self, obj_in: UserBase) -> UserModel:
        try:
            new_user = UserModel(**obj_in.model_dump())
            new_user.save()
            return UserInDB.model_validate(new_user)
        except Exception as e:
            print(f"Create user failed: {str(e)}")
            return []
    
    def get_user_has_not_order(self) -> List[UserModel]:
        try:
            users = UserModel._get_collection().find({"ordered": False})
            return [UserModel.from_mongo(user) for user in users] if users else []
        except Exception as e:
            print(f"Retrieving non buying users failed: {str(e)}")
            return []
    
    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        qs: QuerySet = UserModel.objects(email=email.lower())
        try:
            user = qs.get()
        except DoesNotExist:
            return None
        return UserInDB.model_validate(user)

user_repository = UserRepository()
