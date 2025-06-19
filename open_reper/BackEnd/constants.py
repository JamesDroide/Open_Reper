#backend/constants.py
from typing import Dict, List, Tuple

opening_mapping: Dict[str, List[Tuple[str, str]]] = {
    'posicional': [
        ('E00', 'Apertura Catalana'),
        ('A10', 'Apertura Inglesa'),
        ('D02', 'Sistema Londres')
    ],
    'combinativo': [
        ('C39', 'Gambito de Rey'),
        ('C44', 'Apertura Escocesa'),
        ('C21', 'Gambito Danés')
    ],
    'universal': [
        ('C50', 'Apertura Italiana'),
        ('C60', 'Apertura Española'),
        ('D00', 'Gambito de Dama')
    ]
}

style_descriptions = {
    'Posicional': 'Aperturas que priorizan el control posicional y estructural.',
    'Combinativo': 'Aperturas dinámicas con combinaciones tácticas agresivas.',
    'Universal': 'Aperturas versátiles que combinan estrategia y táctica.'
}

openings = {
    'Catalana': 'E00',
    'Inglesa': 'A10',
    'Londres': 'D02',
    'Escocesa': 'C44',
    'Gambito_de_Rey': 'C39',
    'Gambito_Danes': 'C21',
    'Italiana': 'C50',
    'Española': 'C60',
    'Gambito_de_Dama': 'D00'
}