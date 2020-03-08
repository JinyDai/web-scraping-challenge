from flask import Flask, render_template, redirect
import pymongo
import scrap_mars

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db=client.misson_db
mars=db.mars

@app.route("/")
def home():
  # Find one record of data from the mongo database
  mars_info = mars.find_one()
  # Return template and data
  return render_template("index.html",mars_data=mars_info)

@app.route("/scrape")
def scrape():
  mars_data=scrap_mars.scrape()
  
  mars.update({}, mars_data, upsert=True)
  # Redirect back to home page
  return redirect("/")

if __name__ =="__main__":
  app.run(debug=True)
