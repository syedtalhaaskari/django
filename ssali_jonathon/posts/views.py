from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

data = [
    {
        "id": 1,
        "message": "Hello World 1!",
    },
    {
        "id": 2,
        "message": "Hello World 2!",
    },
    {
        "id": 3,
        "message": "Hello World 3!",
    }
]

@api_view(http_method_names=['GET', 'POST'])
def homepage(request: Request):
    if request.method == 'POST':
        request_data = request.data
        data.append({
            "id": len(data) + 1,
            "message": request_data.get('message')
        })
        return Response(data=request_data, status=status.HTTP_201_CREATED)
 
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(http_method_names=["GET"])
def list_posts(request: Request):
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(http_method_names=['GET'])
def post_details(request: Request, post_index: int):
    if post_index >= len(data) or post_index < 0:
        return Response(data={"error": "Post Not Found"}, status=status.HTTP_404_NOT_FOUND)

    post = data[post_index]

    if post:
        return Response(data=post, status=status.HTTP_200_OK)
    