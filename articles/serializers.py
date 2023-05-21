from rest_framework import serializers
from articles.models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Comment
        exclude = ("article",) # 하나일 겨우 exclude를 사용해도 된다.


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)
        

class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many= True) # 게시글에 대한 댓글 불러오기 (comment_set = related_name)
    likes = serializers.StringRelatedField(many = True) # StringRelatedField : String method, 좋아요 유저 이메일로 보이게한다.

    def get_user(self, obj):
        return obj.user.email # user값을 email로 가져오겠다.
    
    class Meta:
        model = Article
        fields = '__all__'


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "image", "content")

    
class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email
    
    def get_likes_count(self, obj):
        return obj.likes.count() # 좋아요 개수를 카운트해라
    
    def get_comment_count(self, obj):
        return obj.comment_set.count() # 댓글 개수를 카운트해라


    class Meta:
        model = Article
        fields = ("pk", "title", "image", "user", "likes_count", "comment_count") # 선택한 항목만 가져오겠다.


