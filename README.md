# ShareForum

>Notice: ShareForum has not been completely developed yet. In other words, it's under development.

## What's this?
This is a forum system powered by Django and Bootstrap to share your ideas of some interesting books. All of the forum's posts are based the book node though, it can also have many other topics by extending the book node.

## Features(under development)
- Powered by Django and Bootstrap。
- Scalable multi-node system.
- Follow, collect, and get the dynamic news. 
- Personalized user page.
- Multi-user、multi-role permission management system.
- Restful API.
- Common forum's functions:
    + Register, login/logout, reset password, email confirm.
    + Post, reply.
    + Add node, tag.
    + Notification.
    + Popularity statistics

## Preview ShareForum
![](http://arian-blogs.oss-cn-beijing.aliyuncs.com/18-5-31/10912899.jpg)

## How to use?
1. Clone this repository into your computer.
2. Get dependencies:
```bash
pip install -r requirements.txt
```
    or(recommend):
```bash
pipenv install
```
3. Put the sensitive values in your environment varibles accordding to the `settings_dev.py` , which should include something secret varibles that are needed to run the forum.
 
    You can alse use another way: Create a new file named `.env` in the `Share` folder, then write some key-value pairs in it. ShareForum will load them as environment varibles when the programming is started.

4. Start up:
```bash
python manage.py runserver
```
5. Create a administor user:
```bash
python manage.py createsuperuser
```

## What's more
Welcome to issue some problems that you find in this project. I appriciate your work very much!