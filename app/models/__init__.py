"""SQLModel table models (§6 data model).

Importing this package registers every table on ``SQLModel.metadata``.
"""

from app.models.brand import Brand
from app.models.cpu import CPU
from app.models.gpu import DiscreteGPU
from app.models.smartphone import Smartphone
from app.models.soc import SoC

__all__ = ["Brand", "SoC", "Smartphone", "DiscreteGPU", "CPU"]
