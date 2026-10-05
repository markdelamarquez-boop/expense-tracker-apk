import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.core.window import Window

# Set smooth window size
Window.size = (390, 700)
Window.clearcolor = (0.07, 0.09, 0.15, 1)  # Deep Dark Theme Background

# --- DATABASE SETUP ---
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    amount REAL,
    category TEXT,
    date TEXT
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value REAL
)""")

cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('budget', 0.0)")
conn.commit()


# --- MODERN STYLED COMPONENTS ---

class GlassCard(BoxLayout):
    """Modern Rounded Container with Customizable Border and Background"""
    def __init__(self, bg_color=(0.12, 0.16, 0.24, 1), radius=16, border_color=None, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.radius = radius
        self.border_color = border_color
        
        with self.canvas.before:
            if self.border_color:
                Color(*self.border_color)
                self.border_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
            Color(*self.bg_color)
            self.rect = RoundedRectangle(
                pos=(self.pos[0] + 1, self.pos[1] + 1) if self.border_color else self.pos,
                size=(self.size[0] - 2, self.size[1] - 2) if self.border_color else self.size,
                radius=[self.radius]
            )
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        if self.border_color:
            self.border_rect.pos = instance.pos
            self.border_rect.size = instance.size
            self.rect.pos = (instance.pos[0] + 1, instance.pos[1] + 1)
            self.rect.size = (instance.size[0] - 2, instance.size[1] - 2)
        else:
            self.rect.pos = instance.pos
            self.rect.size = instance.size


class ModernButton(Button):
    """Custom Styled Action Button"""
    def __init__(self, bg_color=(0.05, 0.58, 0.53, 1), text_color=(1, 1, 1, 1), radius=12, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        self.color = text_color
        self.radius = radius
        
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class ModernInput(TextInput):
    """Sleek Styled Input Field"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0.12, 0.16, 0.24, 1)
        self.foreground_color = (0.9, 0.95, 1, 1)
        self.hint_text_color = (0.4, 0.48, 0.6, 1)
        self.cursor_color = (0.05, 0.58, 0.53, 1)
        self.padding = [14, 12, 14, 12]


class LogoBadge(BoxLayout):
    """Custom Modern Circular Logo Badge"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (70, 70)
        self.pos_hint = {'center_x': 0.5}
        
        with self.canvas.before:
            Color(0.05, 0.58, 0.53, 1)
            self.circle = Ellipse(pos=self.pos, size=self.size)
            
        self.bind(pos=self.update_circle, size=self.update_circle)
        
        lbl = Label(
            text="$", 
            font_size='36sp', 
            bold=True, 
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        self.add_widget(lbl)

    def update_circle(self, instance, value):
        self.circle.pos = instance.pos
        self.circle.size = instance.size


# --- SCREENS ---

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=[30, 40, 30, 40], spacing=20)

        # Header Section
        header_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.35)
        header_box.add_widget(LogoBadge())
        
        header_box.add_widget(Label(
            text="Expense Tracker", 
            font_size='26sp', 
            bold=True, 
            color=(0.95, 0.96, 0.98, 1),
            size_hint_y=0.3
        ))
        header_box.add_widget(Label(
            text="Manage your personal budget wisely", 
            font_size='13sp', 
            color=(0.5, 0.58, 0.7, 1),
            size_hint_y=0.2
        ))
        main_layout.add_widget(header_box)

        # Input Card
        form_card = GlassCard(
            orientation='vertical', 
            padding=18, 
            spacing=12, 
            size_hint_y=0.38,
            border_color=(0.2, 0.26, 0.36, 0.5)
        )

        self.username_input = ModernInput(hint_text="Username", multiline=False)
        self.password_input = ModernInput(hint_text="Password", password=True, multiline=False)

        form_card.add_widget(self.username_input)
        form_card.add_widget(self.password_input)

        btn_login = ModernButton(
            text="SIGN IN", 
            bg_color=(0.05, 0.58, 0.53, 1), 
            bold=True,
            font_size='15sp'
        )
        btn_login.bind(on_press=self.do_login)
        form_card.add_widget(btn_login)

        main_layout.add_widget(form_card)

        # Register Button Container
        actions_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.2)
        btn_register = ModernButton(
            text="Don't have an account? Sign Up", 
            bg_color=(0.15, 0.2, 0.3, 0.6), 
            text_color=(0.05, 0.68, 0.63, 1),
            font_size='13sp'
        )
        btn_register.bind(on_press=self.go_to_register)
        actions_box.add_widget(btn_register)

        main_layout.add_widget(actions_box)
        self.add_widget(main_layout)

    def do_login(self, instance):
        u = self.username_input.text.strip()
        p = self.password_input.text.strip()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        if cursor.fetchone():
            self.manager.transition = FadeTransition(duration=0.25)
            self.manager.current = "dashboard"
            self.manager.get_screen("dashboard").load_data()
        else:
            self.show_popup("Authentication Error", "Invalid username or password.")

    def go_to_register(self, instance):
        self.manager.transition = FadeTransition(duration=0.25)
        self.manager.current = "register"

    def show_popup(self, title, message):
        popup = Popup(
            title=title, 
            content=Label(text=message, color=(0.9, 0.9, 0.9, 1)), 
            size_hint=(0.82, 0.24)
        )
        popup.open()


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=[30, 40, 30, 40], spacing=20)

        header_box = BoxLayout(orientation='vertical', spacing=6, size_hint_y=0.25)
        header_box.add_widget(Label(
            text="Create Account", 
            font_size='24sp', 
            bold=True, 
            color=(0.95, 0.96, 0.98, 1)
        ))
        header_box.add_widget(Label(
            text="Start tracking your cashflow today", 
            font_size='13sp', 
            color=(0.5, 0.58, 0.7, 1)
        ))
        main_layout.add_widget(header_box)

        form_card = GlassCard(
            orientation='vertical', 
            padding=18, 
            spacing=12, 
            size_hint_y=0.45,
            border_color=(0.2, 0.26, 0.36, 0.5)
        )

        self.new_user_input = ModernInput(hint_text="Choose Username", multiline=False)
        self.new_pass_input = ModernInput(hint_text="Choose Password", password=True, multiline=False)

        form_card.add_widget(self.new_user_input)
        form_card.add_widget(self.new_pass_input)

        btn_reg = ModernButton(
            text="CREATE ACCOUNT", 
            bg_color=(0.2, 0.45, 0.85, 1), 
            bold=True,
            font_size='15sp'
        )
        btn_reg.bind(on_press=self.do_register)
        form_card.add_widget(btn_reg)

        main_layout.add_widget(form_card)

        btn_back = ModernButton(
            text="← Back to Sign In", 
            bg_color=(0.15, 0.2, 0.3, 0.6), 
            text_color=(0.7, 0.75, 0.85, 1),
            size_hint_y=0.1
        )
        btn_back.bind(on_press=self.go_back)
        main_layout.add_widget(btn_back)

        self.add_widget(main_layout)

    def do_register(self, instance):
        u = self.new_user_input.text.strip()
        p = self.new_pass_input.text.strip()

        if not u or not p:
            self.show_popup("Warning", "All fields are required!")
            return

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
            conn.commit()
            self.show_popup("Success", "Account created successfully!")
            self.go_back(None)
        except sqlite3.IntegrityError:
            self.show_popup("Error", "Username already taken!")

    def go_back(self, instance):
        self.manager.transition = FadeTransition(duration=0.25)
        self.manager.current = "login"

    def show_popup(self, title, message):
        popup = Popup(
            title=title, 
            content=Label(text=message, color=(0.9, 0.9, 0.9, 1)), 
            size_hint=(0.82, 0.24)
        )
        popup.open()


class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.monthly_budget = 0.0

        main_layout = BoxLayout(orientation='vertical', padding=[16, 20, 16, 16], spacing=12)

        # Header Bar
        header = BoxLayout(orientation='horizontal', size_hint_y=0.07)
        header.add_widget(Label(
            text="Dashboard", 
            font_size='22sp', 
            bold=True, 
            color=(0.95, 0.96, 0.98, 1), 
            halign='left',
            valign='middle'
        ))
        
        btn_logout = ModernButton(
            text="Logout", 
            bg_color=(0.8, 0.2, 0.25, 0.8), 
            size_hint_x=0.25,
            font_size='12sp'
        )
        btn_logout.bind(on_press=self.logout)
        header.add_widget(btn_logout)
        main_layout.add_widget(header)

        # Budget Summary Card
        self.card = GlassCard(
            orientation='vertical',
            padding=16,
            spacing=6,
            size_hint_y=0.25,
            bg_color=(0.1, 0.18, 0.28, 1),
            border_color=(0.05, 0.58, 0.53, 0.6)
        )

        # Pinalitan mula "Budget Target" patungong "Budget"
        self.lbl_budget = Label(text="Budget: PHP 0.00", font_size='13sp', color=(0.6, 0.7, 0.8, 1), halign='left')
        self.lbl_total = Label(text="PHP 0.00", font_size='28sp', bold=True, color=(1, 0.4, 0.45, 1), halign='left')
        self.lbl_remaining = Label(text="Remaining: PHP 0.00", font_size='13sp', color=(0.3, 0.85, 0.6, 1), halign='left')

        btn_set_budget = ModernButton(
            text="SET BUDGET", 
            bg_color=(0.05, 0.58, 0.53, 1), 
            bold=True,
            font_size='12sp',
            size_hint_y=0.35
        )
        btn_set_budget.bind(on_press=self.open_budget_popup)

        self.card.add_widget(self.lbl_budget)
        self.card.add_widget(self.lbl_total)
        self.card.add_widget(self.lbl_remaining)
        self.card.add_widget(btn_set_budget)

        main_layout.add_widget(self.card)

        # Quick Add Expense Form
        input_card = GlassCard(
            orientation='vertical',
            padding=12,
            spacing=8,
            size_hint_y=0.28,
            border_color=(0.2, 0.26, 0.36, 0.4)
        )

        self.desc_input = ModernInput(hint_text="Item Description (e.g. Dinner)", multiline=False)
        
        row_inputs = BoxLayout(orientation='horizontal', spacing=8)
        self.amt_input = ModernInput(hint_text="Amount", multiline=False, input_filter='float', size_hint_x=0.5)
        self.cat_input = ModernInput(hint_text="Category", multiline=False, size_hint_x=0.5)
        row_inputs.add_widget(self.amt_input)
        row_inputs.add_widget(self.cat_input)

        btn_add = ModernButton(
            text="+ Add Expense", 
            bg_color=(0.2, 0.45, 0.85, 1), 
            bold=True, 
            font_size='14sp'
        )
        btn_add.bind(on_press=self.add_expense)

        input_card.add_widget(self.desc_input)
        input_card.add_widget(row_inputs)
        input_card.add_widget(btn_add)

        main_layout.add_widget(input_card)

        # History Header
        main_layout.add_widget(Label(
            text="Recent Transactions", 
            font_size='14sp', 
            bold=True, 
            color=(0.6, 0.7, 0.8, 1), 
            size_hint_y=0.04,
            halign='left'
        ))

        # Expense History Scroll Area
        self.scroll = ScrollView(size_hint_y=0.36)
        self.expense_list = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.expense_list.bind(minimum_height=self.expense_list.setter('height'))
        self.scroll.add_widget(self.expense_list)

        main_layout.add_widget(self.scroll)
        self.add_widget(main_layout)

    def load_data(self):
        cursor.execute("SELECT value FROM settings WHERE key='budget'")
        row = cursor.fetchone()
        self.monthly_budget = row[0] if row else 0.0
        self.load_expenses()

    def open_budget_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=15, spacing=12)
        
        input_budget = ModernInput(
            text=str(self.monthly_budget) if self.monthly_budget > 0 else "",
            hint_text="Enter budget amount", 
            multiline=False, 
            input_filter='float'
        )
        
        btn_save = ModernButton(text="SAVE BUDGET", bg_color=(0.05, 0.58, 0.53, 1), bold=True)

        content.add_widget(Label(text="Enter Monthly Budget (PHP):", color=(0.8, 0.88, 1, 1)))
        content.add_widget(input_budget)
        content.add_widget(btn_save)

        popup = Popup(title="Set Budget", content=content, size_hint=(0.85, 0.32))

        def save_budget(btn_inst):
            val = input_budget.text.strip()
            if val:
                new_b = float(val)
                self.monthly_budget = new_b
                cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('budget', ?)", (new_b,))
                conn.commit()
                self.load_expenses()
            popup.dismiss()

        btn_save.bind(on_press=save_budget)
        popup.open()

    def add_expense(self, instance):
        desc = self.desc_input.text.strip()
        amt = self.amt_input.text.strip()
        cat = self.cat_input.text.strip() or "General"
        date_str = datetime.now().strftime("%b %d")

        if not desc or not amt:
            return

        cursor.execute("INSERT INTO expenses (description, amount, category, date) VALUES (?, ?, ?, ?)",
                       (desc, float(amt), cat, date_str))
        conn.commit()

        self.desc_input.text = ""
        self.amt_input.text = ""
        self.cat_input.text = ""
        
        self.load_expenses()

    def load_expenses(self):
        self.expense_list.clear_widgets()
        cursor.execute("SELECT id, description, amount, category, date FROM expenses ORDER BY id DESC")
        rows = cursor.fetchall()

        total = 0.0
        for row in rows:
            exp_id, desc, amt, cat, dt = row
            total += amt
            
            item_card = GlassCard(
                orientation='horizontal', 
                size_hint_y=None, 
                height=52, 
                padding=[12, 6, 12, 6], 
                spacing=10,
                bg_color=(0.12, 0.16, 0.24, 0.9),
                border_color=(0.18, 0.24, 0.34, 0.5)
            )

            info_box = BoxLayout(orientation='vertical', spacing=2)
            lbl_title = Label(
                text=f"{desc}", 
                font_size='13sp', 
                bold=True,
                color=(0.9, 0.95, 1, 1),
                halign='left'
            )
            lbl_sub = Label(
                text=f"{cat} • {dt}", 
                font_size='10sp', 
                color=(0.5, 0.6, 0.7, 1),
                halign='left'
            )
            info_box.add_widget(lbl_title)
            info_box.add_widget(lbl_sub)

            lbl_amt = Label(
                text=f"-₱{amt:.2f}", 
                font_size='13sp', 
                bold=True,
                color=(1, 0.45, 0.45, 1),
                size_hint_x=0.3
            )

            btn_del = ModernButton(
                text="X", 
                size_hint_x=0.12, 
                bg_color=(0.3, 0.15, 0.2, 0.6),
                text_color=(1, 0.4, 0.4, 1),
                radius=8
            )
            btn_del.bind(on_press=lambda inst, e_id=exp_id: self.delete_expense(e_id))

            item_card.add_widget(info_box)
            item_card.add_widget(lbl_amt)
            item_card.add_widget(btn_del)
            
            self.expense_list.add_widget(item_card)

        # Na-update na text label
        self.lbl_budget.text = f"Budget: PHP {self.monthly_budget:,.2f}"
        self.lbl_total.text = f"PHP {total:,.2f}"
        
        remaining = self.monthly_budget - total
        rem_color = (0.3, 0.85, 0.6, 1) if remaining >= 0 else (1, 0.35, 0.35, 1)
        self.lbl_remaining.color = rem_color
        self.lbl_remaining.text = f"Remaining: PHP {remaining:,.2f}"

    def delete_expense(self, exp_id):
        cursor.execute("DELETE FROM expenses WHERE id=?", (exp_id,))
        conn.commit()
        self.load_expenses()

    def logout(self, instance):
        self.manager.transition = FadeTransition(duration=0.25)
        self.manager.current = "login"


# --- MAIN APP ---
class ExpenseApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        return sm

if __name__ == '__main__':
    ExpenseApp().run()