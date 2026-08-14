from django.test import TestCase


class PublicPagesTests(TestCase):
    def test_markets_page_renders(self):
        response = self.client.get("/markets/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Food markets")

    def test_logout_does_not_accept_get_requests(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 405)

# Create your tests here.
