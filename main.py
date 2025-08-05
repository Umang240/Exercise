# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from pydantic import BaseModel, Field 
from fastapi import status
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI() 

def read_root():
    return HTMLResponse("<h1>Hello, World!</h1> <p>Welcome to FastAPI!</p>")

app.get("/", response_class=HTMLResponse)(read_root)   



@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "message": "You requested this item."}



class Item(BaseModel):
    name : str
    price : float

@app.post("/items/")
def create_item(item: Item):
    return {"name": item.name, "price": item.price, "message": "Item created successfully."}

@app.get("/search/")
def search_items(q: str = None):
    if q:
        return {"message": f"Searching for {q}"}
    return {"message": "No search query provided."}

@app.get("/home/")
def home():
    return HTMLResponse("<h1>Welcome to the home page!</h1> <p>Enjoy your stay.</p>")

class User(BaseModel):
    username: str
    email: str

@app.post("/submit/")
def submit_user(user: User):
    return {"username": user.username, "email": user.email, "message": f"{user.username} submitted successfully."}

class Product(BaseModel):
    name: str = Field(..., example="Sample Product")
    brand: str = Field(..., example="Lakme")
    price: int 
    in_stock: bool = Field(..., example=True)


@app.post("/products/", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    print(product)
    print(product.model_dump())
    if product.price < 100:
        raise HTTPException(
            status_code=400, 
            detail="Price must be at least 100")
    return {
        "name": product.name,
        "brand": product.brand,
        "price": product.price,
        "in_stock": product.in_stock
    }




templates = Jinja2Templates(directory="templates")

@app.get("/show/")
def show_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "data": "Hello from FastAPI!"})

@app.get("/login/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": "Please log in" })

@app.post("/login/")
async def login(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    
    if not username or not password:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Userrname and password are required."
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": f"Welcome, {username}!",
        "username": username,
        "password": password
    })
    

