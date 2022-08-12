

def make_readable(seconds):
    hours =  f"0{seconds//3600}" if (seconds//3600) < 10 else (seconds//3600)
    minutes = f"0{(seconds - ((seconds//3600)*3600)) // 60}" if (seconds - ((seconds//3600)*3600)) // 60 < 10  else (seconds - ((seconds//3600)*3600)) // 60
    seconds =  f"0{seconds - seconds//3600 * 3600 - ((seconds - ((seconds//3600)*3600)) // 60) *60}" if seconds - seconds//3600 * 3600 - ((seconds - ((seconds//3600)*3600)) // 60) *60 < 10 else seconds - seconds//3600 * 3600 - ((seconds - ((seconds//3600)*3600)) // 60) *60
    return f"{hours}:{minutes}:{seconds}"

print(make_readable(5))