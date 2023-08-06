# GrowPy

## Project Description

For questions and comments contact the developer directly at: <seilis@unbc.ca>.


## Installation
GrowPy is available through [PyPi](https://pypi.org/project/growpy/), and can be installed via `pip` using
```
pip install growpy
```
or 
```
pip3 install growpy
```

## Example Usage

```python
from growpy import models
import tensorflow as tf
import matplotlib.pyplot as plt

# Constuct/Import data
x = tf.abs(tf.random.uniform((100000,1), 0, 10))
y = 500 / (1 + (500-50)/50 * tf.exp(-0.5 * x))

# Construct model
model = models.GeneralizedLogistic()
optimizer = tf.keras.optimizers.Nadam()
loss = tf.keras.losses.MeanSquaredError()
model.compile(optimizer=optimizer, loss=loss)


# Train model
history = model.fit(x, y, epochs=100, batch_size=1000)

# Inspect results
print(model.weights)

fig, axes = plt.subplots(2, 1)
axes[0].scatter(x,y, alpha=0.5, s=1)
axes[0].scatter(x, model(x), alpha=0.5, s=1)
axes[0].set_ylabel('y')
axes[0].set_xlabel('x')

axes[1].plot(history.history['loss'])
axes[1].set_ylabel('MSE')
axes[1].set_xlabel('Epoch')
plt.show()
```

## License

BSD 3-Clause License

Copyright (c) 2021, Galen Seilis
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
