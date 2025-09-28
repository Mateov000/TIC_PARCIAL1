import unittest
from Guia2 import ejercicios
from utils import helpers

class TestEjercicios(unittest.TestCase):
    def test_deducir_fuente_memoria_nula_simple(self):
        mensaje = "aabbc"
        alfabeto, encuentros = ejercicios.deducir_fuente_memoria_nula(mensaje)
        self.assertEqual(set(alfabeto), set(['a', 'b', 'c']))
        self.assertEqual(sum(encuentros), len(mensaje))
        # Check correct counts
        self.assertEqual(encuentros[alfabeto.index('a')], 2)
        self.assertEqual(encuentros[alfabeto.index('b')], 2)
        self.assertEqual(encuentros[alfabeto.index('c')], 1)

    def test_deducir_fuente_memoria_nula_empty(self):
        mensaje = ""
        alfabeto, encuentros = ejercicios.deducir_fuente_memoria_nula(mensaje)
        self.assertEqual(alfabeto, [])
        self.assertEqual(encuentros, [])

    def test_simular_palabra_fuente_memoria_nula_basic(self):
        alfabeto = ['x', 'y']
        probabilidades = [0.7, 0.3]
        largo = 10
        palabra = ejercicios.simular_palabra_fuente_memoria_nula(alfabeto, probabilidades, largo)
        self.assertEqual(len(palabra), largo)
        for letra in palabra:
            self.assertIn(letra, alfabeto)

    def test_simular_palabra_fuente_memoria_nula_probabilities_sum(self):
        alfabeto = ['a', 'b', 'c']
        probabilidades = [0.2, 0.5, 0.3]
        largo = 5
        palabra = ejercicios.simular_palabra_fuente_memoria_nula(alfabeto, probabilidades, largo)
        self.assertEqual(len(palabra), largo)
        for letra in palabra:
            self.assertIn(letra, alfabeto)

    def test_calcular_entropia_fuente_binaria_zero(self):
        # Entropy should be 0 when w=0 or w=1
        self.assertEqual(ejercicios.calcular_entropia_fuente_binaria(0), helpers.entropia_desde_fuente([0, 1]))
        self.assertEqual(ejercicios.calcular_entropia_fuente_binaria(1), helpers.entropia_desde_fuente([1, 0]))

    def test_calcular_entropia_fuente_binaria_half(self):
        # Entropy should be maximal when w=0.5
        result = ejercicios.calcular_entropia_fuente_binaria(0.5)
        expected = helpers.entropia_desde_fuente([0.5, 0.5])
        self.assertAlmostEqual(result, expected)

    def test_calcular_entropia_fuente_binaria_typical(self):
        # Test for a typical value
        w = 0.7
        result = ejercicios.calcular_entropia_fuente_binaria(w)
        expected = helpers.entropia_desde_fuente([w, 1-w])
        self.assertAlmostEqual(result, expected)

    def test_calcular_entropia_fuente_binaria_invalid(self):
        # Test for invalid probabilities (should not crash)
        with self.assertRaises(ValueError):
            ejercicios.calcular_entropia_fuente_binaria(-0.1)
        with self.assertRaises(ValueError):
            ejercicios.calcular_entropia_fuente_binaria(1.1)

    def test_normalizar_vector_basic(self):
        vector = [2, 3, 5]
        result = ejercicios.normalizar_vector(vector)
        self.assertAlmostEqual(sum(result), 1.0)
        self.assertEqual(len(result), len(vector))
        expected = [2/10, 3/10, 5/10]
        for r, e in zip(result, expected):
            self.assertAlmostEqual(r, e)

    def test_normalizar_vector_zero(self):
        vector = [0, 0, 0]
        with self.assertRaises(ZeroDivisionError):
            ejercicios.normalizar_vector(vector)

    def test_deducir_fuente_de_markov_simple(self):
        mensaje = "aabbcc"
        alfabeto, matriz = ejercicios.deducir_fuente_de_markov(mensaje)
        self.assertEqual(set(alfabeto), set(['a', 'b', 'c']))
        self.assertEqual(len(matriz), len(alfabeto))
        for columna in zip(*matriz):
            self.assertEqual(len(columna), len(alfabeto))
        # Probabilities should sum to 1 for each column
        for columna in zip(*matriz):
            col_sum = sum(columna)
            self.assertAlmostEqual(col_sum, 1.0)

    def test_simular_palabra_fuente_de_markov_basic(self):
        alfabeto = ['a', 'b']
        matriz = [[0.8, 0.2], [0.2, 0.8]]
        largo = 10
        palabra = ejercicios.simular_palabra_fuente_de_markov(alfabeto, matriz, largo)
        self.assertEqual(len(palabra), largo)
        for letra in palabra:
            self.assertIn(letra, alfabeto)

    def test_deducir_si_memoria_nula_o_markoviana_memoria_nula(self):
        matriz = [
            [0.5, 0.5],
            [0.5, 0.5]
        ]
        tolerancia = 0.01
        result = ejercicios.deducir_si_memoria_nula_o_markoviana(matriz, tolerancia)
        self.assertTrue(result)

    def test_deducir_si_memoria_nula_o_markoviana_markoviana(self):
        matriz = [
            [0.9, 0.1],
            [0.1, 0.9]
        ]
        tolerancia = 0.5
        result = ejercicios.deducir_si_memoria_nula_o_markoviana(matriz, tolerancia)
        self.assertFalse(result)
            

if __name__ == "__main__":
    unittest.main()