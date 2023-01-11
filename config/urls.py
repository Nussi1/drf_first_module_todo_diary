from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include("projects.urls")),
    path('todo/', include("todo.urls")),
    path('blog/', include("blog.urls")),
    path('diary/', include("diary.urls")),
    path('flashcard/', include("flashcard.urls")),
]
