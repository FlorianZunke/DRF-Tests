from rest_framework import viewsets, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from forum_app.models import Like, Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, LikeSerializer
from .permissions import IsOwnerOrAdmin, CustomQuestionPermission
from .throttling import QuestionThrottle

from rest_framework.throttling import ScopedRateThrottle
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination   

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomQuestionPermission]
    throttle_classes = [QuestionThrottle]

    #Das gehört zusammen setzt dann den Scope als class
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'question-scope'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # DjangoFilterBackend ermöglicht das Filtern von Abfragen
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username'] #sucht nur nach dem original Text, man kann keine einzelnen Wörter finden. Für Checkboxen
    
    search_fields = ['content'] #sucht nach einzelnen Wörtern in der Antwort. Braucht als Key Search(also auch in der URL)
    
    ordering_fields = ['content', 'author__username']
    ordering = ['content'] #startet mit der Sortierung nach content(mit Key ordering kann nochmal andere Sortierung angegeben werden)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    #Ist das gleiche wie Zeile 32-33. Nur das man hier nach einzelen Wörtern suchen kann
    # def get_queryset(self):
    #     queryset = Answer.objects.all()

    #     content_param = self.request.query_params.get('content', None)
    #     if content_param is not None:
    #         queryset = queryset.filter(content__icontains=content_param)

    #     username_param = self.request.query_params.get('author', None)
    #     if username_param is not None:
    #         queryset = queryset.filter(author__username=username_param)
        
    #     return queryset

class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrAdmin]



class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CustomLimitOffSetPagination(LimitOffsetPagination):
    default_limit = 10 # Standardmäßig 10 Einträge pro Seite
    limit_query_param = 'limit' # Ermöglicht die Angabe der Anzahl der Einträge pro Seite über den URL-Parameter 'limit'
    offset_query_param = 'offset' # Ermöglicht die Angabe des Offsets über den URL-Parameter 'offset', gibt an wo ich starte
    max_limit = 100 # Maximale Anzahl von Einträgen, die pro Seite zurückgegeben werden können



class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrAdmin]
    pagination_class = LargeResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
