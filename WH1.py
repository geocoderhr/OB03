import inspect  # Импорт модуля для работы с функциями и их параметрами

# Monkey patch для Python 3.13:
# Функция inspect.getargspec() была удалена, поэтому заменяем её на inspect.getfullargspec()
if not hasattr(inspect, "getargspec"):
    def getargspec(func):
        spec = inspect.getfullargspec(func)
        return (spec.args, spec.varargs, spec.varkw, spec.defaults)
    inspect.getargspec = getargspec

import pickle  # Импорт модуля для сериализации объектов (сохранения и загрузки состояния)
import pymorphy2  # Импорт библиотеки для морфологического анализа и склонения русских слов

# Создаем экземпляр морфологического анализатора
morph = pymorphy2.MorphAnalyzer()

def decline_word(word, case):
    """
    Функция для склонения слова в заданный падеж.

    Параметры:
      word - исходное слово (строка)
      case - требуемый падеж, например, 'accs' для винительного падежа

    Возвращает:
      Слово, преобразованное в нужную форму.
      Если склонение невозможно, возвращает исходное слово.
    """
    parsed = morph.parse(word)[0]  # Получаем наиболее вероятный разбор слова
    declined = parsed.inflect({case})  # Склоняем слово в нужный падеж
    if declined:
        result = declined.word
        # Если исходное слово начиналось с заглавной буквы, делаем результат с заглавной
        if word[0].isupper():
            result = result.capitalize()
        return result
    return word

# Базовый класс Animal с общими атрибутами и методами для всех животных
class Animal:
    def __init__(self, name, age):
        self.name = name  # Имя животного (на русском)
        self.age = age    # Возраст животного

    def make_sound(self):
        # Абстрактный метод, который должен быть реализован в подклассах
        pass


    def __str__(self):
        return f"Имя: {self.name}, Возраст: {self.age}"

    def eat(self):
        # Метод для вывода информации о том, что животное ест
        print(f"{self.name} ест.")



# Подкласс Bird, наследующий от Animal
class Bird(Animal):
    def __init__(self, name, age, wing_span):
        super().__init__(name, age)  # Инициализация общих атрибутов через базовый класс
        self.wing_span = wing_span  # Размах крыльев птицы

    def make_sound(self):
        # Переопределенный метод: выводит звук, который издает птица
        print(f"{self.name} чирикает.")

# Подкласс Mammal, наследующий от Animal
class Mammal(Animal):
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.fur_color = fur_color  # Цвет шерсти животного

    def make_sound(self):
        # Переопределенный метод: выводит звук, который издает млекопитающее
        print(f"{self.name} рычит.")

# Подкласс Reptile, наследующий от Animal
class Reptile(Animal):
    def __init__(self, name, age, scale_type):
        super().__init__(name, age)
        self.scale_type = scale_type  # Тип чешуи рептилии

    def make_sound(self):
        # Переопределенный метод: выводит звук, который издает рептилия
        print(f"{self.name} шипит.")

def animal_sound(animals):
    """
    Функция для демонстрации полиморфизма:
    Принимает список животных и вызывает их метод make_sound().
    """
    for animal in animals:
        animal.make_sound()

# Класс ZooKeeper для сотрудников, занимающихся уходом за животными
class ZooKeeper:
    def __init__(self, name):
        self.name = name  # Имя смотрителя зоопарка

    def feed_animal(self, animal):
        # Склоняем имя животного в винительный падеж для корректного отображения
        animal_name_declined = decline_word(animal.name, 'accs')
        print(f"{self.name} кормит {animal_name_declined}.")

# Класс Veterinarian для сотрудников, отвечающих за здоровье животных
class Veterinarian:
    def __init__(self, name):
        self.name = name  # Имя ветеринара

    def heal_animal(self, animal):
        # Склоняем имя животного в винительный падеж для корректного отображения
        animal_name_declined = decline_word(animal.name, 'gent')
        print(f"{self.name} лечит {animal_name_declined}.")

class Cleaner:
    def __init__(self, name):
        self.name = name

    def cleaning_animal(self,animal):
        # Склоняем имя животного в винительный падеж для корректного отображения
        animal_name_declined = decline_word(animal.name, 'gent')
        print(f"{self.name} чистит клетки {animal_name_declined}")

    def cleaning_cages(self, animals):
        """
        Метод для чистки клеток всех животных.
        Принимает список животных и выводит сообщение для каждого.
        """
        for animal in animals:
            animal_name_declined = decline_word(animal.name, 'gent')
            print(f"{self.name} чистит клетку для {animal_name_declined}.")

# Класс Zoo, использующий композицию для хранения информации о животных и сотрудниках,
# а также предоставляющий методы для сохранения и загрузки состояния зоопарка
class Zoo:
    def __init__(self, name):
        self.name = name         # Название зоопарка (на русском)
        self.animals = []        # Список животных в зоопарке
        self.employees = []      # Список сотрудников зоопарка

    def add_animal(self, animal):
        # Метод для добавления животного в зоопарк
        self.animals.append(animal)
        print(f"Добавлен {animal.name} в зоопарк {self.name}.")

    def add_employee(self, employee):
        # Метод для добавления сотрудника в зоопарк
        self.employees.append(employee)
        print(f"Добавлен сотрудник {employee.name} в зоопарк {self.name}.")

    def save_state(self, filename):
        # Метод для сохранения состояния зоопарка в файл с использованием pickle
        with open(filename, "wb") as file:
            pickle.dump(self, file)
        print("Состояние зоопарка сохранено в файл.")

    def display_animals(self):
        print("Список животных в зоопарке:")
        for animal in self.animals:
            print(animal)



    @classmethod
    def load_state(cls, filename):
        # Класс-метод для загрузки состояния зоопарка из файла
        with open(filename, "rb") as file:
            zoo = pickle.load(file)
        print("Состояние зоопарка загружено из файла.")
        return zoo

# Пример использования программы
if __name__ == "__main__":
    # Создаем экземпляры животных с именами на русском языке
    parrot = Bird("Попугай", 2, wing_span=0.5)
    lion = Mammal("Лев", 5, fur_color="золотой")
    snake = Reptile("Змея", 3, scale_type="гладкие")


    # Демонстрация полиморфизма: вызываем метод make_sound() для каждого животного
    animals = [parrot, lion, snake]
    animal_sound(animals)

    # Создаем зоопарк с названием на русском языке и добавляем животных
    zoo = Zoo("Городской зоопарк")
    zoo.add_animal(parrot)
    zoo.add_animal(lion)
    zoo.add_animal(snake)

    # Создаем сотрудников зоопарка с именами на русском языке и добавляем их
    keeper = ZooKeeper("Алиса")
    vet = Veterinarian("Боб")
    clean = Cleaner("Константин")

    zoo.add_employee(keeper)
    zoo.add_employee(vet)
    zoo.add_employee(clean)

    # Вызов специфичных методов сотрудников:
    # Теперь имя животного склоняется в винительном падеже (например, "Лев" -> "Льва")
    keeper.feed_animal(lion)  # Выведет: "Алиса кормит Льва."
    vet.heal_animal(snake)  # Выведет: "Боб лечит Змею."
    clean.cleaning_cages(zoo.animals)

    # Сохранение состояния зоопарка в файл "zoo_state.pkl"
    zoo.save_state("zoo_state.pkl")

    # Загрузка состояния зоопарка из файла "zoo_state.pkl"
    loaded_zoo = Zoo.load_state("zoo_state.pkl")
