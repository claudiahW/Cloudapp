from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile
from .. import db
from ..requests import get_quotes
from flask_login import login_required
from ..models import  BlogPost, User
# Views
@main.route('/',methods = ["GET"])
def  index():
  '''
  Function that returns the home page
  '''
#   blogs_found = Blogs.query.order_by(Blogs.submitted.desc()).all()
  quotes = get_quotes()
  title = "Claudblog"
  return render_template('index.html',title = title,quotes = quotes)
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.update_profile',uname=user.username))
    return render_template('profile/update.html',form =form)  
@main.route('/post', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.posts'))
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('post.html', posts=all_posts)
@main.route('/post/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.posts'))
@main.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('main.posts'))
    else:
        return render_template('edit.html', post=post)
@main.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        posts_author = request.form['author']
        posts_content = request.form['content']
        new_post = BlogPost(title=post_title, content=posts_content, author=posts_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.posts'))
    else:
        return render_template('new_post.html')