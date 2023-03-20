from django.shortcuts import render,redirect
from .models import Post,Comment,Like,LikeComment,Chat,Message
from apps.users.models import User,Followers
from django.db.models import Q

# Create your views here.
def index(request):
    # follow_status = Followers.objects.filter(from_user = request.user)
    # user = User.objects.get(id = follow_status.to_user.id)
    # posts=Post.objects.all().filter(user = user).order_by('-id')
    posts=Post.objects.all().order_by('-id')
    
    if request.method == "POST":
        if 'like' in request.POST:
            post = request.POST.get('post')
            try:
                like = Like.objects.get(user=request.user , post_id = post)
                like.delete()
                return redirect('index')
            except:
                like = Like.objects.create(user=request.user,post_id = post)
                like.save()
                return redirect('index')
            
        if 'create_chat' in request.POST:
            to_user = request.POST.get('to_user')
            try:
                try:
                    chat = Chat.objects.get(from_user = request.user , to_user_id = to_user)
                    return redirect('chat_detail',chat.id, request.user.username)
                except:
                    chat = Chat.objects.get(to_user = request.user , from_user_id = to_user)
                    return redirect('chat_detail',chat.id, request.user.username)
            except:
                chat = Chat.objects.create(from_user = request.user , to_user_id = to_user)
                chat.save()
                return redirect('chat_detail',chat.id, request.user.username)
            
    context={
        'posts':posts,

    }
    return render(request,'index.html',context)

def post_delete(request,id):
    post = Post.objects.get(id = id)
    if request.user == post.user:
        if request.method == 'POST':
            post.delete()
            return redirect('index')
    else:
        return redirect('index')
    return render(request, 'post_delete.html')
    
def post_detail(request, id):
    post = Post.objects.get(id = id)
    if request.method =='POST':
        if 'comment' in request.POST:
            text = request.POST.get('text')
            try:
                comment= Comment.objects.create(post = post ,user = request.user,text = text)
                comment.save()
                return redirect('post_detail', post.id)
            except:
                return redirect('post_detail', post.id)
        if 'like' in request.POST:
            try:
                like = Like.objects.get(user=request.user , post = post)
                like.delete()
                return redirect('post_detail', post.id)
            except:
                like = Like.objects.create(user=request.user,post = post)
                like.save()
                return redirect('post_detail', post.id)
            
        if 'like_comment' in request.POST:
            like_comment_id = request.POST.get('like_comment_id')
            try:
                like_comment = LikeComment.objects.get(user = request.user,comment_id = like_comment_id)
                like_comment.delete()
                return redirect('post_detail' ,post.id)
            except:
                like_comment = LikeComment.objects.create(user = request.user , comment_id = like_comment_id)
                return redirect('post_detail' , post.id)
        
        if 'comment_delete' in request.POST:
            comment = request.POST.get('comment_user_id')
            comment_deleted = Comment.objects.get(id = comment)
            if request.user == comment_deleted.user or request.user == post.user:
                comment_deleted.delete()
                return redirect('post_detail',post.id)
            else:
                return redirect('post_detail',post.id)
                                                                                                                                                                                                                                                                                                                                                                                                                                              
    context = {
        'post':post,
    }
    return render(request, 'comment.html', context)

def search(request):
    posts = Post.objects.all()
    users = User.objects.all()
    search_key = request.GET.get('key')
    if search_key:
        posts = Post.objects.all().filter(Q(title__icontains = search_key))
        users = User.objects.all().filter(Q(username__icontains = search_key))
    context = {
        'users':users,
        'posts':posts
    }
    return render(request, 'include/search.html',context)



def update_post(request,id):
    post = Post.objects.get(id = id)
    if request.user == post.user:
        if request.method == 'POST':
                file=request.FILES.get('file')
                text=request.POST.get('text')
                description=request.POST.get('description')
                title=request.POST.get('title')
            
                post.file = file
                post.text = text
                post.description = description
                post.title = title
                post.save()
                return redirect('index')
    context = {
        'post':post,
                    
 }
    return render(request,'include/update_post.html' , context)

def create_post(request,id):
    post = Post.objects.all()
    if request.method == 'POST':
        if 'create_post' in request.POST:
            post_text = request.POST.get('post_text')
            post_file = request.FILES.get('post_file')
            post_title = request.POST.get('post_title')
            post_description = request.POST.get('post_description')
           
            post.post_text = post_text
            post.post_file = post_file
            post.post_title = post_title
            post.post_description = post_description
            post.save()
            return redirect('index')
    context = {
        'post':post
    }
    return render(request, 'include/create_post.html',context)   


            
def chats(request,id):
    user = User.objects.get(id = id)
    all_chats = Chat.objects.all().filter(Q(from_user=user) | Q(to_user = user))
    context ={
        'all_chats':all_chats
    }
    return render(request,'include/chat_mine.html',context)
            