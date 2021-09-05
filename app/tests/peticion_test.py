import unittest
from app.models.peticion import (
    Notificacion, NotiEvento, NotificacionEstado, TipoNotificaciones,
    Peticion, TipoPeticiones, PeticionEvento, PeticionEstado
)

from mongoengine import ValidationError

class NotificacionModelTestCase(unittest.TestCase):
    def setUp(self):
        self.notificacion = Notificacion(
            tipo = TipoNotificaciones.COMENTARIO
        )
        self.notificacion_sin_tipo = Notificacion()

    def test_cambio_estado(self):
        """
        Verificar la transicion de estado cuando se llama al metodo
        transition
        """
        self.notificacion.transition(NotiEvento.LEER)
        self.assertEqual(self.notificacion.estado, NotificacionEstado.LEIDA)

    def test_no_cambio_estado(self):
        """
        Termina la ejecucion del programa si se le pasa un evento incorrecto
        y por lo tanto no se cambia de estado
        """
        self.assertRaises(Exception, self.notificacion.transition, "EVENTO_RARO")
    def test_tipo_es_requerido(self):
        """
        Al guardar la notificacion se verifica que el tipo es requerido
        arrojando una exepcion
        """
        self.assertRaises(
            ValidationError,
            self.notificacion_sin_tipo.validate,
        )

if __name__ == '__main__':
    unittest.main()
