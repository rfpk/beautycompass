from apps.products.models import Product
from apps.profile.tasks import logger
from config.celery_settings import app
from datetime import datetime, timedelta


@app.task(max_retries=1, default_retry_delay=5)
def check_product_status():
    three_months_ago = datetime.now() - timedelta(days=3 * 30)
    new_products = Product.objects.filter(new_status=True, created_at__lte=three_months_ago)
    if new_products:
        new_products.update(new_status=False)
        logger.info(f'Status novelty of products {new_products.values_list("id", flat=True)} was changed: True')
