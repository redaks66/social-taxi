@app.route("/profile", methods=["POST", "GET"])  # Страница с профилем
@login_required
def profile():
    login = session['userLogged']
    user_name, user_description, datetime = dbase.get_user_info(login)
    if request.method == 'POST':
        if len(request.form['login_message']) >= 2 and len(request.form['message_name']) >= 2 and \
                len(request.form['status_message']) >= 2 and len(request.form['text_message']) >= 2:
            res = dbase.add_message(request.form['login_message'], request.form['message_name'],
                                    request.form['status_message'], request.form['text_message'])
            if not res:
                flash('Ошибка добавления сообщения', category='error')
                print("Ошибка добавления сообщения")
                return redirect(url_for('profile'))
            else:
                flash('Сообщение добавлено успешно', category='success')
                print("Сообщение добавлено успешно")
                return redirect(url_for('profile'))
        else:
            flash('Минимум по 2 символа во всех полях', category='error')
            print('Минимум')
            return redirect(url_for('profile'))
    print("Профиль: " + user_name)
    return render_template("profile.html", menu=menu, menu_admin=menu_admin, user_name=user_name,
                           user_description=user_description, login=login, datetime=datetime)