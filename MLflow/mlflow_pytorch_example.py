import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import mlflow
import mlflow.pytorch

# Define the model
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(28*28, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 10)

    def forward(self, x):
        x = x.to(dtype=torch.float32)
        x = x.view(-1, 28*28)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Function to train the model
def train_model(model, trainloader, criterion, optimizer, epochs):
    for epoch in range(epochs):
        running_loss = 0.0
        correct = 0
        total = 0
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data

            # Zero the parameter gradients
            optimizer.zero_grad()

            # Forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            # Calculate training accuracy
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        # Calculate average loss and accuracy for the epoch
        avg_loss = running_loss / len(trainloader)
        training_accuracy = 100 * correct / total
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.3f}, Accuracy: {training_accuracy:.2f}%")

        # Log the average loss and training accuracy for this epoch
        mlflow.log_metric("loss", avg_loss, step=epoch)
        mlflow.log_metric("training_accuracy", training_accuracy, step=epoch)


# Function to evaluate the model
def evaluate_model(model, testloader):
    correct = 0
    total = 0
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f"Accuracy of the network on the test images: {accuracy:.2f}%")
    return accuracy

# Main function to run the experiment
def run_experiment(experiment_name="Default", epochs=2, learning_rate=0.001, batch_size=32):
    # Set the experiment name in MLflow
    mlflow.set_experiment(experiment_name)

    # Start the MLflow run
    with mlflow.start_run():
        # Log hyperparameters
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("batch_size", batch_size)

        # Prepare the dataset
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
        trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
        trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True)

        testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)
        testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False)

        # Initialize the model, loss function, and optimizer
        model = SimpleNN()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)

        # Train the model
        train_model(model, trainloader, criterion, optimizer, epochs)

        # Evaluate the model
        accuracy = evaluate_model(model, testloader)

        # Log metrics
        mlflow.log_metric("test accuracy", accuracy)

        # Log the model
        mlflow.pytorch.log_model(model, "model")
        

if __name__ == "__main__":
    # Example: Run experiment with specific parameters
    epochs = [10, 20, 30, 40]
    learning_rates = [0.01, 0.001, 0.001]
    batch_sizes = [8, 16, 32, 64]
    for epoch in epochs:
        for lr in learning_rates:
            for batch in batch_sizes:
                
                run_experiment(experiment_name="MNIST_Classification_expirement1", epochs=epoch, learning_rate=lr, batch_size=batch)
