import json
from flask import Flask, abort, request
from about_me import me
from mock_data import catalog
from config import db
from bson import ObjectId
from dns import resolver

app = Flask('class2python')


@app.route("/", methods=['GET'])  # root
def home():
    return "This is the home page"

# Create an about endpoint and show your name


@app.route("/about")
def about():
    return me["first"] + " " + me["last"]


@app.route("/myaddress")
def address():
    return f'{me["address"]["street"]} {me["address"]["number"]}'

 ########################################################### API ENDPOINTS################################################################################################################################

 # Postman -> Test endpoints of REST APIs


@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    results = []
    cursor = db.products.find({})  # get all data from the collection

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)

# POST Method to create new products


@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()
    db.slapme.insert_one(product)

    product["_id"] = str(product["_id"])

    return json.dumps(product)


@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    cursor = db.products.find({})
    # Here... count how many products are in the list catalog
    num_items = 0 
    for prod in cursor:
        num_items += 1
    return json.dumps(num_items)
# Request 127.0.0.1:5000/api/product/


@app.route("/api/product/<id>", methods=["GET"])
def get_product(id):
    # find the product whose _id is equal to id
    # catalog
    for prod in catalog:
        if prod["_id"] == id:
            return json.dumps(prod)

    return abort(404, "Id does not match any product")

    # travel catalog with for loop
    # Get the product inside the list
    # if the _id of the product is equal to th id variable
    # found it, return that product as json


# Create an endpoint that returns the sum of all the products' price
# GET /api/catalog/total
# @app.route('/api/catalog/total', methods=['GET'])
@app.get("/api/catalog/total")
def get_total():
    total = 0
    cursor = db.products.find({})
    for prod in cursor:
        # total = total + prod["price"]
        total += prod["price"]

    return json.dumps(total)

# get product by category
# get /api/products/<category>


@app.get("/api/products/<category>")
def products_by_category(category):
    results = []
    cursor = db.products.find({"category": category})
    for prod in cursor:
        prod["_id"].lower() == str(prod["_id"])
        results.append(prod)

    return json.dumps(results)

# get the list of categories
# get /api/categories


@app.get("/api/categories")
def get_unique_categories():
    cursor = db.products.find({})
    results = []
    for prod in catalog:
        cat = prod["category"]
        # if cat does not exist in results, then
        if not cat in results:
            results.append(cat)

    return json.dumps(results)

    # get the cheapest product


@app.get("/api/product/cheapest")
def get_cheapest_product():
    cursor = db.products.find({})
    solution = cursor[0]
    for prod in cursor:
        if prod["price"] < solution["price"]:
            solution = prod

    solution["_id"] = str(solution["_id"])
    return json.dumps(solution)


app.run(debug=True)
