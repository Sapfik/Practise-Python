

def peak_height(mountain):
    mountain = [i.replace(' ', '') for i in mountain][2:]
    mountain = mountain[:-2]
    return min(mountain, key=len)
    # return min(mountain, key=len)

print(peak_height([
          "^^^^^^        ",
          " ^^^^^^^^     ",
          "  ^^^^^^^     ",
          "  ^^^^^       ",
          "  ^^^^^^^^^^^ ",
          "  ^^^^^^      ",
          "  ^^^^        "
        ]   ))