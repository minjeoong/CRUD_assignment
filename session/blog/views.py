from django.utils import timezone
from django.contrib import messages
# from time import timezone
from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog, Comment
from .forms import BlogForm



def home(request):
    # 블로그 오브젝트를 모두 가져옴
    blogs = Blog.objects.all() 
    return render(request,'home.html',{'blogs':blogs})

def detail(request,blog_id):
    blog = get_object_or_404(Blog,pk=blog_id)
    comments = Comment.objects.filter(post = blog_id)
    
    if request.method == 'POST':
        comment = Comment()
        comment.post = blog
        comment.body = request.POST['body']
        comment.created_at = timezone.now()
        
        if not comment:
            messages.info(request, '아무것도 작성되지 않았습니다.')
        else:
            comment.save()
    comment_cnt = comments.count()
    return render(request,'detail.html',{'blog':blog, 'comments':comments, "comment_cnt":comment_cnt})


def new(request):
    return render(request,'new.html')
    
# def create(request):
#     new_blog = Blog()
#     # post - 딕셔너리 형으로 인덱싱  
#     new_blog.title = request.POST['title']
#     new_blog.content = request.POST['content']
#     new_blog.save()
#     # redirect - 디테일 url 로 id 를 가지고 이동 
#     return redirect('detail',new_blog.id)
def create(request):
    form = BlogForm(request.POST)
    # 착한 사용자
    if form.is_valid():
        new_blog = form.save(commit=False)
        new_blog.save()
        return redirect('detail', new_blog.id)
    
    # 나쁜 사용자
    return render(request, "new.html")


def edit(request, blog_id):
    # 블로그 테이블을 가져오고 pk 는 블로그 아이디를 가져옴
    edit_blog = get_object_or_404(Blog, pk = blog_id)
    return render(request, 'edit.html', {"edit_blog":edit_blog})

# def update(request, blog_id):
#     old_blog = get_object_or_404(Blog, pk=blog_id)
#     old_blog.title = request.POST['title']
#     old_blog.content = request.POST['content']
#     old_blog.save()
#     return redirect('detail',old_blog.id)
def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk = blog_id)
    form = BlogForm(request.POST, instance = old_blog)
    # 착한 사용자
    if form.is_valid():
        new_blog = form.save(commit=False)
        new_blog.save()
        return redirect('detail', old_blog.id)
    # 나쁜 사용자
    return render(request, 'new.html')

def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    delete_blog.delete()
    # 지웠으니 홈으로 가줌
    return redirect('home')



# def SearchForm(request):
#     searchkey = request.POST.get('searchkey')
#     searchfini = Blog.objects.filter(title__contains = searchkey)
#     return render(request, 'post_search.html')
def SearchForm(request):
    if request.method == 'POST':
        searchkey = request.POST.get('searchkey')
        # title 필드에 searchkey 문자열이 포함된 블로그들을 찾음
        search_result = Blog.objects.filter(title__contains=searchkey)
        return render(request, 'post_search.html', {'blogs': search_result, 'searchkey':searchkey})
    else:
        # GET 요청일 경우 검색 페이지를 보여줌
        return redirect('home')