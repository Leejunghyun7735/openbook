from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.db.models.query_utils import Q
from articles.models import Article, Comment
from articles.serializers import ArticleSerializer, ArticleCreateSerializer, ArticleListSerializer, CommentSerializer, CommentCreateSerializer


class ArticleView(APIView):
    # 게시글 보기
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시글 작성
    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    # 게시글 상세보기
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id) # 정보를 가져오거나 404 오류를 띄우겠다
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시글 수정하기
    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user: # 요청한 유저랑 게시글 유저랑 같으면
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    # 게시글 삭제하기
    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response("삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)


class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated] # 로그인 한사람만 권한 부여
    # 팔로우한 사람의 게시글 보기
    def get(self, request):
        q = Q
        # Q objects : 복잡한 조건을 걸 때 사용한다.
        # Q(조건) | Q(조건) : | = or, ^ = and
        for user in request.user.followings.all():
            q.add(Q(user=user),q.OR) # or 조건문 사용        
        feeds = Article.objects.filter(q) # 팔로우한 사람들의 게시글을 가져와라.
        serializer = ArticleListSerializer(feeds, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
                

class CommentView(APIView):
    # article_id 게시글에 관한 댓글 보기
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        comments = article.comment_set.all() # article에 작성이 된 comments들의 쿼리셋을 다 불러온다.
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 댓글 작성하기
    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    # 댓글 수정하기
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    # 댓글 삭제하기
    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response("삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView):
    # 좋아요 추가/삭제
    # manytomany일 경우에는 remove와 add를 통해서 추가와 제거를 할 수 있다.
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.likes.all(): # 요청한 유저가 게시글 좋아요에 있으면
            article.likes.remove(request.user)
            Response("좋아요를 눌렀습니다.", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            Response("좋아요를 취소했습니다.", status=status.HTTP_200_OK)


