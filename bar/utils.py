from datetime import datetime
from random import randint

PENDING, READY, PAID = range(3)
STATUS_CHOICES = (
	(PENDING, 'PENDING'),
	(READY, 'READY'),
	(PAID, 'PAID'),
)

TEL_CODES = [("256", "+256"),]


def generate_order_ref():
	random = randint(1000,9999)
	date = datetime.now().strftime("%Y%m%d%H%M")
	return f"ORDER-{date}-{random}"


def join_telephone(code, telephone, joiner="-"):
	return f"{code}{joiner}{telephone}"

def split_telephone(telephone, splitter="-"):
	if telephone:
		return telephone.split(splitter)
	return ['','']


def create_purchase_from_stock():
	pass