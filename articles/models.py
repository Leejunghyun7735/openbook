from django.db import models
from users.models import User

# 게시글
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='%Y/%m/') # 이미지 파일은 월별로 저장하겠다.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, related_name="like_articles") 
    # ManyToMany : 한 유저가 여러 게시글을 좋아요를 할 수 있고 한 게시글에 여러 유저가 좋아요를 누를 수 있다.
    # ManyToMany에서는 중복을 방지하기 위해 related_name을 꼭 정해주자

    def __str__(self):
        return str(self.title) 
    

# 댓글
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comment_set")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)
    

