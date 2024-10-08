from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def create_and_get_all_users(request):
    if request.method == 'GET':
        print("fetching all users")
        
        # Access query parameters
        param1 = request.query_params.get('param1')  # Example: /api/users/?param1=value
        param2 = request.query_params.get('param2')  # Example: /api/users/?param2=value
        print(param1, param2)

        person = [{"name": "danish", "email": "danish@gmail.com"}]
        return Response(person)
    elif request.method == 'POST':
        print("creating new user")

        # Access JSON input
        data = request.data  # Data will contain parsed JSON
        value1 = data.get('key1')
        value2 = data.get('key2')
        print(value1, value2)

        person = [
            {"name": "danish", "email": "danish@gmail.com"},
            {"name": "fahad", "email": "fahad@gmail.com"}
        ]
        return Response(person)