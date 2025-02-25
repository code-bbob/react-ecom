from rest_framework import serializers
from .models import Order, OrderItem, Delivery, Cart
from shop.models import Product
from shop.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Adjust queryset based on your Product model
    product = ProductSerializer(read_only = True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderItemPostSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Adjust queryset based on your Product model
    # product = ProductSerializer(read_only = True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class DeliverySerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Delivery
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()
    delivery = DeliverySerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'orderNumber', 'user', 'created_at', 'updated_at', 'order_items','delivery','status']#yo field ma xai uta ko related name use hunxa

    def get_user(self, obj):
        return obj.user.name

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items', [])
        order = Order.objects.create(**validated_data)

        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)

        return order

class CartSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source='product.product_id', read_only=True)
    image = serializers.SerializerMethodField()
    name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Cart
        fields = ['product_id', 'image', 'quantity','name','price']

    def get_image(self, obj):
        request = self.context.get('request')  # Get request from context
        first_image = obj.product.images.first()  # Get first product image
        
        if first_image and first_image.image:
            image_url = first_image.image.url
            
            # Ensure full URL is generated
            if request is not None:
                return request.build_absolute_uri(image_url)  # Generate absolute URL
        
        return None