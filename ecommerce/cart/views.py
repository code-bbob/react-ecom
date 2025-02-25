from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem,Cart
from .serializers import OrderSerializer, OrderItemSerializer, DeliverySerializer, OrderItemPostSerializer,CartSerializer
from rest_framework.permissions import IsAuthenticated
import random
from rest_framework import generics
from .utils import Util
from shop.models import Product

class   OrderAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print(request.user)
        orders = Order.objects.filter(user=request.user, status = "Unplaced")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        user = request.user
        order_items_data = data.pop('order_items', [])
        print(data)
        order_serializer = OrderSerializer(data=data)
        if order_serializer.is_valid(raise_exception=True):
            print("hehehehehehe")
            order = order_serializer.save(user=user)
            print(order)
            order_items_serializer = OrderItemPostSerializer(data=order_items_data, many=True)
            print(order_items_serializer)
            if order_items_serializer.is_valid(raise_exception=True):
                order_items_serializer.save(order=order)
                return Response(order_serializer.data, status=status.HTTP_201_CREATED)
            else:
                order.delete()  # Rollback order creation if order_items are not valid
                return Response(order_items_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
    # Assuming you're using the user's ID to identify their order
        user = request.user
        order = Order.objects.filter(user=user,status="Unplaced").first()
        print(order)
        serializer = OrderSerializer(order)

        if order:
            order_items_data = request.data.get('order_items', [])

            # Loop through order_items_data and update existing instances
            for order_item_data in order_items_data:
                product_id = order_item_data.get('product')
                quantity = order_item_data.get('quantity')
                if (quantity == 0):
                    OrderItem.objects.filter(order=order, product_id=product_id).delete()
                else:   
                # Get or create an existing order item based on product_id
                    order_item, created = OrderItem.objects.get_or_create(order=order, product_id=product_id)

                    # Update the quantity
                    order_item.quantity = quantity
                    order_item.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

# class CheckoutView(APIView):
#     permission_classes=[IsAuthenticated]
#     def post(self, request):
#         user=request.user
#         order=Order.objects.filter(user=user, status ="Unplaced").first()
#         print(user)
#         order.status="Placed"
#         order.save()
#         body = 'A new order has been placed '+ str(order) + '\nPlease check the admin page for more details and dont forget to set the status to clear after it is cleared'
#         data = {
#         'subject':'New order Placed',
#         'body':body,
#         'to_email':'bbobbasnet@gmail.com'
#       } 
#         Util.send_email(data)
#         return Response(status=status.HTTP_200_OK)
    

class CheckoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        user=request.user
        order=Order.objects.filter(user=user, status ="Unplaced").first()
        serializer = DeliverySerializer(data=request.data)  
        if serializer.is_valid():
            serializer.save(order=order)
            order.status="Placed"
            order.save()
            body = 'A new order has been placed '+ str(order) + '\nPlease check the admin page for more details and dont forget to set the status to clear after it is cleared'
            data = {
            'subject':'New order Placed',
            'body':body,
            'to_email':'bbobbasnet@gmail.com'
            } 
            # Util.send_email(data)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({''},status=status.HTTP_400_BAD_REQUEST)
        
# class CartView(APIView):
    
#     permission_classes=[IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         cart = Cart.objects.filter(user=user)
#         serializer = CartSerializer(cart, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         data = request.data
#         user = request.user
#         id = data.get('product')
#         product = Product.objects.get(pk=id )
#         data['product'] = product
#         quantity = data.get('quantity')
#         serializer = CartSerializer(data=data,many=True)
#         if serializer.is_valid():
#             serializer.save(user=user, product=product, quantity=quantity)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartView(APIView):
    """Manage the shopping cart"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all cart items for the authenticated user"""
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        """Add a product to the cart"""
        data = request.data  # Extract request data
        product_id = data.get('product_id')  # Get product ID from request

        # Ensure product ID is provided
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Try to fetch the Product instance
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get quantity (default is 1)
        quantity = int(data.get('quantity', 1))
        price = int(data.get('price', 0))

        # Check if the product is already in the cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product,
            defaults={'quantity': quantity,'price':price}
        )

        # If item exists, update quantity
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({
            "message": "Added to cart",
            "item": CartSerializer(cart_item).data
        }, status=status.HTTP_201_CREATED)

    def patch(self, request):
        """Update a cart item's quantity"""
        data = request.data
        product_id = data.get('product_id')
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the product instance
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the corresponding cart item
        try:
            cart_item = Cart.objects.get(user=request.user, product=product)
        except Cart.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

        # Get and validate the new quantity
        quantity = data.get('quantity')
        if quantity is None:
            return Response({"error": "Quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity < 1:
                return Response({"error": "Quantity must be at least 1"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = quantity
        cart_item.save()

        return Response({
            "message": "Cart item updated",
            "item": CartSerializer(cart_item).data
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        """Remove a product from the cart"""
        data = request.data  # Extract request data
        product_id = data.get('product_id')  # Use product_id consistently

        # Ensure product ID is provided
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the product instance
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = Cart.objects.get(user=request.user, product=product)
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

class MergeCartView(APIView):
    """
    Merge the unauthenticated cart (sent from the client) with the user's cart.
    Expected payload:
    {
      "items": [
        {"product_id": "550e8400-e29b-41d4-a716-446655440000", "quantity": 2},
        {"product_id": "660e8400-e29b-41d4-a716-446655440000", "quantity": 1},
        ...
      ]
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        items = request.data.get("items", [])
        if not items:
            return Response({"message": "No items provided for merging."},
                            status=status.HTTP_400_BAD_REQUEST)

        merged_cart_items = []

        for item_data in items:
            product_id = item_data.get("product_id")
            quantity = item_data.get("quantity", 1)
            price = item_data.get("price", 0)
            
            if not product_id:
                continue  # Skip items without a product_id

            try:
                # Assuming your Product model uses product_id as its UUID primary key
                product = Product.objects.get(product_id=product_id)
            except Product.DoesNotExist:
                continue  # Skip invalid products

            # Try to get an existing cart item for this product and user
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={"quantity": quantity,"price":price}
            )
            if not created:
                # If the item exists, update its quantity by adding the new quantity
                cart_item.quantity += quantity
                cart_item.save()

            merged_cart_items.append(cart_item)

        # Serialize and return the merged cart items
        serializer = CartSerializer(merged_cart_items, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
