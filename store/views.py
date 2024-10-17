from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductList(ListCreateAPIView):
    # ================================================================================================
    # This method is only useful when you want to have some logic or condition for creating a queryset
    # e.g checking for the current user and depending on its permissions, creating defferent querysets
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    # ================================================================================================
    
    # ================================================================================================
    # This method is only useful when you want to have some logic or condition for the serializer
    # e.g different users or different roles can have different serializer classes
    # def get_serializer_class(self):
    #     return ProductSerializer
    # ================================================================================================
    
    # In this case, there is no need to use the previously mentioned functions
    # Instead we use the "queryset" and "serializer_class" attributes
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({"error": "Product cannot be deleted becuase it's associated with an orderitem."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(product_count=Count('products')), pk=pk)

    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({"error": "Collection cannot be deleted becuase it's associated with a product."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
