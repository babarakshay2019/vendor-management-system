import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from order.models import PurchaseOrder
from tests.factories import PurchaseOrderFactory, UserFactory


@pytest.fixture
def authenticated_client():
    client = APIClient()
    user = UserFactory()
    client.force_authenticate(user=user)
    yield client


@pytest.mark.django_db
def test_acknowledge_purchase_order(authenticated_client):
    purchase_order = PurchaseOrderFactory()
    url = reverse("purchase_orders-acknowledge", args=[purchase_order.id])

    response = authenticated_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert (
        PurchaseOrder.objects.get(id=purchase_order.id).acknowledgment_date is not None
    )


@pytest.mark.django_db
def test_acknowledge_nonexistent_purchase_order(authenticated_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    authenticated_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    nonexistent_purchase_order_id = 9999
    url = reverse("purchase_orders-acknowledge", args=[nonexistent_purchase_order_id])

    response = authenticated_client.post(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_acknowledge_purchase_order_with_existing_acknowledgment_date(
    authenticated_client,
):
    purchase_order = PurchaseOrderFactory(acknowledgment_date=timezone.now())
    url = reverse("purchase_orders-acknowledge", args=[purchase_order.id])

    response = authenticated_client.post(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
