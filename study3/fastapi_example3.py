from fastapi import FastAPI
from pydantic import BaseModel
#from chunks import Chunk_Full
from chunks3 import Chunk3

model3 = Chunk3("Simble.txt")
#model3 = Chunk3()

# аннотации типов
# класс с типами данных параметров 
class Item(BaseModel):
    name: str
    description: str
    price: float

# создаем объект приложения
app = FastAPI()

# функция, которая будет обрабатывать запрос по пути "/"
# полный путь запроса http://127.0.0.1:8000/
@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

# функция, которая обрабатывает запрос по пути "/about"
@app.get("/about")
def about():
    return {"message": "Страница с описанием проекта"}

# функция-обработчик с параметрами пути
@app.get("/users/{id}")
#def users(id: int): # валидация типа id,  должно быть int
def users(id):
    return {"user_id": id}

# функция-обработчик post запроса с параметрами
@app.post("/users")
def get_model(item:Item):
    return {"user_name": item.name, "description": item.description, "price": item.price}

#@app.get("/get_answer")
#def get_answer(text: str):
#    answer = model.get_answer(text)
#    return {"answer": answer}    
    #return f"This is your text: {text}"

@app.get("/get_answer3")
def get_answer3(text: str):
    source_chunks = model3.chunk_list()
    print(source_chunks[20:])
    db = model3.make_index()
    answer = model3.get_answer3(text)
    return {"answer": answer}    
    #return f"This is your text: {text}"
