# torchmasked

Tensor operations with mask for PyTorch.

Sometimes you need to perform operations on tensors with the masked elements been ignored, for example:

```python
>>> input = torch.tensor([1., 2., 3.])
>>> result = torch.sum(input)
>>> print(result)

tensor(6.)

>>> mask = torch.tensor([1, 1, 0]).byte()
>>> masked_result = torchmasked.masked_sum(input, mask)
>>> print(masked_result)

tensor(3.)  # element input[2] is masked and ignored
```

Then this package could be helpful.


&nbsp;

## Installation

From source:

```bash
pip install git+https://github.com/Renovamen/torchmasked.git --upgrade

# or

python setup.py install
```


&nbsp;

## Supported Operations

- max (masked version of `torch.max`)
- min (`torch.min`)
- sum (`torch.sum`)
- mean (`torch.mean`)
- softmax (`torch.nn.functional.softmax` and `torch.nn.Softmax`)


&nbsp;

## License

[MIT](LICENSE)
