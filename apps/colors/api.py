from rest_framework import generics
from rest_framework import parsers
from rest_framework import response
from rest_framework import views


from .serializers import InputImageFileSerializer, ImageFileSerializer
from .models import ImageFile
from . import services


class PostImagesApiController(views.APIView):
    """

    """
    parser_classes = (parsers.MultiPartParser,)

    def get_serializer_class(self):
        return InputImageFileSerializer

    def get_image_handler_service(self):
        return services.ImageColorExtractor

    def post(self, request, format=None):
        processing_data = {}
        SerializerClass = self.get_serializer_class()
        ServiceClass = self.get_image_handler_service()

        for key in request.FILES:
            f = request.FILES[key]
            serializer_input = {
                'source': f
            }
            serializer = SerializerClass(data=serializer_input)
            is_valid = serializer.is_valid()

            if is_valid:
                source = serializer.validated_data['source']
                service = ServiceClass(source=source)
                service.run()

            processing_data[f.name] = {
                'success': is_valid,
                'errors': serializer.errors
            }

        return response.Response(data=processing_data)


class ImageFileSearchController(generics.ListAPIView):
    """
        Returns paginated list of images.
        Param color or hex may be specified to filter results.
    """
    serializer_class = ImageFileSerializer

    def get_queryset(self):
        qs = ImageFile.objects.prefetch_related('colors')
        color = self.request.query_params.get('color', None)
        hex_ = self.request.query_params.get('hex', None)

        if color:
            qs = qs.filter(color__name__contains=color.lower())

        if hex_:
            if not hex_.startswith('#'):
                hex_ = '#' + hex_

            qs = qs.filter(color__hex=hex_.lower())

        return qs.order_by('color__priority').all()