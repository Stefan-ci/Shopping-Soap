import datetime
from products.models import Soap
from hitcount.models import Hit
from orders.models import Order
from contacts.models import Contact
from refunds.models import Refund
from reports.models import Sales, Expenses
from django.contrib.auth.models import User
from reports.utils import sales_made, expenses_made
from reports.utils import sales_made, expenses_made, monthly_sales, monthly_expenses



def generic_data(request):
	date = datetime.datetime.now()
	curr_month = date.month
	curr_year = date.year

	not_granted_refunds_count = Refund.objects.filter(
		accepted=False).count()
	all_refunds_list = Refund.objects.all()
	all_refunds_count = Refund.objects.all().count()
	unread_contacts_count = Contact.objects.filter(
		unread=True,
		is_answered=False,
		deleted=False).count()
	unread_contacts_nav_list = Contact.objects.filter(
		unread=True,
		is_answered=False,
		deleted=False)[:8]
	unread_contacts_list = Contact.objects.filter(
		unread=True,
		is_answered=False,
		deleted=False)[:50]
	not_received_orders_count = Order.objects.filter(
		ordered=True,
		being_delivered=True,
		received=False,
	).count()
	not_delivered_orders_count = Order.objects.filter(
		ordered=True,
		being_delivered=False,
		received=False,
	).count()

	complete_orders_count = Order.objects.filter(ordered=True).count()
	
	total_sales_count = Sales.objects.all().count()
	total_expenses_count = Expenses.objects.all().count()

	not_complete_orders_count = Order.objects.filter(ordered=False).count()

	total_hits = Hit.objects.all().count()

	new_added_items_count = Soap.objects.filter(date__month=8).count()

	total_items_count = Soap.objects.all().count()

	lambda_users_count = User.objects.filter(is_staff=False, is_superuser=False).count()
	superusers_count = User.objects.filter(is_superuser=True).count()
	staff_users_count = User.objects.filter(is_staff=True, is_superuser=False).count()
	users_count = User.objects.all().count()

	total_orders_count = Order.objects.filter(ordered=True).count()

	# Sales' annual chart reports data (getting by month)
	# Sale means that payment done successfully. So we will work with `Payment` model
	jan_sale = Sales.objects.filter(date__month=1).count()
	feb_sale = Sales.objects.filter(date__month=2).count()
	march_sale = Sales.objects.filter(date__month=3).count()
	apr_sale = Sales.objects.filter(date__month=4).count()
	may_sale = Sales.objects.filter(date__month=5).count()
	jun_sale = Sales.objects.filter(date__month=6).count()
	jul_sale = Sales.objects.filter(date__month=7).count()
	aug_sale = Sales.objects.filter(date__month=8).count()
	sept_sale = Sales.objects.filter(date__month=9).count()
	oct_sale = Sales.objects.filter(date__month=10).count()
	nov_sale = Sales.objects.filter(date__month=11).count()
	dec_sale = Sales.objects.filter(date__month=12).count()


	jan_expense = Expenses.objects.filter(date__month=1).count()
	feb_expense = Expenses.objects.filter(date__month=2).count()
	march_expense = Expenses.objects.filter(date__month=3).count()
	apr_expense = Expenses.objects.filter(date__month=4).count()
	may_expense = Expenses.objects.filter(date__month=5).count()
	jun_expense = Expenses.objects.filter(date__month=6).count()
	jul_expense = Expenses.objects.filter(date__month=7).count()
	aug_expense = Expenses.objects.filter(date__month=8).count()
	sept_expense = Expenses.objects.filter(date__month=9).count()
	oct_expense = Expenses.objects.filter(date__month=10).count()
	nov_expense = Expenses.objects.filter(date__month=11).count()
	dec_expense = Expenses.objects.filter(date__month=12).count()

	# Users' annual chart reports data (getting by month)
	jan_user = User.objects.filter(date_joined__month=1).count()
	feb_user = User.objects.filter(date_joined__month=2).count()
	march_user = User.objects.filter(date_joined__month=3).count()
	apr_user = User.objects.filter(date_joined__month=4).count()
	may_user = User.objects.filter(date_joined__month=5).count()
	jun_user = User.objects.filter(date_joined__month=6).count()
	jul_user = User.objects.filter(date_joined__month=7).count()
	aug_user = User.objects.filter(date_joined__month=8).count()
	sept_user = User.objects.filter(date_joined__month=9).count()
	oct_user = User.objects.filter(date_joined__month=10).count()
	nov_user = User.objects.filter(date_joined__month=11).count()
	dec_user = User.objects.filter(date_joined__month=12).count()

	total_sales_made = sales_made()
	curr_month_sales = monthly_sales(curr_month)
	total_expenses_made = expenses_made()
	curr_month_expenses = monthly_expenses(curr_month)
	total_profits_made = total_sales_made - total_expenses_made

	context = {
		'not_received_orders_count': not_received_orders_count,
		'not_delivered_orders_count': not_delivered_orders_count,
		'total_orders_count': total_orders_count,

		'unread_contacts_count': unread_contacts_count,
		'unread_contacts_list': unread_contacts_list,
		'unread_contacts_nav_list': unread_contacts_nav_list,

		'all_refunds_list': all_refunds_list,
		'all_refunds_count': all_refunds_count,
		'not_granted_refunds_count': not_granted_refunds_count,

		'total_sales_count': total_sales_count,
		'total_expenses_count': total_expenses_count,
		'curr_month_sales': curr_month_sales,
		'curr_month_expenses': curr_month_expenses,

		'jan_sale': jan_sale,
		'feb_sale': feb_sale,
		'march_sale': march_sale,
		'apr_sale': apr_sale,
		'may_sale': may_sale,
		'jun_sale': jun_sale,
		'jul_sale': jun_sale,
		'aug_sale': aug_sale,
		'sept_sale': sept_sale,
		'oct_sale': oct_sale,
		'nov_sale': nov_sale,
		'dec_sale': dec_sale,

		'jan_expense': jan_expense,
		'feb_expense': feb_expense,
		'march_expense': march_expense,
		'apr_expense': apr_expense,
		'may_expense': may_expense,
		'jun_expense': jun_expense,
		'jul_expense': jun_expense,
		'aug_expense': aug_expense,
		'sept_expense': sept_expense,
		'oct_expense': oct_expense,
		'nov_expense': nov_expense,
		'dec_expense': dec_expense,

		'jan_user': jan_user,
		'feb_user': feb_user,
		'march_user': march_user,
		'apr_user': apr_user,
		'may_user': may_user,
		'jun_user': jun_user,
		'jul_user': jun_user,
		'aug_user': aug_user,
		'sept_user': sept_user,
		'oct_user': oct_user,
		'nov_user': nov_user,
		'dec_user': dec_user,

		'mon_visits': daily_visits(1, curr_month, curr_year),
		'tue_visits': daily_visits(2, curr_month, curr_year),
		'wed_visits': daily_visits(3, curr_month, curr_year),
		'thus_visits': daily_visits(4, curr_month, curr_year),
		'fri_visits': daily_visits(5, curr_month, curr_year),
		'sat_visits': daily_visits(6, curr_month, curr_year),
		'sun_visits': daily_visits(7, curr_month, curr_year),

		'jan_sale_amount': monthly_sales(1),
		'feb_sale_amount': monthly_sales(2),
		'march_sale_amount': monthly_sales(3),
		'apr_sale_amount': monthly_sales(4),
		'may_sale_amount': monthly_sales(5),
		'jun_sale_amount': monthly_sales(6),
		'jul_sale_amount': monthly_sales(7),
		'aug_sale_amount': monthly_sales(8),
		'sept_sale_amount': monthly_sales(9),
		'oct_sale_amount': monthly_sales(10),
		'nov_sale_amount': monthly_sales(11),
		'dec_sale_amount': monthly_sales(12),

		'jan_expense_amount': monthly_expenses(1),
		'feb_expense_amount': monthly_expenses(2),
		'march_expense_amount': monthly_expenses(3),
		'apr_expense_amount': monthly_expenses(4),
		'may_expense_amount': monthly_expenses(5),
		'jun_expense_amount': monthly_expenses(6),
		'jul_expense_amount': monthly_expenses(7),
		'aug_expense_amount': monthly_expenses(8),
		'sept_expense_amount': monthly_expenses(9),
		'oct_expense_amount': monthly_expenses(10),
		'nov_expense_amount': monthly_expenses(11),
		'dec_expense_amount': monthly_expenses(12),

		'total_hits': total_hits,
		'users_count': users_count,
		'total_sales_made': total_sales_made,
		'total_profits_made': total_profits_made,
		'superusers_count': superusers_count,
		'total_expenses_made': total_expenses_made,
		'total_items_count': total_items_count,
		'staff_users_count': staff_users_count,
		'lambda_users_count': lambda_users_count,
		'complete_orders_count': complete_orders_count,
		'new_added_items_count': new_added_items_count,
		'not_complete_orders_count': not_complete_orders_count,
	}

	return context


def daily_visits(day, month, year):
	day = int(day)
	month = int(month)
	year = int(year)
	visits = Hit.objects.filter(
		created__day=day,
		created__month=month,
		created__year=year).count()
	if visits is None:
		visits = 0
	return visits
