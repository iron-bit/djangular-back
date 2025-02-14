from rest_framework import routers

from blueddit.api.views import TagViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('tag', TagViewSet)

urlpatterns = router.urls