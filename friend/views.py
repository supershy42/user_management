from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import send_friend_request, respond_to_friend_request, get_friends_list
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        try:
            send_friend_request(request.user, to_user_id)
            return Response({"message": "Friend request sent successfully"}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)


class RespondToFriendRequestView(APIView):
    def post(self, request):
        friend_request_id = request.data.get('friend_request_id')
        action = request.data.get('action')
        try:
            respond_to_friend_request(friend_request_id, action)
            return Response(
                {"message": f"Friend request {action}ed"},
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)


class FriendListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = get_friends_list(request.user)
        if not friends:
            return Response(
                {"message": "No friends found."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(friends, status=status.HTTP_200_OK)