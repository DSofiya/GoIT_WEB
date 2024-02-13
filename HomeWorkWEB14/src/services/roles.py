from fastapi import Request, Depends, HTTPException, status

from src.database.models import Role, User
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: list[Role]):
        """
        The __init__ function is called when the class is instantiated.
            It sets up the instance of the class with a list of allowed roles.
        
        :param self: Represent the instance of the class
        :param allowed_roles: list[Role]: Define the allowed roles for the command
        :return: The object itself
        :doc-author: Trelent
        """
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, user: User = Depends(auth_service.get_current_user)):
        """
        The __call__ function is the function that will be called when a user tries to access an endpoint.
        It takes in two parameters: request and user. The request parameter is the Request object, which contains information about the HTTP request made by a client (e.g., headers, body). 
        The user parameter is our User object from auth_service's get_current_user function.
        
        :param self: Access the class attributes
        :param request: Request: Get the request object
        :param user: User: Get the user object from the auth_service
        :return: A function that takes a request and user as parameters
        :doc-author: Trelent
        """
        print(user.role, self.allowed_roles)
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN"
            )
