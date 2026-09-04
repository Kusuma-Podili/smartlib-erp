"""JSON:API (v1.1) and HAL (Hypertext Application Language) Serializers."""

from typing import Dict, Any, List, Optional


class JsonApiSerializer:
    """Formats resources in accordance with the JSON:API v1.1 specification."""

    @staticmethod
    def serialize_resource(type_name: str, resource_id: str, attributes: Dict[str, Any],
                           relationships: Optional[Dict[str, Any]] = None, links: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        data = {
            "type": type_name,
            "id": str(resource_id),
            "attributes": attributes
        }
        if relationships:
            data["relationships"] = relationships
        if links:
            data["links"] = links
        return {"data": data}

    @classmethod
    def serialize_collection(cls, type_name: str, items: List[Dict[str, Any]],
                             id_key: str = "id", self_url: str = "") -> Dict[str, Any]:
        data_list = []
        for item in items:
            item_copy = dict(item)
            res_id = str(item_copy.pop(id_key, "0"))
            data_list.append({
                "type": type_name,
                "id": res_id,
                "attributes": item_copy
            })
        result = {"data": data_list}
        if self_url:
            result["links"] = {"self": self_url}
        return result


class HalSerializer:
    """Formats resources using HAL hypermedia link relations (_links, _embedded)."""

    @staticmethod
    def serialize(resource_dict: Dict[str, Any], self_href: str,
                  extra_links: Optional[Dict[str, str]] = None,
                  embedded: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        hal = dict(resource_dict)
        links = {"self": {"href": self_href}}
        if extra_links:
            for rel, href in extra_links.items():
                links[rel] = {"href": href}
        hal["_links"] = links
        if embedded:
            hal["_embedded"] = embedded
        return hal
