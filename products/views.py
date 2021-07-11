from django.shortcuts import render
from .models import Product, Purchase
import pandas as pd
from .utils import get_simple_plot, get_sales_man_from_id, get_image
from .forms import PurchaseForm
import matplotlib.pyplot as plt
import seaborn as sns
from django.contrib.auth.decorators import login_required


@login_required
def salesDistView(request):
    df = pd.DataFrame(Purchase.objects.all().values())
    print(df)
    df['sales_man_id'] = df['sales_man_id'].apply(get_sales_man_from_id)
    df.rename({'sales_man_id': 'salesman'}, axis=1, inplace=True)
    df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    plt.switch_backend('Agg')
    plt.xticks(rotation=45)
    sns.barplot(x='date', y='total_price', hue='salesman', data=df)
    plt.tight_layout()
    graph = get_image()

    context = {
        'graph': graph,
    }
    return render(request, 'products/sales.html', context)


@login_required
def char_select_view(request):
    graph = None
    error_message = None
    df = None
    price = None

    try:
        product_df = pd.DataFrame(Product.objects.all().values())
        purchase_df = pd.DataFrame(Purchase.objects.all().values())
        product_df['product_id'] = product_df['id']

        if purchase_df.shape[0] > 0:
            df = pd.merge(purchase_df, product_df, on='product_id').drop(['id_y', 'date_y'], axis=1).rename({'id_x': 'id',
                                                                                                             'date_x': 'date'},
                                                                                                            axis=1)
            price = df['price']
            if request.method == 'POST':
                chart_type = request.POST.get('sales')
                date_from = request.POST['date_from']
                date_to = request.POST['date_to']
                df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
                df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')

                if chart_type != "":
                    if date_from != "" and date_to != "":
                        df = df[(df['date'] > date_from) & (df['date'] < date_to)]
                        df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')
                    graph = get_simple_plot(chart_type, x=df2['date'], y=df2['total_price'], data=df)
                else:
                    error_message = 'please select a chart type to continue'
        else:
            error_message = 'No records in database'
    except:
        product_df = None
        purchase_df = None
        error_message = 'No records in database'

    context = {
        'graph': graph,
        'price': price,
        'error_message': error_message,
    }
    return render(request, 'products/main.html', context)


@login_required
def add_purchase_view(request):
    form = PurchaseForm(request.POST or None)
    added_message = None

    if form.is_valid():
        obj = form.save(commit=False)
        obj.sales_man = request.user
        obj.save()

        form = PurchaseForm()
        added_message = "The purchase has been added"
    context = {
        'form': form,
        'added_message': added_message,
    }
    return render(request, 'products/add_purchase.html', context)
