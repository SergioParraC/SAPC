from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.APUs.models import *
from apps.APUs.api.serializers.apu_serializer import SuppliesInAPUSerializer, APUSerializer

"""Vista generica, contiene todos lo metodos HTTP"""   
class APUDetailsViewSet(viewsets.ModelViewSet):
    queryset = AnalysisOfUnitaryPricesModel.objects.all()
    serializer_class = APUSerializer

    def get_serializer_class(self):
        if self.action in ['supplies_list', 'supply_detail']:
            return SuppliesInAPUSerializer
        return APUSerializer

    @action(detail=True, methods=['get', 'post'], url_path='supplies')
    def supplies_list(self, request, pk=None):
        apu = self.get_object()
        if request.method == 'GET':
            supplies = SuppliesInAPUModel.objects.filter(fk_id_APU=apu)
            serializer = SuppliesInAPUSerializer(supplies, many=True, context=self.get_serializer_context())
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = SuppliesInAPUSerializer(
                data=request.data, 
                context=self.get_serializer_context()
            )
            if serializer.is_valid():
                serializer.save(fk_id_APU=apu)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'put', 'delete'], url_path='supplies/(?P<supply_id>[^/.]+)')
    def supply_detail(self, request, pk=None, supply_id=None):
        apu = self.get_object()
        try:
            supply = SuppliesInAPUModel.objects.get(fk_id_APU=apu, id=supply_id)
        except SuppliesInAPUModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = SuppliesInAPUSerializer(supply, context=self.get_serializer_context())
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = SuppliesInAPUSerializer(supply, data=request.data, partial=True, context=self.get_serializer_context())
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            supply.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        