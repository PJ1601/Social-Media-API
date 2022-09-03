from email import contentmanager
import json
from turtle import title
import pytest
from app import schemas
from app.models import Post

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    def validate(post):
        return schemas.Post_Vote(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    # assert posts_list[0].Post.id == test_posts[0].id
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/8888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.Post_Vote(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [
    ('awesome new title', 'awesome new content', True),
    ('awesome cool title', 'awesome cool content', True),
    ('The tallest skyscraper', 'wohoo', True), 
    ('Favorite Anime', 'Jujutsu Kisen', False)
])
def test_create_posts(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content 
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "a title", "content": "a content"})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "a title"
    assert created_post.content == "a content" 
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']
 

def test_unauthorized_user_create_posts(client,test_user, test_posts):
    res = client.post("/posts/", json={"title": "a title", "content": "a content"})
    assert res.status_code == 401


def test_unauthorized_user_delete_posts(client,test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/8000000")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client,test_user, test_user_2, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    # assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert updated_post.title == data['title']
    assert updated_post.content == data["content"]
    assert updated_post.published == True
    assert updated_post.owner_id == test_user['id']


def test_update_other_user_post(authorized_client, test_user, test_user_2, test_posts):
    data = {
        "title": "Updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_posts(client,test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/8000000", json=data)
    assert res.status_code == 404



