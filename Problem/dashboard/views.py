from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import App, Subscription, Plan
from .serializers import AppSerializer, PlanSerializer, SubscriptionSerializer
from django.db import transaction

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            self.perform_create(serializer)
            
            free_plan = Plan.objects.get(name="Free")
            Subscription.objects.create(app=self.object, plan=free_plan)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        self.object = serializer.save(owner=self.request.user)

    def get_queryset(self):
        return App.objects.filter(owner=self.request.user)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            plan = Plan.objects.get(id=request.data.get("plan"))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        if plan:
            instance.plan = plan
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return 

    def get_queryset(self):
        return Subscription.objects.filter(app__owner=self.request.user)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()
        
        return Response({"status": "Instance marked as inactive"}, status=status.HTTP_204_NO_CONTENT)