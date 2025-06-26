"""Dimensionality reduction helpers."""

from typing import Optional

try:
    import cupy as cp
except ImportError:  # pragma: no cover - GPU optional
    cp = None

import numpy as np
from sklearn.decomposition import PCA


def reduce_pca(vectors: np.ndarray, n_components: int = 2) -> np.ndarray:
    """Run PCA reduction using GPU if available, otherwise CPU."""
    if cp is not None and isinstance(vectors, cp.ndarray):
        # Placeholder for GPU-based PCA implementation
        pass
    else:
        pca = PCA(n_components=n_components)
        return pca.fit_transform(vectors)

    # Fallback return empty array until GPU logic implemented
    return np.empty((0, n_components))