import site
import wsgiref.simple_server
import json

tarea = {}
elemnt_prox = 1 

def server(environ, start_response):
    global elemnt_prox
    metodo = environ['Request_method']
    ruta= environ['PATH_info']

    if metodo == 'GET' and ruta== '/tasks':
        status = '200 ok'
        headers= [{'Content-type', 'application/json'}]
        start_response(status,headers)
        lista_tareas= list(tarea.values())
        json_respuesta= json.dumps(lista_tareas)

    elif metodo== "POST" and ruta=='/tasks':
        long = int(environ.get('CONTENT_LENGTH' , 0))
        cuerpo= environ['wsgi.input'].read(longitud)

        datos= json.loads(cuerpo) if cuerpo else{}

        tarea_nueva={
            "id": elemnt_prox,
            "title" : datos.get("title", ""),
            "done": datos.get("done", False)
        }

        tarea[elemnt_prox] = tarea_nueva
        elemnt_prox +=1

        status= '201 created'
        headers= [{'Content-type', 'application/json'}]
        start_response(status, headers)
        return[json.dumps(tarea_nueva).encode('utf-8')]

    elif ruta.startswith('/tasks'):
        id_str = ruta.split('/')[-1]
        if not id_str.isdigit():
            status = '404 Not Found'
            headers = [{'Content-Type', 'application/json'}]
            start_response(status, headers)
            error= {"error": "El Id debe ser un entero"}
            return [json.dumps(error).encode('utf-8')]

        id_tarea= int(id_str)

        if id_tarea not in tarea(): 
            status = '404 Not Found'
            headers = [{'Content-Type', 'application/json'}]
            start_response(status, headers)
            error= {"error": "Tarea no encontrada"}
            return [json.dumps(error).encode('utf-8')]

        if metodo == 'GET':
            status='200 ok'
            headers= [{'Content-type', 'application/json'}]
            start_response(status, headers)
            tarea_encontrada = tarea[id_tarea]
            json_respuesta= json.dumps(tarea_encontrada)
            return[json_respuesta.enconde('utf-8')]

        elif metodo== 'PATCH':
            longitud = int(environ.get('Content_length',0))
            cuerpo= environ['wsgi.input'].read(longitud)
            if cuerpo: 
                datos_parc = json.loads(cuerpo)
                for clave, valor in datos_parc.items():
                    if clave in tarea[id_tarea]:
                        tarea[id_tarea][clave] = valor
                        status='200 ok '
                        headers = [('Content-type', 'application/json')]
                        start_response(status, headers)
                        json_respuesta= json.dumps(tarea[id_tarea])
                        return [json_respuesta.encode('utf-8')]

                    elif metodo == 'DELETE':
                        del tarea[id_tarea]
                        status = '200 ok'
                        headers = [('Content-type', 'application/json')]
                        start_response (status, headers)
                        json_respuesta = json.dumps({"mensaje": "Tarea eliminada"})
                        return [json_respuesta.encode('utf-8')]
                    else:
                        status = '405 Method Not Allowed'
                        headers = [('Content-type', 'application/json')]
                        start_response(status, headers)
                        error = {"error": "metodo no permitido para esta ruta"}
                        return[json.dumps(error).encode('utf-8')]
            else:
                status= '404 Not found'
                headers= [('Content-type', 'application/json')]
                start_response(status, headers)
                error = {"error": "ruta no encontrada o metodo incorrecto"}
                json_error= json.dumps(error)
                return [json_error.encode('utf-8')]
            if __name__== '_main_':
                puerto = 9292
                print(f"Servidor escuchando en http://localhost:{puerto}...")
                wsgiref.simple_server.make_server ("puerto, server").serve_forever()[site:1]