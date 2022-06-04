from starlette.routing import Route

from server.api.rooms.endpoints import List, Create, Join

rooms_routes = [
    Route("/my", List),
    Route('/create', Create),
    Route('/{id}/join', Join)

]
