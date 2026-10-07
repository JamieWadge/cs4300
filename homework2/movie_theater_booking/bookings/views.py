from django.shortcuts import render

class MovieViewSet(viewsets.ViewSet):
    queryset = Movie.objects.all()
    serializer = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
