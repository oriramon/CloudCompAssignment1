from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import requests
import json
import pprint

app = Flask("meals")
api = Api(app)
dishes = dict()
meals = dict()
parser = reqparse.RequestParser()

#test 
dishes = {
    1: {"name": "apple", "ID": 1, "cal": 2, "size": 34.0, "sodium": 70, "sugar": 8},
    2: {"name": "focaccia", "ID": 2, "cal": 9, "size": 100.0, "sodium": 570, "sugar": 1.8},
    3: {"name": "Chicken", "ID": 3, "cal": 1, "size": 10.0, "sodium": 20, "sugar": 3},
}

#test
meals = {
    1: {"name": "chicken special", 
    "ID": 1,
    "appetizer": 3,
    "main": 2,
    "dessert": 1,
    "cal": 12,
    "sodium": 660,
    "sugar": 12.8},

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

        try:
            nextID = max(int(id) for id in dishes.keys()) + 1
        except:
            nextID = 1

        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, headers={'X-Api-Key': 'Igzod2YKnAdshNgN8f2ORQ==nxXDcDaEXB2TNq8U'})
        keys = {"name": "name", "calories": "cal", "serving_size_g": "size", "sodium_mg": "sodium", "sugar_g": "sugar"}
        if response.status_code == requests.codes.ok: #not handling error correctly
            # response["ID"] = nextID
            dishes[nextID] = {val: response.json()[i][key] for key, val in keys for i in range(len(response.json()))}
            # dishes[nextID] = response.json()
            dishes[nextID]["ID"] = nextID
            print(dishes)
            # print(response.text) #DEBUGGING 
            # print(dishes) #DEBUGGING
            return nextID, 201
        else:
            print("Error:", response.status_code, response.text)

        return response.text
    # GET will return the JSON object listing all dishes, indexed by ID
    def get(self):
        return dishes
    
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
        for i in dishes:
            if name in dishes[i].values():
                return dishes[i], 200
        return -5, 404
    
    def delete(self, name):
        for i in dishes:
            if name in dishes[i].values():
                dishes.pop(i)
                return i, 200
        return -5, 404

class Meals(Resource):
    def post(self):
         # Get the JSON request
        try:
            data = request.json
        
        # If request content-type is not application/json
        except:
            return 0, 415
        
        # Check if meal exists
        for i in meals:
            if data.get('name') == meals[i]["name"]:
                return -2, 422
            
        #attempt to GET dish information 
        try:
            appetizer = int(data.get('appetizer'))
            main = int(data.get('main'))
            dessert = int(data.get('dessert'))
        
        # One of the required parameters was not given or not specified correctly
        except:
            return -1, 422
        
        # If there are no issues add the meal
        if appetizer in dishes.keys() and main in dishes.keys() and dessert in dishes.keys():
            try:
                nextID = max(int(id) for id in meals.keys()) + 1
            except:
                nextID = 1
            meals[nextID] = data
            meals[nextID]["ID"] = nextID
            meals[nextID]["cal"] = float(dishes[appetizer]["cal"]) + float(dishes[main]["cal"]) + float(dishes[dessert]["cal"])
            meals[nextID]["sodium"] =  float(dishes[appetizer]["sodium"]) + float(dishes[main]["sodium"]) + float(dishes[dessert]["sodium"])
            meals[nextID]["sugar"] = float(dishes[appetizer]["sugar"]) + float(dishes[main]["sugar"]) + float(dishes[dessert]["sugar"])
            print(meals) #FOR DEBUGGING
            return nextID, 201
        
        # If one of the sent dishes does not exists
        else:
            return -6, 422
    
    def get(self):
        return meals

class Meal_ID(Resource):
    # /meals/{ID}
    def put(self, id):
        if id in meals:
                # Get the JSON request
            try:
                data = request.json
            
            # If request content-type is not application/json
            except:
                return 0, 415
            
            # Check if the id matches the name
            if data.get('name') != meals[id]['name']:
                    return -2, 422
                
            #attempt to GET dish information 
            try:
                appetizer = int(data.get('appetizer'))
                main = int(data.get('main'))
                dessert = int(data.get('dessert'))
            
            # One of the required parameters was not given or not specified correctly
            except:
                return -1, 422
            
            # If there are no issues add the meal
            if appetizer in dishes.keys() and main in dishes.keys() and dessert in dishes.keys():
                meals[id] = data
                meals[id]["ID"] = id
                meals[id]["cal"] = float(dishes[appetizer]["cal"]) + float(dishes[main]["cal"]) + float(dishes[dessert]["cal"])
                meals[id]["sodium"] =  float(dishes[appetizer]["sodium"]) + float(dishes[main]["sodium"]) + float(dishes[dessert]["sodium"])
                meals[id]["sugar"] = float(dishes[appetizer]["sugar"]) + float(dishes[main]["sugar"]) + float(dishes[dessert]["sugar"])
                print(meals) #FOR DEBUGGING
                return id, 201
            
            # If one of the sent dishes does not exists
            else:
                return -6, 422
        return "Error: no such id exists", 422
    
    def get(self, id):
        if id in meals:
            return meals[id], 200
        else:
            return -5, 404
        
    def delete(self, id):
        if id in meals:
            meals.pop(id)
            return id, 200
        else:
            return -5, 404

class Meal_Name(Resource):    
    # /meals/{name}
    def get(self, name):
        for id in meals:
            if meals[id]["name"] == name:
                return meals[id], 200
        return -5, 404
    def delete(self, name):
        for id in meals:
            if meals[id]["name"] == name:
                meals.pop(id)
                return id, 200
        return -5, 404

api.add_resource(Dishes, '/dishes')
api.add_resource(Dish_ID, '/dishes/<int:id>')
api.add_resource(Dish_Name, '/dishes/<string:name>')
api.add_resource(Meals, '/meals')
api.add_resource(Meal_ID, '/meals/<int:id>')
api.add_resource(Meal_Name, '/meals/<string:name>')

if __name__ == '__main__':
    print("running rest-word-svr-v1.py")
    app.run(host='0.0.0.0', port=8000, debug=True)
