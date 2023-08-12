# This is the Doku for Tensorflow

# Set CUDA toolkit to enable Tensorflow to use the GPUs
https://www.tensorflow.org/install/gpu

# Load a classical dataset in a Tuple
```python
from typing import Tuple
import numpy as np
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist

# define method to import and preprocess data
def preprocess_data() -> tuple:
    (x_train, y_train),(x_test, y_test) = mnist.load_data()

    # Import x data and transform for usability
    x_train = x_train.astype(np.float32)
    x_train = np.expand_dims(x_train, axis=-1)
    x_test = x_test.astype(np.float32)
    x_test = np.expand_dims(x_test, axis=-1)
    # Dataset attributes
    num_classes = 10
    # Reshape y output data
    y_train = to_categorical(y_train, num_classes=num_classes, dtype=np.float32)
    y_test = to_categorical(y_test, num_classes.num_classes, dtype=np.float32)

    return (x_train, y_train),(x_test, y_test)

```

# Using the Keras API
## Modules to build a model
--TODO: define stuff as classes/methods  
Import from keras
``` python
from tensorflow.keras.layers import Activation  
from tensorflow.keras.layers import Dense  
from tensorflow.keras.models import Sequential
```

Example of a model building function using the add() method:  
* usually you would have a model with more layers
``` python
def build_model(num_features: int, num_targets: int) -> Sequential:
    # In the Sequential model class the output of a layer is the input of the next added layer.
    model = Sequential()
    # Add a hidden layer of n=units neurons
    model.add(Dense(units=500, input_shape=(num_features,)))
    # Add an activation layer after hidden layer (escential for learning non-linear problems)
    model.add(Activation("relu"))
    # Add output layer. For classification problems it would be a softmax function, which fits the predicted output to a probability [0,1] range.
    model.add(Activation("softmax"))
    # print model configuration
    model.summary()

    return model


```
### Model Types

Sequential
```python
from tensorflow.keras.models import Sequential
```
Model
```python
from tensorflow.python.keras.engine.training import Model
```

### Convolutional Neural Networks (CNN)
### Image filters and pooling
Import filters from keras
``` python
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Reshape

#Example of model with filters:
def build_model(num_features: int, num_targets: int) -> Sequential:

    #Add a 2D Convolutional filter with a given kernel_size and depth (num of filters)
    model.add(Conv2D(filters=16, kernel_size=3, input_shape=img_shape))


    #Still get some activation
    model.add(Activation("relu"))

    #Do some pooling to reduce dimensionality while keeping all information
    model.add(MaxPooling2D())

    #Add a second 2D convolutional filter
    model.add(Conv2D(filters=32, kernel_size=3))
    model.add(Activation("relu"))

    #Reduce again dimensionality
    model.add(MaxPooling2D())

    #Flatten to give a vector input to the output layer
    model.add(Flatten())

    #Output layer
    #Classify
    model.add(Dense(units=num_classes))
    model.add(Activation("softmax"))

    model.summary()

    return model
```

# Use the Model class to build a model
``` python
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D

from tensorflow.python.keras.engine.training import Model

def build_model(
    img_shape: Tuple[int, int, int],
    num_classes: int,
    optimizer: tf.keras.optimizers.Optimizer,
    learning_rate: float,
    filters_1: int,
    kernel_size_1: int,
    filters_2: int,
    kernel_size_2:int,
    filters_3:int,
    kernel_size_3:int,
    dense_layer_size: int
) -> Model:
    # in the model class the input has to be of type 'Input'
    input_img = Input(shape=img_shape)

    # follow the intuition of x as input and y as output
    x = Conv2D(filters=filters_1, kernel_size=kernel_size_1, padding="same")(input_img)
    x = Activation("relu")(x)
    x = Conv2D(filters=filters_1, kernel_size=kernel_size_1, padding="same")(x)
    x = Activation("relu")(x)
    x = MaxPooling2D()(x)

    x = Conv2D(filters=filters_2, kernel_size=kernel_size_2, padding="same")(x)
    x = Activation("relu")(x)
    x = Conv2D(filters=filters_2, kernel_size=kernel_size_2, padding="same")(x)
    x = Activation("relu")(x)
    x = MaxPooling2D()(x)

    x = Conv2D(filters=filters_3, kernel_size=kernel_size_3, padding="same")(x)
    x = Activation("relu")(x)
    x = Conv2D(filters=filters_3, kernel_size=kernel_size_3, padding="same")(x)
    x = Activation("relu")(x)
    x = MaxPooling2D()(x)

    x = Flatten()(x)
    x = Dense(units=dense_layer_size)(x)
    x = Activation("relu")(x)
    # output layer
    x = Dense(units=num_classes)(x)
    y_pred = Activation("softmax")(x)

    # create model object
    model = Model(
        inputs=[input_img],
        outputs=[y_pred]
    )

    opt = optimizer(learning_rate=learning_rate)

    # for cross validation we need to compile the model here
    model.compile(
        loss = "categorical_crossentropy",
        optimizer = opt,
        metrics=["accuracy"]
    )

    return model
```


## Training model

``` python
model.fit(
    x=x_train_,
    y=y_train_,
    epochs=10,
    batch_size=128,
    verbose=1,
    validation_data=(x_val_, y_val_),
    callbacks=[tb_callback]
)
```

# Using Tensorboard

Import tensorboard and os to write log files
``` python
import os
from tensorflow.keras.callbacks import TensorBoard
```
define dirs of the project where you are storing your models and logs
``` python
MODELS_DIR = os.path.abspath("/mnt/c/Users/ACUERVOD/Documents/udemy-tutos/tensorflow-tuto/models")
```
create if doesn't exist
``` python
if not os.path.exists(MODELS_DIR):
    os.mkdir(MODELS_DIR)
```

define file that will store the model in .h5 format
``` python
MODEL_FILE_PATH = os.path.join(MODELS_DIR, "mnist_model.h5")
```

define logs dir
``` python
LOGS_DIR = os.path.abspath("/mnt/c/Users/ACUERVOD/Documents/udemy-tutos/tensorflow-tuto/logs")
```
create of doesn't exist
``` python
if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)
```
define name of logs file
``` python
MODEL_LOG_DIR = os.path.join(LOGS_DIR, "mnist_model3")
```
define tensorboard callback object
``` python
tb_callback =  TensorBoard(
    log_dir = MODEL_LOG_DIR,
    write_graph=True
)
```

use tansorboard callback as input in model.fit() method
``` python
model.fit(
    x=x_train_,
    y=y_train_,
    epochs=10,
    batch_size=128,
    verbose=1,
    validation_data=(x_val_, y_val_),
    callbacks=[tb_callback]
)
```

### *****Open the Tensorboard
go to logs directory in the terminal
```
tensorboard --logdir=./
```

# Use callbacks and Tensorboard
Use case example:  
Prepare a learning_rate scheduler function and a extension of TensorBoard
``` python
import tensorflow as tf

# scheduler function to reduce leraning_rate of the optimimzer with the number of epochs
def lr_scheduler(epoch, lr) -> float:
    if epoch < 10:
        return lr
    else:
        return lr * tf.math.exp(-0.1 * epoch)

# create a modified TensorBoard that stores the learing_rate at the end of each epoch
class LRTensorBoard(tf.keras.callbacks.TensorBoard):
    def __init__(self, log_dir: str, **kwargs: dict) -> None:
        super().__init__(log_dir=log_dir, **kwargs)

    def on_epoch_end(self, epoch: int, logs:dict) -> None:
        logs.update({"learning_rate": self.model.optimizer.learning_rate.numpy()})
        super().on_epoch_end(epoch, logs=logs)
```
Implement the defined objects in the main code
``` python
from tf_utils.tf_callbacks import lr_scheduler
from tf_utils.tf_callbacks import LRTensorBoard

# call a self defined function [lr_scheduler] as a LearningRateScheduler callback
lrs_callback = LearningRateScheduler(
    schedule=lr_scheduler,
    verbose=1
)

# call the self expanded TensorBoard
lr_callback = LRTensorBoard(
    log_dir=model_log_dir,
    histogram_freq=0,
    profile_batch=0,
    write_graph=False
)

# pass the callbacks to the model training
model.fit(
    train_dataset,
    epochs=epochs,
    batch_size=batch_size,
    verbose=1,
    validation_data=val_dataset,
    callbacks=[lrs_callback, lr_callback] ######
)
```