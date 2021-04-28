#Flask - make a object of the needed information about the System, - Name of Object, Quantity, Location , Date,  Description(if needed)
#Create in the html a table , with a plus button that adds all this info down below, and adds it into the table.
#Add a edit button.
from flask import Flask, render_template,request
from flask_cors import CORS
from mongoengine import *
import datetime
import uuid
connect('mydb')
class Warehouse(Document):
    name = StringField(max_length=30,required=True)
    quantity= StringField(max_length=6,required=True)
    location = StringField(max_length=30,required=True)
    date = StringField(max_length=30,required=True)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

def Save(name,quantity,location,date):
    info = Warehouse(name = name,quantity= quantity,location=location,date=date)
    info.save()


def Waretable(warehouse):
    return{
        "id": str(uuid.uuid4()),
        "name": warehouse.name,
        "quantity": warehouse.quantity,
        "date": warehouse.date,
        "location" : warehouse.location,
    }


app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    listdict = []
    for item in Warehouse.objects:
        listdict.append(Waretable(item))
    return {"data":listdict}

@app.route("/newdata",methods=['POST'])
def prase_request():
    data = request.json
    Save(data["name"],data["quantity"],data["location"],data["date"])
    return(data)

if __name__ == "__main__":
    app.run()


