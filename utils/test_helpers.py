import math
import unittest

from utils.helpers import (
    calcular_info_evento,
    lista_info_desde_lista_probabilidades,
    entropia_desde_fuente,
    generar_extension_memoria_nula,
)

class TestHelpers(unittest.TestCase):

    def test_calcular_info_evento_basic(self):
        self.assertEqual(calcular_info_evento(1), 0)
        self.assertEqual(calcular_info_evento(0), 0)
        self.assertTrue(math.isclose(calcular_info_evento(0.5), 1.0))
        self.assertTrue(math.isclose(calcular_info_evento(0.25), 2.0))

    def test_calcular_info_evento_edge(self):
        self.assertTrue(math.isclose(calcular_info_evento(0.125), 3.0))
        self.assertTrue(math.isclose(calcular_info_evento(0.75), math.log2(1/0.75)))

    def test_lista_info_desde_lista_probabilidades(self):
        probs = [1, 0.5, 0.25]
        infos = lista_info_desde_lista_probabilidades(probs)
        expected = [0, 1, 2]
        for i, e in zip(infos, expected):
            self.assertTrue(math.isclose(i, e))

    def test_lista_info_desde_lista_probabilidades_empty(self):
        self.assertEqual(lista_info_desde_lista_probabilidades([]), [])

    def test_entropia_desde_fuente(self):
        probs = [0.5, 0.5]
        ent = entropia_desde_fuente(probs)
        self.assertTrue(math.isclose(ent, 1.0))
        probs = [0.25, 0.25, 0.25, 0.25]
        ent = entropia_desde_fuente(probs)
        self.assertTrue(math.isclose(ent, 2.0))
        probs = [1.0, 0.0]
        ent = entropia_desde_fuente(probs)
        self.assertTrue(math.isclose(ent, 0.0))

    def test_entropia_desde_fuente_non_uniform(self):
        probs = [0.7, 0.3]
        ent = entropia_desde_fuente(probs)
        expected = -0.7 * math.log2(0.7) - 0.3 * math.log2(0.3)
        self.assertTrue(math.isclose(ent, expected))

    def test_generar_extension_memoria_nula_N0(self):
        alfabeto = ['a', 'b']
        probs = [0.5, 0.5]
        N = 0
        alf_ext, probs_ext = generar_extension_memoria_nula(alfabeto, probs, N)
        self.assertEqual(alf_ext, alfabeto)
        self.assertEqual(probs_ext, probs)

    def test_generar_extension_memoria_nula_N1(self):
        alfabeto = ['a', 'b']
        probs = [0.5, 0.5]
        N = 1
        alf_ext, probs_ext = generar_extension_memoria_nula(alfabeto, probs, N)
        expected_alf = ['aa', 'ab', 'ba', 'bb']
        expected_probs = [0.25, 0.25, 0.25, 0.25]
        self.assertEqual(alf_ext, expected_alf)
        for p, ep in zip(probs_ext, expected_probs):
            self.assertTrue(math.isclose(p, ep))

    def test_generar_extension_memoria_nula_N2(self):
        alfabeto = ['0', '1']
        probs = [0.7, 0.3]
        N = 2
        alf_ext, probs_ext = generar_extension_memoria_nula(alfabeto, probs, N)
        self.assertEqual(len(alf_ext), 8)
        self.assertEqual(len(probs_ext), 8)
        self.assertTrue(math.isclose(sum(probs_ext), 1.0))

    def test_generar_extension_memoria_nula_empty(self):
        alfabeto = []
        probs = []
        N = 1
        alf_ext, probs_ext = generar_extension_memoria_nula(alfabeto, probs, N)
        self.assertEqual(alf_ext, [])
        self.assertEqual(probs_ext, [])

    def test_generar_extension_memoria_nula_single_symbol(self):
        alfabeto = ['x']
        probs = [1.0]
        N = 3
        alf_ext, probs_ext = generar_extension_memoria_nula(alfabeto, probs, N)
        self.assertEqual(alf_ext, ['xxxx'])
        self.assertEqual(probs_ext, [1.0])

    def test_probabilities_sum_to_one(self):
        alfabeto = ['a', 'b', 'c']
        probs = [0.2, 0.3, 0.5]
        N = 2
        _, probs_ext = generar_extension_memoria_nula(alfabeto, probs, N)
        self.assertTrue(math.isclose(sum(probs_ext), 1.0))

    def test_entropia_desde_fuente_empty(self):
        self.assertEqual(entropia_desde_fuente([]), 0)


    

if __name__ == "__main__":
    unittest.main()