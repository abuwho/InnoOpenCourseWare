from .views_imports import *

# Create a lesson
@swagger_auto_schema(method='POST', request_body=RequestCreateLessonSerializer, responses={201: ResponseCreateLessonSerializer()})
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def create_lesson(request):
    """
    Create a lesson.

    This endpoint is used to create a lesson. The user must be the instructor of the course.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The response containing the serialized created lesson.

    """
    data = request.data
    serialized = RequestCreateLessonSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        section = Section.objects.get(id=serialized.data.get("section"))
        course = section.course

        if course.instructor != request.user:
            return Response({"message": "Unauthorized: You are not the instructor of this course"}, status=401)
        
        lesson = Lesson(title=serialized.validated_data.get("title"), section=section,
                        type=serialized.validated_data.get("type"), pdf=serialized.validated_data.get("pdf"),
                        video_url=serialized.validated_data.get("video_url"), summary=serialized.validated_data.get("summary"))
        lesson.save()
        return Response(ResponseCreateLessonSerializer(lesson).data, status=201)
    
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)


# Update a lesson
@swagger_auto_schema(method='PUT', request_body=RequestUpdateLessonSerializer, responses={200: ResponseUpdateLessonSerializer()})
@api_view(['PUT'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def update_lesson(request):
    """
    Update a lesson.

    This endpoint is used to update a lesson. The user must be the instructor of the course.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The response containing the serialized updated lesson.

    """
    data = request.data
    serialized = RequestUpdateLessonSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        lesson = Lesson.objects.get(id=serialized.validated_data.get("id"))
        section = Section.objects.get(id=serialized.validated_data.get("section"))
        course = section.course
        if course.instructor != request.user:
            return Response({"message": "Unauthorized: You are not the instructor of this course"}, status=401)
        
        # Update the lesson
        if serialized.validated_data.get("title") is not None:
            lesson.title = serialized.validated_data.get("title")
        if serialized.validated_data.get("type") is not None:
            lesson.type = serialized.validated_data.get("type")
        if serialized.validated_data.get("pdf") is not None:
            lesson.pdf = serialized.validated_data.get("pdf")
        if serialized.validated_data.get("video_url") is not None:
            lesson.video_url = serialized.validated_data.get("video_url")
        if serialized.validated_data.get("summary") is not None:
            lesson.summary = serialized.validated_data.get("summary")
        lesson.save()
        return Response(ResponseUpdateLessonSerializer(lesson).data, status=200)

    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)



# Delete a lesson
@swagger_auto_schema(methods=['DELETE'], request_body=RequestDeleteLessonSerializer,
                     responses={200: {}, 400: {}})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lesson(request):
    """
    Delete a lesson.

    This endpoint is used to delete a lesson. The user must be the instructor of the course. 

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The response containing confirmation of deleting the lesson.
    
    """
    data = request.data
    serialized = RequestDeleteLessonSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)

        user = request.user
        lesson_id = serialized.data.get("lesson")

        lesson_object = Lesson.objects.get(id=lesson_id)
        section_object = lesson_object.section

        if user != section_object.course.instructor:
            raise ValueError("You are not the instructor of this course")

        lesson_object.delete()

        return Response({"message": "The lesson has been deleted"}, 200)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)