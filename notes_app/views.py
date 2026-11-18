
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from notes_app.serializers import RegisterSerializer, NotesSerializer, TaskSerializer

from notes_app.models import NotesDb, TaskDb

from rest_framework_simplejwt.tokens import RefreshToken

# USER REGISTRATION
class RegisterView(APIView):

    def post(self, request):
        serializer_instance = RegisterSerializer(data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save()

            return Response({
                "message": "User created successfully",
                "User_details": serializer_instance.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer_instance.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# LIST AND CREATE NOTES
class NotesListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # GET ALL NOTES OF LOGGED-IN USER
    def get(self, request):
        notes = NotesDb.objects.filter(user=request.user)

        serializer_instance = NotesSerializer(notes, many=True)

        return Response(
            serializer_instance.data,
            status=status.HTTP_200_OK
        )

    # CREATE A NOTE
    def post(self, request):
        serializer_instance = NotesSerializer(data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)

            return Response({
                "message": "Notes created successfully",
                "Notes_details": serializer_instance.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer_instance.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# DELETE USER ACCOUNT
class UserDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()

        return Response({
            "message": "User account deleted successfully"
        }, status=status.HTTP_200_OK)


# USER LOGOUT
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()

        return Response({
            "message": "Logout successful!"
        }, status=status.HTTP_200_OK)


# RETRIEVE, UPDATE AND DELETE PARTICULAR NOTE
class NotesDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # GET NOTE OBJECT
    def get_object(self, request, pk):
        return get_object_or_404(
            NotesDb,
            id=pk,
            user=request.user
        )

    # GET PARTICULAR NOTE
    def get(self, request, pk):
        note = self.get_object(request, pk)

        serializer = NotesSerializer(note)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # UPDATE NOTE
    def put(self, request, pk):
        note = self.get_object(request, pk)

        serializer = NotesSerializer(
            note,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Note updated successfully",
                "Note_details": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE PARTICULAR NOTE
    def delete(self, request, pk):
        note = self.get_object(request, pk)
        note.delete()

        return Response({
            "message": "Note deleted successfully"
        }, status=status.HTTP_200_OK)



#Task create and get
class  TaskListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        tasks=TaskDb.objects.filter(user=request.user)
        serializer_instance=TaskSerializer(tasks,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
            serializer_instance=TaskSerializer(data=request.data)
            if serializer_instance.is_valid():
                serializer_instance.save(user=request.user)
                return Response(data={
                    "message":"Task created successfully",
                    "Task_details" : serializer_instance.data})
            else:
                return Response(data=serializer_instance.errors)
            
# Task update retrieve delete          
class TasksDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_task(self, request, pk):
        return get_object_or_404(TaskDb, id=pk, user=request.user)


    def get(self, request, pk):
        task = self.get_task(request, pk)

        serializer_instance = TaskSerializer(task)

        return Response(serializer_instance.data, status=200)

    def put(self, request, pk):
        task = self.get_task(request, pk)

        serializer_instance = TaskSerializer(task, data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save()

            return Response({
                "message": "Task updated successfully",
                "Task_details": serializer_instance.data
            }, status=200)

        return Response(serializer_instance.errors, status=400)

    def delete(self, request, pk):
        task = self.get_task(request, pk)
        task.delete()

        return Response({
            "message": "Task deleted successfully"
        }, status=200)


# LOGOUT
class JWT_LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "message" : "Logout Successfull."
            })
        except Exception:
            return Response({
                "Error": "Invalid refresh token"
                })
    
# class JWT_LogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data.get('refresh')

#             if not refresh_token:
#                 return Response(
#                     {"Error": "Refresh token is required"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             return Response({
#                 "message": "Logout Successful."
#             }, status=status.HTTP_200_OK)

#         except Exception:
#             return Response(
#                 {"Error": "Invalid refresh token"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )