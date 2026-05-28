from pydantic import BaseModel, computed_field

from modelos.clientes import Cliente
from modelos.Transacciones import Transacciones
class FacturaBase(BaseModel):
    #atributos
    fecha: int
    cliente: Cliente
    transacciones: list[Transacciones] = []
    
@computed_field
@property
def valor_total(self) -> float:
    #consultar el id actual y poder filtrar transacciones
    factura_id_actual = getattr(self, "id", None)

    if factura_id_actual is None or not self.Transacciones:
        return 0.0
    return sum(
        t.cantiddad * t.vr_unitario for t in self.Transacciones 
        if t.factura_id == factura_id_actual
    )
class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int | None = None
