from rest_framework.generics import ListCreateAPIView
from TodoApp.serializers import TodoSerializer
from TodoApp.models import Todo
from rest_framework import status
from rest_framework.response import Response
from todo.response_format import CustomResponse
  
class TodoListCreateApiView(ListCreateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id', None)
        if id is not None and id != 0:
            try:
                result = self.get_queryset().filter(id=id, is_running=True).first()
            except Todo.DoesNotExist:
                return CustomResponse(None, status.HTTP_404_NOT_FOUND,"Todos doesn't exist.")
            serializer = self.get_serializer(result)
            if serializer.data == []:
                return CustomResponse(serializer.data, status.HTTP_404_NOT_FOUND)
            return CustomResponse(serializer.data, status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(self.get_queryset().filter(is_running=True), many=True)
            return CustomResponse(serializer.data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse(serializer.data, status.HTTP_201_CREATED)
        else:
            return CustomResponse(None, status.HTTP_400_BAD_REQUEST)
        

    def put(self, request, *args, **kwargs):
        id = self.kwargs.get('id', None)
        
        try:
            instance = self.get_queryset().get(id=id)
        except Todo.DoesNotExist:
            return CustomResponse(None, status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse(serializer.data, status.HTTP_201_CREATED)
        else:
            return CustomResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        id = self.kwargs.get('id', None)
        try:
            instance = self.get_queryset().get(id=id)
        except Todo.DoesNotExist:
            return CustomResponse(None, status.HTTP_404_NOT_FOUND)
        instance.delete()
        return CustomResponse(None,status.HTTP_204_NO_CONTENT)