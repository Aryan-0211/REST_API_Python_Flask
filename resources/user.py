from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity,jwt_required,get_jwt
from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema


# Define a Blueprint for user-related routes
blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)  # Validate input data against the UserSchema
    def post(self, user_data):
        # Check if the username already exists
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")  # Return a conflict error

        # Create a new user with a hashed password
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])  # Hash the password securely
        )
        db.session.add(user)  # Add the user to the database
        db.session.commit()  # Commit the transaction

        return {"message": "User created successfully."}, 201  # Return success response

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            # Ensure user ID is valid before proceeding
            if not user.id:
                abort(500, message="User ID is missing or invalid.")
            
            # Generate the access token
            access_token = create_access_token(identity=str(user.id), fresh = True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        
        abort(401, message="Invalid credentials.")
        

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200
        
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"Successfully Logged Out"}


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)  # Specify the response schema
    def get(self, user_id):
        # Fetch the user by ID or raise a 404 error if not found
        user = UserModel.query.get_or_404(user_id)
        return user  # Return the user data

    def delete(self, user_id):
        # Fetch the user by ID or raise a 404 error if not found
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)  # Delete the user from the database
        db.session.commit()  # Commit the transaction

        return {"message": "User successfully deleted"}, 200  # Return success response
