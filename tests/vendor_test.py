import json

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tests.factories import UserFactory, VendorFactory
from vendor.models import Vendor


@pytest.fixture
def authenticated_client():
    client = APIClient()
    user = UserFactory()
    client.force_authenticate(user=user)
    yield client


@pytest.mark.django_db
def test_create_vendor(authenticated_client):
    vendor_data = {
        "user": {"username": "test-user-name", "password": "vid@123"},
        "name": "test name",
        "contact_details": "test contact details",
        "address": "test address",
    }

    url = reverse("vendors-list")
    response = authenticated_client.post(
        url, data=json.dumps(vendor_data), content_type="application/json"
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert Vendor.objects.filter(id=response.data["id"]).exists()


@pytest.mark.django_db
def test_get_performance_metrics(authenticated_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    vendor = VendorFactory()

    authenticated_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    url = reverse("vendors-get-performance-metrics", args=[vendor.id])
    response = authenticated_client.get(url)

    # Assert the response status code and any other expected behavior
    assert response.status_code == 200
    assert "on_time_delivery_rate" in response.data
    assert "quality_rating_avg" in response.data
