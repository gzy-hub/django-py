# 在admin那边用到的表单验证，在mall面的admin.py中引用
from django import forms

from mall.models import Product


class ProductAdminForm(forms.ModelForm):
    """商品编辑"""

    class Meta:
        model = Product
        # 排除这两个字段
        exclude = ['created_at', 'updated_at']
        widgets = {
            # 修改表单的输入界面（下拉，radio）
            'types': forms.RadioSelect
        }

    def clean_price(self):
        """验证商品的价格"""
        price = self.cleaned_data['price']
        if int(price) <= 0:
            raise forms.ValidationError('销售价格不能小于0')
        return price
