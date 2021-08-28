from datetime import datetime
from flask_user import UserManager
from flask import (
    request, render_template, redirect,
    url_for
)
from flask_login import current_user
from app.usuario.forms import (
    RegisterForm as CustomRegisterFormClass,
    LoginForm as CustomLoginFormClass,
    EditUserProfileForm as CustomEditUserProfileFormClass
)
from app.models.user import User, USUARIO_GENEROS
from app.usuario.vistas import facebook_blueprint
from flask_user.decorators import login_required
from flask_dance.contrib.facebook import facebook
import requests

class CustomUserManager(UserManager):
    """
    Customized User Manager to override/extend 
    Flask User's manager
    """
    def customize(self, app):

        # Configure customized forms
        self.RegisterFormClass = CustomRegisterFormClass
        self.LoginFormClass = CustomLoginFormClass
        self.EditUserProfileFormClass = CustomEditUserProfileFormClass
        # NB: assign:  xyz_form = XyzForm   -- the class!
        #   (and not:  xyz_form = XyzForm() -- the instance!)

    def facebook_callback_view(self):
        """
        This callback is called after a successful Facebok
        OAuth login.
        """
        if not facebook.authorized:
            flash(_("No haz dado autrización para obtener tus datos"), "warning")
            return redirect(url_for("user.login"))

        user_res = facebook.get("me?fields=id,name,gender,email,birthday,picture")
        if not user_res.ok:
            flash(_("Error: no se pudieron obtener los datos del usuario de facebook, intenta de nuevo"), "danger")
            return redirect(url_for("user.login"))

        gender_map={
            "male": USUARIO_GENEROS[0][0],
            "female": USUARIO_GENEROS[1][0],
        }

        # Get user data as a dict
        user_data = user_res.json()
        user, user_email = self.db_manager.get_user_and_user_email_by_email(user_data["email"])
        if not user:
             # Create new user if needed
             user = User(
                 email=user_data["email"],
                 active=True,
                 nombre=user_data["name"],
                 fecha_nacimiento=datetime.strptime(
                     user_data["birthday"],
                     "%d/%m/%Y"
                 ),
                 genero=gender_map[user_data["gender"]],
             )
             # Get profile picture from facebook servers
             picture_res = requests.get(user_data["picture"]["data"]["url"], stream=True)

             if picture_res.ok:
                 # Save picture bytes to database
                 user.foto.replace(picture_res.raw, content_type=picture_res.headers["Content-Type"])

             # Save user to database
             user.save()

        # Log user in
        safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_LOGIN_ENDPOINT)

        # Redirect user to mural
        return self._do_login_user(user, safe_next_url)

    def _add_url_routes(self, app):
        super()._add_url_routes(app)
        app.add_url_rule("/fb-callback", "user.fb_callback", self.facebook_callback_view)

    @login_required
    def edit_user_profile_view(self):
        """
        Overridden edit user profile view to add profile
        picture
        """
        # Initialize form
        form = self.EditUserProfileFormClass(request.form, obj=current_user)

        # Process valid POST
        if request.method == 'POST' and form.validate():
            # Update fields
            form.populate_obj(current_user)

            # Save object
            self.db_manager.save_object(current_user)
            self.db_manager.commit()

            # Save profile picture
            image_data = request.files.get(form.nombre_foto.name)
            if image_data:
                current_user.foto.replace(image_data, content_type=image_data.mimetype)
                current_user.save()

            if form.delete_foto.data and current_user.foto:
                current_user.foto.delete()
                current_user.save()

            return redirect(self._endpoint_url(self.USER_AFTER_EDIT_USER_PROFILE_ENDPOINT))

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_EDIT_USER_PROFILE_TEMPLATE, form=form)
