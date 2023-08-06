import torch
from torch import nn
from typing import Optional

import torchmasked.functional as F

__all__ = ['MaskedSoftmax']

class MaskedSoftmax(nn.Module):
    def __init__(self, dim: Optional[int] = None) -> None:
        super(MaskedSoftmax, self).__init__()
        self.dim = dim

    def __setstate__(self, state):
        self.__dict__.update(state)
        if not hasattr(self, 'dim'):
            self.dim = None

    def forward(self, input: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        return F.masked_softmax(input, mask, dim=self.dim, _stacklevel=5)

    def extra_repr(self) -> str:
        return 'dim={dim}'.format(dim=self.dim)
