from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import requests
import json
import pprint

app = Flask("meals")
api = Api(app)
dishes = dict()
parser = reqparse.RequestParser()

#test 
dishes = {
    234: {"first element": "test1",},
}

# global nextID #DEBUG - nextID must be initiated 
# TODO: 
# error handling
# combining multiple elements
# handle init of nextID with empty dict

class Dishes(Resource):
    # POST adds a dish of the given name. If successful, it returns the dish ID, a positive integer, and the code 201 (Resource successfully created).
    # POST may also return a non-positive ID
    def post(self):
        # Get the JSON request
        data = request.json
        #attempt to GET dish information from nutritional API
        query = data.get('name')
        nextID = max(int(id) for id in dishes.keys()) + 1
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, headers={'X-Api-Key': 'Igzod2YKnAdshNgN8f2ORQ==nxXDcDaEXB2TNq8U'})
        keys = ["name", "calories", "serving_size_g", "sodium_mg", "sugar_g"] 
        if response.status_code == requests.codes.ok: #not handling error correctly
            # response["ID"] = nextID
            dishes[nextID] = {key: response.json()[i][key] for key in keys for i in range(len(response.json()))}
            # dishes[nextID] = response.json()
            dishes[nextID]["ID"] = nextID
            print(dishes)
            # print(response.text) #DEBUGGING 
            # print(dishes) #DEBUGGING
            return 201
        else:
            print("Error:", response.status_code, response.text)

        return response.text
    # GET will return the JSON object listing all dishes, indexed by ID
    def get(self):
        print(dishes) #DEBUG
        return ""
    
    #Deleting all dishes not allowed
    def delete(self):
        return "This method is not allowed for the requested URL", 405

class Dish_ID(Resource):
    def get(self, id):
        if id in dishes:
            return dishes[id], 200
        else:
            return -5, 404
        
    def delete(self, id):
        if id in dishes:
            dishes.pop(id)
            return id, 200
        else:
            return -5, 404

class Dish_Name(Resource):
    def get(self, name):
        for id in dishes:
            if name in dishes[id]["name"]:
                return dishes[id]
        return ""
    def delete(self, name):
        return ""

class Meals(Resource):
    def post(self):
        return ""
    def get(self):
        return ""

class Meal(Resource):
    # /meals/{ID}
    def put(self, ID):
        return ""
    def get(self, ID):
        return ""
    def delete(self, ID):
        return ""
    
    # /meals/{name}
    def get(self, name):
        return ""
    def delete(self, name):
        return ""

api.add_resource(Dishes, '/dishes')
api.add_resource(Dish_ID, '/dishes/<int:id>')
api.add_resource(Dish_Name, '/dishes/<string:name>')
# api.add_resource(Meals, '/meals')
# api.add_resource(Meal, '/meals/<ID>')
# api.add_resource(Meal, '/meals/<name>')

if __name__ == '__main__':
    print("running meals.py")
    app.run(host='0.0.0.0', port=8000, debug=True)
