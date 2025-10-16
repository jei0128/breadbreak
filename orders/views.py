from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj.user_id == request.user.id


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        qs = Order.objects.select_related("user").prefetch_related("items").order_by("-created_at")
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def set_status(self, request, pk=None):
        order = self.get_object()
        status_value = request.data.get("status")
        valid_statuses = {choice for choice, _ in order.Status.choices}
        if status_value not in valid_statuses:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = status_value
        order.save(update_fields=["status"])
        return Response(OrderSerializer(order).data)
