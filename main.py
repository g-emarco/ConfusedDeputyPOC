from flask import Flask
from flask_restx import Api

from organization.organizations_ns import organization_namespace
from security_scan.security_ns import recommendations_ns

app = Flask(__name__)
api = Api(app)


api.add_namespace(organization_namespace)
api.add_namespace(recommendations_ns)

# main driver function
if __name__ == "__main__":
    app.run()
