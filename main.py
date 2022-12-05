from flask import Flask
from flask_restx import Api, Namespace

from organization.organizations_ns import organization_namespace

app = Flask(__name__)
api = Api(app)


api.add_namespace(organization_namespace)


# main driver function
if __name__ == "__main__":
    app.run()
