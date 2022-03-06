from app import app
from flask import render_template, request, redirect
import users, areas, threads, messages


@app.route("/")
def index():
    print('/ (index)')
    #list = messages.get_list()
    #return render_template("index.html", count=len(list), messages=list)
    return render_template("login.html")

@app.route("/new_message<thread_id>", methods=["GET","POST"])
def new_message(thread_id):
    print('/new_message')
    thread_title = threads.get_title(thread_id)
    return render_template("new_message.html", thread_id=thread_id, thread_title=thread_title)

@app.route("/edit_message<message_id>", methods=["GET","POST"])
def edit_message(message_id):
    if request.method == "GET":
        print('/edit_message GET')
        message = messages.get_by_id(message_id)
        return render_template("edit_message.html", message_id=message[0], thread_id=message[1], content=message[2], user_id=message[3])
    # if request.method == "POST":
    #     print('/edit_message POST')
    #     message_id = request.form["message_id"]
    #     content = request.form["content"]
    #     if messages.edit(message_id, content):
    #         #return redirect("/")
    #         return redirect("/areas")
    #     return render_template("error.html", message="Viestin muuttaminen ei onnistunut")

@app.route("/handle_edit_message", methods=["GET","POST"])
def handle_edit_message():
    print('/handle_edit_message')
    message_id = request.form["message_id"]
    content = request.form["content"]
    users.check_csrf_token(request)
    if messages.edit(message_id, content):
        #return redirect("/")
        return redirect("/areas")
    return render_template("error.html", message="Viestin muuttaminen ei onnistunut")
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "GET":
#         print('/login GET')
#         return render_template("login.html")
#     if request.method == "POST":
#         print('/login POST')
#         username = request.form["username"]
#         password = request.form["password"]
#         if users.login(username, password):
#             #return redirect("/")
#             return redirect("/areas")
#         else:
#             return render_template("error.html", message="Väärä tunnus tai salasana")


@app.route("/new_thread<area_id>", methods=["GET","POST"])
def new_thread(area_id):
    print('/new_thread')
    area_name = areas.get_area_name(area_id)
    return render_template("new_thread.html", area_id=area_id, area_name=area_name)

@app.route("/new_area", methods=["GET","POST"])
def new_area():
    print('/new_area')
    #area_name = areas.get_area_name(area_id)
    return render_template("new_area.html")

@app.route("/new_secret_area", methods=["GET","POST"])
def new_secret_area():
    print('/new_secret_area')
    users_list = users.get_list_normal_users()
    return render_template("new_secret_area.html", users=users_list)

@app.route("/send_message", methods=["POST"])
def send_message():
    print('/send_message POST')
    content = request.form["content"]
    thread_id = request.form["thread_id"]
    users.check_csrf_token(request)
    if messages.send(content, thread_id):
        #return redirect("/")
        return redirect("/areas")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

@app.route("/create_thread", methods=["POST"])
def create_thread():
    print('/create_thread POST')
    thread_title = request.form["thread_title"]
    area_id = request.form["area_id"]
    users.check_csrf_token(request)
    if threads.create(thread_title, area_id):
        #return redirect("/")
        return redirect("/areas")
    else:
        return render_template("error.html", message="Ketjun luonti ei onnistunut")


@app.route("/create_area", methods=["POST"])
def create_area():
    print('/create_area POST')
    area_name = request.form["area_name"]
    users.check_csrf_token(request)
    if areas.create(area_name):
        #return redirect("/")
        return redirect("/areas")
    else:
        return render_template("error.html", message="Alueen luonti ei onnistunut")

@app.route("/create_secret_area", methods=["POST"])
def create_secret_area():
    print('/create_secret_area POST')
    area_name = request.form["area_name"]
    users_list = request.form.getlist("users")
    users.check_csrf_token(request)
    print(users_list)
    if areas.create_secret(area_name, users_list):
        #return redirect("/")
        return redirect("/areas")
    else:
        return render_template("error.html", message="Salaisen alueen luonti ei onnistunut")

@app.route("/delete_message<message_id>", methods=["GET","POST"])
def delete_message(message_id):
    print(f'/delete_message POST, message_id: {message_id}')
    if messages.delete(message_id):
        #return redirect("/")
        return redirect("/areas")
    else:
        return render_template("error.html", message="Viestin poistaminen ei onnistunut")

@app.route("/delete_thread<thread_id>", methods=["GET","POST"])
def delete_thread(thread_id):
    print(f'/delete_thread POST, thread_id: {thread_id}')
    if threads.delete(thread_id):
        #return redirect("/")
        return redirect("/areas")
    else:
        return render_template("error.html", message="Ketjun poistaminen ei onnistunut")

@app.route("/delete_area<area_id>", methods=["GET","POST"])
def delete_area(area_id):
    print(f'/delete_area POST, area_id: {area_id}')
    if areas.delete(area_id):
        #return redirect("/")
        return redirect("/areas")
    else:
        return render_template("error.html", message="Alueen poistaminen ei onnistunut")

# @app.route("/send_message<thread_id>", methods=["GET","POST"])
# def send_message(thread_id):
#     print('/send_message')
#     content = request.form["content"]
#     if messages.send(content, thread_id):
#         #return redirect("/")
#         return redirect("/areas")
#     else:
#         return render_template("error.html", message="Viestin lähetys ei onnistunut")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        print('/login GET')
        return render_template("login.html")
    if request.method == "POST":
        print('/login POST')
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            #return redirect("/")
            return redirect("/areas")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    print('/logout')
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        print('/register GET')
        return render_template("register.html")
    if request.method == "POST":
        print('/register POST')
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        is_admin = bool(request.form["user_type"])
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1, is_admin):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")


@app.route("/areas")
def handle_areas():
    print('/areas')
    #list = messages.get_list()
    #return render_template("areas.html", count=len(list), messages=list)
    return render_template("areas.html", areas=areas.get_list())


@app.route("/threads<area_id>", methods=["GET", "POST"])
def handle_threads(area_id):
    area_name = areas.get_area_name(area_id)
    return render_template("threads.html", threads=threads.get_list(area_id), area_id=area_id, area_name=area_name)

@app.route("/messages<thread_id>", methods=["GET", "POST"])
def handle_messages(thread_id):
    thread_title = threads.get_title(thread_id)
    area_id = threads.get_area_id(thread_id)
    area_name = areas.get_area_name(area_id)
    return render_template(
        "messages.html", messages=messages.get_list(thread_id), thread_title=thread_title, 
        thread_id=thread_id,area_id=area_id, area_name=area_name
    )

@app.route("/search_messages", methods=["GET", "POST"])
def search_messages():
    #ls = threads.get_list(area_id)
    #return render_template("threads.html", threads=ls)
    #ls = messages.get_list(thread_id)
    searched_content = request.form["searched_content"]
    users.check_csrf_token(request)
    messages_list = messages.get_by_content(searched_content)
    return render_template("searched_messages.html", messages=messages_list)

# @app.route("/modify_subject<subject_name>", methods=["GET"])
# @login_required
# def render_modify_subject(subject_name):
#     vinkki = vinkki_service.palauta_vinkki(subject_name)[0]
#     return render_template("modify_subject.html", otsikko = vinkki.palauta_otsikko(), 
#         kirjailija = vinkki.palauta_kirjailija(), 
#         isbn = vinkki.palauta_isbn(), 
#         tagit = vinkki.palauta_tagit(), 
#         url = vinkki.palauta_url(), 
#         kommentti = vinkki.palauta_kommentti(), 
#         kuvaus = vinkki.palauta_kuvaus(), 
#         kurssit = vinkki.palauta_kurssit())


# @app.route("/modify_subject<subject_name>", methods=["GET", "POST"])
# @login_required
# def modify_subject(subject_name):
#     vanhaotsikko = subject_name
#     otsikko = request.form.get("otsikko")
#     kirjailija = request.form.get("kirjailija")
#     isbn = request.form.get("isbn")
#     tagit = request.form.get("tagit")
#     url = request.form.get("url")
#     kommentti = request.form.get("kommentti")
#     kuvaus = request.form.get("kuvaus")
#     kurssit = request.form.get("kurssit")
#     try:
#         vinkki_service.muokkaa_vinkkia(vanhaotsikko, otsikko, kirjailija, isbn, tagit, url, kommentti, kuvaus, kurssit)
#         return render_list()
#     except Exception as error:
#         flash(str(error))
#         return redirect_to_home()
