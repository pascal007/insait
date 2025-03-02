from resources.GeneratedTextResource import GeneratedTextResource, GeneratedTextResourceById
from resources.UserResource import CreateUserResource, LoginUserResource


def initialize_routes(api):
    api.add_resource(CreateUserResource, '/register')
    api.add_resource(LoginUserResource, '/login')
    api.add_resource(GeneratedTextResourceById, '/generated-text/<uuid:prompt_id>')
    api.add_resource(GeneratedTextResource, '/generated-text')
