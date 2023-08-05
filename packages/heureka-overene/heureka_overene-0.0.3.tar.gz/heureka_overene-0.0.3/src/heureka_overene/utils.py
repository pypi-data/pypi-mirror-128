import re

user_regex = re.compile(
	r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
	r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
	re.IGNORECASE
)

domain_regex = re.compile(
	# max length for domain name labels is 63 characters per RFC 1034
	r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',
	re.IGNORECASE
)

def is_valid_email(email: str) -> bool:
	if '@' not in email:
		return False
	user, domain = email.rsplit('@', 1)
	return user_regex.match(user) and domain_regex.match(domain)