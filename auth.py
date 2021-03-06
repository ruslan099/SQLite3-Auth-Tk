from tkinter import *
from tkinter import messagebox
import sqlite3
from class_database import Db

def app():
    main = Tk()
    main.title("Авторизация")
    main.geometry("300x200")
    main.resizable(False, False)
    main.configure(bg='#a2ab87')

    db = Db("database/users.db")

    def registration():
        main.destroy()
        win = Tk()
        win.title("Регистрация")
        win.geometry("300x300")
        win.configure(bg='#a2ab87')
        win.resizable(False, False)

        success = Label(win)
        error_null = Label(win)
        error_unique = Label(win)
        def create_user():
            success.configure(text="Регистрация успешна!", fg='green', bg='#a2ab87', font=('Courier', 12, 'bold'))
            success.pack_forget()
            error_null.configure(text="Заполните все поля!", fg='red', bg='#a2ab87', font=('Courier', 12, 'bold'))
            error_null.pack_forget()
            error_unique.configure(text="Данный логин занят!", fg='red', bg='#a2ab87', font=('Courier', 12, 'bold'))
            error_unique.pack_forget()

            fname = name.get()
            sname = surname.get()
            post_mail = post.get()
            nik = enter_logs.get()
            skip = enter_pas.get()

            try:
                if fname and sname and post_mail and nik and skip is not None:
                    #Добавление юзера в БД через метод класса class_database.py
                    db.add_to_db(fname, sname, post_mail, nik, skip)        
                    success.pack()
                    but_reg['text'] = 'Авторизация'
                    but_reg.configure(bg="grey", command=app)
                else:
                    error_null.pack()
            except sqlite3.IntegrityError:
                error_unique.pack()
            

        first_name = Label(win, text="Имя:", bg='#a2ab87')
        first_name.pack(pady=5)
        name = Entry(win, width=30, borderwidth=2)
        name.pack()
        
        last_name = Label(win, text="Фамилия:", bg='#a2ab87')
        last_name.pack()
        surname = Entry(win, width=30, borderwidth=2)
        surname.pack()

        mail = Label(win, text="Почта:", bg='#a2ab87')
        mail.pack()
        post = Entry(win, width=30, borderwidth=2)
        post.pack()

        logs = Label(win, text="Логин:", bg='#a2ab87')
        logs.pack()
        enter_logs = Entry(win, width=30, borderwidth=2)
        enter_logs.pack()

        pas = Label(win, text="Пароль:", bg='#a2ab87')
        pas.pack()
        enter_pas = Entry(win, show="*", width=30, borderwidth=2)
        enter_pas.pack()

        but_reg = Button(win, text="Регистрация", bg="#a3adcf", borderwidth=3, command=create_user)
        but_reg.pack(pady=10)
        win.mainloop() 

    login_okay = Label(main)
    login_error = Label(main)
    def account():
        login_okay.pack_forget()
        login_okay.configure(text="Вы успешно вошли!", fg='green', bg='#a2ab87', font=('Courier', 12, 'bold'))
        login_error.pack_forget()
        login_error.configure(text="Неверный логин/пароль", bg='#a2ab87', fg='red', font=('Courier', 12, 'bold'))

        login = inplogin.get()
        password = inppass.get()

        if bool(len(db.check_valid(login, password))) is True:      #Если равно 1(True), значит запись с таким же логином и паролем есть в БД.(УСПЕШНО)
            login_okay.pack()
            global res
            res = db.check_valid(login, password)
            but_log['text'] = 'В профиль!'
            but_log.configure(command=profile)
            inplogin.configure(state='disabled')
            inppass.configure(state='disabled')
            
        else:
            login_error.pack()
    
    def profile():
        main.destroy()
        win_profile = Tk()
        win_profile.geometry('300x250')
        win_profile.title(f'Профиль - {res[0][1]}')
        win_profile.configure(bg='#a2ab87')

        lbl_info = Label(win_profile, text="Информация о профиле", fg="black", bg="#a2ab87")
        lbl_info.configure(font=('Courier', 14, 'bold'))
        lbl_info.pack(pady=5)

        lbl_name = Label(win_profile, text=f"Имя: {res[0][1]}", fg="white", bg="#a2ab87")
        lbl_name.configure(font=('Courier', 10, 'bold'))
        lbl_name.pack(pady=2)
        
        lbl_surname = Label(win_profile, text=f"Фамилия: {res[0][2]}", fg="white", bg="#a2ab87")
        lbl_surname.configure(font=('Courier', 10, 'bold'))
        lbl_surname.pack(pady=2)

        lbl_mail = Label(win_profile, text=f"Почта: {res[0][3]}", fg="white", bg="#a2ab87")
        lbl_mail.configure(font=('Courier', 10, 'bold'))
        lbl_mail.pack(pady=2)

        lbl_login = Label(win_profile, text=f"Логин: {res[0][4]}", fg="white", bg="#a2ab87")
        lbl_login.configure(font=('Courier', 10, 'bold'))
        lbl_login.pack()

        def delete_acc():
            db.delete_account(res[0][0])
            messagebox.showinfo("Информация", f"Аккаунт с логином {res[0][1]} был удален!")
            win_profile.destroy()
            main.mainloop()

        but_del = Button(win_profile, text="Удалить аккаунт", bg="red", fg="white", borderwidth=3, width=20, height=2,
        command=delete_acc)
        but_del.pack(pady=20)

        win_profile.mainloop()

    login = Label(main, text="Логин:", bg='#a2ab87')
    login.pack()
    inplogin = Entry(main, width=30, borderwidth=2)
    inplogin.pack()

    passwd = Label(main, text="Пароль:", bg='#a2ab87')
    passwd.pack()
    inppass = Entry(main, show="*", width=30, borderwidth=2)
    inppass.pack()

    but_log = Button(main, text="Войти", command=account)
    but_log.pack(pady=5)
    reg = Button(main, text="Зарегистрироваться", command=registration)
    reg.pack(pady=2)

    main.mainloop()


if __name__ == '__main__':
    app()