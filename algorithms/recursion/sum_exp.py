
def sum_exp(b, n):
    if n == 0:
        return 1
    else:
        return b + sum_exp(b, n - 1)

def main():
    print(sum_exp(2, 4))

if __name__ == '__main__':
    main()
