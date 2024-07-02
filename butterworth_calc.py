import sympy as sp
s = sp.symbols('s')

# min_valからmax_valまでの整数を入力
def get_int_input(prompt, min_val, max_val):
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Please enter an integer between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

# 正の整数を入力
def get_positiveint_input(prompt):
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if 0 < value:
                return value
            else:
                print(f"Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

# 正の小数を入力
def get_float_input(prompt):
    while True:
        user_input = input(prompt)
        try:
            value = float(user_input)
            if value > 0:
                return value
            else:
                print(f"Please enter positive demicals.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

# 正の異なる小数2つを入力
def get_2float_input(prompt1, prompt2):
    while True:
        user_input1 = input(prompt1)
        user_input2 = input(prompt2)
        try:
            value1 = float(user_input1)
            value2 = float(user_input2)
            if value1 > 0 and value2 > 0:
                if value1 < value2:
                    return value1, value2
                else:
                    print(f"cutoff1({value1}) must be smaller than cutoff2({value2}).")
            else:
                print("Please enter positive demicals.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Butterworthフィルタについて、与えられた次数の伝達関数の逆数を導出
def calc_1_Fs(n):
    polelist = []
    for i in range(2*n):
        theta  = ((n - 1 + 2*i)*myPI)/(2*n)
        pole = sp.cos(theta) + sp.I * sp.sin(theta)
        polelist.append(sp.simplify(pole))
    # F(s)は極がs平面において左半面にあるもののみで構成する
    filtered_polelist = [i for i in polelist if i.as_real_imag()[0] < 0]
    ans = 1
    # 極(p_i)それぞれにつき、1/F(s)に(s-p_i)を掛け算する
    for p_i in filtered_polelist:
        ans *= (s - p_i)
    ans_out = sp.collect(sp.simplify(sp.expand(ans)), s)
    return ans_out


# 連分数展開(continued fraction expantion)した結果を順々に出力する
def CFE(f):
    # 出力インピーダンスを求めるために、伝達関数を偶数次と奇数次の部分に分ける
    # 偶数次の部分の取得
    even_f = sp.Poly((f + f.as_expr().subs(s, -s))/2, s)  
    even_f = sp.simplify(even_f)
    # 奇数次の部分の取得
    odd_f = f - even_f
    # dividendとdivisorを決定
    ans_list = []
    if odd_f.degree() > even_f.degree():
        dividend  = odd_f
        divisor = even_f
    else:
        dividend  = even_f
        divisor = odd_f
    # sに関する連分数展開を割れなくなるまで実行
    remainder = 1
    while remainder != 0:
        quotient, remainder = sp.div(dividend, divisor, s)
        ans = quotient.coeffs()[0]
        ans_list.append(ans)
        dividend = divisor
        divisor = remainder
    return ans_list

# LPFの周波数変換
def changefreq_LPF(ans_list, Cmode, cutoff, R):
    if (len(ans_list) + Cmode) % 2 != 0:
        changelist = [R / (2 * myPI * cutoff), 1 / (2 * R * myPI * cutoff)] # Inductor
    else:
        changelist = [1 / (2 * R * myPI * cutoff), R / (2 * myPI * cutoff)] # Capacitor
    ans_change = [ans_list[i] * changelist[i%2] for i in range(len(ans_list))]
    return ans_change

# HPFの周波数変換
def changefreq_HPF(ans_list, Cmode, cutoff, R):
    if (len(ans_list) + Cmode) % 2 == 0:
        changelist = [R / (2 * myPI * cutoff), 1 / (2 * R * myPI * cutoff)] # Capacitor
    else:
        changelist = [1 / (2 * R * myPI * cutoff), R / (2 * myPI * cutoff)] # Inductor
    ans_change = [1 / ans_list[i] * changelist[i%2] for i in range(len(ans_list))]
    return ans_change

# BPFの周波数変換
def changefreq_BPF(ans_list, mode, f1, f2, R):
    ans_change = []
    fb = f2 - f1
    f0 = sp.sqrt(f1 * f2)
    for i in range(len(ans_list)):
        if (len(ans_list) + mode + i) % 2 != 0: # 直列部分
            ans_change.append(ans_list[i] * R / (2 * myPI * fb)) # inductor
            ans_change.append(fb / (ans_list[i] * 2 * myPI * f0**2 * R)) # capacitor
        else: # 並列部分
            ans_change.append(fb * R / (ans_list[i] * 2 * myPI * f0**2)) # inductor
            ans_change.append(ans_list[i] / (2 * myPI * fb * R)) # capatitor
    return ans_change

# BEFの周波数変換
def changefreq_BEF(ans_list, mode, f1, f2, R):
    ans_change = []
    fb = f2 - f1
    f_inf = sp.sqrt(f1 * f2)
    for i in range(len(ans_list)):
        if (len(ans_list) + mode + i) % 2 == 0: # 並列部分
            ans_change.append(ans_list[i] * fb * R / (2 * myPI * f_inf**2))
            ans_change.append(1 / (ans_list[i] * 2 * myPI * fb * R))
        else: # 直列部分
            ans_change.append(R / (ans_list[i] * 2 * myPI * fb))
            ans_change.append(fb * ans_list[i] / (2 * myPI * f_inf**2 * R))
    return ans_change

def getunit(a):
    if a % 2 == 0:
        print("First element is INDUCTOR\n")
        unit = ['[H]', '[F]']
    else:
        print("First element is CAPACITOR\n")
        unit = ['[F]', '[H]']
    return unit


# LPFとHPFの出力    
def print_n_curcuits(n, Cmode, Fmode, ans, digits): # LPFとHPF
    ans = [sp.re(ans[i]) for i in range(n)] # 実部のみ取り出す
    print("\n---- result ----")
    unit = getunit(n+Cmode+Fmode)
    for i in range(len(ans)):
        print("element {}: {:.{}e} ".format(i+1, sp.N(ans[i]), digits) + unit[i%2])
    print("--- Latex Output --- ")
    for i in range(len(ans)):
        print("element {}: {:.{}e} ".format(i+1, sp.N(ans[i]), digits) + unit[i%2])

# BPFとBEFの出力
def print_2n_curcuits(n, Cmode, ans, digits): # BPFとBEF
    ans = [sp.re(ans[i]) for i in range(2*n)] # 実部のみ取り出す
    print("\n---- result ----")
    name = ['inductor: ', 'capacitor:']
    unit = ['[H]', '[F]']
    for i in range(2*n):
        if i % 2 == 0:
            print("elements group {} is placed in ".format(i//2+1), end="")
            if (n+Cmode+(i//2))  % 2 == 0:
                print("parallel")
            else:
                print("series")
        print("  {} {:.{}e} ".format(name[i%2], sp.N(ans[i]), digits) + unit[i%2])

# ここから実行部分

# input
fastcalc = get_int_input("select calc mode:\n 1: fast\n 2: precise\n", 1, 2) #　近似解or厳密解
if fastcalc == 1:
    myPI = 3.1415926535
else:
    myPI = sp.pi
Fmode = get_int_input("select filter mode:\n 1: LPF\n 2: HPF\n 3: BPF\n 4: BEF\n", 1, 4) # フィルタの種類
Cmode = get_int_input("select curcuit mode:\n 1: R-inf\n 2: 0-R\n", 1, 2) # 回路の種類
n = get_positiveint_input("enter order: ") # フィルタの次数

text = ["・cutoff frequency\n", ""]
change_text = "select whether you want to change:\n"+text[(Fmode-1)//2]+"・resistance value\n 1: Yes\n 2: No\n"

change = get_int_input(change_text, 1, 2) # 規格化回路から周波数と抵抗の変換を行うかどうか

if change == 1:
    if Fmode == 1 or Fmode == 2: # LPFと HPF
        cutoff =  get_float_input("enter cutoff frequency [Hz]: ") # カットオフ周波数
    R = get_float_input("enter resistance value [Ω]: ")
else: # 規格化回路
    cutoff = 1/(2*myPI)
    R = 1

if Fmode == 3 or Fmode == 4: # BPFとBEF
    f1, f2 = get_2float_input("enter cutoff1 frequency [Hz]: ", "enter cutoff2 frequency [Hz]: ")    

digits = get_positiveint_input("enter the number of digits for result: ") # 素子の値の表示桁数

# calculate
f_transfer = calc_1_Fs(n) # 伝達関数の逆数を計算
ans = CFE(f_transfer) # 連分数展開

# 周波数変換
if Fmode == 1 and change == 1:
    ans = changefreq_LPF(ans, Cmode, cutoff, R)
elif Fmode == 2 and change == 1:
    ans = changefreq_HPF(ans, Cmode, cutoff, R)
elif Fmode == 3:
    ans = changefreq_BPF(ans, Cmode, f1, f2, R)
elif Fmode == 4:
    ans = changefreq_BEF(ans, Cmode, f1, f2, R)

# output
if Fmode == 1 or Fmode == 2:
    print_n_curcuits(n, Cmode, Fmode, ans, digits)
else:
    print_2n_curcuits(n, Cmode, ans, digits)