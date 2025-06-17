from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
from firebase_admin import auth as admin_auth
from werkzeug.utils import secure_filename
from datetime import timedelta
from groq import Groq
from firebase_admin import credentials
from urllib.parse import urlparse
from typing import Union
import firebase_admin
import requests
import random
import string
import pyrebase
import time
import os
import json
import datetime
import base64
import uuid


app = Flask(__name__)

firebaseConfig = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "projectId": "",
  "storageBucket": "",
  "messagingSenderId": "",
  "appId": "",
  "measurementId": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()

cred = credentials.Certificate("adminsdk.json")  # Replace with your actual service account file
firebase_admin.initialize_app(cred)

@app.route('/landing')
def landing():
    return render_template('landing_page.html')

@app.route('/')
def home():
    token, refresh_token, issue_time = get_valid_token()

    if not token:
        return redirect(url_for("landing"))
    
    # Initialize default values
    local_id = ""
    profile_image_url = "https://cdn.pixabay.com/photo/2023/02/18/11/00/icon-7797704_1280.png"
    saved_posts_id_list = []  # Initialize as empty list
    notifications = False  # Initialize as False
    
    try:
        if token:
            decoded_token = admin_auth.verify_id_token(token)
            local_id = decoded_token.get("uid")
            profile_image_url = f"https://snapvibe.share.zrok.io/static/profile_image/{local_id}.png"
            
            # Get saved posts with proper error handling
            saved_posts = db.child("saved_posts").child(local_id).get(token=token).val()
            notifications = db.child("is_new_notification").child(local_id).get(token=token).val()
            user_following = db.child("users").child(local_id).child("following").get(token=token).val()
            user_following_list = list(user_following) if user_following else []
            
            story_data = {}
            
            for i in user_following_list:
                story = db.child("story").child(i).get(token=token).val()
                if story is not None:
                    story_data[i] = dict(story)
                    
            
            user_story = db.child("story").child(local_id).get(token=token).val()
            if user_story is not None:
                story_data[local_id] = dict(user_story)
                    
            print(list(story_data))
            print(user_following_list)
                    
            

            if saved_posts or notifications:
                saved_posts_id_list = list(saved_posts.keys())
                notifications = notifications
            else:
                saved_posts_id_list = []
                notifications = False
    except Exception as e:
        print(f"Error in home route: {e}")
        # Keep default values if any error occurs

    response = make_response(render_template(
        "home_page.html", 
        user_id=local_id, 
        profile_image_url=profile_image_url, 
        saved_posts_id_list=saved_posts_id_list,
        notifications=notifications,
        user_following_list=user_following_list,
        user_following=user_following,
        story_data=story_data
        )
    )
    
    if refresh_token:
        response.set_cookie(
            "firebase_token", 
            token, 
            httponly=True, 
            secure=True, 
            max_age=timedelta(days=365).total_seconds()
        )
        response.set_cookie(
            "refresh_token", 
            refresh_token, 
            httponly=True, 
            secure=True, 
            max_age=timedelta(days=365).total_seconds()
        )
        response.set_cookie(
            "token_issue_time", 
            issue_time, 
            max_age=timedelta(days=365).total_seconds()
        )
        
    return response

def get_image(name):
    url = "https://cdn.pixabay.com/photo/2023/02/18/11/00/icon-7797704_1280.png"
    save_path = os.path.join("static", "profile_image")
    os.makedirs(save_path, exist_ok=True)  

    response = requests.get(url)
    
    if response.status_code == 200:
        filename = f"{name}.png"
        full_path = os.path.join(save_path, filename)
        with open(full_path, "wb") as file:
            file.write(response.content)
        return True
    else:
        return False


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        birthday_data = data.get("birthday")
        termsChecked = data.get("termsChecked")

        if not name or not email or not password or not termsChecked or not username:
            return jsonify({"error": "All fields are required"}), 400
            
        try:
            username_exists = db.child("usernames").child(username).get()
            if username_exists.val() is not None:
                return jsonify({"error": "Username already in use"}), 400
        
        except:
            pass

        try:
            user = auth.create_user_with_email_and_password(email, password)
            
            if "localId" not in user:
                return jsonify({"error": "Please. Try again"}), 500
            
            local_id = user["localId"]
            user = auth.refresh(user["refreshToken"])
            id_token = user.get("idToken")
            
            get_image(local_id)
            
            user_data = {
                "name": name,
                "email": email, 
                "username": username,
                "birthday_data": birthday_data,
                "followers": [],
                "following": [],
                "posts": [],
                "photos": [],
                "profile_data": {
                    "bio": f"Hello there! I am {name} and I am using SnapVide!",
                    "profile_pic": f"https://snapvibe.share.zrok.io/static/profile_image/{local_id}.png",
                    "education": "",
                    "location": "",
                    "work": "",
                    "website": "",
                    "tagline": f"My name is {name}",
                    "joined": str(datetime.datetime.now()),
                }
            }
            
            db.child("users").child(local_id).set(user_data, token=id_token)
            db.child("usernames").child(username).set(local_id, token=id_token)
            
            auth.send_email_verification(id_token)
            
            return jsonify({"message": True}), 200
        except Exception as e:
            try:
                message = json.loads(e.args[1])["error"]["message"]
                print(message)
                if message == "EMAIL_EXISTS":
                    return jsonify({"error": "Email already in use"}), 400
                elif message == "INVALID_EMAIL":
                    return jsonify({"error": "Invalid email"}), 400
                elif "WEAK_PASSWORD" in message:
                    return jsonify({"error": "Password should be at least 8 characters"}), 400
                else:
                    return jsonify({"error": message}), 400
            except:
                return jsonify({"error": "An unexpected error occurred"}), 500
        
        
    return render_template('sign_up_page.html')

@app.route("/verification-link")
def verification_page():
    return render_template("verification_page.html")


@app.route("/verify-email", methods=['POST', 'GET'])
def send_verification():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        if email and password:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
            except:
                return jsonify({"message": "Invalid email or password"}), 400
            try:
                user = auth.refresh(user["refreshToken"])
                email_send = auth.send_email_verification(user["idToken"])
                if email_send:
                    return jsonify({"message": "Email Sent!"}), 200
                else:
                    return jsonify({"message": "Email Not Sent!"}), 400
            except Exception as e:
                print("Error sending verification email:", e)
                return jsonify({"message": "An error occurred while sending the email"}), 500
                
    return render_template("verifaction_email.html")


@app.route("/sign-in", methods=['GET', 'POST'])
def sign_in():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            user_info = auth.get_account_info(user["idToken"])

            # Check if email is verified
            if not user_info["users"][0]["emailVerified"]:
                return jsonify({"message": "Please verify your email before signing in!"}), 403
            
            id_token = user["idToken"]
            refresh_token = user["refreshToken"]

            # Set cookies for ID token and refresh token
            response = make_response(jsonify({"message": "200"}), 200)
            response.set_cookie("firebase_token", id_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("token_issue_time", str(int(time.time())), max_age=timedelta(days=365).total_seconds())

            return response
        except Exception as e:
            print(f"Error during sign-in: {e}")
            return jsonify({"message": "Invalid! email or password. Please Check."}), 401
    return render_template('sign_in_page.html')


def get_valid_token():
    token = request.cookies.get("firebase_token")
    refresh_token = request.cookies.get("refresh_token")
    issue_time = request.cookies.get("token_issue_time")
    
    print(token ,"======", refresh_token, issue_time)

    if not token or not refresh_token or not issue_time:
        return None, None, None

    current_time = int(time.time())
    if current_time > int(issue_time) + 3600 - 300:
        
        try:
            new_user = auth.refresh(refresh_token)
            new_token = new_user["idToken"]
            new_refresh_token = new_user["refreshToken"]
            new_issue_time = str(int(time.time()))
            time.sleep(10)
            return new_token, new_refresh_token, new_issue_time
        except Exception as e:
            print("Token refresh failed:", e)
            return None, None, None
    else:
        return token, None, None  # Token still valid

@app.template_filter('to_json')
def to_json(str_dict):
    return json.loads(str_dict)


@app.template_filter('is_within_24_hours')
def is_within_24_hours(timestamp):
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            # Try without microseconds if the format doesn't match
            timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    
    current_time = datetime.datetime.now()
    time_difference = current_time - timestamp
    
    return time_difference < timedelta(hours=24)

    
@app.template_filter('time_ago')
def time_ago(target_time: Union[datetime.datetime, str], 
             format: str = None) -> str:
    target_time = datetime.datetime.strptime(target_time, "%Y-%m-%d %H:%M:%S.%f")
    if isinstance(target_time, str):
        if not format:
            raise ValueError("Format required when target_time is string")
        target_time = datetime.datetime.strptime(target_time, format)  # Use datetime.strptime
    
    now = datetime.datetime.now()  # Use datetime.now
    diff = now - target_time
    
    seconds = diff.total_seconds()
    
    if seconds < 0:
        return "in the future"
    
    intervals = (
        ('year', 31536000),  # 365 * 24 * 60 * 60
        ('month', 2592000),  # 30 * 24 * 60 * 60 (approximate)
        ('day', 86400),      # 24 * 60 * 60
        ('hour', 3600),      # 60 * 60
        ('minute', 60),
        ('second', 1)
    )
    
    for unit, unit_seconds in intervals:
        value = seconds // unit_seconds
        if value >= 1:
            return f"{int(value)} {unit}{'s' if value > 1 else ''} ago"
    
    return "just now"
    
    
@app.route("/profile", methods=['GET'])
def profile():
    token, refresh_token, issue_time = get_valid_token()
    
    print(token ,"======", refresh_token, issue_time)
    
    if not token:
        return redirect(url_for("landing"))  # Redirect to landing if not authenticated
    
    try:
        decoded_token = admin_auth.verify_id_token(token)
        local_id = decoded_token.get("uid")
        if not local_id:
            local_id = ""
            
        print("==================>", local_id)
        
        # Get user data from Firebase
        user_data = db.child("users").child(local_id).get(token=token).val()
        
        if not user_data:
            return render_template("profile_page.html", 
                                user_data={},
                                domain="",
                                user_id=local_id,
                                saved_posts_id_list=[])
        
        # Initialize default values for profile data if missing
        if "profile_data" not in user_data:
            user_data["profile_data"] = {
                "bio": "",
                "profile_pic": "https://cdn.pixabay.com/photo/2023/02/18/11/00/icon-7797704_1280.png",
                "education": "",
                "location": "",
                "work": "",
                "website": "",
                "tagline": "",
                "joined": ""
            }
        
        # Get saved posts
        saved_posts = db.child("saved_posts").child(local_id).get(token=token).val() or {}
        notifications = db.child("is_new_notification").child(local_id).get(token=token).val()
        if notifications is not None:
            notifications = notifications
        else:
            notifications = {"is_new_notification": False}
        saved_posts_id_list = list(saved_posts.keys()) if saved_posts else []
        
        # Extract domain from website if exists
        domain = ""
        if "website" in user_data["profile_data"] and user_data["profile_data"]["website"]:
            domain = urlparse(user_data["profile_data"]["website"]).netloc
            
    except Exception as e:
        print("Error fetching profile data:", e)
        user_data = {
            "profile_data": {
                "profile_pic": "https://cdn.pixabay.com/photo/2023/02/18/11/00/icon-7797704_1280.png"
            }
        }
        domain = ""
        saved_posts_id_list = []
    
    response = make_response(
        render_template(
            "profile_page.html",
            user_data=user_data,
            domain=domain,
            user_id=local_id,
            saved_posts_id_list=saved_posts_id_list,
            notifications=notifications
        )
    )
    
    if refresh_token:
        response.set_cookie(
            "firebase_token", 
            token, 
            httponly=True, 
            secure=True, 
            max_age=timedelta(days=365).total_seconds()
        )
        response.set_cookie(
            "refresh_token", 
            refresh_token, 
            httponly=True, 
            secure=True, 
            max_age=timedelta(days=365).total_seconds()
        )
        response.set_cookie(
            "token_issue_time", 
            issue_time, 
            max_age=timedelta(days=365).total_seconds()
        )
    
    return response
    
UPLOAD_FOLDER = "static/profile_image"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["profile_image"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/edit-profile", methods=['GET', 'POST'])
def edit_profile():
    token, refresh_token, issue_time = get_valid_token()
    
    
    if not token:
        return redirect(url_for("landing"))
    
    try:
        user = auth.get_account_info(token)
        local_id = user["users"][0]["localId"]
        
        if request.method == "POST":
            data = request.form.to_dict()
            print(data)
            bio = data.get("bio")
            profile_pic = data.get("profile_pic")
            education = data.get("education")
            location = data.get("location")
            work = data.get("work")
            website = data.get("website")
            tagline = data.get("tagline")
            
            print(tagline, location, work, website, education, profile_pic, bio)
            
            if "profile_image" in request.files:
                file = request.files["profile_image"]
                if file and allowed_file(file.filename):
                    extension = file.filename.rsplit(".", 1)[1].lower()
                    filename = f"{local_id}.png"
                    file_path = os.path.join(app.config["profile_image"], filename)
                    file.save(file_path)

                    # Upload to Firebase Storage
                    profile_pic = f"https://snapvibe.share.zrok.io/static/profile_image/{filename}" if filename else None

                    # Here you can upload the image to Firebase Storage and get the URL
                    # profile_image_url = upload_to_firebase_storage(file_path, firebase_path)
                    
            else:
                profile_pic = f"https://snapvibe.share.zrok.io/static/profile_image/{local_id}.png"

            db.child("users").child(local_id).child("profile_data").update({
                "bio": bio,
                "profile_pic": profile_pic,
                "education": education,
                "location": location,
                "work": work,
                "website": website,
                "tagline": tagline
            }, token=token)

            return jsonify({"message": "Profile updated successfully!"}), 200
        
        user_data = db.child("users").child(local_id).get(token=token).val()
        response = make_response(render_template("edit_profile_page.html", user_data=user_data))
        
        if refresh_token:
            response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
        
        return response
    except Exception as e:
        print("Error fetching profile data:", e)
        return jsonify({"message": "An error occurred while fetching profile data"}), 500
    

app.config["post_data"] = "static/post_data"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}
os.makedirs("static/post_data", exist_ok=True)

def allowed_file_for_post(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

FILE_PATH = "image_ids.txt"  # File to store generated IDs

def generate_image_id():
    """Generate a unique 8-character image ID and store it in a file."""
    
    if not os.path.exists(FILE_PATH):
        open(FILE_PATH, 'w').close()  # Create file if it doesn't exist

    with open(FILE_PATH, 'r') as file:
        existing_ids = set(file.read().splitlines())  # Load existing IDs into a set

    while True:
        image_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        if image_id not in existing_ids:
            with open(FILE_PATH, 'a') as file:
                file.write(image_id + '\n')  # Store the new ID
            return image_id  # Return the unique ID
    
@app.route("/create-post", methods=['GET', 'POST'])
def create_post():
    token, refresh_token, issue_time = get_valid_token()
    
    
    if not token:
        return redirect(url_for("landing"))
    
    try:
        user = auth.get_account_info(token)
        local_id = user["users"][0]["localId"]
        
        if request.method == "POST":
            data = request.get_json()
            print(data)
            post_content = data.get('content')
            privacy = data.get('privacy')
            post_type = data.get("type")
            base64_media = data.get('media')
            media_name = data.get('mediaName')
            media_size = data.get('mediaSize')

            media_filename = None
            media_url = None

            # If there's media, decode and save it
            if base64_media is not None and media_name and allowed_file_for_post(media_name):
                try:
                    # Extract file extension and media type from base64 string
                    media_header = base64_media.split(";")[0]
                    media_type = media_header.split(":")[1]  # e.g. "image/png" or "video/mp4"
                    ext = media_name.split(".")[-1].lower()
                    
                    # Generate unique filename
                    id = generate_image_id()
                    media_filename = secure_filename(f"post_{id}.{ext}")
                    media_path = os.path.join(app.config['post_data'], media_filename)

                    # Decode and save the media file
                    media_data = base64.b64decode(base64_media.split(",")[1])
                    with open(media_path, "wb") as media_file:
                        media_file.write(media_data)

                    # Set the media URL based on type
                    media_url = f"https://snapvibe.share.zrok.io/static/post_data/{media_filename}"

                except Exception as e:
                    return jsonify({"success": False, "message": "Error processing media", "error": str(e)}), 400
            else:
                id = generate_image_id()
                
            try:
                user_data = db.child("users").child(local_id).get(token).val()
                username = user_data["username"]
                profile_pic = user_data["profile_data"]["profile_pic"]
                
            except:
                pass
            
            post_data = {
                "content": post_content,
                "privacy": privacy,
                "type": post_type,
                "media": media_url,
                "media_name": media_filename,
                "username": username,
                "profile_pic": profile_pic,
                "post_id": id,
                "user_id": local_id,
                "timestamp": str(datetime.datetime.now()),
                "likes": [],
                "comments": [],
                "shares": [],
            }
            
            try:
                if post_type == "image":
                    db.child("users").child(local_id).child("photos").child(id).set(media_url, token=token)
                    
                db.child("posts").child(id).set(post_data, token=token)
                db.child("users").child(local_id).child("posts").child(id).update(post_data, token=token)
                return jsonify({"success": True, "message": "Post created successfully!"}), 200
            except Exception as e:
                print("Error saving post:", e)
                return jsonify({"success": False, "message": "Error saving post"}), 500
            
    
        response = make_response(render_template("create_post_page.html"))
        
        if refresh_token:
            response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
        
        return response
            
            
            
    except:
        pass


@app.route("/like-post", methods=['POST'])
def like_post():
    token, refresh_token, issue_time = get_valid_token()
    
    if not token:
        return redirect(url_for("landing"))
    
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        post_info = data.get("id", "")
        action = data.get("action", "")  # Like or Unlike
        post_id, user_id, post_url = post_info.split("####", 2)
        
        

        if not post_info or action not in ["like", "unlike"]:
            return jsonify({"error": "400", "message": "Invalid request"}), 400
        
        try:
            # Verify the ID token and extract the user ID
            decoded_token = admin_auth.verify_id_token(token)
            user_id_2 = decoded_token.get("uid")
            print("User performing action:", user_id_2)
        except Exception as e:
            print("Error verifying token:", e)
            return jsonify({"message": "Invalid token"}), 401
        
        try:
            user_data = db.child("users").child(user_id_2).get(token=token).val()
            username = user_data["username"]
            
        except:
            username = "UnKnow user"
        
        try:
            # Check if the user has already liked the post
            check_like = db.child("posts").child(post_id).child("likes").child(user_id_2).get(token=token).val()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            if action == "like" and (check_like is None or not check_like):
                # Add a like
                db.child("posts").child(post_id).child("likes").child(user_id_2).update(
                    {"user_id": user_id_2, "timestamp": timestamp}, token=token
                )
                db.child("users").child(user_id).child("posts").child(post_id).child("likes").child(user_id_2).update(
                    {"user_id": user_id_2, "timestamp": timestamp}, token=token
                )
                db.child("notifications").child(user_id).child(str(timestamp)).set({"username":username,"user_id": user_id_2 ,"post_id":post_id, "timestamp": str(datetime.datetime.now()), "notifications":"Like post", "media":post_url}, token=token)
                db.child("is_new_notification").child(user_id_2).set({"is_new_notification":True}, token=token)
                response = make_response(jsonify({"message": "Post Liked"}), 200)

            elif check_like:
                # Remove a like
                db.child("posts").child(post_id).child("likes").child(user_id_2).remove(token=token)
                db.child("users").child(user_id).child("posts").child(post_id).child("likes").child(user_id_2).remove(
                    token=token
                )
                db.child("notifications").child(user_id).child(str(timestamp)).set({"username":username, "user_id": user_id ,"post_id":post_id, "timestamp": str(datetime.datetime.now()), "notifications":"Remove Like post", "media":post_url}, token=token)
                db.child("is_new_notification").child(user_id_2).set({"is_new_notification":True}, token=token)
                response = make_response(jsonify({"message": "Post Unliked"}), 200)

            response = make_response(jsonify({"message": "No changes made"}), 200)
            
            if refresh_token:
                response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
                response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
                response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
            
            return response

        except Exception as e:
            print("Error processing like/unlike action:", e)
            return jsonify({"message": "An error occurred"}), 500
        
        
@app.route('/post-action', methods=['POST'])
def post_action():
    token, refresh_token, issue_time = get_valid_token()
    
    if not token:
        return redirect(url_for("landing"))
    
    data = request.json
    action = data.get('action')
    post_id = data.get('button_id')
    
    if action == "delete":
        try:
            decoded_token = admin_auth.verify_id_token(token)
            user_id = decoded_token["uid"]
            
            db.child("posts").child(post_id).remove(token=token)
            db.child("users").child(user_id).child("posts").child(post_id).remove(token=token)
            response = make_response(jsonify({"success": True, "message": "Post Delete successfully!"}), 200)
        
            if refresh_token:
                response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
                response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
                response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
            
            return response
        except Exception as e:
            return jsonify({"success": False, "message": "Error to delete post!", "error": str(e)}), 400
        
        



@app.route('/api/comments', methods=['GET'])
def get_comments():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    post_id = request.args.get('post_id')
    if not post_id:
        return jsonify({'error': 'post_id parameter is required'}), 400
    
    comments = db.child("posts").child(post_id).child("comments").get(token=token).val()
    
    if comments is None:
        return jsonify([])
    
    # Convert OrderedDict to a list of comment dictionaries
    comments_list = list(comments.values()) if comments else []
    
    # Ensure all timestamps are strings (if they aren't already)
    for comment in comments_list:
        if 'timestamp' in comment and not isinstance(comment['timestamp'], str):
            comment['timestamp'] = str(comment['timestamp'])
    
    response = make_response(jsonify(comments_list))
    
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())

    return response

@app.route('/api/comments', methods=['POST'])
def add_comment():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    try:
        decoded_token = admin_auth.verify_id_token(token)  # Verify ID token
        user_id = decoded_token.get("uid")  # Get Firebase user ID

        # Fetch user data
        user_data = db.child("users").child(user_id).get(token).val()
        if user_data:
            username = user_data["username"]
            user_profile_pic = f"https://snapvibe.share.zrok.io/static/profile_image/{user_id}.png"

    except:
        return jsonify({"error": "401", "message": "Unauthorized"}), 401
    
    data = request.json
    
    # Validate input
    if not data or 'post_id' not in data or 'content' not in data:
        return jsonify({'error': 'post_id and content are required'}), 400
    
    post_id = data['post_id']
    content = data['content'].strip()
    user_id_2 = data["email"]
    image_url = data["url"]
    
    print(user_id_2, image_url)
    
    if not content:
        return jsonify({'error': 'Comment cannot be empty'}), 400

    
    # Create new comment with enhanced structure
    new_comment = {
        'id': str(uuid.uuid4()),  # Unique ID for each comment
        'content': content,
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),  # Fixed: using datetime.now with timezone
        'user': {
            'id': user_id,
            'name': username,
            'avatar': user_profile_pic,
        },
        'likes': [],  # Initialize likes count
        'replies': []  # Initialize empty replies array
    }
    
    db.child("users").child(user_id_2).child("posts").child(post_id).child("comments").child(new_comment['id']).set(new_comment, token=token)
    db.child("posts").child(post_id).child("comments").child(new_comment['id']).set(new_comment, token=token)
    db.child("notifications").child(user_id_2).child(str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))).set({"username": username, "user_id":user_id, "timestamp": str(datetime.datetime.now()), "notifications": "comment", "comment": content, "media":image_url, "post_id":post_id}, token=token)
    db.child("is_new_notification").child(user_id_2).set({"is_new_notification":True}, token=token)
    
    response = make_response(jsonify(new_comment), 201)
    
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response


@app.route("/user/<username>")
def user_profile(username):
    token, refresh_token, issue_time = get_valid_token()
    
    
    if not token:
        return redirect(url_for("landing"))
    
    if username:
    
        try:
            decoded_token = admin_auth.verify_id_token(token)
            local_id = decoded_token.get("uid")
            
            user_id_token = db.child("usernames").child(username).get(token=token).val()
            user_following = db.child("users").child(local_id).child("following").get(token=token).val()
            
            user_following = list(user_following) if user_following else []
            
            if not user_id_token:
                return jsonify({"message": "User not found"}), 404
            
            user_profile_data = db.child("users").child(user_id_token).get(token=token).val()
            saved_posts = db.child("saved_posts").child(local_id).get(token=token).val()
            notifications = db.child("is_new_notification").child(local_id).get(token=token).val()
            if notifications is not None:
                notifications = notifications
            else:
                notifications = {"is_new_notification": False}
            
            saved_posts_id_list = list(saved_posts) if saved_posts else []
            
            if "website" in user_profile_data["profile_data"]:
                website = user_profile_data["profile_data"]["website"]
                domain = urlparse(website).netloc
            
        except Exception as e:
            print("Error fetching user profile data:", e)
            user_profile_data = {}
            local_id = ""
            domain = ""
            user_id_token = ""
            saved_posts_id_list = []
        
        print(user_id_token, user_profile_data)
        response = make_response(render_template("user_profile_page.html", user_following=user_following, user_data=user_profile_data, user_id=user_id_token, domain=domain, local_id=local_id, saved_posts_id_list=saved_posts_id_list, notifications=notifications))
        
        if refresh_token:
            response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
        
        return response
    
    


@app.route("/photos")
def photos():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))  
    
    try:
        decoded_token = admin_auth.verify_id_token(token)
        local_id = decoded_token.get("uid")
        
        photos = db.child("users").child(local_id).child("photos").get(token=token).val()
        
        photos_list = []
        
        for i in photos:
            photos_list.append(photos[i])
    except:
        photos = {}
        local_id = ""
        photos_list = []
    
    response = make_response(render_template("photos.html", photos=photos, local_id=local_id, photos_list=photos_list))
    
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response


@app.route("/get-posts", methods=["Get"])
def get_posts():
    token, refresh_token, issue_time = get_valid_token()

    if not token:
        return redirect(url_for("landing"))

    if request.method == "GET":
        try:
            decoded_token = admin_auth.verify_id_token(token)
            local_id = decoded_token.get("uid")
            
            posts = db.child("posts").get(token=token).val()
            
            
            
            if posts:
                response = make_response(jsonify({"posts": posts}))
            else:
                response = make_response(jsonify({"posts": None}))
                
        except:
            response = make_response(jsonify({"posts": None}))
        
        
        if refresh_token:
            response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
        
        return response


@app.route("/save-post", methods=['POST'])
def save_post():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    if request.method == 'POST':
        data = request.get_json()
        post_id = data.get("id", "")
        action = data.get("action", "")
        
        if not post_id or action not in ["save", "unsave"]:
            return jsonify({"error": "400", "message": "Invalid request"}), 400

        try:
            decoded_token = admin_auth.verify_id_token(token)  # Verify ID token
            user_id = decoded_token.get("uid")  # Get Firebase user IDl"

        except:
            return jsonify({"error": "401", "message": "Unauthorized"}), 401

        # Check if user already liked the post
        save_post = db.child("saved_posts").child(user_id).child(post_id).get(token).val()

        if action == "save" and save_post is None:
            data = {"post_id": post_id, "time": str(datetime.datetime.now())}
            db.child("saved_posts").child(user_id).child(post_id).set(data, token)
            response = make_response(jsonify({"success": "kkk", "message": "Saved successfully"}), 200)

        elif save_post:
            db.child("saved_posts").child(user_id).child(post_id).remove(token)
            response = make_response( jsonify({"success": "kkkk", "message": "Unsaved  successfully"}), 200)

        else:
            response = make_response(jsonify({"message": "No changes made"}), 200)
    
    
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response
    
@app.route("/saved-posts")
def saved_posts():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    try:
        decoded_token = admin_auth.verify_id_token(token)  # Verify ID token
        user_id = decoded_token.get("uid")
        
        saved_posts_id = db.child("saved_posts").child(user_id).get(token=token).val()
        
        saved_posts_data = {}
        
        if saved_posts_id:
            saved_posts_id = list(saved_posts_id)
            for i in saved_posts_id:
                data = db.child("posts").child(i).get(token=token).val()
                saved_posts_data[i] = data


        notifications = db.child("is_new_notification").child(user_id).get(token=token).val()
        if notifications is not None:
            notifications = notifications
        else:
            notifications = {"is_new_notification": False}
                
        
    except:
        saved_posts = {}
        
    response = make_response(render_template("saved_posts_page.html", notifications=notifications, saved_posts_data=saved_posts_data, local_id=user_id, saved_posts_id_list=saved_posts_id))
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response

    

@app.route("/notifications")
def notifications():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    try:
        decoded_token = admin_auth.verify_id_token(token)
        local_id = decoded_token.get("uid")
        
        notifications = db.child("notifications").child(local_id).get(token=token).val()
        db.child("is_new_notification").child(local_id).set({"is_new_notification":False}, token=token)
        
        notifications_id = list(notifications)[::-1]
        
    except:
        notifications_id = []
        
    response = make_response(render_template("notifications_page.html", notifications=notifications, notifications_id=notifications_id))
    
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
        
    return response


@app.route("/share/<string:post_id>")
def share(post_id):
    if post_id:
        token, refresh_token, issue_time = get_valid_token()
        if not token:
            return redirect(url_for("landing"))
        
        try:
            decoded_token = admin_auth.verify_id_token(token)
            local_id = decoded_token.get("uid")
            
            notification = db.child("is_new_notification").child(local_id).get(token=token).val()
            post_data = db.child("posts").child(post_id).get(token=token).val()
            saved_posts_id = db.child("saved_posts").child(local_id).get(token=token).val()
            post_data = {post_id:post_data}
            if saved_posts_id is not None:
                saved_posts_id_list = list(saved_posts_id)
            else:
                saved_posts_id_list = []
            
        except:
            pass
        
        response = make_response(render_template("share_post_page.html", saved_posts_data=post_data, notification=notification, local_id=local_id, saved_posts_id_list=saved_posts_id_list))
        
        if refresh_token:
            response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
        
        return response


@app.route("/view/<string:post_id>")
def view(post_id):
    if post_id:
        token, refresh_token, issue_time = get_valid_token()
        if not token:
            return redirect(url_for("landing"))
        
        try:
            decoded_token = admin_auth.verify_id_token(token)
            local_id = decoded_token.get("uid")
            
            post_data = db.child("posts").child(post_id).get(token=token).val()
            saved_posts_id = db.child("saved_posts").child(local_id).get(token=token).val()
            post_data = {post_id:post_data}
            if saved_posts_id is not None:
                saved_posts_id_list = list(saved_posts_id)
            else:
                saved_posts_id_list = []
            
        except:
            pass
        
        response = make_response(render_template("view_post_page.html", saved_posts_data=post_data, local_id=local_id, saved_posts_id_list=saved_posts_id_list))

        if refresh_token:
            response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
        
        return response

def get_ai_answer(Conversation):
    client = Groq(api_key="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")
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=Conversation,
            temperature=1,
            max_tokens=1024,  # Replace max_completion_tokens with max_tokens
            top_p=1,
            stream=False,
            stop=None,
        )
        answer = completion.choices[0].message.content
        return answer

    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, there was an error processing your request."
    

@app.route("/get-ai-response", methods=["POST"])
def get_ai_response():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    if request.method == 'POST':
        data = request.get_json()
        
        answer = get_ai_answer(data["messages"])
        
        response = make_response(jsonify({"message":answer}), 200)
        if refresh_token:
            response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
        
        return response



@app.route("/ai")
def ai():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))

    response = make_response(render_template("testing.html"))
    
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response


@app.route("/api/following-user", methods=['POST'])
def following_user():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))

    data = request.get_json()
    username_to_follow = data.get("username")
    action = data.get("action", "follow")  # Default to follow if not specified
    
    if not username_to_follow:
        return jsonify({"error": "Username required"}), 400

    try:
        # Decode current user's token
        decoded_token = admin_auth.verify_id_token(token)
        local_id = decoded_token.get("uid")

        # Get current user's username
        local_username = db.child("users").child(local_id).child("username").get(token=token).val()

        # Get the user_id of the person to follow/unfollow
        target_user_id = db.child("usernames").child(username_to_follow).get(token=token).val()

        if not target_user_id:
            return jsonify({"error": "User not found"}), 404

        if action == "follow":
            # Update following for current user
            db.child("users").child(local_id).child("following").child(target_user_id).set({
                "username": username_to_follow,
                "user_id": target_user_id,
                "timestamp": str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            }, token=token)

            # Update followers for target user
            db.child("users").child(target_user_id).child("followers").child(local_id).set({
                "username": local_username,
                "user_id": local_id,
                "timestamp": str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            }, token=token)
            
            
            db.child("notifications").child(target_user_id).child(str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))).set({"username": local_username, "user_id":local_id, "timestamp": str(datetime.datetime.now()), "notifications": "Follow"}, token=token)
            db.child("is_new_notification").child(target_user_id).set({"is_new_notification":True}, token=token)

            response = make_response(jsonify({
                "message": "Followed successfully",
                "action": "follow",
                "status": "following"
            }), 200)

        elif action == "unfollow":
            # Remove from current user's following
            db.child("users").child(local_id).child("following").child(target_user_id).remove(token=token)

            # Remove from target user's followers
            db.child("users").child(target_user_id).child("followers").child(local_id).remove(token=token)
            
            
            db.child("notifications").child(target_user_id).child(str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))).set({"username": local_username, "user_id":local_id, "timestamp": str(datetime.datetime.now()), "notifications": "Unfollow"}, token=token)
            db.child("is_new_notification").child(target_user_id).set({"is_new_notification":True}, token=token)

            response = make_response(jsonify({
                "message": "Unfollowed successfully",
                "action": "unfollow",
                "status": "not_following"
            }), 200)

        else:
            response = make_response(jsonify({"error": "Invalid action"}), 400)
            

    except Exception as e:
        response = make_response(jsonify({"error": str(e)}), 500)
        
        
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response
    


@app.route('/upload-story', methods=['POST'])
def upload_story():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    try:
        decoded_token = admin_auth.verify_id_token(token)
        local_id = decoded_token.get("uid")
        
        user_data = db.child("users").child(local_id).get(token=token).val()
        username = user_data["username"]
        profile_pic = user_data["profile_data"]["profile_pic"]
        timestamp = str(datetime.datetime.now())

        story = request.files.get('story')
        media_type = request.form.get('media_type') 
        if story:
            # Save the file and process it
            os.makedirs('static/story', exist_ok=True)
            # Save file with proper path handling
            file_path = os.path.join('static', 'story', f'{local_id}.png' if media_type == "image" else f'{local_id}.mp4')
            story.save(file_path) 
              
            db.child("story").child(local_id).set({
                "user_id": local_id,
                "username": username,
                "profile_pic": profile_pic,
                "timestamp": timestamp,
                "story_views": {},
                "story": f"https://snapvibe.share.zrok.io/static/story/{local_id}.png" if media_type == "image" else f"https://snapvibe.share.zrok.io/static/story/{local_id}.mp4",
                "media_type": media_type,
                
            }, token=token)
            
            response = make_response(jsonify({'success': True}))
            
        else:
            response = make_response(jsonify({'success': False, 'message': 'No file uploaded'}), 400)
            
            
        if refresh_token:
            response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
            response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
        
        return response
    except:
        pass
       


@app.route("/add-story-views", methods=['POST'])
def add_story_viwes():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    try:
        decoded_token = admin_auth.verify_id_token(token)
        local_id = decoded_token.get("uid")
        username = db.child("users").child(local_id).child("username").get(token=token).val()
        data = request.get_json()
    
        db.child("story").child(data["user_id"]).child("story_views").child(local_id).set({"username": username, "profile_pic": f"https://snapvibe.share.zrok.io/static/profile_image/{local_id}.png", "user_id": local_id}, token=token)
        response = make_response(jsonify({"message": "view added"}), 200)

    except Exception as e:
        response = make_response(jsonify({"message": "view not added"}), 400)
    
    
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response
    
    

@app.route('/logout')
def logout():
    # Clear the cookies for authentication
    response = make_response(redirect(url_for('landing')))
    response.set_cookie('firebase_token', '', expires=0)
    response.set_cookie('refresh_token', '', expires=0)
    response.set_cookie('token_issue_time', '', expires=0)
    # return response
    return response


@app.route('/delete-story', methods=['POST'])
def delete_story():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    try:
        decoded_token = admin_auth.verify_id_token(token)
        local_id = decoded_token.get("uid")
        
        db.child("story").child(local_id).remove(token=token)
        
        response = make_response(jsonify({"success": "Story deleted successfully!"}), 200)
    except Exception as e:
        response = make_response(jsonify({"message": "An error occurred while deleting the story"}), 500)
        
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response
    
    

@app.route('/api/toggle-comment-like', methods=['POST'])
def add_comment_like():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    try:
        decoded_token = admin_auth.verify_id_token(token)
        local_id = decoded_token.get("uid")
        
        data = request.get_json()
        post_id = data.get("post_id")
        comment_id = data.get("comment_id")
        action = data.get("action")
        user_id = data.get("user_id")
        username = data.get("username")
        
        if action == "like":
            db.child("posts").child(post_id).child("comments").child(comment_id).child("likes").child(local_id).set({"user_id": local_id}, token=token)
            db.child("notifications").child(user_id).child(str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))).set({"username":username, "user_id": user_id ,"post_id":post_id, "timestamp": str(datetime.datetime.now()), "notifications":"Like comment"}, token=token)
            db.child("is_new_notification").child(user_id).set({"is_new_notification":True}, token=token)
            response = make_response(jsonify({"message": "Comment liked"}), 200)
            
        elif action == "unlike":
            db.child("posts").child(post_id).child("comments").child(comment_id).child("likes").child(local_id).remove(token=token)
            response = make_response(jsonify({"message": "Comment unliked"}), 200)
        
    except Exception as e:
        response = make_response(jsonify({"message": "An error occurred while adding comment like"}), 500)
    
    
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response
    
    
@app.route('/api/toggle-story-like', methods=['POST'])
def add_story_like():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    try:
        decoded_token = admin_auth.verify_id_token(token)
        local_id = decoded_token.get("uid")
        
        data = request.get_json()
        story_id = data.get("story_id")
        username = data.get("username")
        action = data.get("action")
        
        print(data)
        print(story_id)
        
        if action == "like":
            db.child("story").child(story_id).child("likes").child(local_id).set({"user_id": local_id, "username": username}, token=token)
            return jsonify({"success": "Story liked"}), 200
            
        elif action == "unlike":
            db.child("story").child(story_id).child("likes").child(local_id).remove(token=token)
            return jsonify({"success": "Story unliked"}), 200
        
    except Exception as e:
        print("Error adding story like:", e)
        return jsonify({"message": "An error occurred while adding story like"}), 500


@app.route('/api/change-privacy', methods=["POST"])
def changeprivacy():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))


    try:
        decoded_token = admin_auth.verify_id_token(token)
        local_id = decoded_token.get("uid")
        
        data = request.get_json()
        privacy = data.get("privacy")
        post_id = data.get("post_id")
        
        db.child("posts").child(post_id).update({"privacy": privacy}, token=token)
        db.child("users").child(local_id).child("posts").child(post_id).update({"privacy": privacy}, token=token)

        print(data)

        response = make_response(jsonify({"message": "Privacy is Change."}), 200)

    except:
        response = make_response(jsonify({"message": "Fail to change privacy"}), 400)
    
    
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response
    
    
@app.route('/api/delete-comment', methods=['POST'])
def delete_comment():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    try:
        data = request.get_json()
        comment_id = data.get('comment_id')
        post_id = data.get('post_id')
        user_id = data.get('user_id')
        username = data.get('username')

        if not comment_id or not post_id:
            return jsonify({"success": False, "message": "Invalid input"}), 400

        # Delete the comment from the database
        db.child("posts").child(post_id).child("comments").child(comment_id).remove(token=token)
        db.child("users").child(user_id).child("posts").child(post_id).child("comments").child(comment_id).remove(token=token)
        
        response = make_response(jsonify({"success": True, "message": "Comment deleted successfully"}), 200)

    except Exception as e:
        response = make_response(jsonify({"success": False, "message": "Failed to delete comment"}), 500)

    
    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response

@app.errorhandler(404)
def page_not_found(e):
    # Note the 404 status explicitly set
    return render_template('404_page.html'), 404


@app.route('/settings')
def settings():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))
    
    # try:
    #     decoded_token = admin_auth.verify_id_token(token)
    #     local_id = decoded_token.get("uid")
        
    #     user_data = db.child("users").child(local_id).get(token=token).val()
        
    #     if user_data:
    #         username = user_data["username"]
    #         profile_pic = user_data["profile_data"]["profile_pic"]
            
    # except Exception as e:
    #     print("Error fetching user data:", e)
        # username = ""
        # profile_pic = ""

    response = make_response(render_template("settings_page.html"), 200)

    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response


@app.route('/search')
def search():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))

    try:
        decoded_token = admin_auth.verify_id_token(token)
        local_id = decoded_token.get("uid")

        all_users = db.child("usernames").get(token=token).val()
        users_list = list(all_users)

        users_data = []

        if users_list:
            for i in users_list:
                users_data.append({"username": i, "id":all_users[i], "profilePic":f"https://snapvibe.share.zrok.io/static/profile_image/{all_users[i]}.png"})


    except Exception as e:
        users_data = []

    

    response = make_response(render_template("search_user_result.html", users_data=users_data))

    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response


@app.route("/settings/change-fullname", methods=['POST', 'GET'])
def change_full_name():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))


    try:
        decoded_token = admin_auth.verify_id_token(token)
        local_id = decoded_token.get("uid")

        name = db.child("users").child(local_id).child("name").get(token=token).val()
        if name is None:
            name = ""

    except:
        name=""

    if request.method == 'POST':
        try:
            decoded_token = admin_auth.verify_id_token(token)
            local_id = decoded_token.get("uid")

            data = request.get_json()
            print(data)
            if data:
                db.child("users").child(local_id).update({"name":data["fullName"]}, token=token)
                response = make_response(jsonify({"message": "Name Changed"}), 200)
        except:
            response = make_response(jsonify({"message": "Name Not Changed"}), 400)

    response = make_response(render_template("change_name_page.html", name=name))

    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response


@app.route("/settings/change-password", methods=['POST', 'GET'])
def change_password():
    token, refresh_token, issue_time = get_valid_token()
    if not token:
        return redirect(url_for("landing"))

    if request.method == 'POST':
        try:
            decoded_token = admin_auth.verify_id_token(token)
            local_id = decoded_token.get("uid")

            data = request.get_json()
            print(data)
            if data:
                response = make_response(jsonify({"message": "Password is changed"}), 200)
        except:
            response = make_response(jsonify({"message": "Password is not changed"}), 400)

    response = make_response(render_template("change_password_page.html"))

    if refresh_token:
        response.set_cookie("firebase_token", token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, max_age=timedelta(days=365).total_seconds())
        response.set_cookie("token_issue_time", issue_time, max_age=timedelta(days=365).total_seconds())
    
    return response




if __name__ == '__main__':
    app.run(debug=True)

