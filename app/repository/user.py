
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
    
    def get_users_has_not_order(self, page_index: int = 1, page_size: int = 100) -> List[UserModel]:
        try:
            skip_count = (page_index - 1) * page_size
            users = UserModel._get_collection().find().skip(skip_count).limit(page_size)
            return [UserModel.from_mongo(user) for user in users] if users else []
        except Exception as e:
            print(f"Retrieving non-buying users failed: {str(e)}")
            return []
    
    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        qs: QuerySet = UserModel.objects(email=email.lower())
        try:
            user = qs.get()
        except DoesNotExist:
            return None
        return UserInDB.model_validate(user)
    
    def get_total_non_buying_users(self) -> int:
        try:
            total_non_buying_users = UserModel._get_collection().count_documents({"ordered": False})
            print("total_non_buying_users", total_non_buying_users)
            return total_non_buying_users
        except Exception as e:
            print(f"Error getting total non-buying users: {str(e)}")
            return 0
        
    
    

user_repository = UserRepository()
