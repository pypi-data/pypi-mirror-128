from flask import json
from apiflask import APIFlask, Schema, input, output, abort, HTTPTokenAuth, auth_required
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

TEST_TOKEN_VALUE = 'test'

app = APIFlask(__name__, json_errors=False)
app.description = '''
When you visit ths API documentation provided by Swagger UI at `/docs`.
You can click the "Authorize" button on the top right corner and fill
the test token value `test`. The `/token` endpoint also returns the test value.
'''

@app.errorhandler(404)
def not_found(e):
    return 'not found', 404


@app.error_processor
def my_auth_error_processor(error):
    body = {
        'error_message': error.message,
        'error_detail': error.detail,
        'status_code': error.status_code
    }
    return body, error.status_code, error.headers




auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token):
    if token == TEST_TOKEN_VALUE:
        return 'authorized user'


pets = [
    {'id': 0, 'name': 'Kitty', 'category': 'cat'},
    {'id': 1, 'name': 'Coco', 'category': 'dog'},
    {'id': 2, 'name': 'Flash', 'category': 'cat'}
]


class PetInSchema(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))


class PetOutSchema(Schema):
    id = Integer()
    name = String()
    category = String()


class TokenOutSchema(Schema):
    token = String()


@app.post('/token')
@output(TokenOutSchema)
def get_token():
    return {'token': TEST_TOKEN_VALUE}


@app.get('/')
def say_hello():
    return {'message': 'Hello!'}


@app.get('/pets/<int:pet_id>')
@auth_required(auth)
@output(PetOutSchema)
def get_pet(pet_id):
    if pet_id > len(pets) - 1 or pets[pet_id].get('deleted'):
        abort(404)
    return pets[pet_id]


@app.get('/pets')
@auth_required(auth)
@output(PetOutSchema(many=True))
def get_pets():
    return pets


@app.post('/pets')
@auth_required(auth)
@input(PetInSchema)
@output(PetOutSchema, 201)
def create_pet(data):
    pet_id = len(pets)
    data['id'] = pet_id
    pets.append(data)
    return pets[pet_id]


@app.patch('/pets/<int:pet_id>')
@auth_required(auth)
@input(PetInSchema(partial=True))
@output(PetOutSchema)
def update_pet(pet_id, data):
    if pet_id > len(pets) - 1:
        abort(404)
    for attr, value in data.items():
        pets[pet_id][attr] = value
    return pets[pet_id]


@app.delete('/pets/<int:pet_id>')
@auth_required(auth)
@output({}, 204)
def delete_pet(pet_id):
    if pet_id > len(pets) - 1:
        abort(404)
    pets[pet_id]['deleted'] = True
    pets[pet_id]['name'] = 'Ghost'
    return ''
