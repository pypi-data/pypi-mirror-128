class NoSampleValuesForFeaturizationError(Exception):
    """Raised when no sample data provided for featurization"""
    pass


class UnsupportedSampleValuesForFeaturizationError(Exception):
    """Raised when unsupported sample data are provided for featurization"""
    pass


class UnsupportedSampleLabelsForFeaturizationError(Exception):
    """Raised when unsupported sample labels are provided for featurization"""
    pass


class NoFeaturesPipelineForFeaturizationError(Exception):
    """Raised when no pipeline provided for featurization"""
    pass


class UnsupportedFeaturesPipelineForFeaturizationError(Exception):
    """Raised when unsupported pipeline are provided for featurization"""
    pass
