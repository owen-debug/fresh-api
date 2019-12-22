from django_redis import get_redis_connection

from utils.views import ReadOnlyModelViewSet
from . import models
from . import serializers


class GoodsApi(ReadOnlyModelViewSet):
    """商品api"""
    queryset = models.Goods.objects.all()
    serializer_class = serializers.GoodsModelSerializer


class GoodsTypeApi(ReadOnlyModelViewSet):
    """商品类型"""
    queryset = models.GoodsType.objects.all()
    serializer_class = serializers.GoodsTypeModelSerializer


class GoodsBannerApi(ReadOnlyModelViewSet):
    """商品的banner"""
    queryset = models.IndexGoodsBanner.objects.all()
    serializer_class = serializers.GoodsBannerModelSerializer


class GoodsSkuApi(ReadOnlyModelViewSet):
    """GoodsSku"""
    queryset = models.GoodsSKU.objects.all()
    serializer_class = serializers.GoodsSkuModelSerializer
    filterset_fields = ['type']

    def get_object(self):
        obj = super(GoodsSkuApi, self).get_object()
        user = self.request.user
        # 添加用户的浏览记录
        if user.is_authenticated:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            pk = self.kwargs[lookup_url_kwarg]
            # 添加用户的历史浏览记录
            coon = get_redis_connection('default')
            history_key = 'history_%d' % user.id
            # 移除之前的该商品id
            coon.lrem(history_key, 0, pk)
            # 把goods_id左侧插入redis列表
            coon.lpush(history_key, pk)
            # 取用户保存的最新5条信息
            coon.ltrim(history_key, 0, 4)
        return obj


class GoodsImageApi(ReadOnlyModelViewSet):
    """商品的图片"""
    queryset = models.GoodsImage.objects.all()
    serializer_class = serializers.GoodsImageModelSerializer


class IndexTypeGoodsBannerApi(ReadOnlyModelViewSet):
    """IndexTypeGoodsBanner"""
    queryset = models.IndexTypeGoodsBanner.objects.all()
    serializer_class = serializers.IndexTypeGoodsBannerModelSerializer


class IndexPromotionBannerApi(ReadOnlyModelViewSet):
    queryset = models.IndexPromotionBanner.objects.all()
    serializer_class = serializers.IndexPromotionBannerModelSerializer
