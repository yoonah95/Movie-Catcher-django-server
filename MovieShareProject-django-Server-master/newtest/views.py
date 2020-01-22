from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets
from django.core.files.storage import FileSystemStorage
import cv2


class JSONResponse(HttpResponse):

	print("!!!!!")

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data, 'application/json; indent=4')
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['GET','POST'])
def test_list(request, format=None):

    if request.method == 'GET':
        packages = TestModel.objects.all()
        serializer = TestSerializer(packages, many=True)
        return JSONResponse(serializer.data)


class PassIdViewSet(viewsets.ModelViewSet):
	queryset = PassId.objects.all()
	serializer_class = PassIdSerializer


	def create(self, request, *args, **kwargs):
		print(request.data['passid'])
		response_data={"success": "1"}
		return JSONResponse(response_data)

def test(request):
	return render(request, "./newtest/index.html")


class ClientViewSet(viewsets.ModelViewSet):
	queryset = Client.objects.all()
	serializer_class = ClientSerializer




def get_video_duration(file_path):
        cap = cv2.VideoCapture(file_path)
        cap.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
        num_frames = cap.get(cv2.CAP_PROP_POS_FRAMES)
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = float(num_frames) / float(fps)
        return int(duration)




def upload_file(request):
	if request.method == 'POST':
		clientid = request.POST.get("clientid",False)
		img = request.FILES['img']
		video = request.FILES['video']

		fs = FileSystemStorage()
		#filename = fs.save(img.name, img)
		file = Media(clientid = clientid, 
			img = img, 
			video = video
			)
		file.save()


		ds = get_video_duration('.' + file.video.url)

		if ds <10 or ds>30 :
			file.delete()

		context = {'ds':ds}
		



		return render(request, 'newtest/index.html')

	else :
		#print(request.path.split('/')[2])
		context = { 'clientid' : request.path.split('/')[2], 'ds':'-1',			
		}

		return render(request, 'newtest/index.html', context)


def show_file(request):
	
	if(request.method=='GET') :
		medias = Media.objects.filter(clientid = request.path.split('/')[2])

		context = { 'clientid' : request.path.split('/')[2] ,
					'medias' : medias
		}

		return render(request, 'newtest/index2.html', context)

	else:
		return render(request, 'newtest/index2.html')




def friend_add(request):
	if request.method == 'POST':
		clientid = request.POST.get("friendid",False)
		friendid = request.POST.get("clientid",False)
		print(clientid, friendid)


		fs = FileSystemStorage()
		#filename = fs.save(img.name, img)
		file = FriendAddList(
			clientid = clientid, 
			friendid = friendid
			)

		file.save()

		addlist = FriendAddList.objects.filter(clientid = friendid)
		flist = FriendList.objects.filter(clientid = friendid)
		#print(flist)
		context = { 'clientid' : friendid, 
					'addlist' : addlist, 
					'flist' : flist,	
		}
		print(context)


		return render(request, 'newtest/friend.html', context)

	else :

		addlist = FriendAddList.objects.filter(clientid = request.path.split('/')[2])
		flist = FriendList.objects.filter(clientid = request.path.split('/')[2])
		#print(flist)
		context = { 'clientid' : request.path.split('/')[2], 
					'addlist' : addlist, 
					'flist' : flist,	
		}

		return render(request, 'newtest/friend.html', context)


def friend_list(request):

	if request.POST.get("yes",False) == '1':
		clientid = request.POST.get("clientid",False)
		friendid = request.POST.get("friendid",False)
		fs = FileSystemStorage()
		#filename = fs.save(img.name, img)
		file = FriendList(
			clientid = clientid, 
			friendid = friendid
			)
		file2 = FriendList(
			clientid = friendid, 
			friendid = clientid
			)		
		file.save()
		file2.save()

		#friendAddList에 있는 목록 삭제 
		f_list = FriendAddList.objects.filter(clientid=clientid,friendid=friendid)
		for f in f_list :
			f.delete()

		addlist = FriendAddList.objects.filter(clientid = clientid)
		flist = FriendList.objects.filter(clientid = clientid)
		context = { 'clientid' : clientid, 
					'addlist' : addlist, 
					'flist' : flist,	
		}
		print(context)

		return render(request, 'newtest/friendadd.html', context)

	elif request.POST.get("no",False) == '0':

		clientid = request.POST.get("clientid",False)
		friendid = request.POST.get("friendid",False)

		f_list = FriendAddList.objects.filter(clientid=clientid,friendid=friendid)
		for f in f_list :
			f.delete()

		addlist = FriendAddList.objects.filter(clientid = clientid)
		flist = FriendList.objects.filter(clientid = clientid)
		context = { 'clientid' : clientid, 
					'addlist' : addlist, 
					'flist' : flist,	
		}

		return render(request, 'newtest/friendadd.html', context)

	else :

		addlist = FriendAddList.objects.filter(clientid = request.path.split('/')[2])
		flist = FriendList.objects.filter(clientid = request.path.split('/')[2])
		print(flist)
		context = { 'clientid' : request.path.split('/')[2], 
					'addlist' : addlist, 
					'flist' : flist,	
		}

		return render(request,'newtest/friendadd.html',context)

def ajaxpass(request):
	friendid = request.GET.get('friendid', None)
	clientid = request.GET.get('clientid', None)
	print(friendid, clientid)

	getfriend = FriendList.objects.filter(clientid = clientid)
	exfriend = Client.objects.filter(clientid = friendid)

	print(getfriend)
	print(exfriend)

	if friendid == clientid :
		context = {'hihi': '4' }
		return JSONResponse(context)

	for a in exfriend :
		for b in getfriend :
			if b.friendid == clientid : 
				context = {'hihi' : '1' }
				return JSONResponse(context)

		context = {'hihi' : '3' }
		return JSONResponse(context)

	context = {'hihi' : '2'}
	return JSONResponse(context)