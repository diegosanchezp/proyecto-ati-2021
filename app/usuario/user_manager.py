from flask_user import UserManager
from app.usuario.forms import (
    RegisterForm as CustomRegisterFormClass,
    LoginForm as CustomLoginFormClass,
)
class CustomUserManager(UserManager):
    """
    Customized User Manager to override/extend 
    Flask User's manager
    """

    def customize(self, app):

        # Configure customized forms
        self.RegisterFormClass = CustomRegisterFormClass
        self.LoginFormClass = CustomLoginFormClass
        # NB: assign:  xyz_form = XyzForm   -- the class!
        #   (and not:  xyz_form = XyzForm() -- the instance!)
