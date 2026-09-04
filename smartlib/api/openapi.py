"""OpenAPI 3.0.3 Specification Document Builder."""

import json
from typing import Dict, Any, List
from .router import ApiRouter


class OpenApiGenerator:
    """Extracts route specifications and schemas into standard OpenAPI 3.0.3 JSON."""

    def __init__(self, router: ApiRouter, title: str = "SmartLib ERP API", version: str = "1.0.0"):
        self.router = router
        self.title = title
        self.version = version

    def generate_spec(self) -> Dict[str, Any]:
        paths: Dict[str, Any] = {}
        for route in self.router.routes:
            p = route.path_pattern
            if p not in paths:
                paths[p] = {}

            method_lower = route.method.lower()
            parameters = []
            for pname in route.param_names:
                parameters.append({
                    "name": pname,
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"}
                })

            paths[p][method_lower] = {
                "summary": route.summary or f"{route.method} {p}",
                "tags": route.tags,
                "parameters": parameters,
                "responses": {
                    "200": {"description": "Successful operation"},
                    "400": {"description": "Bad Request"},
                    "404": {"description": "Resource Not Found"},
                    "500": {"description": "Internal Server Error"}
                }
            }

        return {
            "openapi": "3.0.3",
            "info": {
                "title": self.title,
                "version": self.version,
                "description": "Enterprise Library Resource Planning RESTful Hypermedia API"
            },
            "paths": paths,
            "components": {
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.generate_spec(), indent=indent)
