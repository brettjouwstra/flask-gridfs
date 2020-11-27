# flask-gridfs
Tiny Flask App running in a Docker container that saves uploaded files in MongoDB GridFS. 

### Authentication

The "password" set in the .env file must be passed in the headers using the "auth" key. 

Example:

headers = {"auth": "my_very_secret_string"}

### More Header Values

Any metadata associated with the file can be passed in the headers as well. Flask ignores a listing and then creates a dictionary out of the remain values. 
