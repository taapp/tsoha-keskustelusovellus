from flask import render_template, request, redirect, url_for
from app import app
import users
import areas
import threads
import messages


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/new_message<thread_id>", methods=["GET", "POST"])
def new_message(thread_id):
    thread_title = threads.get_title(thread_id)
    return render_template(
        "new_message.html", thread_id=thread_id, thread_title=thread_title
    )


@app.route("/edit_message<message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    if request.method == "GET":
        message = messages.get_by_id(message_id)
        thread_id = message[1]
        area_id = threads.get_area_id(thread_id)
        area_name = areas.get_area_name(area_id)
        thread_title = threads.get_title(thread_id)
        return render_template(
            "edit_message.html",
            message_id=message[0],
            thread_id=thread_id,
            content=message[2],
            user_id=message[3],
            area_id=area_id,
            area_name=area_name,
            thread_title=thread_title,
        )


@app.route("/handle_edit_message", methods=["GET", "POST"])
def handle_edit_message():
    message_id = request.form["message_id"]
    content = request.form["content"].strip()
    thread_id = messages.get_by_id(message_id)[1]
    if len(content) < 1:
        return render_template(
            "error.html",
            message="Viestin sisällön pitää olla ainakin yhden merkin pituinen.",
        )
    if len(content) > 500:
        return render_template(
            "error.html",
            message="Viestin sisällön pitää olla alle 500 merkin pituinen.",
        )
    users.check_csrf_token(request)
    if messages.edit(message_id, content):
        return redirect(url_for("handle_messages", thread_id=thread_id))
    return render_template("error.html", message="Viestin muuttaminen ei onnistunut")


@app.route("/new_thread<area_id>", methods=["GET", "POST"])
def new_thread(area_id):
    area_name = areas.get_area_name(area_id)
    return render_template("new_thread.html", area_id=area_id, area_name=area_name)


@app.route("/new_area", methods=["GET", "POST"])
def new_area():
    return render_template("new_area.html")


@app.route("/new_secret_area", methods=["GET", "POST"])
def new_secret_area():
    users_list = users.get_list_normal_users()
    return render_template("new_secret_area.html", users=users_list)


@app.route("/send_message", methods=["POST"])
def send_message():
    content = request.form["content"].strip()
    thread_id = request.form["thread_id"]
    users.check_csrf_token(request)
    if len(content) < 1:
        return render_template(
            "error.html",
            message="Viestin sisällön pitää olla ainakin yhden merkin pituinen.",
        )
    if len(content) > 500:
        return render_template(
            "error.html",
            message="Viestin sisällön pitää olla alle 500 merkin pituinen.",
        )
    if messages.send(content, thread_id):
        return redirect(url_for("handle_messages", thread_id=thread_id))
    return render_template("error.html", message="Viestin lähetys ei onnistunut")


@app.route("/create_thread", methods=["POST"])
def create_thread():
    thread_title = request.form["thread_title"].strip()
    area_id = request.form["area_id"]
    users.check_csrf_token(request)
    if len(thread_title) < 1:
        return render_template(
            "error.html",
            message="Ketjun otsikon pitää olla ainakin yhden merkin pituinen.",
        )
    if len(thread_title) > 40:
        return render_template(
            "error.html", message="Ketjun otsikon pitää olla alle 41 merkin pituinen."
        )
    if threads.create(thread_title, area_id):
        return redirect(url_for("handle_threads", area_id=area_id))
    return render_template("error.html", message="Ketjun luonti ei onnistunut")


@app.route("/create_area", methods=["POST"])
def create_area():
    area_name = request.form["area_name"].strip()
    users.check_csrf_token(request)
    if len(area_name) < 1:
        return render_template(
            "error.html",
            message="Alueen nimen pitää olla ainakin yhden merkin pituinen.",
        )
    if len(area_name) > 40:
        return render_template(
            "error.html", message="Alueen nimen pitää olla alle 41 merkin pituinen."
        )
    if areas.create(area_name):
        return redirect("/areas")
    return render_template("error.html", message="Alueen luonti ei onnistunut")


@app.route("/create_secret_area", methods=["POST"])
def create_secret_area():
    area_name = request.form["area_name"].strip()
    users_list = request.form.getlist("users")
    users.check_csrf_token(request)
    if len(area_name) < 1:
        return render_template(
            "error.html",
            message="Alueen nimen pitää olla ainakin yhden merkin pituinen.",
        )
    if len(area_name) > 40:
        return render_template(
            "error.html", message="Alueen nimen pitää olla alle 41 merkin pituinen."
        )
    if areas.create_secret(area_name, users_list):
        return redirect("/areas")
    return render_template("error.html", message="Salaisen alueen luonti ei onnistunut")


@app.route("/delete_message<message_id>", methods=["GET", "POST"])
def delete_message(message_id):
    thread_id = messages.get_by_id(message_id)[1]
    if messages.delete(message_id):
        return redirect(url_for("handle_messages", thread_id=thread_id))
    return render_template("error.html", message="Viestin poistaminen ei onnistunut")


@app.route("/delete_thread<thread_id>", methods=["GET", "POST"])
def delete_thread(thread_id):
    area_id = threads.get_area_id(thread_id)
    if threads.delete(thread_id):
        return redirect(url_for("handle_threads", area_id=area_id))
    return render_template("error.html", message="Ketjun poistaminen ei onnistunut")


@app.route("/delete_area<area_id>", methods=["GET", "POST"])
def delete_area(area_id):
    if areas.delete(area_id):
        return redirect("/areas")
    return render_template("error.html", message="Alueen poistaminen ei onnistunut")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/areas")
        return render_template("error.html", message="Väärä tunnus tai salasana")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"].strip()
        password1 = request.form["password1"].strip()
        password2 = request.form["password2"].strip()
        is_admin = bool(request.form["user_type"])
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if len(username) < 1:
            return render_template(
                "error.html",
                message="Käyttäjänimen pitää olla ainakin yhden merkin pituinen.",
            )
        if len(username) > 20:
            return render_template(
                "error.html",
                message="Käyttäjänimen pitää olla alle 21 merkin pituinen.",
            )
        if len(password1) < 1:
            return render_template(
                "error.html",
                message="Salasanan pitää olla ainakin yhden merkin pituinen.",
            )
        if len(password1) > 30:
            return render_template(
                "error.html", message="Salasanan pitää olla alle 31 merkin pituinen."
            )
        if users.register(username, password1, is_admin):
            return redirect("/")
        return render_template("error.html", message="Rekisteröinti ei onnistunut")


@app.route("/areas")
def handle_areas():
    return render_template("areas.html", areas=areas.get_list())


@app.route("/threads<area_id>", methods=["GET", "POST"])
def handle_threads(area_id):
    area_name = areas.get_area_name(area_id)
    return render_template(
        "threads.html",
        threads=threads.get_list(area_id),
        area_id=area_id,
        area_name=area_name,
    )


@app.route("/messages<thread_id>", methods=["GET", "POST"])
def handle_messages(thread_id):
    thread_title = threads.get_title(thread_id)
    area_id = threads.get_area_id(thread_id)
    area_name = areas.get_area_name(area_id)
    return render_template(
        "messages.html",
        messages=messages.get_list(thread_id),
        thread_title=thread_title,
        thread_id=thread_id,
        area_id=area_id,
        area_name=area_name,
    )


@app.route("/search_messages", methods=["GET", "POST"])
def search_messages():
    searched_content = request.form["searched_content"].strip()
    users.check_csrf_token(request)
    if len(searched_content) < 1:
        return render_template(
            "error.html",
            message="Etsityn sisällön pitää olla ainakin yhden merkin pituinen.",
        )
    if len(searched_content) > 30:
        return render_template(
            "error.html", message="Etsityn sisällön pitää olla alle 30 merkin pituinen."
        )
    messages_list = messages.get_by_content(searched_content)
    return render_template(
        "searched_messages.html",
        messages=messages_list,
        searched_content=searched_content,
    )
