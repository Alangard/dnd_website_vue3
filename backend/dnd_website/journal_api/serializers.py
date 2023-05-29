from rest_framework import serializers
from .models import *
from django.db.models import Count




## Accounts serializers ############################################################

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [  'id',
                    "username", 
                    "password",
                    "avatar",
                    "email",
                    "favorites_reaction",
                    "recent_reaction",
                    "is_staff",
                    "is_active"]
        

        
class ShortAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "username", "avatar"]

## Utils #########################################################################

class RecursiveCommentSerializer(serializers.Serializer):
    # Output recursive children comments
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
    

class FilterCommentListSerializer(serializers.ListSerializer):
    # Drop double comments
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)
    
 ## Comments serializers ########################################################


class CommentsSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer()
    children = RecursiveCommentSerializer(many=True)
    replies_count = serializers.IntegerField(source='get_childrens_comment_count', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'parent', 'author', 'status', 'created_datetime', 'report_reasons', 'comment_text', 'replies_count', 'children']
        list_serializer_class = FilterCommentListSerializer
    

## Tags serializers ################################################################

class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class TagDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']

# Reactions serializers ########################################################

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'

        
# Post reactions serializers ###################################################

class PostReactionSerializer(serializers.ModelSerializer):
    author = AccountSerializer()
    reaction = ReactionSerializer()
    class Meta:
        model = PostReaction
        fields = '__all__'
        include = ['author', 'reaction']

## Posts serilizers #################################################################
class PostShortReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        # exclude = ['reaction_category']

    id = serializers.IntegerField(source='reaction__id')
    reaction_name = serializers.CharField(source='reaction__reaction_name')
    reaction_url = serializers.CharField(source='reaction__reaction_url')

    class Meta:
        model = Reaction
        fields = ['id', 'reaction_name', 'reaction_url']


class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(many=True, read_only=True)
    # reactions = PostReactionSerializer(many=True, read_only=True)
    # author = ShortAccountSerializer(read_only=True)
    post_author_username = serializers.CharField(source='author.username', default='', read_only=True)
    comments_count = serializers.IntegerField(source='get_comments_count', read_only = True)

    class Meta:
        model = Post
        fields = '__all__'

# Post list preview on feed
class PostListReadSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(many=True, read_only=True)
    author = ShortAccountSerializer(read_only=True)
    reactions = PostShortReactionSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        # fields=['id', 'author', 'tags', 'title', 'created_datetime','description','thumbnail', 'comments_count','commented','reacted', 'reactions']
        fields = '__all__'


    # It's corectly work, but having n+1 issue#

    # tags = TagListSerializer(many=True, read_only=True)

    # author = ShortAccountSerializer(read_only=True)

    # reactions = serializers.SerializerMethodField()

  
    # def get_reactions(self, obj):
    #     # todo: optimizing this
    #     objs = PostReaction.objects.filter(post=obj.id).values('reaction__id', 'reaction__reaction_name', 'reaction__reaction_url').annotate(reaction_count=Count('reaction__id')).order_by('-reaction_count')[:3]
    #     return PostShortReactionSerializer(objs, many=True, read_only=True).data
        


    # class Meta:
    #     model = Post
    #     fields=['author', 'title', 'description','thumbnail', 'created_datetime', 'tags','reactions','comments_count','commented','reacted']

  

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'title', 'description', 'body', 'tags', 'is_publish', 'publish_datetime']

# Reaction's categories  serializers ##########################################

class ReactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReactionCategory
        fields = '__all__'






class ReportReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportReason
        fields= '__all__'
    

