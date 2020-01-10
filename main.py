from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase


class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.username.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.username.text)

                self.reset()

                sm.current = "login"
            else:
                invalid_form()
        else:
            invalid_form()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.username.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def login_button(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "frij"
        else:
            invalid_login()

    def create_button(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created


class WindowManager(ScreenManager):
    pass


class FrijWindow(Screen):
    FrijInv = ObjectProperty(None)
    addItems = ObjectProperty(None)
    items = ObjectProperty(None)

    def current_inv_button(self):
        MainWindow.current = self.FrijInv
        sm.current = "FrijInv"

    def add_inv_button(self):
        MainWindow.current = self.addItems
        sm.current = "addItems"
        AddItems()

    @staticmethod
    def back():
        sm.current = "login"


class FrijInv(Screen):
    @staticmethod
    def back():
        sm.current = "frij"


class AddItems(Screen):
    def back(self):
        sm.current = "frij"
        self.reset()

    def reset(self):
        self.items.text = ""

    def input(self):
        pass


def invalid_login():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password. Try again'),
                size_hint=(None, None), size=(500, 500))

    pop.open()


def invalid_form():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"),
           FrijWindow(name="frij"), FrijInv(name="FrijInv"), AddItems(name="addItems")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
