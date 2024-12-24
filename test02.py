import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime


def create_gui():
    """Создает и отображает основное окно приложения."""

    root = tk.Tk()
    root.title("База данных")

    # ----- Верхняя панель (название, имя пользователя, выход) -----
    top_frame = tk.Frame(root)
    top_frame.pack(side="top", fill="x", padx=5, pady=5)

    app_name = tk.Label(top_frame, text="База данных", font=("Arial", 12, "bold"))
    app_name.pack(side="left")

    user_name = tk.Label(top_frame, text="Администратор")
    user_name.pack(side="right", padx=10)

    exit_button = tk.Button(top_frame, text="Выйти", command=root.destroy)
    exit_button.pack(side="right")

    # ----- Левая панель (кнопки меню) -----
    left_frame = tk.Frame(root)
    left_frame.pack(side="left", fill="y", padx=5, pady=5)

    # Словарь для отслеживания, какая вкладка активна
    active_frame = {"value": None}

    # Глобальные переменные
    product_items = [tk.StringVar(value="Товар №1"),
                     tk.StringVar(value="Товар №2"),
                     tk.StringVar(value="Товар №3")]
    product_quantities = [tk.IntVar(value=1) for _ in product_items]
    product_info = {}

    sales_items = [tk.StringVar(value="Продажа №1"),
                   tk.StringVar(value="Продажа №2"),
                   tk.StringVar(value="Продажа №3")]

    staff_items = [tk.StringVar(value="Администратор 1"),
                   tk.StringVar(value="Администратор 2"),
                   tk.StringVar(value="Администратор 3")]
    staff_info = {}

    def show_frame(frame):
        """Переключает отображаемую вкладку"""
        if active_frame["value"] is not None:
            active_frame["value"].pack_forget()
        frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        active_frame["value"] = frame

    def create_main_frame():
        main_frame = tk.Frame(root)

        search_entry = tk.Entry(main_frame)
        search_entry.pack(side="top", fill="x", pady=5)

        # Создаем Frame для списка товаров, чтобы можно было использовать полосу прокрутки
        list_frame = tk.Frame(main_frame)
        list_frame.pack(side="top", fill="both", expand=True)

        # Добавляем Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        # Используем Checkbuttons для отображения товаров
        product_listbox = tk.Canvas(list_frame, yscrollcommand=scrollbar.set)
        product_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=product_listbox.yview)

        # Создаем фрейм для элементов внутри Canvas и добавляем его в canvas
        products_frame = tk.Frame(product_listbox)
        product_listbox.create_window((0, 0), window=products_frame, anchor="nw")

        for item_var in product_items:
            check_var = tk.BooleanVar()
            check_button = tk.Checkbutton(products_frame, textvariable=item_var, variable=check_var)
            check_button.pack(anchor='w', padx=5)

        # Настраиваем автоматическое изменение области прокрутки
        def update_scroll_region(event):
            product_listbox.config(scrollregion=product_listbox.bbox("all"))

        products_frame.bind("<Configure>", update_scroll_region)

        create_order_button = tk.Button(main_frame, text="Создать заказ", width=15)
        create_order_button.pack(side="bottom", pady=10, anchor='e')
        return main_frame

    def create_cart_frame():
        """Создает и возвращает фрейм для корзины."""
        cart_frame = tk.Frame(root)
        items_frame = tk.Frame(cart_frame)
        items_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        quantity_labels = []

        for i, item_var in enumerate(product_items):
            item_frame = tk.Frame(items_frame)
            item_frame.pack(side="top", fill="x", pady=2)

            # Кнопка удаления товара
            delete_button = tk.Button(item_frame, text="Удалить", width=8, command=lambda idx=i: delete_product(idx))
            delete_button.pack(side="left")

            tk.Label(item_frame, textvariable=item_var).pack(side="left", padx=5)

            tk.Button(item_frame, text="-", width=2,
                      command=lambda idx=i: update_quantity(idx, -1, quantity_labels)).pack(
                side="left", padx=2)
            quantity_label = tk.Label(item_frame, text=f"{product_quantities[i].get()} шт")
            quantity_label.pack(side="left", padx=2)
            quantity_labels.append(quantity_label)

            tk.Button(item_frame, text="+", width=2,
                      command=lambda idx=i: update_quantity(idx, 1, quantity_labels)).pack(
                side="left", padx=2)

        # Фрейм для даты, суммы заказа и итога
        right_frame = tk.Frame(cart_frame)
        right_frame.pack(side="right", fill="y", padx=5, pady=5)

        date_entry = tk.Entry(right_frame)
        date_entry.pack(side="top", pady=5, fill='x')
        tk.Button(right_frame, text="Сумма заказов").pack(
            side="top", pady=5, fill='x'
        )
        tk.Button(right_frame, text="Итог").pack(side="top", pady=5, fill='x')

        return cart_frame

    def update_quantity(index, change, quantity_labels):
        product_quantities[index].set(max(1, product_quantities[index].get() + change))
        quantity_labels[index].config(text=f"{product_quantities[index].get()} шт")

    def delete_product(index):
        product_items[index].set("")  # Очистка названия
        product_quantities[index].set(1)  # Сброс кол-ва

    def create_sales_frame():
        sales_frame = tk.Frame(root)

        # Создаем Frame для списка продаж, чтобы можно было использовать полосу прокрутки
        list_frame = tk.Frame(sales_frame)
        list_frame.pack(side="top", fill="both", expand=True)

        # Добавляем Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        # Используем Checkbuttons для отображения продаж
        sales_listbox = tk.Canvas(list_frame, yscrollcommand=scrollbar.set)
        sales_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=sales_listbox.yview)

        # Создаем фрейм для элементов внутри Canvas и добавляем его в canvas
        sales_list_frame = tk.Frame(sales_listbox)
        sales_listbox.create_window((0, 0), window=sales_list_frame, anchor="nw")

        for item_var in sales_items:
            check_var = tk.BooleanVar()
            check_button = tk.Checkbutton(sales_list_frame, textvariable=item_var, variable=check_var)
            check_button.pack(anchor='w', padx=5)

        # Настраиваем автоматическое изменение области прокрутки
        def update_scroll_region(event):
            sales_listbox.config(scrollregion=sales_listbox.bbox("all"))

        sales_list_frame.bind("<Configure>", update_scroll_region)

        info_frame = tk.Frame(sales_frame, width=300, height=150, bg='lightgray')
        info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        info_label = tk.Label(info_frame, text="Информация о продаже", anchor='nw', justify="left")
        info_label.pack(fill="both", expand=True)

        return sales_frame

    def create_staff_frame():
        staff_frame = tk.Frame(root)

        # Создаем Frame для списка персонала, чтобы можно было использовать полосу прокрутки
        list_frame = tk.Frame(staff_frame)
        list_frame.pack(side="top", fill="both", expand=True)

        # Добавляем Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        # Используем Checkbuttons для отображения персонала
        staff_listbox = tk.Canvas(list_frame, yscrollcommand=scrollbar.set)
        staff_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=staff_listbox.yview)

        # Создаем фрейм для элементов внутри Canvas и добавляем его в canvas
        staff_list_frame = tk.Frame(staff_listbox)
        staff_listbox.create_window((0, 0), window=staff_list_frame, anchor="nw")

        for i, item_var in enumerate(staff_items):
            check_var = tk.BooleanVar()
            staff_entry = tk.Checkbutton(staff_list_frame, textvariable=item_var, variable=check_var,
                                         command=lambda idx=i: set_selected_staff(idx))
            staff_entry.pack(anchor="w", padx=5)

        # Настраиваем автоматическое изменение области прокрутки
        def update_scroll_region(event):
            staff_listbox.config(scrollregion=staff_listbox.bbox("all"))

        staff_list_frame.bind("<Configure>", update_scroll_region)

        info_frame = tk.Frame(staff_frame, width=200, height=100, bg='lightgray')
        info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        info_label = tk.Label(info_frame, text='Подробная информация о персонале', anchor='nw', justify="left")
        info_label.pack(fill="both", expand=True)

        buttons_frame = tk.Frame(staff_frame)
        buttons_frame.pack(side="right", fill="y", padx=5, pady=5)

        def open_add_staff_window():
            open_edit_staff_info_window(info_label)

        def open_edit_staff_window():
            if selected_staff["value"] is not None:
                open_edit_staff_info_window(info_label, selected_staff["value"])
            else:
                messagebox.showinfo("Ошибка", "Выберите сотрудника")

        def delete_selected_staff():
            if selected_staff["value"] is not None:
                delete_staff_from_all_forms(selected_staff["value"], info_label)
            else:
                messagebox.showinfo("Ошибка", "Выберите сотрудника для удаления")

        tk.Button(buttons_frame, text="Добавить персонал", command=open_add_staff_window).pack(side="top", pady=5,
                                                                                               fill='x')
        tk.Button(buttons_frame, text="Редактировать информацию о персонале", command=open_edit_staff_window).pack(
            side="top", pady=5, fill='x')
        tk.Button(buttons_frame, text="Удалить", command=delete_selected_staff).pack(side="top", pady=5, fill='x')

        # Запись выбранного товара
        selected_staff = {"value": None}

        def set_selected_staff(index):
            selected_staff["value"] = index
            if staff_info.get(index):
                info_label.config(text=staff_info[index])
            else:
                info_label.config(text="")

        return staff_frame

    def create_products_frame():
        products_frame = tk.Frame(root)

        # Создаем Frame для списка товаров, чтобы можно было использовать полосу прокрутки
        list_frame = tk.Frame(products_frame)
        list_frame.pack(side="top", fill="both", expand=True)

        # Добавляем Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        # Используем Checkbuttons для отображения товаров
        product_listbox = tk.Canvas(list_frame, yscrollcommand=scrollbar.set)
        product_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=product_listbox.yview)

        # Создаем фрейм для элементов внутри Canvas и добавляем его в canvas
        products_list_frame = tk.Frame(product_listbox)
        product_listbox.create_window((0, 0), window=products_list_frame, anchor="nw")

        for i, item_var in enumerate(product_items):
            check_var = tk.BooleanVar()
            check_button = tk.Checkbutton(products_list_frame, textvariable=item_var, variable=check_var,
                                          command=lambda idx=i: set_selected_product(idx))
            check_button.pack(anchor='w', padx=5)

        # Настраиваем автоматическое изменение области прокрутки
        def update_scroll_region(event):
            product_listbox.config(scrollregion=product_listbox.bbox("all"))

        products_list_frame.bind("<Configure>", update_scroll_region)

        info_frame = tk.Frame(products_frame, width=200, height=100, bg='lightgray')
        info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        info_label = tk.Label(info_frame, text='Информация о товаре', anchor='nw', justify="left")
        info_label.pack(fill="both", expand=True)

        buttons_frame = tk.Frame(products_frame)
        buttons_frame.pack(side="right", fill="y", padx=5, pady=5)

        def open_edit_window():
            if selected_product["value"] is not None:
                open_edit_product_info_window(selected_product["value"], info_label)
            else:
                messagebox.showinfo("Ошибка", "Выберите товар")

        def open_add_window():
            open_add_product_info_window(info_label)

        def delete_selected_product():
            if selected_product["value"] is not None:
                delete_product_from_all_forms(selected_product["value"], info_label)
            else:
                messagebox.showinfo("Ошибка", "Выберите товар для удаления")

        tk.Button(buttons_frame, text="Добавить товар", command=open_add_window).pack(side="top", pady=5, fill='x')
        tk.Button(buttons_frame, text="Редактировать информацию товара", command=open_edit_window).pack(side="top",
                                                                                                        pady=5,
                                                                                                        fill='x')
        tk.Button(buttons_frame, text="Удалить товар", command=delete_selected_product).pack(side="top", pady=5,
                                                                                             fill='x')

        # Запись выбранного товара
        selected_product = {"value": None}

        def set_selected_product(index):
            selected_product["value"] = index
            if product_info.get(index):
                info_label.config(text=product_info[index])
            else:
                info_label.config(text="")

        return products_frame

    def create_reports_frame():
        reports_frame = tk.Frame(root)

        # Create a label to display the report
        report_label = tk.Label(reports_frame, text="Отчет", font=("Arial", 12), justify='left')
        report_label.pack(side='left', fill="both", expand=True, padx=5, pady=5)

        # Create a frame for the list of reports
        list_frame = tk.Frame(reports_frame)
        list_frame.pack(side="right", fill="y", padx=5, pady=5)

        # Create buttons for each report type
        report_types = [
            "Отчет о прибыли",
            "Отчет о продажах",
            "Отчет о количестве клиентов",
            "Отчет о возвратах"
        ]

        def generate_report(report_type):
            report_text = f"Сгенерирован отчёт: {report_type}\n"  # здесь будет логика генерации отчёта
            report_label.config(text=report_text)

        for report_type in report_types:
            tk.Button(list_frame, text=report_type, width=25, anchor='w',
                      command=lambda type=report_type: generate_report(type)).pack(side="top", fill="x", pady=2)

        send_report_button = tk.Button(list_frame, text="Отправить отчет", width=25)
        send_report_button.pack(side="bottom", pady=10)
        return reports_frame

    def open_edit_product_info_window(product_index, info_label):
        """Открывает окно редактирования информации о товаре."""
        edit_window = tk.Toplevel(root)
        edit_window.title("Редактировать информацию о товаре")

        tk.Label(edit_window, text="Наименование").pack(anchor="w", padx=10, pady=2)
        name_entry = tk.Entry(edit_window)
        name_entry.pack(fill="x", padx=10, pady=2)
        name_entry.insert(0, product_items[product_index].get())

        tk.Label(edit_window, text="Характеристики").pack(anchor="w", padx=10, pady=2)
        characteristics_entry = tk.Entry(edit_window)
        characteristics_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(edit_window, text="Длительность лицензии").pack(anchor="w", padx=10, pady=2)
        license_duration_entry = tk.Entry(edit_window)
        license_duration_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(edit_window, text="Цена").pack(anchor="w", padx=10, pady=2)
        price_entry = tk.Entry(edit_window)
        price_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(edit_window, text="Описание").pack(anchor="w", padx=10, pady=2)
        description_entry = tk.Entry(edit_window)
        description_entry.pack(fill="x", padx=10, pady=2)

        # Загружаем начальную информацию, если есть
        if product_info.get(product_index):
            info_str = product_info[product_index].split("\n")
            if len(info_str) > 0:
                characteristics_entry.insert(0, info_str[0].split(": ")[1])
            if len(info_str) > 1:
                license_duration_entry.insert(0, info_str[1].split(": ")[1])
            if len(info_str) > 2:
                price_entry.insert(0, info_str[2].split(": ")[1])
            if len(info_str) > 3:
                description_entry.insert(0, info_str[3].split(": ")[1])

        def save_info():
            """Сохраняет информацию о товаре и обновляет лейбл"""
            info = f"Характеристики: {characteristics_entry.get()}\n" \
                   f"Длительность лицензии: {license_duration_entry.get()}\n" \
                   f"Цена: {price_entry.get()}\n" \
                   f"Описание: {description_entry.get()}"

            # Обновляем название товара
            product_items[product_index].set(name_entry.get())

            product_info[product_index] = info
            info_label.config(text=info)
            edit_window.destroy()

        def cancel_edit():
            """Закрывает окно без сохранения"""
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Сохранить", command=save_info)
        save_button.pack(side="left", padx=10, pady=10)

        cancel_button = tk.Button(edit_window, text="Отмена", command=cancel_edit)
        cancel_button.pack(side="right", padx=10, pady=10)

        return edit_window

    def open_add_product_info_window(info_label):
        """Открывает окно добавления информации о товаре."""
        add_window = tk.Toplevel(root)
        add_window.title("Добавить информацию о товаре")

        tk.Label(add_window, text="Наименование").pack(anchor="w", padx=10, pady=2)
        name_entry = tk.Entry(add_window)
        name_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(add_window, text="Характеристики").pack(anchor="w", padx=10, pady=2)
        characteristics_entry = tk.Entry(add_window)
        characteristics_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(add_window, text="Длительность лицензии").pack(anchor="w", padx=10, pady=2)
        license_duration_entry = tk.Entry(add_window)
        license_duration_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(add_window, text="Цена").pack(anchor="w", padx=10, pady=2)
        price_entry = tk.Entry(add_window)
        price_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(add_window, text="Описание").pack(anchor="w", padx=10, pady=2)
        description_entry = tk.Entry(add_window)
        description_entry.pack(fill="x", padx=10, pady=2)

        def save_info():
            """Сохраняет информацию о товаре и обновляет лейбл"""
            new_item_name = name_entry.get()
            if not new_item_name:
                messagebox.showinfo("Ошибка", "Введите наименование товара")
                return

            info = f"Характеристики: {characteristics_entry.get()}\n" \
                   f"Длительность лицензии: {license_duration_entry.get()}\n" \
                   f"Цена: {price_entry.get()}\n" \
                   f"Описание: {description_entry.get()}"

            new_product_var = tk.StringVar(value=new_item_name)
            product_items.append(new_product_var)
            product_quantities.append(tk.IntVar(value=1))
            product_info[len(product_items) - 1] = info

            info_label.config(text=info)
            add_window.destroy()
            show_frame(create_products_frame())

        def cancel_edit():
            """Закрывает окно без сохранения"""
            add_window.destroy()

        save_button = tk.Button(add_window, text="Сохранить", command=save_info)
        save_button.pack(side="left", padx=10, pady=10)

        cancel_button = tk.Button(add_window, text="Отмена", command=cancel_edit)
        cancel_button.pack(side="right", padx=10, pady=10)

    def delete_product_from_all_forms(product_index, info_label):
        """Удаляет товар из всех форм"""
        if product_index is not None:
            del product_items[product_index]
            del product_quantities[product_index]

            new_product_info = {}
            for index, info in product_info.items():
                if index < product_index:
                    new_product_info[index] = info
                elif index > product_index:
                    new_product_info[index - 1] = info

            product_info.clear()
            product_info.update(new_product_info)
            info_label.config(text="")
            show_frame(create_products_frame())

    def delete_staff_from_all_forms(staff_index, info_label):
        """Удаляет сотрудника из всех форм"""
        if staff_index is not None:
            del staff_items[staff_index]

            new_staff_info = {}
            for index, info in staff_info.items():
                if index < staff_index:
                    new_staff_info[index] = info
                elif index > staff_index:
                    new_staff_info[index - 1] = info

            staff_info.clear()
            staff_info.update(new_staff_info)
            info_label.config(text="")
            show_frame(create_staff_frame())

    def open_edit_staff_info_window(info_label, staff_index=None):
        """Открывает окно редактирования информации о персонале."""
        edit_window = tk.Toplevel(root)
        edit_window.title("Информация о персонале")

        tk.Label(edit_window, text="Фамилия").pack(anchor="w", padx=10, pady=2)
        last_name_entry = tk.Entry(edit_window)
        last_name_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(edit_window, text="Имя").pack(anchor="w", padx=10, pady=2)
        first_name_entry = tk.Entry(edit_window)
        first_name_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(edit_window, text="Отчество").pack(anchor="w", padx=10, pady=2)
        middle_name_entry = tk.Entry(edit_window)
        middle_name_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(edit_window, text="Дата рождения").pack(anchor="w", padx=10, pady=2)
        birthdate_entry = tk.Entry(edit_window)
        birthdate_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(edit_window, text="Телефон").pack(anchor="w", padx=10, pady=2)
        phone_entry = tk.Entry(edit_window)
        phone_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(edit_window, text="Логин").pack(anchor="w", padx=10, pady=2)
        login_entry = tk.Entry(edit_window)
        login_entry.pack(side="left", fill="x", padx=10, pady=2, expand=True)

        tk.Label(edit_window, text="Пароль").pack(anchor="w", padx=10, pady=2)
        password_entry = tk.Entry(edit_window, show="*")
        password_entry.pack(side="left", fill="x", padx=10, pady=2, expand=True)

        if staff_index is not None:
            if staff_info.get(staff_index):
                info_str = staff_info[staff_index].split("\n")
                if len(info_str) > 0:
                    last_name_entry.insert(0, info_str[0].split(": ")[1])
                if len(info_str) > 1:
                    first_name_entry.insert(0, info_str[1].split(": ")[1])
                if len(info_str) > 2:
                    middle_name_entry.insert(0, info_str[2].split(": ")[1])
                if len(info_str) > 3:
                    birthdate_entry.insert(0, info_str[3].split(": ")[1])
                if len(info_str) > 4:
                    phone_entry.insert(0, info_str[4].split(": ")[1])
                if len(info_str) > 5:
                    login_entry.insert(0, info_str[5].split(": ")[1])
                if len(info_str) > 6:
                    password_entry.insert(0, info_str[6].split(": ")[1])

        def save_info():
            """Сохраняет информацию о персонале и обновляет лейбл"""
            info = f"Фамилия: {last_name_entry.get()}\n" \
                   f"Имя: {first_name_entry.get()}\n" \
                   f"Отчество: {middle_name_entry.get()}\n" \
                   f"Дата рождения: {birthdate_entry.get()}\n" \
                   f"Телефон: {phone_entry.get()}\n" \
                   f"Логин: {login_entry.get()}\n" \
                   f"Пароль: {password_entry.get()}"

            if staff_index is None:
                new_staff_name = f"{first_name_entry.get()} {last_name_entry.get()}"
                new_staff_var = tk.StringVar(value=new_staff_name)
                staff_items.append(new_staff_var)
                staff_info[len(staff_items) - 1] = info
                info_label.config(text=info)
                show_frame(create_staff_frame())
            else:
                staff_info[staff_index] = info
                info_label.config(text=info)
                staff_items[staff_index].set(f"{first_name_entry.get()} {last_name_entry.get()}")

            edit_window.destroy()

        def cancel_edit():
            """Закрывает окно без сохранения"""
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Сохранить", command=save_info)
        save_button.pack(side="left", padx=10, pady=10)

        cancel_button = tk.Button(edit_window, text="Отмена", command=cancel_edit)
        cancel_button.pack(side="right", padx=10, pady=10)
        return edit_window

    menu_buttons = [
        ("Каталог", create_main_frame),
        ("Корзина", create_cart_frame),
        ("Продажи", create_sales_frame),
        ("Товары", create_products_frame),
        ("Персонал", create_staff_frame),
        ("Отчеты", create_reports_frame),
    ]

    for text, frame_func in menu_buttons:
        button = tk.Button(
            left_frame,
            text=text,
            width=10,
            anchor="w",
            command=lambda func=frame_func: show_frame(func()) if func else None
        )
        button.pack(side="top", fill="x", pady=2)

    show_frame(create_main_frame())
    root.mainloop()


if __name__ == "__main__":
    create_gui()