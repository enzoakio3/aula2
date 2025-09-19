from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nome: str
    senha: str

class Usuario(UsuarioBase):
    class Config:
        orm_mode = True