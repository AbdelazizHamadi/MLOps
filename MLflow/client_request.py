import numpy as np
import requests
import json
import torch 
import torchvision
import torchvision.transforms as transforms

# Define the number of images in the batch
batch_size = 16

# Generate a random batch of 28x28 grayscale images (like MNIST format)
images = torch.zeros((batch_size, 28, 28), dtype=torch.float32)

# flatten the tensor and convert to list 
instances = [torch.flatten(image).tolist() for image in images]

# Prepare the payload as a JSON object with the "instances" key
payload = json.dumps({"instances": instances})

# Define the URL of the MLflow model server
# after running : mlflow models serve -m mlruns/experimentID/runID/artifacts/model -p 4545 --no-conda

url = "http://127.0.0.1:4545/invocations"

# Send the POST request with the payload
response = requests.post(url, data=payload, headers={"Content-Type": "application/json"})

# Assume response.json() gives you the prediction in string format
predictions = response.json()

# results will be (batch_size, 10)
_, predicted_labels = torch.max(torch.tensor(predictions["predictions"]), 1)

print(f"predicted_labels: {predicted_labels}")

