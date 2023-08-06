### Important info
1. Django superuser (admin):
```json
{
  "username": "qustodio", 
  "password": "pyday123"
}
```
2. Repo with the common grpc code (pb2):
   1. [Link](https://pypi.org/project/qservices-library)
   2. Package installation: `pip install qservices-library`

### How to create all the boilerplate code for a gRPC model
1. Create the proto model:
```bash
# Needs to be in the container to have access 
# to the proper tools and paths
docker-compose run catalog python manage.py generateproto 
--model catalog.models.Book --fields=id,title,author --file book.proto
```
2. Copy&Paste the generated proto-model (from previous step) into _protobufs/catalog/book.proto_
3. Change the package name in book.proto (line 3) to catalog.
4. Create the gRPC model code (pb2):
```bash
python -m grpc_tools.protoc --proto_path=protobufs 
--python_out=common/pb2 --grpc_python_out=common/pb2 ./protobufs/catalog/book.proto
```
7. Create the serializer class BookProtoSerializer (in catalog/catalog/serializers.py)
8. Create the service class BookService (in catalog/catalog/services.py)
9. Register the service in the grpc handler (in catalog/catalog/handlers.py)
```bash
book_pb2_grpc.add_BookControllerServicer_to_server(
    BookService.as_servicer(), 
    server
)
```


### Create DB service (docker compose local)
- Create DB service
    - Use the desired docker image for the DB
    - Include service to the network
    - Use environment variables to config container (should be in the image's documentation):
        - Username
        - Password
        - Db name
- Change django settings to use the container as the database
    - Use credentials set on the container
    - Use the db service as the database hostname

