from flask_user import UserManager
from flask import request, render_template, redirect
from flask_login import current_user
from app.usuario.forms import (
    RegisterForm as CustomRegisterFormClass,
    LoginForm as CustomLoginFormClass,
    EditUserProfileForm as CustomEditUserProfileFormClass
)
from flask_user.decorators import login_required

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

            return redirect(self._endpoint_url(self.USER_AFTER_EDIT_USER_PROFILE_ENDPOINT))

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_EDIT_USER_PROFILE_TEMPLATE, form=form)
