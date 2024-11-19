# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializer import BookSerializer
# Create your views here.



@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializedData = BookSerializer(books, many=True).data
    # print("========",BookSerializer(books, many=True),"==========")
    return Response(serializedData)

@api_view(['POST'])
def create_book(request):
    data=request.data
    # print("-----",request,"-----")
    serializer = BookSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        print("created")
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "DELETE"])
def book_detail(request, pk):
    try:
        # Fetch the book by primary key (ID)
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        # If the book is not found, return 404 error
        return Response({"message": "Book not found!"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        # Handle DELETE request: delete the book
        book.delete()
        return Response({"message": "Book deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        data=request.data
        # Handle PUT request: update the book
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)