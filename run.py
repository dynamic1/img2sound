from flask_script import Manager
from flask_cors import CORS

from api import create_app

app =  create_app('development')

# for Access-Control-Allow-Origin ( CORS - Cross-Origin Request)
CORS(app)

manager = Manager(app)

@manager.command
def migrate():

    #Migration script
    pass


if __name__ == "__main__":
    manager.run()
else:
    print("asdfasdfasdfg")

