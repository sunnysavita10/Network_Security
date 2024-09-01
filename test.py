
'''from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://snshrivas:Snshrivas@cluster0.u141hkk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)'''
    
    
import mlflow

x,y=75,10
z=x+y
#tracking the experiment with the mlflow

with mlflow.start_run():
    mlflow.log_param("x",x)
    mlflow.log_param("y",y)
    mlflow.log_metric("z",z)

print(z)
print("sunny")