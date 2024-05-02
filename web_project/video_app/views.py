from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Video, User
from .serializers import VideoSerializer
from django.shortcuts import render, get_object_or_404
from .models import Video
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import VideoForm
from django.http import JsonResponse
from django.core import serializers
import cv2, threading
from django.http import StreamingHttpResponse


# def requestSessionInitializedChecker(request):
#     """Function to initialize request sessions if they don't exist."""

#     # Try except for KeyError
#     try:
#         pass
#     except:
#         # Initialize request variables if they don't exist
#         request.session['isLoggedIn'] = False
#         request.session['username'] = ""
#         request.session['Name'] = ""
#     return request

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    def list(request):
        # Fetch all videos from the queryset
        videos = Video.objects.all()
        # videos_json = serializers.serialize('json', videos)
        data = [{'name': video.name, 'url': video.video_url} for video in videos]
        # Render the HTML template with the videos data
        # data = {
        #     'videos' : video_list,
        # }
        # render(request, 'index.html', {'videos': videos})
        # , JsonResponse(data, safe=False)
        return render(request, 'index.html', {'videos': videos, 'data' : data})

def stream_video(request,video_id):
    # Implement video streaming using OpenCV
    # Each video should be assigned a separate thread
    # videos = Video.objects.all()
    # video = get_object_or_404(Video, pk=video_id)
    video = Video.objects.get(pk=video_id)
    video_file = video.video_file
    # video_path = video_url
    # video_file = request.FILES.get('video_file')
    video_play  = '/web_project/' + str(video_file)
    cap = cv2.VideoCapture(video_play)


    # Function to generate video frames
    def generate_frames():
        while cap.isOpened():
            ret, frame = cap.read()     
            if not ret:
                break
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # Set response headers
    headers = {
        'Content-Type': 'multipart/x-mixed-replace; boundary=frame'
    }
    # generate_frames()
    # Return streaming HTTP response
    StreamingHttpResponse(generate_frames(), headers=headers) 
    return render(request,'index.html', {'video_play': video_play})
    #  content_type='multipart/x-mixed-replace; boundary=frame'
    # return render(request, 'index.html', {'video': video})

    
    # Implement streaming logic
   
    # Open video file

# Threading for video_stream    

def backgroundtaskForVideo():
    videoThread = threading.Thread(target=stream_video)
    videoThread.daemon = True
    videoThread.start()



def search_videos(request):
    if request.method == 'POST':
        videos = Video.objects.all()
        query = request.GET.get('query')
        searchQuery = request.POST["searchQuery"]
        videos = Video.objects.filter(name__icontains=searchQuery)
        return render(request, 'index.html', {'videos': videos, 'query': query})
    
def delete_video(request, video_id):
    # video = get_object_or_404(Video, id=video_id)
   
    if request.method == 'GET':
        video = Video.objects.get(pk=video_id)
        # videoFile= video.video_file
        video.delete()
        return redirect('videoviewlist')
    else:
        return render(request, 'index.html', {'video': video})



def upload_video(request):
    if request.method == 'POST':
        #  image_file = request.FILES.get('video_file')
        #  videoobj = Video.objects.get()
        #  videoobj.video_file = image_file
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            userId = request.user
            userObj = User.objects.get(username = request.user)
            # Video(user=userObj)
            video = form.save(commit= False)  # Save form data to a variable without committing to the database yet
            video.user = request.user
              # Assign the current user to the video
            form.save()  # Now save the video object to the database
            return redirect('videoviewlist')  # Redirect to a success page
        
    else:
        form = VideoForm()
        return render(request, 'index.html', {'form': form})
    
    #         video = form.save()
    #         video.user = request.user
    #         form.save()
    #         return redirect('videoviewlist')  # Redirect to a success page
    # else:
    #     form = VideoForm()
    #     return render(request, 'index.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to home page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('videoviewlist')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
