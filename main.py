import sys
from datetime import datetime, date
import psycopg2
import re
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QListWidgetItem, QTableWidget, \
    QTableWidgetItem, QDialog, QFormLayout, QMessageBox
from PyQt5.QtWidgets import QComboBox, QDateEdit, QLabel
from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QListWidgetItem, QTableWidget, \
    QTableWidgetItem, QDialog, QFormLayout, QMessageBox, QLabel, QTextEdit

import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG)


def add_product(self):
    dialog = ProductDialog()
    if dialog.exec_() == QDialog.Accepted:
        product_data = dialog.get_product_data()
        logging.debug(f"Data from ProductDialog: {product_data}")
        # Валидация данных
        if not product_data["name"] or not product_data["composition"] or not product_data["price"] or not product_data[
            "expiration"] or not product_data["quantity"] or not product_data["description"]:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            logging.warning("Not all fields are filled.")
            return
        try:
            price = product_data["price"]
            quantity = int(product_data["quantity"])
            expiration_date = datetime.strptime(product_data["expiration"], "%Y-%m-%d").date()
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректные данные: {e}")
            logging.warning(f"Invalid input {e}")
            return
        try:
            row_position = self.product_table.rowCount()
            self.product_table.insertRow(row_position)
            self.product_table.setItem(row_position, 0, QTableWidgetItem(product_data["name"]))
            self.product_table.setItem(row_position, 1, QTableWidgetItem(product_data["composition"]))
            self.product_table.setItem(row_position, 2, QTableWidgetItem(str(price)))
            self.product_table.setItem(row_position, 3, QTableWidgetItem(expiration_date.strftime("%Y-%m-%d")))
            self.product_table.setItem(row_position, 4, QTableWidgetItem(str(quantity)))
            self.product_table.setItem(row_position, 5, QTableWidgetItem(product_data["description"]))
            query = """
                INSERT INTO products (name, composition, price, expiration, quantity, description)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            logging.debug(f"add_product query: {query}")
            self.cursor.execute(query, (
                product_data["name"],
                product_data["composition"],
                price,
                expiration_date,
                quantity,
                product_data["description"]
            ))
            self.connection.commit()
            QMessageBox.information(self, "Успех", "Товар успешно добавлен в базу данных.")
            logging.info("Product added successfully to DB.")
        except Exception as e:
            self.connection.rollback()
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить товар в базу данных: {e}")
            logging.error(f"Error adding product to database: {e}")

def is_valid_phone(phone):
    pattern = r'^\+7 \(\d{3}\) \d{3} \d{2} \d{2}$'
    return re.fullmatch(pattern, phone) is not None


class ProductDialog(QDialog):
    def __init__(self, product_data=None):
        super().__init__()
        self.setWindowTitle("Добавить товар" if product_data is None else "Редактировать товар")
        self.setFixedSize(500, 300)
        self.initUI()

        if product_data:
            self.name_input.setText(product_data["name"])
            self.composition_input.setText(product_data["composition"])
            self.price_input.setText(product_data["price"])
            self.expiration_input.setText(product_data["expiration"])
            self.quantity_input.setText(product_data["quantity"])
            self.description_input.setText(product_data["description"])

    def initUI(self):
        layout = QFormLayout()

        self.name_input = QtWidgets.QLineEdit(self)
        self.composition_input = QtWidgets.QLineEdit(self)
        self.price_input = QtWidgets.QLineEdit(self)
        self.expiration_input = QtWidgets.QLineEdit(self)
        self.quantity_input = QtWidgets.QLineEdit(self)
        self.description_input = QtWidgets.QLineEdit(self)

        layout.addRow("Наименование:", self.name_input)
        layout.addRow("Характеристики:", self.composition_input)
        layout.addRow("Длительность лицензии:", self.expiration_input)
        layout.addRow("Цена:", self.price_input)
        layout.addRow("Количество:", self.quantity_input)
        layout.addRow("Описание:", self.description_input)

        # Использование QDialogButtonBox для правильной работы кнопок
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def get_product_data(self):
        return {
            "name": self.name_input.text(),
            "composition": self.composition_input.text(),
            "price": self.price_input.text(),
            "expiration": self.expiration_input.text(),
            "quantity": self.quantity_input.text(),
            "description": self.description_input.text()
        }


class StaffDialog(QDialog):
    def __init__(self, staff_data=None):
        super().__init__()
        self.setWindowTitle("Добавить сотрудника" if staff_data is None else "Редактировать сотрудника")
        self.setFixedSize(500, 300)
        self.initUI()

        if staff_data:
            # Заполнение полей для редактирования
            self.last_name_input.setText(staff_data["last_name"])
            self.first_name_input.setText(staff_data["first_name"])
            self.middle_name_input.setText(staff_data["middle_name"])
            self.birth_date_input.setText(staff_data["birth_date"])
            self.phone_input.setText(staff_data["phone"])
            self.login_input.setText(staff_data["login"])
            self.password_input.setText(staff_data["password"])


    def initUI(self):
        layout = QFormLayout()

        self.last_name_input = QtWidgets.QLineEdit(self)
        self.first_name_input = QtWidgets.QLineEdit(self)
        self.middle_name_input = QtWidgets.QLineEdit(self)
        self.birth_date_input = QtWidgets.QLineEdit(self)  # Можно использовать QDateEdit для даты
        self.phone_input = QtWidgets.QLineEdit(self)
        self.login_input = QtWidgets.QLineEdit(self)
        self.password_input = QtWidgets.QLineEdit(self)

        layout.addRow("Фамилия:", self.last_name_input)
        layout.addRow("Имя:", self.first_name_input)
        layout.addRow("Отчество:", self.middle_name_input)
        layout.addRow("Дата Рождения:", self.birth_date_input)
        layout.addRow("Телефон:", self.phone_input)
        layout.addRow("Логин:", self.login_input)
        layout.addRow("Пароль:", self.password_input)

        # Использование QDialogButtonBox для правильной работы кнопок
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)
        self.setLayout(layout)


    def get_staff_data(self):
        return {
            "last_name": self.last_name_input.text(),
            "first_name": self.first_name_input.text(),
            "middle_name": self.middle_name_input.text(),
            "birth_date": self.birth_date_input.text(),
            "phone": self.phone_input.text(),
            "login": self.login_input.text(),
            "password": self.password_input.text()
        }


class Window(QWidget):
    def __init__(self, window_id, total_windows):
        super().__init__()
        self.window_id = window_id
        self.total_windows = total_windows
        self.setFixedSize(1200, 800)  # Устанавливаем размер окна
        self.setWindowTitle('База данных')  # Заголовок окна

        # Подключение к базе данных PostgreSQL
        self.connection = psycopg2.connect(
            dbname="my_tab_db",
            user="postgres",
            password="Ryzen52600!",
            host="localhost",
            port="5432"
        )
        self.cursor = self.connection.cursor()

        # Инициализация кнопок и других элементов
        self.initUI()

    def initUI(self):
        # Уникальное содержимое для каждого окна
        if self.window_id == 0:
            self.create_catalog_content()
        elif self.window_id == 1:
            self.create_cart_content()
        elif self.window_id == 2:
            self.create_sales_content()
        elif self.window_id == 3:
            self.create_product_content()
        elif self.window_id == 4:
            self.create_staff_content()
        elif self.window_id == 5:
            self.create_report_content()
        else:
            self.create_navigation_buttons()

    def create_report_content(self):
        self.create_navigation_buttons()

        # Комбобокс для выбора типа отчёта
        self.report_type_combo = QComboBox(self)
        self.report_type_combo.addItems(["sales", "stock", "staff"])
        self.report_type_combo.setGeometry(210, 100, 200, 30)

        # Поля для ввода даты (если нужно)
        self.start_date_label = QLabel("Начальная дата:", self)
        self.start_date_label.setGeometry(210, 150, 100, 30)
        self.start_date_input = QDateEdit(self)
        self.start_date_input.setDisplayFormat("yyyy-MM-dd")
        self.start_date_input.setDate(QDate.currentDate().addDays(-7))  # Устанавливаем неделю назад
        self.start_date_input.setGeometry(320, 150, 150, 30)

        self.end_date_label = QLabel("Конечная дата:", self)
        self.end_date_label.setGeometry(210, 200, 100, 30)
        self.end_date_input = QDateEdit(self)
        self.end_date_input.setDisplayFormat("yyyy-MM-dd")
        self.end_date_input.setDate(QDate.currentDate())  # Устанавливаем текущую дату
        self.end_date_input.setGeometry(320, 200, 150, 30)

        # Кнопка для генерации отчёта
        self.generate_report_button = QPushButton("Сформировать отчёт", self)
        self.generate_report_button.setGeometry(210, 250, 200, 50)
        self.generate_report_button.clicked.connect(self.generate_report)

        # Таблица для отображения отчёта
        self.report_table = QTableWidget(self)
        self.report_table.setGeometry(210, 320, 770, 400)
        self.report_table.setColumnCount(0)
        self.report_table.setRowCount(0)

    def get_report_query(self, report_type, start_date=None, end_date=None):
        """Генерирует SQL-запрос на основе типа отчета"""
        if report_type == "sales":
            query = """
                 SELECT o.order_date, p.name, p.price, s.last_name, s.first_name
                 FROM orders o
                 JOIN products p ON o.product_id = p.id
                 JOIN staff s ON o.staff_id = s.id
                 WHERE o.order_date BETWEEN %s AND %s;
             """
            return query, (start_date, end_date)
        elif report_type == "stock":
            return "SELECT name, quantity FROM products", None
        elif report_type == "staff":
            return "SELECT last_name, first_name, middle_name FROM staff", None
        elif report_type == "low_stock":
            return "SELECT name, quantity FROM products WHERE quantity < 10", None  # Пример: если товаров меньше 10
        elif report_type == "latest_products":
            return "SELECT name, price, expiration FROM products ORDER BY id DESC LIMIT 10", None  # Пример: 10 последних добавленных
        else:
            return None, None

    def fetch_report_data(self, query, params):
        """Выполняет SQL-запрос и возвращает данные"""
        try:
            self.cursor.execute(query, params) if params else self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные для отчета: {e}")
            return None

    def display_report(self, report_type, start_date=None, end_date=None):
        """Выполняет запрос, обрабатывает данные и отображает отчет в таблице."""
        query, params = self.get_report_query(report_type, start_date, end_date)
        if not query:
            QMessageBox.warning(self, "Ошибка", "Неизвестный тип отчета.")
            return

        data = self.fetch_report_data(query, params)

        if data is None:
            return

        self.report_table.clearContents()
        self.report_table.setRowCount(0)  # Очищаем предыдущие данные

        if not data:
            QMessageBox.information(self, "Информация", "Нет данных для данного отчета")
            return

        # Настройка столбцов в зависимости от типа отчета
        headers = []
        if report_type == "sales":
            headers = ["Дата заказа", "Товар", "Цена", "Фамилия сотрудника", "Имя сотрудника"]
        elif report_type == "stock":
            headers = ["Название", "Количество"]
        elif report_type == "staff":
            headers = ["Фамилия", "Имя", "Отчество"]
        elif report_type == "low_stock":
            headers = ["Название", "Количество"]
        elif report_type == "latest_products":
            headers = ["Название", "Цена", "Срок годности"]

        self.report_table.setColumnCount(len(headers))
        self.report_table.setHorizontalHeaderLabels(headers)

        for row_num, row_data in enumerate(data):
            self.report_table.insertRow(row_num)
            for col_num, cell_data in enumerate(row_data):
                if isinstance(cell_data, date):
                    self.report_table.setItem(row_num, col_num, QTableWidgetItem(cell_data.strftime("%Y-%m-%d")))
                else:
                    self.report_table.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

    def generate_report(self):
        """Обработчик нажатия на кнопку формирования отчета"""
        report_type = self.report_type_combo.currentText()
        start_date = self.start_date_input.date().toString(
            "yyyy-MM-dd") if self.start_date_input else None  # Получение даты начала
        end_date = self.end_date_input.date().toString(
            "yyyy-MM-dd") if self.end_date_input else None  # Получение даты конца
        self.display_report(report_type, start_date, end_date)

    def create_navigation_buttons(self):
        button_labels = ["Каталог", "Корзина", "Продажи", "Товары", "Персонал", "Отчёты"]

        for i, label in enumerate(button_labels):
            if i != self.window_id:  # Не создаем кнопку для самого окна
                btn = QPushButton(label, self)
                btn.setGeometry(20, 150 + i * 60, 180, 50)  # Задаем геометрию кнопок
                btn.clicked.connect(lambda checked, idx=i: self.go_to_window(idx))

    def create_cart_content(self):
        self.create_navigation_buttons()

        # Таблица для товаров
        self.cart_table = QTableWidget(self)
        self.cart_table.setGeometry(210, 150, 770, 400)
        self.cart_table.setColumnCount(2)
        self.cart_table.setHorizontalHeaderLabels(["Товар", "Количество"])
        self.cart_table.setColumnWidth(0, 600)
        self.cart_table.setColumnWidth(1, 150)
        self.cart_table.setRowCount(0)

        # Поле для выбора даты
        self.date_label = QLabel("Дата:", self)
        self.date_label.setGeometry(210, 570, 50, 30)
        self.date_input = QDateEdit(self)
        self.date_input.setGeometry(270, 570, 150, 30)
        self.date_input.setDate(QDate.currentDate())

       # Поле для суммы заказа
        self.total_label = QLabel("Сумма заказа:", self)
        self.total_label.setGeometry(500, 570, 100, 30)
        self.total_value_label = QLabel("0", self)
        self.total_value_label.setGeometry(610, 570, 100, 30)

    def create_catalog_content(self):
        # Добавляем кнопки в первом окне
        self.create_navigation_buttons()  # Добавляем навигационные кнопки

        # Добавляем дополнительные кнопки
        self.order_button = QPushButton('Создать заказ', self)
        self.order_button.setGeometry(1000, 300, 180, 50)  # Задаем позицию
        self.order_button.clicked.connect(self.on_order_button_click)

        self.search_line = QtWidgets.QLineEdit(self)
        self.search_line.setGeometry(210, 100, 770, 30)
        self.search_line.setPlaceholderText("Поиск товара...")

        self.product_catalog = QListWidget(self)
        self.product_catalog.setGeometry(210, 150, 770, 500)
        self.load_products_to_catalog() # Загружаем товары

    def load_products_to_catalog(self):
        try:
            self.cursor.execute("SELECT name FROM products;") # Извлекаем имена продуктов
            products = self.cursor.fetchall() # Получаем все строки

            self.product_catalog.clear()

            for product in products:
                 item = QListWidgetItem(product[0]) # имя продукта
                 item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                 item.setCheckState(QtCore.Qt.Unchecked)
                 self.product_catalog.addItem(item)

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить товары: {e}")

    def load_cart_data(self):
        self.cart_table.setRowCount(0)
        try:
            self.cursor.execute("""
                SELECT p.name, o.quantity, p.price
                FROM orders o
                JOIN products p ON o.product_id = p.id;
            """)
            orders = self.cursor.fetchall()
            if not orders:
                QMessageBox.information(self, "Информация", "Корзина пуста")
            for order in orders:
                row_position = self.cart_table.rowCount()
                self.cart_table.insertRow(row_position)
                self.cart_table.setItem(row_position, 0, QTableWidgetItem(order[0]))  # Имя товара
                self.cart_table.setItem(row_position, 1, QTableWidgetItem(str(order[1])))  # Количество
                self.cart_table.setItem(row_position, 2, QTableWidgetItem(str(order[2])))  # Цена
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке данных корзины: {e}")
            logging.error(f"Error loading cart {e}")

    def calculate_total(self):
        """Вычисляет и отображает общую сумму заказа"""
        total_price = 0
        for row in range(self.cart_table.rowCount()):
            item_name = self.cart_table.item(row, 0).text()
            item_qty = int(self.cart_table.item(row, 1).text())
            # Получение данных о цене из базы данных или тестовых данных
            try:
                self.cursor.execute("SELECT price FROM products WHERE name = %s", (item_name,))
                product_data = self.cursor.fetchone()
                if product_data:
                    product_price = float(product_data[0])
                    total_price += product_price * item_qty
                else:
                    QMessageBox.warning(self, "Ошибка", f"Не найдена цена товара: {item_name}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось получить данные о цене товара: {e}")
        self.total_value_label.setText(str(total_price))

    def load_cart_data_from_catalog(self, item_name):
        """Загружает данные о продукте в корзину из каталога"""
        row_position = self.cart_table.rowCount()
        self.cart_table.insertRow(row_position)  # Добавляем новую строку

        item_widget = QTableWidgetItem(item_name)
        item_widget.setFlags(item_widget.flags() & ~QtCore.Qt.ItemIsEditable)
        self.cart_table.setItem(row_position, 0, item_widget)

        qty_widget = QTableWidgetItem(str(1))  # 1 шт по умолчанию
        qty_widget.setFlags(qty_widget.flags() & ~QtCore.Qt.ItemIsEditable)
        self.cart_table.setItem(row_position, 1, qty_widget)

    def create_product_content(self):
        self.create_navigation_buttons()
        self.product_table = QTableWidget(self)
        self.product_table.setGeometry(210, 150, 770, 500)
        self.product_table.setColumnCount(6)  # 6 столбцов
        self.product_table.setHorizontalHeaderLabels(
            ["Наименование", "Характеристики", "Длительность лицензии", "Цена", "Количество", "Описание"])

        # Кнопки для работы с товарами
        self.add_product_button = QPushButton('Добавить товар', self)
        self.add_product_button.setGeometry(1000, 250, 180, 50)
        self.add_product_button.clicked.connect(self.add_product)

        self.edit_product_button = QPushButton('Редактировать товар', self)
        self.edit_product_button.setGeometry(1000, 350, 180, 50)
        self.edit_product_button.clicked.connect(self.edit_product)

        self.delete_product_button = QPushButton('Удалить товар', self)
        self.delete_product_button.setGeometry(1000, 450, 180, 50)
        self.delete_product_button.clicked.connect(self.delete_product)

        # Кнопка "Добавить в корзину"
        self.add_to_cart_button = QPushButton("Добавить в корзину", self)
        self.add_to_cart_button.setGeometry(1000, 550, 180, 50)
        self.add_to_cart_button.clicked.connect(self.add_to_cart)

        self.load_products()

    def add_to_cart(self):
        current_row = self.product_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите товар для добавления в корзину.")
            return

        product_name = self.product_table.item(current_row, 0).text()  # Получаем имя товара

        cart_window = self.windows[1]  # Получаем окно корзины
        cart_window.load_cart_data_from_catalog(product_name)  # Добавляем товар в корзину
        cart_window.calculate_total()  # Пересчитываем итог
        QMessageBox.information(self, "Успех", f"Товар '{product_name}' добавлен в корзину.")
        self.go_to_window(1)  # Переходим в корзину

    def create_sales_content(self):
        self.create_navigation_buttons()

        # Список продаж
        self.sales_list = QListWidget(self)
        self.sales_list.setGeometry(210, 150, 300, 500)
        self.sales_list.itemClicked.connect(self.on_sale_selected)

        # Заполнение списка тестовыми данными (пока что)
        sales = ["Продажа №1", "Продажа №2", "Продажа №3"]
        for sale in sales:
            self.sales_list.addItem(sale)

        # Информационная панель
        self.sale_info_label = QLabel("Информация о продаже:", self)
        self.sale_info_label.setGeometry(520, 150, 200, 30)

        self.sale_info_text = QTextEdit(self)
        self.sale_info_text.setGeometry(520, 190, 450, 460)
        self.sale_info_text.setReadOnly(True)

    def on_sale_selected(self, item):
        sale_name = item.text()
        sale_data = {
            "Продажа №1": "Состав:  Microsoft Office\n Дата:  2024-01-01\n Цена: 5000 рублей \n Сотрудник:  Петрова А.С.",
            "Продажа №2": "Состав: Adobe Photoshop\n Дата: 2024-01-02\n Цена: 3000 рублей \n Сотрудник: Иванов И.И.",
            "Продажа №3": "Состав: Windows 11 Pro\n Дата:  2024-01-04\n Цена: 10000 рублей \n Сотрудник: Сидоров П.А.",
        }
        self.sale_info_text.setText(sale_data.get(sale_name, "Информация о продаже не найдена."))

    def load_products(self):
        try:
            self.cursor.execute("SELECT * FROM products;")  # Извлечение всех данных из таблицы products
            products = self.cursor.fetchall()  # Получаем все строки

            self.product_table.setRowCount(0)  # Очищаем предыдущие данные

            for product in products:
                row_position = self.product_table.rowCount()
                self.product_table.insertRow(row_position)
                self.product_table.setItem(row_position, 0, QTableWidgetItem(product[1]))  # name
                self.product_table.setItem(row_position, 1, QTableWidgetItem(product[2]))  # composition
                self.product_table.setItem(row_position, 2, QTableWidgetItem(str(product[3])))  # price

                # Проверяем, является ли expiration объектом date или datetime
                if isinstance(product[4], (date, datetime)):
                    self.product_table.setItem(row_position, 3,
                                               QTableWidgetItem(product[4].strftime("%Y-%m-%d")))  # expiration
                else:
                    self.product_table.setItem(row_position, 3, QTableWidgetItem(
                        str(product[4])))  # если это не дата, просто преобразуем в строку
                self.product_table.setItem(row_position, 4, QTableWidgetItem(str(product[5])))  # quantity
                self.product_table.setItem(row_position, 5, QTableWidgetItem(product[6]))  # description
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить товары: {e}")
            logging.error(f"Error loading products: {e}")

    def add_product(self):
        dialog = ProductDialog()
        if dialog.exec_() == QDialog.Accepted:
            product_data = dialog.get_product_data()
            logging.debug(f"Data from ProductDialog: {product_data}")

            # Валидация данных
            if not product_data["name"] or not product_data["composition"] or not product_data["price"] or not \
            product_data["expiration"] or not product_data["quantity"] or not product_data["description"]:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
                logging.warning("Not all fields are filled.")
                return
            try:
                price = product_data["price"]
                quantity = int(product_data["quantity"])
                expiration_date = datetime.strptime(product_data["expiration"], "%Y-%m-%d").date()
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", f"Некорректные данные: {e}")
                logging.warning(f"Invalid input {e}")
                return
            try:
                row_position = self.product_table.rowCount()
                self.product_table.insertRow(row_position)
                self.product_table.setItem(row_position, 0, QTableWidgetItem(product_data["name"]))
                self.product_table.setItem(row_position, 1, QTableWidgetItem(product_data["composition"]))
                self.product_table.setItem(row_position, 2, QTableWidgetItem(str(price)))
                self.product_table.setItem(row_position, 3, QTableWidgetItem(expiration_date.strftime("%Y-%m-%d")))
                self.product_table.setItem(row_position, 4, QTableWidgetItem(str(quantity)))
                self.product_table.setItem(row_position, 5, QTableWidgetItem(product_data["description"]))

                self.cursor.execute("""
                              INSERT INTO products (name, composition, price, expiration, quantity, description)  
                                VALUES (%s, %s, %s, %s, %s, %s)  
                            """, (
                    product_data["name"],
                    product_data["composition"],
                    product_data["price"],
                    product_data["expiration"],
                    product_data["quantity"],
                    product_data["description"]
                ))

                self.connection.commit()
                QMessageBox.information(self, "Успех", "Товар успешно добавлен в базу данных.")
                logging.info("Product added successfully to DB.")
            except Exception as e:
                self.connection.rollback()
                QMessageBox.warning(self, "Ошибка", f"Не удалось добавить товар в базу данных: {e}")
                logging.error(f"Error adding product to database: {e}")

    def closeEvent(self, event):
        # Закрываем соединение при закрытии приложения
        self.cursor.close()
        self.connection.close()

    def edit_product(self):
        current_row = self.product_table.currentRow()
        if current_row < 0:  # Проверка, выбрана ли строка
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите товар для редактирования.")
            return
            # Получаем данные из выбранной строки
        product_data = {
            "name": self.product_table.item(current_row, 0).text(),
            "composition": self.product_table.item(current_row, 1).text(),
            "price": self.product_table.item(current_row, 2).text(),
            "expiration": self.product_table.item(current_row, 3).text(),
            "quantity": self.product_table.item(current_row, 4).text(),
            "description": self.product_table.item(current_row, 5).text(),
        }
        logging.debug(f"Editing Product {product_data}")
        dialog = ProductDialog(product_data)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_data = dialog.get_product_data()
            logging.debug(f"Updated Product {updated_data}")
            # Валидация данных
            if not updated_data["name"] or not updated_data["composition"] or not updated_data["price"] or not \
            updated_data["expiration"] or not updated_data["quantity"] or not updated_data["description"]:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
                logging.warning("Not all fields are filled.")
                return
            try:
                price = updated_data["price"]
                quantity = int(updated_data["quantity"])
                expiration_date = datetime.strptime(updated_data["expiration"], "%Y-%m-%d").date()
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", f"Некорректные данные: {e}")
                logging.warning(f"Invalid input {e}")
                return
            try:
                self.product_table.setItem(current_row, 0, QTableWidgetItem(updated_data["name"]))
                self.product_table.setItem(current_row, 1, QTableWidgetItem(updated_data["composition"]))
                self.product_table.setItem(current_row, 2, QTableWidgetItem(str(price)))
                self.product_table.setItem(current_row, 3, QTableWidgetItem(expiration_date.strftime("%Y-%m-%d")))
                self.product_table.setItem(current_row, 4, QTableWidgetItem(str(quantity)))
                self.product_table.setItem(current_row, 5, QTableWidgetItem(updated_data["description"]))

                # Обновление данных в базе данных
                self.cursor.execute("""  
                            UPDATE products SET name = %s, composition = %s, price = %s, expiration = %s, 
                            quantity = %s, description = %s  
                            WHERE id = %s  
                        """, (updated_data["name"],
                              updated_data["composition"],
                              updated_data["price"],
                              updated_data["expiration"],
                              updated_data["quantity"],
                              updated_data["description"],
                              self.product_table.item(current_row, 0).text()
                              ))  # Предполагая, что id - это первая колонка
                self.connection.commit()  # Сохраняем изменения
                QMessageBox.information(self, "Успех", "Товар успешно обновлён.")
                logging.info("Product updated successfully in DB.")
            except Exception as e:
                self.connection.rollback()  # Откатываем изменения в случае ошибки
                QMessageBox.warning(self, "Ошибка", f"Не удалось обновить товар в базе данных: {e}")
                logging.error(f"Error updating product in database: {e}")

    def delete_product(self):
        current_row = self.product_table.currentRow()
        if current_row < 0:  # Проверка, выбрана ли строка
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите товар для удаления.")
            return

        product_name = self.product_table.item(current_row, 0).text()
        logging.debug(f"Deleting product with name: {product_name}")
        reply = QMessageBox.question(self, 'Подтверждение удаления', f'Вы уверены, что хотите удалить {product_name}?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Удаление товара из базы данных
            try:
                self.cursor.execute("DELETE FROM products WHERE name = %s", (product_name,))
                self.connection.commit()  # Сохраняем изменения
                # Удаляем из таблицы
                self.product_table.removeRow(current_row)
                QMessageBox.information(self, "Успех", "Товар успешно удалён.")
                logging.info("Product deleted successfully from DB.")
            except Exception as e:
                self.connection.rollback()  # Откатываем изменения в случае ошибки
                QMessageBox.warning(self, "Ошибка", f"Не удалось удалить товар из базы данных: {e}")
                logging.error(f"Error deleting product from database: {e}")

    def create_staff_content(self):
        self.create_navigation_buttons()

        self.staff_table = QTableWidget(self)
        self.staff_table.setGeometry(210, 150, 770, 500)  # Задаем размер таблицы
        self.staff_table.setColumnCount(7)  # 6 столбцов
        self.staff_table.setHorizontalHeaderLabels(
            ["Фамилия", "Имя", "Отчество", "Дата Рождения", "Телефон", "Логин", "Пароль"])

        # Кнопки для работы с персоналом
        self.add_staff_button = QPushButton('Добавить сотрудника', self)
        self.add_staff_button.setGeometry(1000, 250, 180, 50)  # Задаем позицию
        self.add_staff_button.clicked.connect(self.add_staff)

        self.edit_staff_button = QPushButton('Редактировать сотрудника', self)
        self.edit_staff_button.setGeometry(1000, 350, 180, 50)  # Задаем позицию
        self.edit_staff_button.clicked.connect(self.edit_staff)

        self.delete_staff_button = QPushButton('Удалить сотрудника', self)
        self.delete_staff_button.setGeometry(1000, 450, 180, 50)  # Задаем позицию
        self.delete_staff_button.clicked.connect(self.delete_staff)

        self.load_staff()

    def load_staff(self):
        try:
            self.cursor.execute("SELECT * FROM staff;")  # Извлечение всех данных из таблицы staff
            staff = self.cursor.fetchall()  # Получаем все строки

            for staff in staff:
                row_position = self.staff_table.rowCount()
                self.staff_table.insertRow(row_position)  # Добавляем новую строку
                self.staff_table.setItem(row_position, 0, QTableWidgetItem(staff[1]))  # last_name
                self.staff_table.setItem(row_position, 1, QTableWidgetItem(staff[2]))  # first_name
                self.staff_table.setItem(row_position, 2, QTableWidgetItem(staff[3]))  # middle_name
                self.staff_table.setItem(row_position, 3,
                                              QTableWidgetItem(staff[4].strftime("%Y-%m-%d")))  # birth_date
                self.staff_table.setItem(row_position, 4, QTableWidgetItem(staff[5]))  # phone
                self.staff_table.setItem(row_position, 5, QTableWidgetItem(staff[6]))  # login
                self.staff_table.setItem(row_position, 6, QTableWidgetItem(staff[7]))  # password
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить персонал: {e}")

    def add_staff(self):
        dialog = StaffDialog()
        if dialog.exec_() == QDialog.Accepted:
            staff_data = dialog.get_staff_data()

            # Валидация номера телефона
            if not is_valid_phone(staff_data["phone"]):
                QMessageBox.warning(self, "Ошибка ввода", "Некорректный номер телефона. Формат: +7 (XXX) XXX XX XX")
                return

            row_position = self.staff_table.rowCount()
            self.staff_table.insertRow(row_position)  # Добавляем новую строку
            self.staff_table.setItem(row_position, 0, QTableWidgetItem(staff_data["last_name"]))
            self.staff_table.setItem(row_position, 1, QTableWidgetItem(staff_data["first_name"]))
            self.staff_table.setItem(row_position, 2, QTableWidgetItem(staff_data["middle_name"]))
            self.staff_table.setItem(row_position, 3, QTableWidgetItem(staff_data["birth_date"]))
            self.staff_table.setItem(row_position, 4, QTableWidgetItem(staff_data["phone"]))  # Номер телефона
            self.staff_table.setItem(row_position, 5, QTableWidgetItem(staff_data["login"]))
            self.staff_table.setItem(row_position, 6, QTableWidgetItem(staff_data["password"]))

            # Запись данных в базу данных
            try:
                self.cursor.execute("""  
                    INSERT INTO staff (last_name, first_name, middle_name, birth_date, phone, login, password)  
                    VALUES (%s, %s, %s, %s, %s, %s, %s)  
                """, (
                    staff_data["last_name"],
                    staff_data["first_name"],
                    staff_data["middle_name"],
                    staff_data["birth_date"],
                    staff_data["phone"],  # Сохраняем номер телефона
                    staff_data["login"],
                    staff_data["password"]
                ))
                self.connection.commit()  # Сохраняем изменения
                QMessageBox.information(self, "Успех", "Сотрудник успешно добавлен в базу данных.")
            except Exception as e:
                self.connection.rollback()  # Откатываем изменения в случае ошибки
                QMessageBox.warning(self, "Ошибка", f"Не удалось добавить сотрудник в базу данных: {e}")

    def edit_staff(self):
        current_row = self.staff_table.currentRow()
        if current_row < 0:  # Проверка, выбрана ли строка
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите сотрудника для редактирования.")
            return

            # Получаем данные из выбранной строки
        staff_data = {
            "last_name": self.staff_table.item(current_row, 0).text(),
            "first_name": self.staff_table.item(current_row, 1).text(),
            "middle_name": self.staff_table.item(current_row, 2).text(),
            "birth_date": self.staff_table.item(current_row, 3).text(),
            "phone": self.staff_table.item(current_row, 4).text(),  # Номер телефона
            "login": self.staff_table.item(current_row, 5).text(),
            "password": self.staff_table.item(current_row, 6).text(),
        }

        dialog = StaffDialog(staff_data)
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_staff_data()

            # Валидация номера телефона
            if not is_valid_phone(staff_data["phone"]):
                QMessageBox.warning(self, "Ошибка ввода", "Некорректный номер телефона. Формат: +7 (XXX) XXX XX XX")
                return

            self.staff_table.setItem(current_row, 0, QTableWidgetItem(updated_data["last_name"]))
            self.staff_table.setItem(current_row, 1, QTableWidgetItem(updated_data["first_name"]))
            self.staff_table.setItem(current_row, 2, QTableWidgetItem(updated_data["middle_name"]))
            self.staff_table.setItem(current_row, 3, QTableWidgetItem(updated_data["birth_date"]))
            self.staff_table.setItem(current_row, 4, QTableWidgetItem(updated_data["phone"]))  # Обновляем номер телефона
            self.staff_table.setItem(current_row, 5, QTableWidgetItem(updated_data["login"]))
            self.staff_table.setItem(current_row, 6, QTableWidgetItem(updated_data["password"]))

            # Обновление данных в базе данных
            try:
                self.cursor.execute("""  
                    UPDATE staff SET last_name = %s, first_name = %s, middle_name = %s,   
                    birth_date = %s, phone = %s, login = %s, password = %s   
                    WHERE id = %s  
                """, (
                    updated_data["last_name"],
                    updated_data["first_name"],
                    updated_data["middle_name"],
                    updated_data["birth_date"],
                    updated_data["phone"],  # Обновляем номер телефона
                    updated_data["login"],
                    updated_data["password"],
                    self.staff_table.item(current_row, 0).text()  # Предполагаем, что id - это первая колонка
                ))
                self.connection.commit()  # Сохраняем изменения
                QMessageBox.information(self, "Успех", "Сотрудник успешно обновлён.")
            except Exception as e:
                self.connection.rollback()  # Откатываем изменения в случае ошибки
                QMessageBox.warning(self, "Ошибка", f"Не удалось обновить сотрудника в базе данных: {e}")

    def delete_staff(self):
        current_row = self.staff_table.currentRow()
        if current_row < 0:  # Проверка, выбрана ли строка
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите сотрудника для удаления.")
            return

        login = self.staff_table.item(current_row, 5).text()  # Предполагаем, что логин находится в 7-й колонке
        password = self.staff_table.item(current_row, 6).text()  # Предполагаем, что пароль находится в 8-й колонке
        staff_name = f"{self.pstaff_table.item(current_row, 0).text()} {self.staff_table.item(current_row, 1).text()}"

        reply = QMessageBox.question(self, 'Подтверждение удаления',
                                     f'Вы уверены, что хотите удалить сотрудника {staff_name}?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Удаление сотрудника из базы данных
            try:
                self.cursor.execute("DELETE FROM staff WHERE login = %s AND password = %s", (login, password))
                self.connection.commit()  # Сохраняем изменения

                # Удаляем сотрудника из таблицы
                self.staff_table.removeRow(current_row)
                QMessageBox.information(self, "Успех", "Сотрудник успешно удалён.")
            except Exception as e:
                self.connection.rollback()  # Откатываем изменения в случае ошибки
                QMessageBox.warning(self, "Ошибка", f"Не удалось удалить сотрудника из базы данных: {e}")

    def on_order_button_click(self):
        # Получение выбранных товаров и перенос в корзину
        selected_items = self.product_catalog.selectedItems()
        if selected_items:
            cart_window = self.windows[1]
            cart_window.cart_table.setRowCount(0) # Очищаем корзину
            for item in selected_items:
                cart_window.load_cart_data_from_catalog(item.text())
            cart_window.calculate_total() # Пересчитываем итог
        self.go_to_window(1)  # Переход к окну корзины

    def go_to_window(self, idx):
        self.hide()  # Скрываем текущее окно
        self.windows[idx].show()  # Показываем следующее окно

    def set_other_windows(self, windows):
        self.windows = windows  # Сохраняем ссылки на другие окна


if __name__ == '__main__':
    app = QApplication(sys.argv)
    total_windows = 6
    windows = [Window(i, total_windows) for i in range(total_windows)]

        # Устанавливаем ссылки на другие окна
    for w in windows:
        w.set_other_windows(windows)

    windows[0].show()  # Показываем первое окно
    sys.exit(app.exec_())