# Контролер для роботи з таблицею категорій
from models.category_model import CategoryModel

# Контролер для створення нової категорії
def create_category(name, page):
    # Викликаємо метод моделі для створення категорії з назвою та сторінкою
    return CategoryModel.create_category(name, page)

# Контролер для отримання всіх категорій
def get_all_categories():
    # Повертаємо список усіх категорій
    return CategoryModel.get_all_categories()

# Контролер для отримання категорій за певною сторінкою
def get_category_by_page(page):
    # Повертаємо категорії, що прив’язані до конкретної сторінки
    return CategoryModel.get_categories_by_page(page)

# Контролер для видалення категорії за її ID
def delete_category(category_id):
    # Видаляємо категорію за її ідентифікатором
    return CategoryModel.delete_category(category_id)

# Контролер для отримання категорії за ID
def get_categoryId(category_id):
    # Повертаємо категорію за її ідентифікатором
    return CategoryModel.get_category_by_id(category_id)
