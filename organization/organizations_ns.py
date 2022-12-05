from dataclasses import dataclass

from flask import request, jsonify, Response
from typing import List, Union, Tuple
from uuid import uuid4, UUID

from flask_restx import Resource, Namespace


organization_namespace = Namespace("organizations")


@dataclass
class Organization:
    name: str
    id: UUID
    service_account_email: str

    def __str__(self):
        return self.name


organizations: List[Organization] = []


@organization_namespace.route("/")
class OrganizationEndpoint(Resource):
    def post(self) -> Response:
        payload = request.json
        created_organization = Organization(
            name=payload.get("organization_name"),
            id=uuid4(),
            service_account_email=payload.get("service_account_email"),
        )

        organizations.append(created_organization)
        return jsonify(created_organization)

    def get(self) -> Response:
        return jsonify([organization.name for organization in organizations])


@organization_namespace.route("/<string:organization_id>")
class OrganizationIdEndpoint(Resource):
    def get(self, organization_id) -> Union[Response, Tuple[str, int]]:
        for organization in organizations:
            if organization.id == UUID(organization_id):
                return jsonify(organization)

        return f"Organization with uuid={organization_id} not found", 404
