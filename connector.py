import json
import os


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, filename):
        """
        Конструктор класса. Принимает имя файла и устанавливает его как
        файл для работы. Если файл не существует, он будет создан.
        """
        self.__data_file = filename
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump([], f)

    @property
    def data_file(self):
        """
        Геттер для имени файла с данными.
        """
        return self.__data_file

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных.
        """
        with open(self.__data_file, 'r') as f:
            rows = json.load(f)

        rows.append(data)

        with open(self.__data_file, 'w') as f:
            json.dump(rows, f)

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации.
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000.
        """
        with open(self.__data_file, 'r') as f:
            rows = json.load(f)

        result = []
        for row in rows:
            match = True
            for field, value in query.items():
                if row.get(field) != value:
                    match = False
                    break
            if match:
                result.append(row)

        return result

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает.
        """
        if not query:
            return

        with open(self.__data_file, 'r') as f:
            rows = json.load(f)

        result = []
        for row in rows:
            match = True
            for field, value in query.items():
                if row.get(field) != value:
                    match = False
                    break
            if not match:
                result.append(row)

        with open(self.__data_file, 'w') as f:
            json.dump(result, f)
