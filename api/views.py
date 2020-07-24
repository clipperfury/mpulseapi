from api.models import Member
from api.serializers import MemberSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework_csv.parsers import CSVParser
from rest_framework_csv.renderers import CSVRenderer
from rest_framework import viewsets, status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from pprint import pprint
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework.parsers import FileUploadParser
from csv import reader
from csv import DictReader


from .serializers import FileSerializer


class MemberList(APIView):
    """
    List all member, or create a new member.
    """
    def get(self, request, format=None):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberByID(APIView):
    """
    Retrieve, update or delete a member instance.
    """
    def get_object(self, pk):
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        member = self.get_object(pk)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        member = self.get_object(pk)
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        member = self.get_object(pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MemberByAccount(APIView):
    """
    Retrieve, update or delete a member instance.
    """

    def get(self, request, account_id, format=None):

        members = Member.objects.filter(account_id=account_id)
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

class MemberByPhone(APIView):
    """
    Retrieve, update or delete a member instance.
    """

    def get(self, request, phone_number, format=None):

        members = Member.objects.filter(phone_number=phone_number)
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

class MemberByClient(APIView):
    """
    Retrieve, update or delete a member instance.
    """

    def get(self, request, client_member_id, format=None):

        members = Member.objects.filter(client_member_id=client_member_id)
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

class ProcessCSV (viewsets.ModelViewSet):

    queryset = Member.objects.all()
    parser_classes = (CSVParser,) + tuple(api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (CSVRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    serializer_class = MemberSerializer

    def get_renderer_context(self):
        context = super(ProcessCSV, self).get_renderer_context()
        context['header'] = (
            self.request.GET['fields'].split(',')
            if 'fields' in self.request.GET else None)
        return context

    def bulk_upload(self, request, *args, **kwargs):
        """
        Try out this view with the following curl command:
        curl -X POST http://localhost:8000/talks/bulk_upload/ \
            -d "speaker,topic,scheduled_at
                Ana Balica,Testing,2016-11-03T15:15:00+01:00
                Aymeric Augustin,Debugging,2016-11-03T16:15:00+01:00" \
            -H "Content-type: text/csv" \
            -H "Accept: text/csv"
        """
        serializer = MemberSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class FileUploadView(APIView):
    """
    Upload a csv file to be processed.  Phase 2 would be to validate it is an actual csv file/format.
    """
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

      file_serializer = FileSerializer(data=request.data)

      if file_serializer.is_valid():
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProcessFile(APIView):
    """
    Process a bulk uploaded file (phase 2 would be to use Celery or other task / queue system to process all files,
    but for now we can request the process of a file which will process it and return back number of processed rows,
    failed rows, and a link to a csv with an added column of success/failure for each row
    """
    def get(self, request, filename, format=None):

        # open file, ignore header
        filepath = './media/' + filename
        try:
            f = open(filepath, 'r')
        except OSError:
            print
            "Could not open/read file:", fname
            sys.exit()

        with f as read_obj:
            csv_dict_reader = DictReader(f)
            header = next(csv_dict_reader)
            # Check file as empty
            if header != None:
                for row in csv_dict_reader:
        # foreach line in the file, put data into request object and run through serializer.

                    serializer = MemberSerializer(data=row)
        # if valid, great
                    if serializer.is_valid():
                        print("Good")
                        serializer.save()
        #    serializer.save()
                    else:
                        print("Bad")

        # if invalid, bad, flag it, and continue


        # return link to processed file
        return Response(u'/media/' + filename)
