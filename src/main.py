from fastapi import FastAPI
from src.routes import login_model 


app = FastAPI()
app.include_router(login_model.router)



app.title = "Login"
app.version = "0.0.1"


