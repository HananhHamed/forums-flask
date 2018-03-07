from flask import Flask
from  app import dummy_data, stores


app = Flask(__name__)

member_store = stores.MemberStore()
post_store = stores.PostStore()

from app import views

if __name__  == "__main__":
    dummy_data.seed_stores(member_store, post_store)
    app.run()


