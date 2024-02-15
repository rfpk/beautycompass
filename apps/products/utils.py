from apps.products.models import logger


def update_product_rate(product_obj) -> float:
    product_reviews = product_obj.reviews.all()
    count = 0
    if not product_reviews.exists():
        logger.info(f'Product: {product_obj.pk} has not currents reviews for set rating')
        return count
    for review in product_reviews:
        count += review.rating
    new_rating = round(count / len(product_reviews), 2)
    logger.info(f'Product: {product_obj.pk} set new rating value – "{new_rating}"')
    return new_rating
