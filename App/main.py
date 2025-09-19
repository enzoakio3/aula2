from fastapi import HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
import App.schemas as schemas
import App.crud as crud
from App.database import get_db
from fastapi.staticfiles import StaticFiles

import traceback

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# monta a pasta static
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/usuario/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioBase, db: Session = Depends(get_db)):
    try:
        return crud.create_usuario(db=db, usuario=usuario)
    except HTTPException as e:
        raise e  
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Erro de chave primária: o ID já existe.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@app.post("/login/")
def login(usuario: schemas.UsuarioBase, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_por_nome(db, usuario.nome, usuario.senha)
    traceback.print_exc()
    if not db_usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário não encontrado")
    
    if db_usuario.senha != usuario.senha:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha incorreta")
