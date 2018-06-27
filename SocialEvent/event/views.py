from event.models import *
from event.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SearchEvent(APIView):
    def get(self, request):
        events = EventGeneral.objects.none()
        params = self.request.query_params;
        keyword = params.get('keyword',None)
        date = params.get('date',None)
        category = params.get('category', None)
        startnum = params.get('startnum', None)
        count = params.get('count', None)

        notSearchParameter = True;
        if keyword is not None:
            notSearchParameter = False
            events |= EventGeneral.objects.filter(title__contains=keyword)
            events |= EventContent.objects.filter(description__contains=keyword)
        if date is not None:
            notSearchParameter = False
            events |= EventGeneral.objects.filter(start_date__lte=date, end_date__gte=date)
        if category is not None:
            notSearchParameter = False
            category_id = Category.objects.filter(name__exact=category)[0].id
            events |= EventGeneral.objects.filter(c_id=category_id)
        if notSearchParameter:
            events = EventGeneral.objects.all()

        if (startnum is not None) and (count is not None) :
            print(startnum)
            print(count)
            startnum = int(startnum)
            count = int(count)
            endnum = startnum+count
            startnum = max(startnum, 0)
            endnum = min(endnum, events.count())
            if (startnum <= endnum):
                events = events[startnum:endnum]
            else:
                events = EventGeneral.objects.none()
        serializer = EventGeneralSerializer(events, many=True)
        return Response(serializer.data)


class CommentView(APIView):
    def get(self, request, id):
        comments = Comment.objects.filter(event_id=id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        print("post comment")
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        Comment.objects.filter(event_id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        comment = Comment.objects.filter(event_id=id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

