class NoFeatureValuesForPredictionError(Exception):
    """Raised when no feature data provided for prediction"""
    pass


class UnsupportedFeatureValuesForPredictionError(Exception):
    """Raised when unsupported feature data are provided for prediction"""
    pass


class UnsupportedFeatureLabelsForPredictionError(Exception):
    """Raised when unsupported feature labels are provided for prediction"""
    pass


class NoModelIdentifierForPredictionError(Exception):
    """Raised when no model identifier is provided for prediction"""
    pass


class UnsupportedModelIdentifierForPredictionError(Exception):
    """Raised when unsupported model identifier is provided for prediction"""
    pass
