from datetime import datetime

class DaoUtil:

    def prepare_to_save(validated_data,user_id):
        try:
            validated_data['fdl'] = 0                      # campo logico para establecer si esta activo (0) o inactivo (1)
            validated_data['cbu'] = user_id                # id de usuario que se registra primero que todos
            validated_data['cat'] = datetime.now()         #fecha en la que se creo el primer registro
            validated_data['luu'] = user_id                #id de usuario que  actualizo o elimino datos de una tabla
            validated_data['uat']= datetime.now()          #fecha en que se realizo una actualizacion (va de la mano con 'luu')
            return validated_data
        except AttributeError as aex:
            raise RuntimeError(f"Atributo no encontrado: {aex}")
        except Exception as ex:
            raise RuntimeError(f"Error general: {ex}")

    def prepare_to_update(instance,user_id):
        try:
            instance.luu  = user_id
            instance.uat  = datetime.now()
            return instance
        except AttributeError as aex:
            raise RuntimeError(f"Atributo no encontrado: {aex}")
        except Exception as ex:
            raise RuntimeError(f"Error general: {ex}")

    def prepare_to_delete(instance, user):
        try:
            instance.fdl = 1
            instance.luu=user.get('id')
            instance.uat = datetime.now()
            return instance
        except AttributeError as aex:
            raise RuntimeError(f"Atributo no encontrado: {aex}")
        except Exception as ex:
            raise RuntimeError(f"Error general: {ex}")


