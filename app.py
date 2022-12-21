from flask import Flask
from flask_restx import Api

from organization.organizations_ns import (
    organization_namespace,
    recommendations_ns,
    organization_safe_namespace,
    recommendations_safe_ns,
)

app = Flask(__name__)
api = Api(app)

api.add_namespace(organization_namespace)
api.add_namespace(recommendations_ns)
api.add_namespace(organization_safe_namespace)
api.add_namespace(recommendations_safe_ns)

# main driver function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
