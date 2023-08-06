# Mongo Manager

Libreria para el manejo de Objetos almacenados en base de datos MongoDB

## Clases

### MongoManager

Crea la conexion con la base de datos, se debe inicilizar antes de 
invocar ningun repositorio de objetos.

### ObjetoMongoAbstract

Clase abstracta en la que se representa un objeto mongo predefinido,
su constructor recibe un object id haciendo referencia al '_id' del objeto Mongo.

### RepositoryBase

Repositorio base de mongo, recibe como parametros en el constructor,
la coleccion a la que se hace referencia y el objeto al que va a convertir
los resultados de las query que se realicen.

## Ejemplo 

En este ejemplo veremos el uso de la libreria definiendo un objeto <i>Book</i> 
que hereda de ObjetoMongoAbstract y para el que implementa un <i>RepositoryBook</i>
 para poder manejar el objeto de manera más comoda.

    class Book(ObjetoMongoAbstract):
            def __init__(self, name, id_mongo=None):
                super().__init__(id_mongo)
                self.name = name

            def get_dict_no_id(self) -> dict:
                return {
                    "name": self.name
                }
        
            @staticmethod
            def generar_object_from_dict(dictionary):
                if dictionary is None:
                    return None
                return Book(name=dictionary.get("name"),
                            id_mongo=dictionary.get('_id'))
        
            def __str__(self) -> str:
                return "{}".format(self.name)
                
    class RepositoryBook(RepositoryBase):
        def __init__(self) -> None:
            super().__init__('book', Book)

    def main():
        a = RepositoryBook()
        b = Book('test')
        a.insert_one(b)
        print(a.get_all()[-1])


    if __name__ == '__main__':
        MongoManager('user', 'psw', 'bd', 'authenticationDatabase')
        main()