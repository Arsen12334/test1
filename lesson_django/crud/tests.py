from django.test import TestCase
from django.urls import reverse

from .models import Item


class ItemModelTests(TestCase):

    def test_str_returns_title(self):
        """Строковое представление записи равно её заголовку."""
        item = Item.objects.create(title="Задача", description="Описание")
        self.assertEqual(str(item), "Задача")

    def test_description_is_optional(self):
        """Описание можно не заполнять."""
        item = Item.objects.create(title="Без описания")
        self.assertEqual(item.description, "")


class ItemReadTests(TestCase):

    def setUp(self):
        self.item = Item.objects.create(title="Первая запись", description="Текст записи")

    def test_list_returns_200(self):
        """Страница списка открывается."""
        response = self.client.get(reverse("crud:item_list"))
        self.assertEqual(response.status_code, 200)

    def test_list_contains_title(self):
        """В списке виден заголовок записи."""
        response = self.client.get(reverse("crud:item_list"))
        self.assertContains(response, "Первая запись")

    def test_list_empty_shows_message(self):
        """Если записей нет, показывается сообщение."""
        Item.objects.all().delete()
        response = self.client.get(reverse("crud:item_list"))
        self.assertContains(response, "Записей пока нет")

    def test_detail_returns_200(self):
        """Страница записи открывается."""
        response = self.client.get(reverse("crud:item_detail", args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_contains_description(self):
        """На странице записи виден её текст."""
        response = self.client.get(reverse("crud:item_detail", args=[self.item.pk]))
        self.assertContains(response, "Текст записи")

    def test_detail_nonexistent_id_returns_404(self):
        """Несуществующая запись даёт 404."""
        response = self.client.get(reverse("crud:item_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)


class ItemCreateTests(TestCase):

    def test_create_page_returns_200(self):
        """Форма создания открывается."""
        response = self.client.get(reverse("crud:item_create"))
        self.assertEqual(response.status_code, 200)

    def test_create_adds_item_and_redirects(self):
        """Корректная форма создаёт запись и ведёт на список."""
        response = self.client.post(
            reverse("crud:item_create"),
            {"title": "Новая запись", "description": "Новый текст"},
        )
        self.assertRedirects(response, reverse("crud:item_list"))
        self.assertTrue(Item.objects.filter(title="Новая запись").exists())

    def test_create_without_title_shows_error(self):
        """Без заголовка запись не создаётся, форма показывается снова."""
        response = self.client.post(
            reverse("crud:item_create"),
            {"title": "", "description": "Текст"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.count(), 0)


class ItemUpdateTests(TestCase):

    def setUp(self):
        self.item = Item.objects.create(title="Старое название", description="Старый текст")

    def test_update_page_shows_current_title(self):
        """Форма изменения заполнена текущими данными."""
        response = self.client.get(reverse("crud:item_update", args=[self.item.pk]))
        self.assertContains(response, "Старое название")

    def test_update_changes_item_and_redirects(self):
        """Корректная форма меняет запись и ведёт на список."""
        response = self.client.post(
            reverse("crud:item_update", args=[self.item.pk]),
            {"title": "Новое название", "description": "Новый текст"},
        )
        self.assertRedirects(response, reverse("crud:item_list"))
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "Новое название")
        self.assertEqual(self.item.description, "Новый текст")

    def test_update_nonexistent_id_returns_404(self):
        """Изменение несуществующей записи даёт 404."""
        response = self.client.get(reverse("crud:item_update", args=[9999]))
        self.assertEqual(response.status_code, 404)


class ItemDeleteTests(TestCase):

    def setUp(self):
        self.item = Item.objects.create(title="Удаляемая запись", description="Текст")

    def test_delete_page_returns_200(self):
        """Страница подтверждения удаления открывается."""
        response = self.client.get(reverse("crud:item_delete", args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_removes_item_and_redirects(self):
        """Подтверждённое удаление убирает запись и ведёт на список."""
        response = self.client.post(reverse("crud:item_delete", args=[self.item.pk]))
        self.assertRedirects(response, reverse("crud:item_list"))
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())

    def test_delete_nonexistent_id_returns_404(self):
        """Удаление несуществующей записи даёт 404."""
        response = self.client.post(reverse("crud:item_delete", args=[9999]))
        self.assertEqual(response.status_code, 404)
