from rest_framework.routers import SimpleRouter

from .views import TodoItemViewSet

app_name = 'listapp'

router = SimpleRouter(trailing_slash=False)
router.register(r'todos', TodoItemViewSet, base_name='todoitems')

urlpatterns = [] + router.urls
