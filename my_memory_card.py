#импортируем модули
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QPixmap, QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout,
    QGroupBox, QButtonGroup, QRadioButton,
    QPushButton, QLabel, QMessageBox, QLineEdit
)
import random
from random import randint, shuffle
import subprocess

# Класс для создания объектов вопросов, содержащий вопрос, один правильный и три неправильных ответов
class Question():
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3, is_text_answer=False):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3
        self.is_text_answer = is_text_answer

# вопросы к программе
questions_list = [] 
questions_list.append(
    Question('Как назывался первый искусственный спутник Земли, запущенный в космос?', 'Спутник-1', 'Луна-1', 'Спутник-2', 'Земля-1'))
questions_list.append(
    Question('Какое государственное космическое агентство запустило первый спутник в космос?', 'СССР', 'США', 'Китай', 'Индия'))
questions_list.append(
    Question('Когда был запущен первый спутник Земли?', '4 октября 1957 года', '12 апреля 1961 года', '20 июля 1969 года', '29 августа 1965 года'))
questions_list.append(
    Question('Кто был первым космонавтом в истории человечества?', 'Юрий Гагарин', 'Нил Армстронг', 'Юрий Алексеевич', 'Алексей Леонов'))
questions_list.append(
    Question('В каком году состоялся первый полет человека в космос?', '1961', '1957', '1969', '1971'))
questions_list.append(
    Question('Как назывался корабль, на котором Юрий Гагарин совершил свой полет в космос?', 'Восток-1', 'Союз-1', 'Луна-1', 'Меркурий-3'))
questions_list.append(
    Question('Сколько времени длился первый полет Юрия Гагарина в космосе?', '108 минут', '1 час', '24 часа', '7 дней'))
questions_list.append(
    Question('Какое звание получил Юрий Гагарин за свой космический полет?', 'Герой Советского Союза', 'Заслуженный космонавт', 'Капитан космического флота', 'Почетный летчик'))
questions_list.append(
    Question('Какая космическая программа предшествовала полету Юрия Гагарина?', 'Восток', 'Союз', 'Луна', 'Марс'))
questions_list.append(
    Question('Где произошло приземление корабля с Юрием Гагариным после полета?', 'Саратовская область', 'Московская область', 'Ленинградская область', 'Красноярский край'))

# создаем окно
app = QApplication([])

# QPush кнопки
btn_OK = QPushButton('Ответить')
btn_start_game = QPushButton('Начать игру')
btn_Exit = QPushButton('Выход')
btn_EndTest = QPushButton('Перейти к концу теста')
lb_Question = QLabel('Самый сложный вопрос в мире!')

# все что снизу - графический интерфейс ( без стилей )
RadioGroupBox = QGroupBox("Варианты ответов")


rbtn_1 = QRadioButton('Вариант 1')
rbtn_2 = QRadioButton('Вариант 2')
rbtn_3 = QRadioButton('Вариант 3')
rbtn_4 = QRadioButton('Вариант 4')


RadioGroup = QButtonGroup() # это для группировки переключателей, чтобы управлять их поведением
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)


layout_ans1 = QHBoxLayout()   
layout_ans2 = QVBoxLayout() # вертикальные будут внутри горизонтального
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn_1) # два ответа в первый столбец
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3) # два ответа во второй столбец
layout_ans3.addWidget(rbtn_4)


layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3) # разместили столбцы в одной строке


RadioGroupBox.setLayout(layout_ans1) # готова "панель" с вариантами ответов 


AnsGroupBox = QGroupBox("Результат теста")
lb_Result = QLabel('прав ты или нет?') # здесь размещается надпись "правильно" или "неправильно"
lb_Correct = QLabel('ответ будет тут!') # здесь будет написан текст правильного ответа


layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter, stretch=2)
AnsGroupBox.setLayout(layout_res)
layout_line1 = QHBoxLayout() # вопрос
layout_line2 = QHBoxLayout() # варианты ответов или результат теста
layout_line3 = QHBoxLayout() # кнопка "Ответить"


layout_line1.addWidget(lb_Question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
layout_line2.addWidget(RadioGroupBox)   
layout_line2.addWidget(AnsGroupBox)  
AnsGroupBox.hide() # скроем панель с ответом, сначала должна быть видна панель вопросов


layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch=2) # кнопка ответить уже есть
layout_line3.addStretch(1)

layout_card = QVBoxLayout()


layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8) # Оставляем эту строку
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5)

# Функция для отображения панели с результатом ответа на вопрос.
def show_result():
    RadioGroupBox.hide()
    AnsGroupBox.show()
    lb_Picture.show()
    btn_OK.setText('Следующий вопрос')

# Функция для отображения панели с вопросом
def show_question():
    lb_Picture.hide()
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_OK.setText('Ответить')
    RadioGroup.setExclusive(False)
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    RadioGroup.setExclusive(True)

# Функция для проверки правильности ответа
def check_answer():
    if answers[0].isChecked():
        show_correct('Правильно!')
        window.score += 1
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            show_correct('Неверно!')

answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]

#  Функция для закрытия главного окна приложения.
def vixod():
    reply = QMessageBox.question(window, 'Выход', 'Вы уверены, что хотите выйти из программы?',
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        app.quit()
    else:
        reply2 = QMessageBox.question(window, 'Пройти тест заново', 'Желаете пройти тест заново?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply2 == QMessageBox.Yes:
            restart()
        else:
            run_application()



End = QLabel()

layout_line3.addWidget(btn_Exit, stretch=2)  # Добавляем кнопку "Выход" на форму один раз в начале
btn_Exit.clicked.connect(vixod)  # Назначаем обработчик нажатия кнопки "Выход"
btn_Exit.hide()


# Функция вызывается, когда пользователь завершает вопросы и показывает итоговый результат.
def happy_End():
    window.setLayout(layout_card)
    
    if window.score == 10:
        lb_Result.setText(f"Тест окончен!\nПравильных ответов: {window.score} из 10.\nВсего вопросов: 10.\nВаш рейтинг: {window.score / window.total * 100:.2f}% \nПасхалка №3: На данную программу ушло больше 20 часов работы🤯")
    else:
        lb_Result.setText(f"Тест окончен!\nПравильных ответов: {window.score} из 10.\nВсего вопросов: 10.\nВаш рейтинг: {window.score / window.total * 100:.2f}%")

    layout_res.setAlignment(Qt.AlignCenter)
    AnsGroupBox.setTitle("Результаты теста")
    show_result()
    btn_Exit.show()
    btn_EndTest.hide()

    btn_OK.setText('Начать сначала')
    btn_OK.clicked.disconnect()
    btn_OK.clicked.connect(restart)


# Функция для начала новых вопросов, сбрасывает текущий прогресс пользователя и генерирует новые вопросы.
def restart():
    window.score = 0
    window.total = 0

    window.question_list = questions_list.copy()

    next_question()

    btn_OK.setText('Ответить')
    btn_OK.clicked.disconnect()
    btn_OK.clicked.connect(click_OK)

window = QWidget()  
window.restarts = 0
# Функция обновляет стили элементов интерфейса, таких как кнопки и надписи.
def style():
    global answers, btn_Exit, btn_OK
    new_font = "18px"
    btn_OK.setStyleSheet(f"background-color: lightblue; font-size: {new_font};")
    btn_Exit.setStyleSheet(f"background-color: lightblue; font-size: {new_font};")
    btn_EndTest.setStyleSheet(f"background-color: lightblue; font-size: {new_font};")
    
    lb_Question.setStyleSheet(f"font-size: {new_font}; font-weight: bold;")
    lb_Result.setStyleSheet(f"font-size: {new_font}; font-weight: bold;")
    lb_Correct.setStyleSheet(f"font-size: {new_font};")
    
    # Обновление стиля для радиокнопок
    for btn in answers:
        btn.setStyleSheet(f"font-size: {new_font};")
    
    # Новый стиль для RadioGroupBox
    RadioGroupBox.setStyleSheet(f"font-size: {new_font}; padding: 10px; background-color: lightgrey;")

    # Стиль для кнопок 'Начать сначала' и 'Выход'
    btn_OK.setStyleSheet(
        "QPushButton {"
        "   font-size: 18px;"
        "   padding: 10px;"
        "   background-color: #00CC66;"  # Новый цвет фона кнопки
        "   border-radius: 5px;"
        "}"
        "QPushButton:hover {"
        "   background-color: #33FF99;"  # Цвет фона кнопки при наведении
        "}"
    )
    
    btn_Exit.setStyleSheet(
        "QPushButton {"
        "   font-size: 18px;"
        "   padding: 10px;"
        "   background-color: #FF6666;"
        "   border-radius: 5px;"
        "}"
        "QPushButton:hover {"
        "   background-color: #FF9999;"
        "}"
    )    

style()

# Добавление космического стиля к окну "Memo Card Cosmos"
def apply_cosmic_style(window):
    window.setStyleSheet(
        """
        QWidget {
            background-color: #FFFFFF;  
            color: #000000;  
        }
        
        QGroupBox {
            background-color: #FFFFFF; 
            color: #000000;  
            border: 2px solid #FFFFFF;  
            border-radius: 5px;  
        }
        
        QRadioButton, QRadioButton::indicator {
            color: #04acac;  
        }
        
        QPushButton {
            background-color: #FFFFFF;  
            color: #000000;  
            border: 1px solid #FFFFFF; 
            border-radius: 5px; 
            padding: 5px 10px; 
        }
        
        QPushButton:hover {
            background-color: #1f4068;  
        }
        """
    )

apply_cosmic_style(window)

# Функция принимает объект вопроса, отображает его на интерфейсе и распределяет ответы случайным образом по переключателям.
def ask(q: Question):
    shuffle(answers) # перемешали список из кнопок, теперь на первом месте списка какая-то непредсказуемая кнопка
    answers[0].setText(q.right_answer) # первый элемент списка заполним правильным ответом, остальные - неверными
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    lb_Question.setText(q.question) # вопрос
    lb_Correct.setText(q.right_answer) # ответ 
    show_question() # показываем панель вопросов 

lb_Picture = QLabel(window) 
lb_Picture.hide()
lb_Picture.setAlignment(Qt.AlignCenter)
layout_card.addWidget(lb_Picture, 0, Qt.AlignCenter)

# Функция показывает пользователю, был ли его ответ правильным или нет.
def show_correct(res):
    lb_Result.setText(res)
    if res == 'Правильно!':
        lb_Result.setStyleSheet("font-size: 18; color: green;")
        pixmap = QPixmap("good.png")
    else:
        lb_Result.setStyleSheet("font-size: 18; color: red;")
        pixmap = QPixmap("bad.png")
    lb_Picture.setPixmap(pixmap.scaled(lb_Picture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    lb_Picture.show()
    show_result()

layout = QVBoxLayout()
layout.addStretch()
layout.addWidget(lb_Picture)
layout.addStretch()
lb_Picture.setAlignment(Qt.AlignCenter)
lb_Picture.setFixedSize(200, 200)   
lb_Picture.hide()      
    
remaining_questions = questions_list.copy()

def style2():
    show_correct.setStyleSheet(f"font-size: {new_font};")

def exit_test():
    happy_End()

def end_test():
    happy_End()

btn_Exit.clicked.connect(exit_test)
layout_line3.addWidget(btn_Exit)
btn_Exit.show()

# Функция выбирает следующий случайный вопрос из списка и вызывает ask() для его отображения.
def next_question():
    window.total += 1
    if window.question_list:
        cur_question = randint(0, len(window.question_list) - 1)
        q = window.question_list.pop(cur_question) 
        ask(q)
    else:
        happy_End()
  
# Функция-обработчик нажатия на кнопку "Ответить". Выполняет проверку ответа или переход к следующему вопросу в зависимости от текущего состояния.
def click_OK():
    if btn_OK.text() == 'Ответить':
        check_answer()
    else:
        next_question()

window.score = 0
window.total = 0
window.question_list = questions_list.copy()

# Инициализация интерфейса
btn_OK.clicked.connect(click_OK)
window.setLayout(layout_card)
window.setWindowTitle('Memo Card Cosmos')
style()
window.resize(400, 300)

next_question()

window.resize(600, 400)

# Класс начального окна программы. Предоставляет пользовательский интерфейс для начала вопросов и отображения информации об авторе.
class StartWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.Prog()

    def Prog(self):
        # Кнопка "начать игру"
        self.btn_start = QPushButton('Начать тест', self)
        self.btn_start.clicked.connect(self.startProg)

        self.btn_game = QPushButton('Игра: Угадай число', self)
        self.btn_game.clicked.connect(play_game)

        self.btn_run_game_py = QPushButton('Космическая игра', self)
        self.btn_run_game_py.clicked.connect(self.run_game_py)

        # Кнопка "показать автора"
        self.btn_author = QPushButton('Показать автора', self)
        self.btn_author.clicked.connect(self.Author)

        # Надпись с описанием программы
        self.description = QLabel('Эта программа создана Sderyabin(om). \n'
                                  'Для конкурса "Алгоритмика Ural 2024. EDUGAMES". \n'
                                  'Просто отвечайте на вопросы. \n'
                                  'Желаю вам удачи! \n'
                                  '(P.S. программа была переработана под конкурс)', self)

        # Кнопка "Пасхалка"
        self.btn_easter_egg = QPushButton('Пасхалка', self)
        self.btn_easter_egg.clicked.connect(self.show_easter_egg)

        # Размещаем элементы на начальном окне
        layout = QVBoxLayout(self)
        layout.addWidget(self.description)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_run_game_py)
        layout.addWidget(self.btn_game)
        layout.addWidget(self.btn_author)
        layout.addWidget(self.btn_easter_egg)
        
        self.setLayout(layout)
        self.setWindowTitle('Справка о программе')
        self.resize(300, 200)

        self.style2()

    # Метод для отображения сообщения о пасхалке
    def show_easter_egg(self):
        QMessageBox.information(self, 'Пасхалка №2', 'Я пытался подобрать космические цвета, но как-то не получилось :( \nПопробуй выполнить тест на максимальный балл что бы получить следующую пасхалку!:)')

# Метод класса StartWindow для определения и применения стилей к виджетам начального окна.
    def style2(self):
        # Настраиваем космические цвета для стилей
        button_color = QColor(63, 81, 181)  # Космический синий
        game_button_color = QColor(156, 39, 176)  # Космический фиолетовый
        background_color = QColor(33, 33, 33)  # Космический черный
        text_color = QColor(0, 0, 0)
        text_color2 = QColor(255, 255, 255)  # Белый

        # Устанавливаем палитру для виджета и его дочерних элементов
        palette = self.palette()

        # Настройка фона основного виджета
        palette.setColor(QPalette.Window, background_color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Общий стиль для кнопок
        text_style = f"""
        QLabel {{
            color: {text_color2.name()}; 
            font-size: 21px;
        }}
        """

        button_style = f"""
        QPushButton {{
            background-color: {button_color.name()};
            color: #fff;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
            font-size: 16px;
            margin: 10px;
        }}
        QPushButton:pressed {{
            background-color: {button_color.darker(50).name()};
        }}
        """

        game_button_style = f"""
        QPushButton {{
            background-color: {game_button_color.name()};
            color: #fff;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
            font-size: 16px;
            margin: 10px;
        }}
        QPushButton:pressed {{
            background-color: {game_button_color.darker(150).name()};
        }}
        QPushButton:hover {{
            background-color: {game_button_color.lighter(150).name()};
        }}
        """

        btn_easter_egg_style = f"""
        QPushButton {{
            background-color: transparent; 
            color: transparent;
            font-size: 5px;
            padding: 5px; 
            border-radius: 5px;
            border: none;
        }}
        QPushButton:hover {{
            background-color: #00FFFF; 
        }}
        """

        # Применяем стиль к кнопкам
        self.btn_run_game_py.setStyleSheet(game_button_style)
        self.description.setStyleSheet(text_style)
        self.btn_game.setStyleSheet(game_button_style)
        self.btn_start.setStyleSheet(button_style)
        self.btn_author.setStyleSheet(button_style)
        self.btn_easter_egg.setStyleSheet(btn_easter_egg_style)

        # Стать для QLabel
        self.setStyleSheet(f"color: {text_color.name()}; margin: 10px;")

# Метод класса StartWindow, который закрывает текущее окно и открывает главное окно викторины.
    def startProg(self):
        self.close()
        window.show()
# Метод класса StartWindow, который показывает информацию об авторе приложения.
    def Author(self):
        QMessageBox.information(self, 'Автор', 'Автор программы - sderyabin(или просто Сергей)')

    def run_game_py(self):
        try:
            subprocess.Popen(["python", "game.py"])
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка запуска", "Файл game.py не найден.")

# Класс для мини-игры "Угадай число"
class GuessNumberGame(QWidget):
    def __init__(self):
        super().__init__()
        self.Prog2()

    def Prog2(self):
        # Инициализация интерфейса игры
        self.setWindowTitle('Угадай число')
        self.resize(200, 150)
        self.number = randint(1, 100)  # Случайное число которое нужно угадать
        self.guess_count = 0  # Счетчик попыток

        self.lbl = QLabel('Я загадал число от 1 до 100, попробуй угадать', self)
        self.textbox = QLineEdit(self)
        self.btn_check = QPushButton('Проверить', self)
        self.btn_check.clicked.connect(self.otveti)

        # Распределение элементов на форме
        layout = QVBoxLayout(self)
        layout.addWidget(self.lbl)
        layout.addWidget(self.textbox)
        layout.addWidget(self.btn_check)

        self.setLayout(layout)
        self.show()

        self.lbl.setStyleSheet(f"font-size: 18; font-weight: bold;")
        self.btn_check.setStyleSheet(f"font-size: 18; font-weight: bold;")
        self.textbox.setStyleSheet(f"font-size: 18; font-weight: bold;")

    def otveti(self):
        # Проверка предположения игрока
        guess = int(self.textbox.text())
        self.guess_count += 1
        
        if guess < self.number:
            self.lbl.setText('Попробуй число побольше.')
        elif guess > self.number:
            self.lbl.setText('Попробуй число поменьше.')
        else:
            self.lbl.setText(f'Правильно! Вы угадали число с {self.guess_count} попытки. \nВ программе есть пасхалки, всего их 4(кстате, это одна из них. \nТы молодец что нашел её! \n Следующую подсказку поищи в окне "справка о программе")')
            self.btn_check.setEnabled(False)

# Функция для запуска игры "Угадай число"
def play_game():
    global guess_game
    guess_game = GuessNumberGame()

# Функция, запускающая главное окно приложения.
def run_application():
    start_window = StartWindow()
    start_window.show()
    app.exec_()

run_application()