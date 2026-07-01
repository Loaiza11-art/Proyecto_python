from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar, ClienteEliminar
from modelos.factura import Factura, FacturaCrear, FacturaEditar, FacturaBase
from modelos.Transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar, TransaccionesaBase
app= FastAPI()

#Lista de clientes en BD
lista_clientes:list[Cliente] = []
lista_facturas:list[Factura] = []
lista_transacciones:list[Transacciones] = []

#endpoint para obtener o listar todos los clientes
@app.get("/Clientes", response_model=list[Cliente])
async def listar_clientes():
    #Creacion de sms mas adecuado al usuario
        return {"Clientes": lista_clientes}

#Aqui es buscar, con el id, permite buscar un resgistro específico 
@app.get("/Clientes{cliente_id}", response_model=Cliente)
async def listar_cliente(cliente_id:int):
    #recorre la lista de clientes
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == cliente_id:
            return obj_cliente
        raise HTTPException(
            status_code=400, detail=f"El cliente con id {cliente_id}, no existe"
        )

#endpoint para crear un cliente y agregar a la lista
@app.post("/Clientes", response_model=Cliente)
async def crear_cliente(datos_cliente:ClienteCrear):
    cliente_val=Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id=len(lista_clientes)+1#id incremento
    lista_clientes.append(cliente_val)
    return cliente_val


#endpoint para editar un cliente y agregarlo a la lista
@app.patch("/Clientes/{cliente_id}", response_model=Cliente)
async def Editar_cliente(cliente_id:int, datos_cliente:ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == cliente_id:
            #validar el cliente
            cliente_val= Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = cliente_id
            lista_clientes[i] = cliente_val
        return {"MENSAJE": "Se edito el cliente satisfactoriamente", "Cliente": cliente_val}
    raise HTTPException(
        status_code=400, detail=f"El cliente con id {cliente_id}, no existe"
    )
    

#endpoint eliminar cliente
@app.delete("/Clientes/{cliente_id}", response_model=Cliente)
async def Eliminar_cliente(cliente_id:int):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == cliente_id:
            cliente_eliminado = lista_clientes.pop(i)
            return {"Cliente": "Cliente eliminado"}
    raise HTTPException(
        status_code=400, detail=f"El cliente con id {cliente_id}, no existe."
    )



# ---- endopoint de facturas ----
@app.get("/facturas", response_model=list[Factura])
def listar_facturas():
    return lista_facturas

@app.get("/facturas/{factura_id}", response_model=Factura)
async def listar_factura(factura_id:int):
    #se recorre la lista de facturas
    for i, obj_factura in enumerate(lista_facturas):
        if obj_factura.id == factura_id:
            return obj_factura
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"La factura con id {factura_id}, no existe"
    )


@app.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(cliente_id: int ,datos_factura: FacturaCrear):
    #Buscar el cliente
    cliente_encontrado = None
    cliente_encontrado = [c for c in lista_clientes if c.id == cliente_id]
    
    #mensaje cuando el cliente no existe
    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cliente con id {cliente_id} no existe, debes crear."
            )
    


#validar datos de la factura
    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.cliente = cliente_encontrado
    #id de la factura
    factura_val.id = len(lista_facturas) + 1
    factura_val.fecha = datetime.now()
    lista_facturas.append(factura_val)
    return factura_val


#enpoint de transacciones
@app.get("/transacciones", response_model=list[Transacciones])
async def listar_transacciones():
    return lista_transacciones

@app.get("/transacciones/{factura_id}", response_model=Transacciones)
async def listar_transacciones (factura_id: int, datos_transaccion: TransaccionesCrear):
    pass

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
        raise HTTPException(status_code=400,
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
    
@app.patch("/transacciones/{id_transaccion}", response_model=Transacciones)
async def editar_transacciones (id_trasaccion: int, datos_transaccion: Transacciones):
    pass

@app.delete("/transacciones/{id_transaccion}", response_model=Transacciones)
async def eliminar_transacciones (id_trasaccion: int):
    pass

