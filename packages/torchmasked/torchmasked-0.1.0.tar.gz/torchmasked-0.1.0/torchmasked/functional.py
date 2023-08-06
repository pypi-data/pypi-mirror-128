import torch
import torch.nn.functional as F
from torch.types import _dtype as DType
from typing import Any, Callable, Optional

__all__ = [
    'masked_softmax',
    'masked_sum',
    'masked_mean',
    'masked_max',
    'masked_min'
]

def _fill_with_mask(input: torch.Tensor, mask: torch.Tensor, fill_value) -> torch.Tensor:
    inverted_mask = (1.0 - mask.float()).bool()
    return input.masked_fill(inverted_mask, fill_value)

def _call_torch(func: Callable, **kwargs) -> Any:
    if kwargs["dim"] is None:
        kwargs.pop("dim")
        kwargs.pop("keepdim")
    return func(**kwargs)

def masked_softmax(
    input: torch.Tensor,
    mask: torch.Tensor,
    dim: Optional[int] = None,
    _stacklevel: int = 3,
    dtype: Optional[DType] = None
) -> torch.Tensor:
    if mask is None:
        return F.softmax(input, dim=dim, _stacklevel=_stacklevel, dtype=dtype)

    masked_input = _fill_with_mask(input, mask, -float('inf'))
    return F.softmax(masked_input, dim=dim, _stacklevel=_stacklevel, dtype=dtype)

def masked_sum(
    input: torch.Tensor,
    mask: torch.Tensor,
    dim: Optional[int] = None,
    keepdim: bool = False,
    dtype: Optional[DType] = None
) -> torch.Tensor:
    if mask is None:
        return _call_torch(input.sum, dim=dim, keepdim=keepdim, dtype=dtype)

    masked_input = _fill_with_mask(input, mask, 0.)
    return _call_torch(masked_input.sum, dim=dim, keepdim=keepdim, dtype=dtype)

def masked_mean(
    input: torch.Tensor,
    mask: torch.Tensor,
    dim: Optional[int] = None,
    keepdim: bool = False,
    dtype: Optional[DType] = None
) -> torch.Tensor:
    if mask is None:
        return _call_torch(input.mean, dim=dim, keepdim=keepdim, dtype=dtype)

    mask_sum = _call_torch(mask.float().sum, dim=dim, keepdim=keepdim)
    mask_sum = mask_sum.clamp(min=1.).to(dtype)

    return masked_sum(input, mask, dim, keepdim, dtype) / mask_sum

def masked_max(
    input: torch.Tensor,
    mask: torch.Tensor,
    dim: Optional[int] = None,
    keepdim: bool = False
) -> torch.Tensor:
    if mask is None:
        return _call_torch(input.max, dim=dim, keepdim=keepdim)

    masked_input = _fill_with_mask(input, mask, -float('inf'))
    return _call_torch(masked_input.max, dim=dim, keepdim=keepdim)

def masked_min(
    input: torch.Tensor,
    mask: torch.Tensor,
    dim: Optional[int] = None,
    keepdim: bool = False
) -> torch.Tensor:
    if mask is None:
        return _call_torch(input.min, dim=dim, keepdim=keepdim)

    masked_input = _fill_with_mask(input, mask, float('inf'))
    return _call_torch(masked_input.min, dim=dim, keepdim=keepdim)
