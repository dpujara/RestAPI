from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT,jwt_required
from security import authenticate,identity

app = Flask(__name__)
app.secret_key = 'dhaval'
api = Api(app)

jwt = JWT(app,authenticate,identity) #This creates a new end point /auth

items = []



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type = float,
    required = True,
    help = "This field can not be blank"
    )

    @jwt_required()
    def get(self,name):
        item = next(filter(lambda x: x['name'] == name,items),None) #None is a default value #It will return first item with name from the items. Next can raise an error if there are no items left in the list
        return {'item': item } , 200 if item else 404

    def post(self,name):

        if next(filter(lambda x: x['name'] == name,items),None) is not None:
            return {'message' : "an item with name '{}' alredy exists".format(name)},400 #bad request
        data = Item.parser.parse_args() #Error first approach
        item = {'name' : name,'price':data['price']}
        items.append(item)
        return item,201

    @jwt_required
    def delete(self,name):
        global items
        items = list(filter(lambda x : x['name'] != name , items))
        return {'message' : 'Item deleted'}

    def put(self,name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x : x['name'] == name,items),None)
        if item is None:
            item = {'name' : name , 'price' : data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items':items}

api.add_resource(Item,'/item/<string:name>') #http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList,'/items')
app.run(port = 5000,debug = True)
