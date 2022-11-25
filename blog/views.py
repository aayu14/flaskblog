from flask import Blueprint, render_template,flash
from flask_login import login_required, current_user
from blog.models import Blogpost
from flask import redirect,render_template,url_for,request
from . import db



views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()   
    return render_template('index.html', posts=posts,user=current_user)
    



@views.route('/about')
@login_required
def about():
    return render_template('about.html',user=current_user)


@views.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post,user=current_user)






@views.route('/posts/new')
@login_required
def newpost():
    return render_template('newpost.html',user=current_user)
    

@views.route('/posts', methods=['POST','GET'])
def posts():
  if request.method == 'POST':
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    img=request.form['img']
    headline = request.form['headline']  
    subtitle = request.form['subtitle']

    post = Blogpost(title=title, subtitle=subtitle, content=content,img=img,headline=headline, author=author)

    db.session.add(post)
    db.session.commit() 
    flash('Post created!', category='success')  
    return redirect(url_for('views.index'))
  else:
    return redirect(url_for('views.newpost'))


@views.route('/posts/delete/<int:id>')
@login_required
def delete(id):
    post =Blogpost.query.filter_by(id=id).first()

    if post:
 
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.index'))

   

    






@views.route('/posts/edit/<int:id>', methods=['POST', 'GET'])

def edit(id):
      post = Blogpost.query.get_or_404(id)
      if request.method == 'POST':

        post.title = request.form['title']
        post.subtitle = request.form['subtitle']
        post.author = request.form['author']
        post.content = request.form['content']
        post.img= request.form['img']
        post.headline = request.form['headline']
        db.session.commit()
        return redirect(url_for('views.index'))
      else:
        return render_template('edit.html',post=post,user=current_user)







