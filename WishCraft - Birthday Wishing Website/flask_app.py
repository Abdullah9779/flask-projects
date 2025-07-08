from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from template import template_one
from template1 import template_two
from template2 import template_three
from datetime import datetime
import os
import shutil


app = Flask(__name__)



def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Set up the SMTP server and login
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade connection to secure encrypted connection
        server.login(sender_email, sender_password)

        # Create the email
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")




@app.route("/")
def home():
    templates = [
        {"id": 1, "name": "Birthday Countdown Card", "desc": "A stylish and classy template.", "image": "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%201%2FScreenshot%202025-02-11%20113107.png?alt=media&token=0f57058c-6f5e-40fd-9f4e-d30f0aff78b5"},
        {"id": 2, "name": "Birthday Countdown Card", "desc": "Elegant Text Template.", "image": "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%202%2FScreenshot%202025-02-13%20103407.png?alt=media&token=3713e2c9-c808-4924-b8cf-32a6a56c0c45"},
        {"id": 3, "name": "Birthday Countdown Card", "desc": "Light Color Template.", "image": "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%203%2FScreenshot%202025-02-13%20104546.png?alt=media&token=3033ca76-6623-4ba7-9ed0-2233ccc5d976"},
    ]
    return render_template("home.html", templates=templates)


@app.route("/view/<int:template_number>")
def view(template_number):
    # Dummy images for demonstration
    templates_pictures = {
        1: [
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%201%2FScreenshot%202025-02-11%20113107.png?alt=media&token=0f57058c-6f5e-40fd-9f4e-d30f0aff78b5",
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%201%2FScreenshot%202025-02-11%20113143.png?alt=media&token=a3c91fbc-e127-4b89-b6bb-72650abe63e4",
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%201%2FScreenshot%202025-02-11%20113221.png?alt=media&token=4ec87278-ae8e-49df-bb0e-33e61b350cf9",
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%201%2FScreenshot%202025-02-11%20113720.png?alt=media&token=5d1d1665-f299-4a7b-a1d6-702a9245aad2",
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%201%2FScreenshot%202025-02-11%20113848.png?alt=media&token=7ab6824f-f302-4fcd-acd5-752e0f213beb"

            ],
        2: [
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%202%2FScreenshot%202025-02-13%20103407.png?alt=media&token=3713e2c9-c808-4924-b8cf-32a6a56c0c45",
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%202%2FScreenshot%202025-02-13%20103809.png?alt=media&token=67a13ae3-3712-4852-9dad-8b56e1f58344",
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%202%2FScreenshot%202025-02-13%20103920.png?alt=media&token=2c08719e-11ec-490e-8d3c-2a67f2d2fed1",
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%202%2FScreenshot%202025-02-13%20104008.png?alt=media&token=ef628cb0-8da5-4e82-826f-e15894886292",
            ],
        3: [
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%203%2FScreenshot%202025-02-13%20104546.png?alt=media&token=3033ca76-6623-4ba7-9ed0-2233ccc5d976",
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%203%2FScreenshot%202025-02-13%20105552.png?alt=media&token=68e47d54-d0c1-4810-a8b6-18515762ccd2",
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%203%2FScreenshot%202025-02-13%20105615.png?alt=media&token=ac1c9e9d-7613-4cf3-966a-5769a68ff58f",
            "https://firebasestorage.googleapis.com/v0/b/buzzchat-user-data.appspot.com/o/My%20site%2FPicture%2FTemplate%203%2FScreenshot%202025-02-13%20105637.png?alt=media&token=e4ad5fe3-0fa4-4b8a-8383-992b7e8d424c",

            ],

    }

    pictures = templates_pictures.get(template_number, [])

    return render_template("view.html", template_number=template_number, templates_picture=pictures)



# Ensure the main upload folder exists
UPLOAD_FOLDER = "/home/abdullahtariq/mysite/static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/create-template/<int:template_number>", methods=["GET", "POST"])
def create_template(template_number):
    if request.method == "POST":
        name = request.form.get("name")
        date = request.form.get("date")
        wish = request.form.get("wish")
        song = request.form.get("song")
        code = request.form.get("code")

        # Create a user-specific folder
        user_folder = os.path.join(app.config["UPLOAD_FOLDER"], code)
        os.makedirs(user_folder, exist_ok=True)

        # Handle file uploads
        image_urls = []
        if "images" in request.files:
            images = request.files.getlist("images")
            for idx, image in enumerate(images, start=1):
                if image and allowed_file(image.filename):
                    ext = image.filename.rsplit(".", 1)[1].lower()
                    filename = f"{name}_{idx}.{ext}"
                    file_path = os.path.join(user_folder, filename)  # Save inside user folder
                    image.save(file_path)
                    image_urls.append(f"/static/uploads/{code}/{filename}")  # Store relative URL

        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")

        if not image_urls:
            return "Error: No images uploaded."

        # Generate HTML using the uploaded images
        if template_number == 1:
            html_code = template_one(name, formatted_date, wish, song, image_urls[1:], image_urls[0])
        elif template_number == 2:
            html_code = template_two(name, formatted_date, wish, song, image_urls[1:], image_urls[0])
        elif template_number == 3:
            html_code = template_three(name, formatted_date, wish, song, image_urls[1:], image_urls[0])

        # Save the HTML file in the same user folder
        html_filename = "Happy_Birthday.html"
        html_path = os.path.join(user_folder, html_filename)
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(html_code)

        # Redirect to the share page
        return redirect(url_for("path_screen", path=f"static%%uploads%%{code}%%{html_filename}"))

    return render_template("create_template.html", template_number=template_number)



@ app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if first_name and last_name and email and subject and message:

            recipient_email = "your-email@email.com"
            email1 = "to-send-mail@email.com"
            sender_password = "your-email-code"

            body = f"""
First Name : {first_name}

Last Name : {last_name}

Email : {email}

subject :

{message}
        """

            send_email(email1, sender_password, recipient_email, subject, body)

            return redirect("/mail-send")

    return render_template("contact.html")




@ app.route("/get-template")
def get_template():
    template_id = request.args.get("template_id")  # Get the template ID from URL parameters
    folder_path = f"/home/abdullahtariq/mysite/static/uploads/{template_id}"

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        return redirect(url_for("path_screen", path=f"static%%uploads%%{template_id}%%Happy_Birthday.html"))

    return render_template("get_template.html")






@ app.route("/mail-send")
def mail_send():
    return render_template("mail_send.html")

@ app.route("/path/<string:path>")
def path_screen(path):
    path = path.replace("%%", "/")
    path = f"https://abdullahtariq.pythonanywhere.com/{path}"

    return render_template("download_screen.html", path=path)


@ app.route("/about")
def about():
    return render_template("about.html")


@ app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")


@app.route("/delete-template", methods=['GET', 'POST'])
def delete_template():
    if request.method == "POST":
        template_id = request.form.get("template_id")  # Get the template ID from form data
        folder_path = f"/home/abdullahtariq/mysite/static/uploads/{template_id}"

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)  # Correctly delete the folder and its contents
            return f"""
                <div style="display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f8f9fa;">
                    <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); text-align: center;">
                        <h1 style="color: #28a745; font-size: 24px; font-weight: bold;">Template '{template_id}' Successfully Deleted</h1>
                        <p style="color: #6c757d; font-size: 16px;">The template has been permanently removed from the system.</p>
                        <a href="/" style="display: inline-block; margin-top: 10px; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Return Home</a>
                    </div>
                </div>
            """

    return render_template("delete_template.html")




