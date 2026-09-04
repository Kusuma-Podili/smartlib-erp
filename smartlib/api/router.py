"""RESTful HTTP Request Router and Dispatcher."""

import re
from typing import Dict, List, Tuple, Callable, Any, Optional
from dataclasses import dataclass, field


@dataclass
class RequestContext:
    method: str
    path: str
    path_params: Dict[str, str] = field(default_factory=dict)
    query_params: Dict[str, List[str]] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[Any] = None
    user_id: Optional[str] = None
    user_role: Optional[str] = None


@dataclass
class ApiResponse:
    status_code: int = 200
    headers: Dict[str, str] = field(default_factory=lambda: {"Content-Type": "application/json"})
    body: Any = None


@dataclass
class ApiRoute:
    method: str
    path_pattern: str
    handler: Callable[[RequestContext], ApiResponse]
    regex: re.Pattern
    param_names: List[str]
    summary: str = ""
    tags: List[str] = field(default_factory=list)


class ApiRouter:
    """Fast URL regex matcher and HTTP request dispatcher."""

    def __init__(self, prefix: str = "/api/v1"):
        self.prefix = prefix
        self.routes: List[ApiRoute] = []

    def add_route(self, method: str, path: str, handler: Callable[[RequestContext], ApiResponse],
                  summary: str = "", tags: Optional[List[str]] = None) -> ApiRoute:
        full_path = self.prefix + path
        param_names = re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", full_path)
        pattern_str = "^" + re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", r"(?P<>[^/]+)", full_path) + "$"
        compiled_regex = re.compile(pattern_str)

        route = ApiRoute(
            method=method.upper(),
            path_pattern=full_path,
            handler=handler,
            regex=compiled_regex,
            param_names=param_names,
            summary=summary,
            tags=tags or ["General"]
        )
        self.routes.append(route)
        return route

    def get(self, path: str, summary: str = "", tags: Optional[List[str]] = None):
        def decorator(f):
            self.add_route("GET", path, f, summary=summary, tags=tags)
            return f
        return decorator

    def post(self, path: str, summary: str = "", tags: Optional[List[str]] = None):
        def decorator(f):
            self.add_route("POST", path, f, summary=summary, tags=tags)
            return f
        return decorator

    def put(self, path: str, summary: str = "", tags: Optional[List[str]] = None):
        def decorator(f):
            self.add_route("PUT", path, f, summary=summary, tags=tags)
            return f
        return decorator

    def delete(self, path: str, summary: str = "", tags: Optional[List[str]] = None):
        def decorator(f):
            self.add_route("DELETE", path, f, summary=summary, tags=tags)
            return f
        return decorator

    def dispatch(self, ctx: RequestContext) -> ApiResponse:
        """Match and execute route handler."""
        for route in self.routes:
            if route.method != ctx.method.upper():
                continue
            match = route.regex.match(ctx.path)
            if match:
                ctx.path_params = match.groupdict()
                return route.handler(ctx)

        return ApiResponse(status_code=404, body={"error": "Not Found", "path": ctx.path})
