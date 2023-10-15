from rest_framework import status, generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from product.models import Product
from product.serializers import ProductDetailsSerializer, ProductListSerializer

# Create your views here.


class ProductListCreateView(APIView):
    """View for creating and listing products"""

    serializer_class = ProductDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        products = Product.objects.all()
        product_list_serializer = ProductListSerializer(instance=products, many=True)

        return Response(data=product_list_serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """View for update, delete and get product by ID"""

    serializer_class = ProductDetailsSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
