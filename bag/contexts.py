from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from userprofiles.models import Membership


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            price: settings.STRIPE_PRICE_ID
            item_data = 1
            product = get_object_or_404(Membership, pk=item_id)
            total += item_data * product.price

            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })

        """
        else:
            product = get_object_or_404(Membership, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })
        """

    grand_total = total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
    }

    return context
