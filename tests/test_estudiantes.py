"""
Pruebas unitarias — Módulo estudiantes
Sistema de Notas Universitarias
"""

import pytest
from src.estudiantes import Estudiante, RegistroEstudiantes


# ─────────────────────────────────────────────
#  Tests: clase Estudiante
# ─────────────────────────────────────────────

class TestEstudiante:

    def test_creacion_correcta(self):
        e = Estudiante("2021001", "Ana García", "ana@iumafis.edu.co")
        assert e.codigo == "2021001"
        assert e.nombre == "Ana García"
        assert e.email == "ana@iumafis.edu.co"

    def test_codigo_se_convierte_a_mayusculas(self):
        e = Estudiante("abc123", "Juan López", "juan@test.com")
        assert e.codigo == "ABC123"

    def test_email_se_convierte_a_minusculas(self):
        e = Estudiante("E001", "María", "MARIA@TEST.COM")
        assert e.email == "maria@test.com"

    def test_nombre_y_codigo_se_eliminan_espacios(self):
        e = Estudiante("  E001  ", "  Carlos  ", "c@c.com")
        assert e.codigo == "E001"
        assert e.nombre == "Carlos"

    def test_codigo_vacio_lanza_error(self):
        with pytest.raises(ValueError, match="código"):
            Estudiante("", "Pedro", "p@test.com")

    def test_codigo_solo_espacios_lanza_error(self):
        with pytest.raises(ValueError):
            Estudiante("   ", "Pedro", "p@test.com")

    def test_nombre_vacio_lanza_error(self):
        with pytest.raises(ValueError, match="nombre"):
            Estudiante("E001", "", "p@test.com")

    def test_email_sin_arroba_lanza_error(self):
        with pytest.raises(ValueError, match="@"):
            Estudiante("E001", "Pedro", "sinatsign.com")

    def test_to_dict(self):
        e = Estudiante("E001", "Ana", "ana@test.com")
        d = e.to_dict()
        assert d == {"codigo": "E001", "nombre": "Ana", "email": "ana@test.com"}

    def test_repr(self):
        e = Estudiante("E001", "Ana", "ana@test.com")
        assert "E001" in repr(e)
        assert "Ana" in repr(e)


# ─────────────────────────────────────────────
#  Tests: clase RegistroEstudiantes
# ─────────────────────────────────────────────

class TestRegistroEstudiantes:

    def setup_method(self):
        """Se ejecuta antes de cada test — crea registro limpio."""
        self.registro = RegistroEstudiantes()
        self.e1 = Estudiante("E001", "Ana García", "ana@test.com")
        self.e2 = Estudiante("E002", "Carlos Mejía", "carlos@test.com")

    def test_registrar_estudiante_nuevo(self):
        self.registro.registrar(self.e1)
        assert self.registro.total() == 1

    def test_registrar_dos_estudiantes(self):
        self.registro.registrar(self.e1)
        self.registro.registrar(self.e2)
        assert self.registro.total() == 2

    def test_registrar_codigo_duplicado_lanza_error(self):
        self.registro.registrar(self.e1)
        duplicado = Estudiante("E001", "Otro Nombre", "otro@test.com")
        with pytest.raises(ValueError, match="(?i)ya existe"):
            self.registro.registrar(duplicado)

    def test_buscar_estudiante_existente(self):
        self.registro.registrar(self.e1)
        encontrado = self.registro.buscar("E001")
        assert encontrado.nombre == "Ana García"

    def test_buscar_codigo_en_minusculas(self):
        self.registro.registrar(self.e1)
        encontrado = self.registro.buscar("e001")
        assert encontrado.codigo == "E001"

    def test_buscar_codigo_inexistente_lanza_error(self):
        with pytest.raises(KeyError):
            self.registro.buscar("X999")

    def test_listar_retorna_ordenado_por_nombre(self):
        self.registro.registrar(self.e2)  # Carlos
        self.registro.registrar(self.e1)  # Ana
        lista = self.registro.listar()
        assert lista[0].nombre == "Ana García"
        assert lista[1].nombre == "Carlos Mejía"

    def test_listar_registro_vacio(self):
        assert self.registro.listar() == []

    def test_eliminar_estudiante_existente(self):
        self.registro.registrar(self.e1)
        self.registro.eliminar("E001")
        assert self.registro.total() == 0

    def test_eliminar_estudiante_inexistente_lanza_error(self):
        with pytest.raises(KeyError):
            self.registro.eliminar("X999")

    def test_total_inicial_es_cero(self):
        assert self.registro.total() == 0
