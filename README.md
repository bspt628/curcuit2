## butterworthcalc.pyの作成
任意の次数のButterworthフィルタの素子の値を計算するプログラムをpythonのsympyを用いて作成しました。


## コンパイル方法
butterworthcalc.pyをダウンロード後、実行するだけで動きます。

## 入力
素子の値を計算するための条件が順々に表示され、指示された通りユーザーが入力を行っていくインタラクティブ形式をとっています。
提示された選択肢以外の値や、数に変換できない入力など、不適切な入力を受け付けた場合はエラーを返し再度入力が求められます。

### 計算モード
```
select calc mode:
 1: fast
 2: precise
```
計算精度を選択します。
- 1を選択した場合近似解が計算されます。具体的には計算中に用いる円周率の値を’3.1415926535’に近似することでこれが実現されます。
  どのような次数についても計算結果が与えられます（最大で、次数1000について確認済み）
- 2を選択した場合厳密解が計算されます。sympyモジュールを活用して、平方根や円周率などを数値で近似することなく計算が行われます。
  次数によっては、計算結果が与えられずプログラムがフリーズしてしまうことがあります。（次数7の時などで確認済み）

### フィルタモード
```
select filter mode:
 1: LPF
 2: HPF
 3: BPF
 4: BEF
```
フィルタの種類を選択します。
- 1を選択した場合、ローパスフィルタ（LPF）の計算が行われます。
- 2を選択した場合、ハイパスフィルタ（HPF）の計算が行われます。
- 3を選択した場合、バンドパスフィルタ（BPF）の計算が行われます。
- 4を選択した場合、バンドエリミネーションフィルタ（BEF）の計算が行われます。

### 回路モード
```
select curcuit mode:
 1: R-inf
 2: 0-R
```
回路の種類を選択します。
- 1を選択した場合、R-∞ 型回路の計算が行われます。
- 2を選択した場合、0-R 型回路の計算が行われます。
  
いずれの場合も、出力される素子の番号の順番は、設計した抵抗素子に近い順番となっています。

### フィルタの次数
```
enter order:
```
フィルタの次数を自然数で入力します。

### 周波数・抵抗成分変換
設計する回路によって表示が変わります。
#### LPF・HPFの設計時
```
select whether you want to change:
・cutoff frequency
・resistance value
 1: Yes
 2: No
```
- 1を選択した場合、カットオフ周波数と抵抗素子の値を任意に決定することができます。
- 2を選択した場合、カットオフ角周波数が1 [rad/s], 抵抗素子の値が1 [Ω]として計算が行われます。

#### BPF・BEFの設計時
```
select whether you want to change:
・cutoff frequency
 1: Yes
 2: No
```
- 1を選択した場合、抵抗素子の値を任意に決定することができます。
- 2を選択した場合、抵抗素子の値が1 [Ω]として計算が行われます。

### 遮断周波数の決定(BPF・BEFのみ)
```
enter cutoff1 frequency [Hz]:
enter cutoff2 frequency [Hz]: 
```
BPF・BEFを選択した時のみ、2つの遮断周波数を入力します。
1つ目の入力値よりも、2つめの入力値は大きい値にすることが求められます。

### 出力結果の表示桁数
```
enter the number of digits for result: 
```
計算した素子の出力結果の表示桁数を自然数で入力します。

## 出力
各フィルタごと、出力結果の見方を説明します。

### LPF・HPFの設計時
4次のR-∞ 型規格化LPFの例をとって説明します。
```
---- result ----
First element is INDUCTOR

element 1: 3.82683e-1 [H]
element 2: 1.08239e+0 [F]
element 3: 1.57716e+0 [H]
element 4: 1.53073e+0 [F]
```
- 素子の番号は、設計した抵抗素子に近い順に並んでいます。つまり、R-∞ 型を選択した場合は入力側、0-R 型を選択した場合は出力側から素子が並んでいます。
- 初めの素子については、キャパシタかインダクタかのどちらかが明記されます。それ以降は、キャパシタとインダクタが交互に配置されます。
- LPFについては、インダクタを直列に、キャパシタを並列に配置します。
- HPFについては、インダクタを並列に、キャパシタを直列に配置します。

### BPF・BEFの設計時
3次の0-R 型BPFの例をとって説明します。
```
---- result ----
elements group 1 is placed in series
  inductor:  8.84194e-3 [H]
  capacitor: 2.86479e-1 [F]
elements group 2 is placed in parallel
  inductor:  1.07430e-1 [H]
  capacitor: 2.35785e-2 [F]
elements group 3 is placed in series
  inductor:  2.65258e-2 [H]
  capacitor: 9.54930e-2 [F]
```
- BPF・BEFの場合は、LPF・HPFの倍の個数の素子が使用され、キャパシタとインダクタがそれぞれ直列または並列に接続され、さらに回路に直列または並列に接続された上で使用されます。
- 素子群の番号は、LPF・HPFと同じく設計した抵抗素子に近い順に並んでいます。
- `elements group x is placed in series`と表示されているときは、下に与えられたキャパシタとインダクタを直列に接続します。
- `elements group x is placed in parallel`と表示されているときは、下に与えられたキャパシタとインダクタを並列に接続します。
- `element group 1`を回路に対して直列に配置するか並列に配置するかは、同次数で抵抗素子の位置が同じLPFの1番目の素子がインダクタかキャパシタかによって決まり、次の表のように対応します。
  
| LPF        | BPF              | BEF              | 
| ---------- | ---------------- | ---------------- | 
| インダクタ | 回路に直列に配置 | 回路に並列に配置 | 
| キャパシタ | 回路に並列に配置 | 回路に直列に配置 | 

以上のように出力を読み取り回路を設計することで、所望の機能を実現するフィルタを実現することができます。

### おまけ・Latex出力
最後の選択肢で1を選ぶと、伝達関数と素子の値をLatex形式で出力することができます。
```
Need latex output?:
 1: Yes
 2: No
```
以下が出力例です。4次のR-∞ 型正規化LPFの例を示します。

---- result ----

Transfer function

$$ n = 4,  F(s) = \frac{1}{s^{4} + s^{3} \left(\sqrt{2 - \sqrt{2}} + \sqrt{\sqrt{2} + 2}\right) + s^{2} \left(\sqrt{2} + 2\right) + s \left(\sqrt{2 - \sqrt{2}} + \sqrt{\sqrt{2} + 2}\right) + 1} $$

Approximate solution

$$ F(s) = \frac{1}{s^{4} + 2.6131 s^{3} + 3.4142 s^{2} + 2.6131 s + 1.0} $$

the value of elements

First element is INDUCTOR

the value of elements

First element is INDUCTOR

$$ element 1: \frac{1}{\sqrt{2 - \sqrt{2}} + \sqrt{\sqrt{2} + 2}} (\simeq 0.38268)\,\mathrm{[H]} $$

$$ element 2: - \sqrt{\sqrt{2} + 2} - \sqrt{2 - \sqrt{2}} + \sqrt{2} \sqrt{2 - \sqrt{2}} + \sqrt{2} \sqrt{\sqrt{2} + 2} (\simeq 1.0824)\,\mathrm{[F]} $$

$$ element 3: \frac{2 + \frac{3 \sqrt{2}}{2}}{\sqrt{2 - \sqrt{2}} + \sqrt{\sqrt{2} + 2}} (\simeq 1.5772)\,\mathrm{[H]} $$

$$ element 4: - \sqrt{2} \sqrt{\sqrt{2} + 2} - \sqrt{2} \sqrt{2 - \sqrt{2}} + 2 \sqrt{2 - \sqrt{2}} + 2 \sqrt{\sqrt{2} + 2} (\simeq 1.5307)\,\mathrm{[F]} $$


