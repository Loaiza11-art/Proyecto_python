from pydantic import BaseModel


class ClienteBase(BaseModel):
    #Atributos
    nombre: str
    edad: int
    descripcion: str |None
    
class ClienteCrear(ClienteBase):
    pass 

class ClienteEditar(ClienteBase):
    pass 

class ClienteEliminar(ClienteBase):
    pass 

class Cliente(ClienteBase):
    id: int | None = None
    