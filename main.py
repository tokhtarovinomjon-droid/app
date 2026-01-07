import flet as ft
import random
# questions.py файлынан ALL_DATA жүктейміз
from questions import ALL_DATA

# --- ТҮСТЕР ПАЛИТРАСЫ ---
COLORS = {
    "primary": "#4F46E5",       # Негізгі көк
    "secondary": "#10B981",     # Жасыл (Математика үшін)
    "accent": "#F59E0B",        # Қызғылт сары (Оқу сауаттылығы)
    "background": "#F3F4F6",    # Фон
    "text_main": "#111827",     # Мәтін
    "white": "#FFFFFF",
    "error": "#EF4444",
    "success": "#10B981"
}

def main(page: ft.Page):
    # Терезе баптаулары
    page.title = "№63 Қ.Сатбаев ҰБТ Бағдарламасы"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = COLORS["background"]
    page.window_width = 400
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Бағдарламаның жағдайы (state)
    state = {
        "current_subject": None, # "history", "math" немесе "reading"
        "questions": [],
        "current_index": 0,
        "score": 0
    }

    # ==========================================
    # 1. БАСТЫ МӘЗІР (Пән таңдау)
    # ==========================================
    def show_main_menu():
        page.clean()
        
        # Мектеп атауы мен тақырып
        header = ft.Column([
            ft.Icon(ft.Icons.SCHOOL, size=60, color=COLORS["primary"]),
            ft.Text("№63 Қ.Сатбаев", size=20, weight=ft.FontWeight.BOLD, color="grey"),
            # ТҮЗЕТІЛГЕН ЖЕР: weight=ft.FontWeight.W900 -> weight=ft.FontWeight.BOLD
            ft.Text("ҰБТ-ға дайындау бағдарламасы", size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=COLORS["text_main"]),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)

        # Пәнді таңдау функциясы
        def select_subject(e):
            subject_key = e.control.data # button-ның data өрісінен аламыз
            state["current_subject"] = subject_key
            show_settings_menu()

        # Батырмалар дизайны
        def create_subject_btn(text, icon, color, key):
            return ft.Container(
                content=ft.Row([
                    ft.Icon(icon, color="white", size=24),
                    ft.Text(text, color="white", size=16, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.START),
                width=320, height=70,
                bgcolor=color,
                border_radius=15,
                padding=ft.Padding(left=20, right=20, top=0, bottom=0),
                on_click=select_subject,
                data=key, # Пәннің кілтін сақтаймыз
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.3, color)),
                animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT)
            )

        # Карточканы жинау
        card = ft.Container(
            content=ft.Column([
                header,
                ft.Divider(height=30, color="transparent"),
                ft.Text("Пәнді таңдаңыз:", size=16, color="grey"),
                create_subject_btn("Қазақстан Тарихы", ft.Icons.HISTORY_EDU, COLORS["primary"], "history"),
                create_subject_btn("Математикалық сауаттылық", ft.Icons.CALCULATE, COLORS["secondary"], "math"),
                create_subject_btn("Оқу сауаттылығы", ft.Icons.MENU_BOOK, COLORS["accent"], "reading"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
            padding=30, bgcolor="white", border_radius=25,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.1, "black"))
        )

        page.add(card)
        page.update()

    # ==========================================
    # 2. БАПТАУ МӘЗІРІ (Сұрақ саны)
    # ==========================================
    def show_settings_menu():
        page.clean()

        # Қай пән таңдалғанын анықтау (тақырып үшін)
        subj_titles = {
            "history": "Қазақстан Тарихы",
            "math": "Мат. Сауаттылық",
            "reading": "Оқу Сауаттылығы"
        }
        current_title = subj_titles.get(state["current_subject"], "Тест")

        # Артқа қайту батырмасы
        btn_back = ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_main_menu(), icon_color="grey")

        # Сұрақ саны
        dd_count = ft.Dropdown(
            label="Сұрақ саны",
            width=280,
            value="5",
            options=[
                ft.dropdown.Option("5"),
                ft.dropdown.Option("10"),
                ft.dropdown.Option("20"),
            ],
            border_radius=12
        )

        # Қиындығы
        dd_diff = ft.Dropdown(
            label="Қиындығы",
            width=280,
            value="Орташа",
            options=[
                ft.dropdown.Option("Оңай"),
                ft.dropdown.Option("Орташа"),
                ft.dropdown.Option("Қиын"),
            ],
            border_radius=12
        )

        btn_start = ft.Container(
            content=ft.Text("БАСТАУ", size=18, weight=ft.FontWeight.BOLD, color="white"),
            width=280, height=60,
            bgcolor=COLORS["text_main"],
            border_radius=15,
            alignment=ft.Alignment(0, 0),
            on_click=lambda e: start_game(dd_count.value),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.3, "black"))
        )

        card = ft.Container(
            content=ft.Column([
                ft.Row([btn_back], alignment=ft.MainAxisAlignment.START),
                ft.Icon(ft.Icons.SETTINGS, size=50, color=COLORS["text_main"]),
                ft.Text(current_title, size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Параметрлерді таңдаңыз", color="grey"),
                ft.Divider(height=20, color="transparent"),
                dd_count,
                dd_diff,
                ft.Divider(height=20, color="transparent"),
                btn_start
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=30, bgcolor="white", border_radius=25,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.1, "black"))
        )

        page.add(card)
        page.update()

    # ==========================================
    # 3. ОЙЫН ЛОГИКАСЫ
    # ==========================================
    def start_game(count_str):
        state["score"] = 0
        state["current_index"] = 0
        
        # Таңдалған пән бойынша сұрақтарды аламыз
        subject_key = state["current_subject"]
        raw_questions = ALL_DATA.get(subject_key, [])

        # Егер сұрақтар аз болса, қолда барды аламыз
        # Тест үшін көбейтіп (shuffle) жасасақ болады
        pool = raw_questions * 5 # Сұрақ қоры аз болса көбейтеміз
        random.shuffle(pool)
        
        limit = int(count_str)
        state["questions"] = pool[:limit]
        
        load_question_screen()

    def load_question_screen():
        if state["current_index"] >= len(state["questions"]):
            show_result()
            return

        page.clean()
        index = state["current_index"]
        total = len(state["questions"])
        data = state["questions"][index]
        
        # Прогресс бар
        top_bar = ft.Row([
            ft.Text(f"Сұрақ {index + 1} / {total}", weight=ft.FontWeight.BOLD, color="grey"),
            ft.ProgressBar(width=150, value=(index+1)/total, color=COLORS["primary"], bgcolor="#E5E7EB")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        txt_question = ft.Text(
            data["q"], 
            size=18, weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=COLORS["text_main"]
        )

        btn_next = ft.Container(
            content=ft.Row([ft.Text("Келесі", color="white"), ft.Icon(ft.Icons.ARROW_FORWARD, color="white")], alignment=ft.MainAxisAlignment.CENTER),
            width=300, height=50, bgcolor=COLORS["text_main"], border_radius=12,
            opacity=0, ignore_interactions=True, animate_opacity=300,
            on_click=lambda e: next_question()
        )

        col_options = ft.Column(spacing=10)

        def check_answer(e):
            selected = e.control.data
            correct = data["a"]
            
            # Батырмаларды өшіру
            for btn in col_options.controls:
                btn.on_click = None
                if btn.data == correct:
                    btn.bgcolor = COLORS["success"]
                    btn.content.color = "white"
                elif btn.data == selected:
                    btn.bgcolor = COLORS["error"]
                    btn.content.color = "white"
                btn.update()

            if selected == correct:
                state["score"] += 1
            
            btn_next.opacity = 1
            btn_next.ignore_interactions = False
            btn_next.update()

        opts = data["opts"].copy()
        random.shuffle(opts)

        for opt in opts:
            btn = ft.Container(
                content=ft.Text(opt, size=16, color=COLORS["text_main"]),
                width=300, height=55, bgcolor="white",
                border=ft.Border.all(1, COLORS["text_main"]), border_radius=12,
                padding=ft.Padding(left=15, top=0, right=15, bottom=0),
                alignment=ft.Alignment(-1, 0),
                on_click=check_answer, data=opt,
                animate=200
            )
            col_options.controls.append(btn)

        card = ft.Container(
            content=ft.Column([
                top_bar,
                ft.Divider(height=20, color="transparent"),
                txt_question,
                ft.Divider(height=20, color="transparent"),
                col_options,
                ft.Divider(height=20, color="transparent"),
                btn_next
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=30, bgcolor="white", border_radius=25,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, "black"))
        )
        page.add(card)
        page.update()

    def next_question():
        state["current_index"] += 1
        load_question_screen()

    # ==========================================
    # 4. НӘТИЖЕ
    # ==========================================
    def show_result():
        page.clean()
        score = state["score"]
        total = len(state["questions"])
        
        card = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.EMOJI_EVENTS, size=80, color=COLORS["accent"]),
                ft.Text("Тест аяқталды!", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Нәтиже: {score} / {total}", size=22, color=COLORS["primary"]),
                ft.Divider(height=20),
                ft.Container(
                    content=ft.Text("Мәзірге оралу", color="white"),
                    width=200, height=50, bgcolor=COLORS["text_main"], border_radius=12,
                    alignment=ft.Alignment(0,0),
                    on_click=lambda e: show_main_menu()
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40, bgcolor="white", border_radius=25,
            shadow=ft.BoxShadow(blur_radius=20, color="black")
        )
        page.add(card)
        page.update()

    # Іске қосу
    show_main_menu()

if __name__ == "__main__":
    ft.run(main)
