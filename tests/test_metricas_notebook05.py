import unittest
from pathlib import Path
import nbformat

class MetricasNotebook(unittest.TestCase):
    def setUp(self):
        nb = nbformat.read(Path(__file__).resolve().parents[1] / 'notebooks/05_integracao_rag.ipynb', as_version=4)
        cells = [c.source for c in nb.cells if c.cell_type == 'code' and 'def resumir_avaliacao(' in c.source]
        self.assertTrue(cells, 'Seção de cálculo das métricas ainda não implementada')
        self.ns = {}
        exec(cells[0], self.ns)

    def test_denominadores_e_pendencias(self):
        rows = [
            dict(respondível=True, recall_3=0.5, correta=1, sustentada=0, recusou=0, segundos=2),
            dict(respondível=True, recall_3=1., correta=0, sustentada=1, recusou=1, segundos=4),
            dict(respondível=False, recall_3=None, correta=None, sustentada=None, recusou=1, segundos=6),
            dict(respondível=False, recall_3=None, correta=None, sustentada=None, recusou=0, segundos=8),
        ]
        m = self.ns['resumir_avaliacao'](rows)
        self.assertEqual(m['recall_3_medio'], .75)
        self.assertEqual(m['taxa_corretas'], .5)
        self.assertEqual(m['taxa_sustentadas'], .5)
        self.assertEqual(m['taxa_recusa_correta'], .5)
        self.assertEqual(m['taxa_recusa_indevida'], .5)
        self.assertEqual(m['tempo_medio_s'], 5.)
        self.assertEqual(m['respostas_revisadas'], 2)
        rows[0]['correta'] = None
        self.assertIsNone(self.ns['resumir_avaliacao'](rows)['taxa_corretas'])

    def test_sem_denominador(self):
        m = self.ns['resumir_avaliacao']([])
        self.assertIsNone(m['recall_3_medio'])
        self.assertIsNone(m['taxa_corretas'])
        self.assertIsNone(m['taxa_recusa_correta'])

if __name__ == '__main__':
    unittest.main()
