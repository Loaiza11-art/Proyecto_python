from datetime import datetime
from fastapi import FastAPI, HTTPException
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar, ClienteEliminar
from modelos.factura import Factura, FacturaCrear, FacturaEditar, FacturaBase
from modelos.Transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar, TransaccionesaBase
app= FastAPI()

#Lista de clientes en BD
lista_clientes:list[Cliente] = []
lista_facturas:list[Factura] = []
lista_transacciones:list[Transacciones] = []

@app.get("/clientes")
async def listar_clientes():
    #Creacion de sms mas adecuado al usuario
        return {"Clientes": lista_clientes}
    
@app.get("/clientes{id}")
async def listar_cliente(id:int):
    #Creacion de sms mas adecuado al usuario
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente
        


@app.post("/clientes", response_model=Cliente)
async def crear_cliente(datos_cliente:ClienteCrear):
    cliente_val=Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id=len(lista_clientes)+1#id incremento
    #id_cliente=len(lista_clientes)+1.
    lista_clientes.append(cliente_val)
    return cliente_val


@app.put("/clientes/{id}")
def editar_cliente(id: int, datos_cliente:ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_val= Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = id
            lista_clientes[i] = cliente_val
            
        return {"MENSAJE": "Se edito el cliente satisfactoriamente", "Cliente": cliente_val}

@app.delete("/clientes")
def eliminar_cliente(id:int, datos_cliente:ClienteEliminar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            lista_clientes.pop(i)
    return {"Cliente": "Cliente eliminado","cliente":obj_cliente}

# ---- endopoint de facturas ----
@app.get("/facturas", response_model=list[Factura])
def listar_facturas():
    return lista_facturas

@app.post("/facturas", response_model=Factura)
def crear_factura(cliente_id: int ,datos_factura: FacturaCrear):
    cliente_encontrado = None
    cliente_encontrado = [c for c in lista_clientes if c.id == cliente_id]
    
    if not cliente_encontrado:
        raise fastapi.HTTPException(satus_code=404, detail=f"Cliente con id {cliente_id} no existe, debes crear.")

#crear la factura
    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.id = len(lista_facturas) + 1
    factura_val.fecha = datetime.now()
    lista_facturas.append(factura_val)
    return factura_val

#enpoint de transacciones
@app.get("/transacciones", response_model=list[Transacciones])
async def listar_transacciones():
    return lista_transacciones

@app.post("/transacciones/{factura.id}")
async def creartransaccion(
    factura_id: int,
    datos_transaacion: TransaccionesCrear,
    cliente_id: int
):
    
    cliente_encontrado: None
    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break
    
    #excepciones
    if not cliente_encontrado:
        raise fastapi.HTTPException(status_code=400,
                            detail=f"Error 400: No esiste in cliente con ese id: {cliente_id}, debes de crear un cliente.")
    #Consultar la factura
    factira_encontrada= None
    for f in lista_facturas:
        if f.id == factura_id:
            factura_encontrada = f
            break

    #si se encuentra la factura, 
    if factura_encontrada:
        #se valida que el cliente de la factura sea el mismo que el cliente_id dado
        if factura_encontrada.cliente.id == cliente_id:
            transaccion_val = Transacciones.model_validate(
                datos_transaacion.model_dump())
            transaccion_val.id = len(lista_transacciones)+1
            transaccio9n_val.factura_id = factura_id
            lista_transacciones.append(transaccion_val)

            factura_encontrada.transacciones.append(transaccion_val)
            mensaje = f"Transacción agregada a la factura{factura_encontrada.id}"
            factura_final = factura_encontrada
            return {"mensaje": mensaje, "factura": factura_final}
        else:
            mensaje = f"Se encontro la factura de if:{factura_if}, pero eds de otro cliente id: {cliente_id} "
            factura_final = factura_encontrada
            return {"mensaje": mensaje,"factura_encontrada": factura_final}
        
    else:
#pero si no se encuentra la factura, 
        #se valida antes de crear la factura
        transaccion_val = Transacciones.model_validate(datos_transaccion.model_dump())
        transaccion_val.id = len(lista_transacciones)+1
        transaccion_val.factura_id = len (lista_factura)+1

#se crea una nueva factura con cliente, fecha, transaccion
        factura = FacturaCrear(
            fecha = datetime.now(),
            cliente = cliente_encontrado,
            transacciones = [transaccion_val]
        )

        factura_val = Factura.model_validate(factura.model_dump())
        factura_val.id = len(lista_facturas)+1
        lista_facturas.append(factura_val)

        lista_transacciones.append(transaccion_val)

        return {"mensaje": f"Factura no existe con el id:{factura_id}, pero se creo la nueva factura, Factura: {factura_val.id}" }