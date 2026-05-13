from fastapi import FastAPI
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar, ClienteEliminar

app= FastAPI()

#Lista de clientes en BD
lista_clientes:list[Cliente] = []

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
