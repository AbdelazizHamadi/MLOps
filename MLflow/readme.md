## MLflow / pytorch
In this repo you will find

### Training 
A simple CNN trained on MNIST dataset. the use case here is to try multiple combination of hyperparams (epochs, learning rate and batch size) and get the best hyperparams combination 
```console
pip install -r requirements.txt

python3 mlflow_pytorch_example.py
```
  
### Deploying 
Deploying it using for example: port 4545 and run it on the current enviroment (requirements.txt) with --no-conda command

```console
mlflow models serve -m mlruns/experimentID/runID/artifacts/model -p 4545 --no-conda
```

and then launch 
```console
python3 client_request.py
```

## Results 
Here's some screenshots that show the ~98% on testing set and ~99% on training set (you can obtain better results by playing with other parameters )

![pic 1](resources/mlf1.jpg)
![pic 3](resources/mlf3.png)
![pic 2](resources/mlf2.jpg)


