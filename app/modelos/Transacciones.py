from pydantic import BaseModel

class TransaccionesaBase(BaseModel):
    #atributos
    cantidad: int
    vr_unitario: float
    descripcion: str
    
class TransaccionesCrear(TransaccionesaBase):
    pass

class TransaccionesEditar(TransaccionesaBase):
    pass

class Transacciones(TransaccionesaBase):
    id: int | None = None
    factura_id: int | None = None