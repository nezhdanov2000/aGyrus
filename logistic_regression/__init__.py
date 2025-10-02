"""
Logistic Regression Components Package

Компоненты логистической регрессии для классификации намерений и извлечения сущностей.
Использует Logistic Regression + TF-IDF для быстрой и точной обработки естественного языка.
"""

from .intent import IntentClassifier
from .entity import EntityExtractor

__version__ = "1.0.0"
__author__ = "Booking Bot Team"

__all__ = ['IntentClassifier', 'EntityExtractor']
