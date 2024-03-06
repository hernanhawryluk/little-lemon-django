# from django.test import TestCase
# from rest_framework.test import RequestsClient

# client = RequestsClient()

# class MenuItemsView(TestCase):
#     def test_menu_response(self):
#         client = RequestsClient()
#         response = client.get('http://localhost:8000/restaurant/menu/')

#         self.assertEqual(response.status_code, 200)

#     def test_menu_item(self):
#         client = RequestsClient()
#         response = client.get('http://localhost:8000/restaurant/menu/1')

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(
#             response.json(),
#             {'id': 1, 'title': 'PanCake', 'price': '1.50', 'inventory': 10},
#         )