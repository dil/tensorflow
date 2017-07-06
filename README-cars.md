===Setup cars TensorFlow model for mobile===

`deep-thought` machine in DiUS HQ retrains a pre-trained TensorFlow model (Inception).

First, copy the retrained model files (`output_graph.pb` and `output_labels.txt`) from `deep-thought` machine into `./cars/tf_files/`.

Then, run:
```
docker run --rm -v `pwd`:/tensorflow -w /tensorflow tensorflow/tensorflow ./setup_cars_tf_model_for_mobile.sh
```

This optimizes the model for usage on mobiles and copies into `cars/android/assets`.


