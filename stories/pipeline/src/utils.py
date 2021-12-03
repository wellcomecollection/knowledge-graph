import httpx

http_client = httpx.Client(timeout=None)


def clean(input_string):
    return input_string.strip().lower().replace(",", "")


def clean_csv(input_string):
    return [clean(y) for y in str(input_string).split(", ") if y != ""]
