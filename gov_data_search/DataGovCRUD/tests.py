from django.test import TestCase,Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Event, ShowInfo, Organizer, Location


#註冊測試
class TestSignUp(TestCase):
    def setUp(self):
        self.client = Client()
        self.sign_up_url = reverse('register')

    def test_sign_up_GET(self):
        response = self.client.get(self.sign_up_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_sign_up_POST_form_valid(self):
        response = self.client.post(self.sign_up_url, {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)

    def test_sign_up_POST_form_invalid(self):
        response = self.client.post(self.sign_up_url, {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'wrongpassword123',
        })
        self.assertEqual(response.status_code, 200)


#登入測試
class TestSignIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.sign_in_url = reverse('login')
        
        # 創建測試用戶
        CustomUser = get_user_model()
        self.test_user = CustomUser.objects.create_user(username='testuser', password='testpassword123')


    def test_sign_in_GET(self):
        response = self.client.get(self.sign_in_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_sign_in_POST_form_valid(self):
        response = self.client.post(self.sign_in_url, {
            'username': 'testuser',
            'password': 'testpassword123',
        })

        self.assertEqual(response.status_code, 302)  # 檢查是否重定向到操作頁面

    def test_sign_in_POST_form_invalid(self):
        response = self.client.post(self.sign_in_url, {
            'username': 'wronguser',
            'password': 'wrongpassword123',
        })

        self.assertEqual(response.status_code, 200)  # 檢查是否仍停留在登入頁面
        

#會員頁面測試
class TestpProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.update_url = reverse('profile')

        # 創建測試用戶
        CustomUser = get_user_model()
        self.test_user = CustomUser.objects.create_user(username='testuser', password='testpassword123')
  

    def test_update_url_in_GET_from_user(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"profile.html")

    def test_update_url_in_GET_from_visitor(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code,302)

#首頁測試
class TestpHome(TestCase):
    def setUp(self):
        self.client = Client()
        self.home = reverse("home")

    def test_update_url_in_GET_from_visitor(self):
        response = self.client.get(self.home)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"home.html")

#操作頁面測試
class TestpOperation(TestCase):
    def setUp(self):
        self.client = Client()
        self.home = reverse("operation")

    def test_update_url_in_GET_from_visitor(self):
        response = self.client.get(self.home)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"operation.html")



    def setUp(self):
        # 創建一些 Organizer 資料
        self.master_organizer = Organizer.objects.create(name='Master Organizer')
        self.sub_organizer = Organizer.objects.create(name='Sub Organizer')
        self.support_organizer = Organizer.objects.create(name='Support Organizer')
        self.other_organizer = Organizer.objects.create(name='Other Organizer')
        
        # 創建多筆 Event 資料
        for i in range(30):  # 超過 20 筆資料來測試分頁
            event = Event.objects.create(
                version="1.0",
                uid=f"event{i}",
                title=f"Event Title {i}",
                category="CAT",
                description="Event description",
                image_url="http://example.com/image.jpg",
                source_web_name="Source Web",
                start_date=timezone.now().date(),
                end_date=timezone.now().date(),
                hit_rate=i  # hit_rate 用來排序
            )
            event.master_unit.add(self.master_organizer)
            event.sub_unit.add(self.sub_organizer)
            event.support_unit.add(self.support_organizer)
            event.other_unit.add(self.other_organizer)

    def test_all_events_view_status_code(self):
        url = reverse('operation/events/')  # 假設在 urls.py 中設置了名稱為 'all_events' 的路徑
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_all_events_view_template(self):
        url = reverse('operation/events/')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'event_list.html')

    def test_all_events_pagination(self):
        url = reverse('operation/events/')
        response = self.client.get(url)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['object_list']), 20)  # 檢查每頁有 20 筆資料

    def test_all_events_sorted_by_hit_rate(self):
        url = reverse('operation/events/')
        response = self.client.get(url)
        events = response.context['object_list']
        hit_rates = [event.hit_rate for event in events]
        self.assertEqual(hit_rates, sorted(hit_rates))  # 檢查事件按 hit_rate 排序


class EventsDetailViewTest(TestCase):

    def setUp(self):
        # 創建 Organizer 和 Location 資料
        self.organizer = Organizer.objects.create(name='Organizer A')
        self.location = Location.objects.create(
            name='Location A',
            address='123 Event Street',
            latitude='25.0330',
            longitude='121.5654'
        )
        
        # 創建 Event 資料
        self.event = Event.objects.create(
            version="1.0",
            uid="event123",
            title="Test Event",
            category="CAT",
            description="Event description",
            image_url="http://example.com/image.jpg",
            source_web_name="Source Web",
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            hit_rate=100,
            show_unit="Show Unit"
        )
        self.event.master_unit.add(self.organizer)
        
        # 創建 ShowInfo 資料
        self.showinfo = ShowInfo.objects.create(
            event=self.event,
            time=timezone.now().date(),
            end_time=timezone.now(),
            on_sale=True,
            price="100",
            location=self.location
        )

    def test_event_detail_view_status_code(self):
        # 測試事件詳細頁的狀態碼是否為 200
        url = reverse('event_detail', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_detail_view_template_used(self):
        # 測試是否使用了正確的模板
        url = reverse('event_detail', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'event_detail.html')

    def test_event_detail_view_context_data(self):
        # 測試上下文中是否包含正確的 showinfos 資料
        url = reverse('event_detail', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        
        # 確認上下文中是否包含 showinfos
        self.assertIn('showinfos', response.context)
        showinfos = response.context['showinfos']
        
        # 檢查 showinfos 的內容是否正確
        self.assertEqual(len(showinfos), 1)
        self.assertEqual(showinfos[0], self.showinfo)
        self.assertEqual(showinfos[0].location, self.location)


class EventDeleteViewTest(TestCase):

    def setUp(self):
        # 創建測試用戶並登入
        CustomUser = get_user_model()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')

        # 創建 Organizer 和 Event 資料
        self.organizer = Organizer.objects.create(name='Organizer A')
        self.event = Event.objects.create(
            version="1.0",
            uid="event123",
            title="Test Event",
            category="CAT",
            description="Event description",
            image_url="http://example.com/image.jpg",
            source_web_name="Source Web",
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            hit_rate=100,
            show_unit="Show Unit"
        )
        self.event.master_unit.add(self.organizer)

    def test_event_delete_view_status_code(self):
        # 測試刪除頁面是否正確加載 (狀態碼 200)
        url = reverse('event_confirm_delete', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_delete_view_template_used(self):
        # 測試是否使用正確的模板
        url = reverse('event_confirm_delete', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'event_confirm_delete.html')

    def test_event_deleted(self):
        # 測試刪除操作是否成功
        url = reverse('event_confirm_delete', kwargs={'pk': self.event.pk})
        response = self.client.post(url)
        
        # 確認事件已被刪除
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())
        
        # 確認重定向到成功的 URL
        self.assertRedirects(response, reverse('operation'))

    def test_event_delete_view_redirect_if_not_logged_in(self):
        # 測試未登入用戶不能訪問刪除頁面，應該重定向到登入頁面
        self.client.logout()
        url = reverse('event_confirm_delete', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        
        # 確認未登入用戶被重定向到登入頁面
        self.assertRedirects(response, f'/accounts/login/?next={url}')


class EventUpdateViewTest(TestCase):

    def setUp(self):
        # 創建測試用戶並登入
        CustomUser = get_user_model()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')

        # 創建 Organizer 和 Event 資料
        self.organizer = Organizer.objects.create(name='Organizer A')
        self.event = Event.objects.create(
            version="1.0",
            uid="event123",
            title="Test Event",
            category="CAT",
            description="Event description",
            image_url="http://example.com/image.jpg",
            source_web_name="Source Web",
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            hit_rate=100,
            show_unit="Show Unit"
        )
        self.event.master_unit.add(self.organizer)

    def test_event_update_view_status_code(self):
        # 測試更新頁面是否正確加載 (狀態碼 200)
        url = reverse('event_update', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_update_view_template_used(self):
        # 測試是否使用正確的模板
        url = reverse('event_update', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'event_form.html')

    def test_event_update_success(self):
        # 測試事件更新操作是否成功
        url = reverse('event_update', kwargs={'pk': self.event.pk})
        updated_data = {
            'version': '2.0',
            'uid': 'event123',
            'title': 'Updated Test Event',
            'category': 'NEW',
            'description': 'Updated description',
            'image_url': 'http://example.com/new_image.jpg',
            'web_sale': 'http://example.com/sale',
            'source_web_promote': 'http://example.com/promote',
            'comment': 'Updated comment',
            'edit_modify_date': timezone.now(),
            'source_web_name': 'New Source Web',
            'start_date': timezone.now().date(),
            'end_date': timezone.now().date(),
            'hit_rate': 200,
            'show_unit': 'Updated Show Unit',
            'discount_info': 'New discount',
            'description_filter_html': '<p>Updated HTML</p>',
            'master_unit': [self.organizer.id],
            'sub_unit': [],
            'support_unit': [],
            'other_unit': [],
        }
        response = self.client.post(url, updated_data)

        # 確認事件更新後是否重定向到成功頁面
        self.assertRedirects(response, reverse('operation'))

        # 確認事件的資料已成功更新
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Updated Test Event')
        self.assertEqual(self.event.description, 'Updated description')
        self.assertEqual(self.event.hit_rate, 200)

    def test_event_update_view_redirect_if_not_logged_in(self):
        # 測試未登入用戶不能訪問更新頁面，應該重定向到登入頁面
        self.client.logout()
        url = reverse('event_update', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        
        # 確認未登入用戶被重定向到登入頁面
        self.assertRedirects(response, f'/accounts/login/?next={url}')

