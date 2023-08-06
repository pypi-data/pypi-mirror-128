<p align="center">
  <a href="https://www.classiq.io"><img src="https://uploads-ssl.webflow.com/60000db7a5f449af5e4590ac/6122b22eea7a9583a5c0d560_classiq_RGB_Green_with_margin.png
" alt="Classiq"></a>
</p>
<p align="center">
    <em>The Classiq Quantum Algorithm Design platform helps teams build sophisticated quantum circuits that could not be designed otherwise</em>
</p>


We do this by synthesizing high-level functional models into optimized quantum circuits, taking into account the
constraints that are important to the designer. Furthermore, we are able to generate circuits for practically any
universal gate-based quantum computer and are compatible with most quantum cloud providers.

## Requirements
Python 3.8+


## Installation
```console
pip install --upgrade pip
$ pip install 'classiq[all]'
```

## Example

```python
from classiq import generator
from classiq_interface.generator.state_preparation import (
    StatePreparation,
    PMF,
    StatePreparationOutputs,
    Metrics,
    NonNegativeFloatRange,
)
from classiq_interface.generator.qft import QftInputs, QFT

probabilities = (0.5, 0.1, 0.2, 0.005, 0.015, 0.12, 0.035, 0.025)
pmf = PMF(pmf=probabilities)
sp_params = StatePreparation(
    probabilities=pmf,
    num_qubits=4,
    error_metric={Metrics.KL: NonNegativeFloatRange(upper_bound=0.3)},
)

circuit_generator = generator.Generator(qubit_count=20, max_depth=100)
output_dict = circuit_generator.StatePreparation(params=sp_params)

state_preparation_output = output_dict[StatePreparationOutputs.OUT]

qft_params = QFT(num_qubits=3)
circuit_generator.QFT(
    params=qft_params, in_wires={QftInputs.IN: state_preparation_output}
)

circuit = circuit_generator.generate()
circuit.show()
```

## License
See [license](https://classiq.io/license).
