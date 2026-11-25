import json
import os


try:
    with open('menu.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print('Файл menu.json не найден!')
    data = {}

# 2. Цены
prices_file = 'prices.json'
if os.path.exists(prices_file):
    with open(prices_file, 'r', encoding='utf-8') as file:
        prices = json.load(file)
else:
    prices = {key.strip(): 500 for key in data.keys()}
    with open(prices_file, 'w', encoding='utf-8') as file:
        json.dump(prices, file, ensure_ascii=False, indent=2)

ingredients_file = 'ingredients.json'
if os.path.exists(ingredients_file):
    with open(ingredients_file, 'r', encoding='utf-8') as file:
        ingredients = json.load(file)
else:
    ingredients = {
        "Тесто ": 100,
        "Соус томатный ": 80,
        "Сыр моцарелла ": 150,
        "Колбаса ": 60,
        "Ветчина ": 50,
        "Бекон ": 40,
        "Грибы ": 70,
        "Перец болгарский ": 45,
        "Лук ": 55,
        "Оливки ": 30,
        "Ананасы ": 25
    }
    with open(ingredients_file, 'w', encoding='utf-8') as file:
        json.dump(ingredients, file, ensure_ascii=False, indent=2)


recipes_file = 'recipes.json'
if os.path.exists(recipes_file):
    with open(recipes_file, 'r', encoding='utf-8') as file:
        recipes = json.load(file)
else:
    recipes = {
        "Мясная ": {"Тесто ": 1, "Соус томатный ": 2, "Сыр моцарелла ": 3, "Колбаса ": 4, "Ветчина ": 2, "Бекон ": 2},
        "Пеппе ронни макарони ": {"Тесто ": 1, "Соус томатный ": 2, "Сыр моцарелла ": 3, "Колбаса ": 5},
        "Сырная ": {"Тесто ": 1, "Соус томатный ": 1, "Сыр моцарелла ": 6},
        "Гавайская ": {"Тесто ": 1, "Соус томатный ": 2, "Сыр моцарелла ": 3, "Ветчина ": 3, "Ананасы ": 3},
        "Маргарита ": {"Тесто ": 1, "Соус томатный ": 2, "Сыр моцарелла ": 4},
        "Карбонара ": {"Тесто ": 1, "Соус томатный ": 1, "Сыр моцарелла ": 3, "Бекон ": 4, "Лук ": 1},
        "Эль Патрицца ": {"Тесто ": 1, "Соус томатный ": 2, "Сыр моцарелла ": 3, "Колбаса ": 2, "Ветчина ": 2,
                          "Бекон ": 2,
                          "Перец болгарский ": 2, "Лук ": 1, "Оливки ": 2},
        "Голдицца ": {"Тесто ": 1, "Соус томатный ": 2, "Сыр моцарелла ": 5},
        "Еденицца ": {"Тесто ": 1, "Соус томатный ": 2, "Сыр моцарелла ": 3, "Грибы ": 3, "Перец болгарский ": 2},
        "пицца 67 ": {"Тесто ": 1, "Соус томатный ": 2, "Сыр моцарелла ": 3}
    }
    with open(recipes_file, 'w', encoding='utf-8') as file:
        json.dump(recipes, file, ensure_ascii=False, indent=2)

history_file = 'history.json'
history = []
if os.path.exists(history_file):
    try:
        with open(history_file, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if content:
                history = json.load(file)
            else:
                history = []
    except json.JSONDecodeError:
        print('️ Файл истории повреждён, создаём новый...')
        history = []
else:
    with open(history_file, 'w', encoding='utf-8') as file:
        json.dump([], file, ensure_ascii=False, indent=2)



def save_menu():
    with open('menu.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=1)


def save_prices():
    with open(prices_file, 'w', encoding='utf-8') as file:
        json.dump(prices, file, ensure_ascii=False, indent=2)


def save_ingredients():
    with open(ingredients_file, 'w', encoding='utf-8') as file:
        json.dump(ingredients, file, ensure_ascii=False, indent=2)


def save_recipes():
    with open(recipes_file, 'w', encoding='utf-8') as file:
        json.dump(recipes, file, ensure_ascii=False, indent=2)


def save_history():
    with open(history_file, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=2)
    print(f' История сохранена. Всего заказов: {len(history)}')


def check_recipe(pizza_name, qty):

    recipe = recipes.get(pizza_name, {})
    missing = {}
    for ing, needed_per_pizza in recipe.items():
        needed = needed_per_pizza * qty
        have = ingredients.get(ing, 0)
        if have < needed:
            missing[ing] = {'needed': needed, 'have': have}
    return missing


def deduct_ingredients(pizza_name, qty):
    recipe = recipes.get(pizza_name, {})
    for ing, needed_per_pizza in recipe.items():
        ingredients[ing] -= needed_per_pizza * qty


while True:
    print('\n' + '=' * 30)
    print(f'📊 В истории {len(history)} заказов')
    choice = input('Выберите действие:\n'
                   '1 - Добавить заказ\n'
                   '2 - История заказов\n'
                   '3 - Пополнить склад ингредиентов\n'
                   '4 - Добавить позицию в меню\n'
                   '5 - Посмотреть остатки на складе\n'
                   '6 - Удалить пиццу из меню\n'
                   '7 - Завершить работу\n'
                   'Ваш выбор: ')


    if choice == '1':
        try:
            people = int(input('Введите количество людей: '))
        except ValueError:
            print('Ошибка: нужно ввести число!')
            continue
        human = input('Введите имя оплачивающего (ФИО): ')
        print('\n0 - Закончить выбор')
        order_items = []
        total_sum = 0
        while True:
            print('\n--- Меню ---')
            menu_keys = list(data.keys())
            for i, key in enumerate(menu_keys, 1):
                name = key.strip()
                price = prices.get(name, 0)
                print(f"{i} - {name} | Цена: {price} руб.")
            ch1 = input("Выберите номер пиццы (или 0 для завершения): ")
            if ch1 == '0':
                break
            try:
                pizza_idx = int(ch1) - 1
                if 0 <= pizza_idx < len(menu_keys):
                    pizza_name = menu_keys[pizza_idx].strip()
                    qty = int(input(f"Сколько '{pizza_name}' добавить? "))

                    missing = check_recipe(pizza_name, qty)
                    if missing:
                        print(f'\n⚠️ НЕ ХВАТАЕТ ингредиентов для {qty} шт. "{pizza_name}":')
                        for ing, info in missing.items():
                            print(f"   {ing}: нужно {info['needed']}, есть {info['have']}")
                        confirm = input('Продолжить всё равно? (да/нет): ').strip().lower()
                        if confirm != 'да':
                            continue

                    recipe = recipes.get(pizza_name, {})
                    print(f'\n Со склада будет списано:')
                    for ing, per_pizza in recipe.items():
                        print(f"  - {ing}: {per_pizza * qty} шт.")

                    deduct_ingredients(pizza_name, qty)
                    order_items.append({
                        'name': pizza_name,
                        'qty': qty,
                        'price': prices.get(pizza_name, 0)
                    })
                    total_sum += prices.get(pizza_name, 0) * qty
                    print(f'\n Добавлено. Сумма позиции: {prices.get(pizza_name, 0) * qty} руб.')
                else:
                    print("Пиццы с таким номером нет в меню.")
            except ValueError:
                print("Ошибка: введите корректное число!")

        if order_items:
            new_order = {
                'payer': human,
                'people': people,
                'items': order_items,
                'total': total_sum
            }
            history.append(new_order)
            save_history()
            save_ingredients()
            print(f'\n Заказ сохранён! Итого к оплате: {total_sum} руб.')
        else:
            print('\n Заказ пустой, сохранение отменено.')

    elif choice == '2':
        print('\n--- История заказов ---')
        print(f' Загружено: {len(history)} заказов')
        if not history:
            print('История заказов пуста.')
        else:
            grand_total = 0
            for i, order in enumerate(history, 1):
                print(f"\nЗаказ №{i} | Оплачивает: {order['payer']} | Персон: {order['people']}")
                for item in order['items']:
                    print(
                        f"  - {item['name']}: {item['qty']} шт. × {item['price']} руб. = {item['qty'] * item['price']} руб.")
                print(f"  💰 ИТОГО ПО ЗАКАЗУ: {order['total']} руб.")
                grand_total += order['total']
            print(f"\n ОБЩАЯ ВЫРУЧКА: {grand_total} руб.")
        input('\n Нажмите Enter, чтобы вернуться в меню')

    elif choice == '3':
        print('\n--- Пополнение склада ингредиентов ---')
        ing_list = list(ingredients.keys())
        for i, ing in enumerate(ing_list, 1):
            print(f"{i} - {ing} (остаток: {ingredients[ing]})")
        try:
            idx = int(input('\nНомер ингредиента для пополнения: ')) - 1
            if 0 <= idx < len(ing_list):
                ing_name = ing_list[idx]
                add_qty = int(input(f'Сколько добавить ингредиента "{ing_name}"? '))
                ingredients[ing_name] += add_qty
                save_ingredients()
                print(f'\n Остаток "{ing_name}" обновлён: {ingredients[ing_name]} шт.')
            else:
                print('Ошибка: нет такого ингредиента.')
        except ValueError:
            print('Ошибка: нужно ввести число')

    # === 4. ДОБАВИТЬ ПИЦЦУ В МЕНЮ ===
    elif choice == '4':
        print('\n--- Добавить позицию в меню ---')
        new_pizza = input('Введите название новой пиццы: ').strip()
        existing = [k.strip() for k in data.keys()]
        if new_pizza in existing:
            print('Такая пицца уже есть в меню')
        else:
            data[new_pizza + " "] = [0] * 11
            try:
                new_price = int(input('Введите цену новой пиццы : '))
                prices[new_pizza] = new_price
            except ValueError:
                prices[new_pizza] = 0
            recipes[new_pizza] = {}
            print('\nТеперь укажите рецепт (сколько какого ингредиента нужно на 1 пиццу).')
            print('Введите 0, если ингредиент не используется. Пустой ввод — пропустить.')
            for ing in ingredients.keys():
                val = input(f'  {ing}: ')
                if val.strip():
                    try:
                        recipes[new_pizza][ing] = int(val)
                    except ValueError:
                        pass
            save_menu()
            save_prices()
            save_recipes()
            print(f'\n Пицца "{new_pizza}" добавлена!')

    # === 5. ПОСМОТРЕТЬ СКЛАД ===
    elif choice == '5':
        print('\n--- Остатки на складе ---')
        for ing, qty in ingredients.items():
            print(f"  {ing}: {qty} шт.")
        input('\nНажмите Enter, чтобы вернуться в меню')

    # === 6. УДАЛИТЬ ПИЦЦУ ИЗ МЕНЮ ===
    elif choice == '6':
        print('\n--- Удалить пиццу из меню ---')
        menu_keys = list(data.keys())
        if not menu_keys:
            print('Меню пустое, нечего удалять.')
        else:
            for i, key in enumerate(menu_keys, 1):
                name = key.strip()
                price = prices.get(name, 0)
                print(f"{i} - {name} | Цена: {price} руб.")

            try:
                idx = int(input('\nВведите номер пиццы для удаления (0 для отмены): ')) - 1
                if idx == -1:
                    print('Удаление отменено.')
                elif 0 <= idx < len(menu_keys):
                    pizza_key = menu_keys[idx]
                    pizza_name = pizza_key.strip()

                    confirm = input(f'Вы уверены? (да/нет): ').strip().lower()
                    if confirm == 'да':
                        if pizza_key in data:
                            del data[pizza_key]

                        keys_to_remove_prices = [k for k in prices.keys() if k.strip() == pizza_name]
                        for k in keys_to_remove_prices:
                            del prices[k]

                        keys_to_remove_recipes = [k for k in recipes.keys() if k.strip() == pizza_name]
                        for k in keys_to_remove_recipes:
                            del recipes[k]

                        save_menu()
                        save_prices()
                        save_recipes()
                        print(f'\nПицца "{pizza_name}" удалена из меню.')
                    else:
                        print('Удаление отменено.')
                else:
                    print('Ошибка: нет такого номера.')
            except ValueError:
                print('Ошибка: нужно ввести число!')
        input('\nНажмите Enter, чтобы вернуться в меню...')
    elif choice == '7':
        print('Завершение работы.')
        break
    else:
        print('Выберите пункт от 1 до 7.')
