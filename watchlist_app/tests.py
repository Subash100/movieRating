from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(username='test',password='test')
        self.token=Token.objects.get(user__username='test')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

        self.stream = models.StreamPlatform.objects.create(name='netflix',about='this is about netflix',website='https://netflix.com')

    def test_streamplatform_create(self):
        data={
            'name':'netflix',
            'about':'this is about netflix',
            'website':'https://netflix.com'
        }
        response=self.client.post(reverse('streamplatform-list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response=self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_streamplatform_detail(self):
        response=self.client.get(reverse('streamplatform-detail',args=[self.stream.pk]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(username='test',password='test')
        self.token=Token.objects.get(user__username='test')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

        self.stream=models.StreamPlatform.objects.create(name='netflix',about='this is about netflix',website='https://netflix.com')

        self.watchlist=models.WatchList.objects.create(platform=self.stream,title='test',storyline='test',active=True)

    def test_watchlist_create(self):
        data={
            'platform':self.stream,
            'title':'test',
            'storyline':'test',
            'active':True
        }
        response=self.client.post(reverse('list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response=self.client.get(reverse('list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response=self.client.get(reverse('detail',args=[self.watchlist.pk]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title,'test')


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(username='test',password='test')
        self.token=Token.objects.get(user__username='test')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

        self.stream=models.StreamPlatform.objects.create(name='netflix',about='this is about netflix',website='https://netflix.com')

        self.watchlist=models.WatchList.objects.create(platform=self.stream,title='test',storyline='test',active=True)


    def test_review_create(self):
        data={
            'review_user':self.user.id,
            'watchlist':self.watchlist.id,
            'rating':5,
            'description':'good',
            'active':True
        }

        response=self.client.post(reverse('reviews-create',args=[self.watchlist.pk]),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        response = self.client.post(reverse('reviews-create', args=[self.watchlist.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            'review_user': self.user.id,
            'watchlist': self.watchlist.id,
            'rating': 5,
            'description': 'good',
            'active': True
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('reviews-create', args=[self.watchlist.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_review_update(self):
        review=models.Reviews.objects.create(review_user=self.user,watchlist=self.watchlist,rating=5,description='good',active=True)
        data={
            'review_user':self.user.id,
            'watchlist':self.watchlist.id,
            'rating':5,
            'description':'bad',
            'active':False
        }

        response=self.client.put(reverse('review-detail',args=[review.pk]),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        response=self.client.put(reverse('review-detail',args=[999]),data)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        response=self.client.put(reverse('review-detail',args=[review.pk]),{})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_review_list(self):
        response=self.client.get(reverse('reviews',args=[self.watchlist.pk]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_detail(self):
        review=models.Reviews.objects.create(review_user=self.user,watchlist=self.watchlist,rating=5,description='good',active=True)

        response=self.client.get(reverse('review-detail',args=[review.pk]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        response=self.client.get(reverse('review-detail',args=[999]))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


    def test_review_user(self):
        response=self.client.get(f'/watch/review/?username={self.user.username}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)