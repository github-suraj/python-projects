# Currency Converter
Provide functionality to pull EXR - Exchange Rates, BP6 - Balance of Payments and International Investment Position (BPM6) from European Central Bank and convert the data (BP6) from the source currency to the target one

## Prerequisite
- Python Version: 3.7+

## Setup environment
- change directory to the project root directory
- Create a virtual environment
    `python -m venv venv`
- Upgrade version for pip
    `python -m pip install pip --upgrade`
- Install dependencies
    `python -m pip install -r requirement.txt`
- Activate Virtual environment
    `. venv/Scripts/activate (Linux)`
    OR
    `venv\Scripts\activate.bat (Windows)`

## Usage

### 1. pull EXR - Exchange Rates
Function is used to retrieve Exchange rate data from the European Central Bank with target currency `EUR` by default. In Example below `GBP` is source currency.

```
>>> from currency_conversion import get_exchange_rate
>>> get_exchange_rate('GBP') 
    TIME_PERIOD  OBS_VALUE
0       1999-01   0.702913
1       1999-02   0.688505
2       1999-03   0.671270
3       1999-04   0.665018
4       1999-05   0.658252
..          ...        ...
279     2022-04   0.836550
280     2022-05   0.849685
281     2022-06   0.857591
282     2022-07   0.849553
283     2022-08   0.844988

[284 rows x 2 columns]
```

### 2. pull BP6 - Balance of Payments and International Investment Position (BPM6)
Function is used to retrieve BP6 - Balance of Payments and International Investment Position (BPM6) raw data from the European Central Bank for a data identifier.
In Example below `M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N` is a data identifier.

```
>>> from currency_conversion import get_raw_data
>>> get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N") 
    TIME_PERIOD     OBS_VALUE
0       1999-01   1427.666667
1       1999-02    379.666667
2       1999-03  -1597.333333
3       1999-04  -3788.666667
4       1999-05   1690.333333
..          ...           ...
277     2022-02  -3776.544917
278     2022-03  -4280.259380
279     2022-04  12755.701376
280     2022-05  -2733.589005
281     2022-06  -9894.277891

[282 rows x 2 columns]
```

### 3. get converted data (BP6) from the source currency to the target one
Function is used to retrieve converted data (BP6) from the source currency to the target one `EUR` by default.
This function can be run in two ways

#### a. target currency not provided
When you do not provide target currency code function will return BP6 raw data for the provided Identifier
Technically same result as with `get_raw_data(identifier)` function
```
>>> from currency_conversion import get_data    
>>> get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N")     
    TIME_PERIOD     OBS_VALUE
0       1999-01   1427.666667
1       1999-02    379.666667
2       1999-03  -1597.333333
3       1999-04  -3788.666667
4       1999-05   1690.333333
..          ...           ...
277     2022-02  -3776.544917
278     2022-03  -4280.259380
279     2022-04  12755.701376
280     2022-05  -2733.589005
281     2022-06  -9894.277891

[282 rows x 2 columns]
```

#### a. target currency provided
When you provide target currency code function will return converted data (BP6) from the source currency to the target one
```
>>> from currency_conversion import get_data                    
>>> get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP")
    TIME_PERIOD     OBS_VALUE
0       1999-01   1003.525460
1       1999-02    261.402399
2       1999-03  -1072.241946
3       1999-04  -2519.531530
4       1999-05   1112.665297
..          ...           ...
279     2022-04  10670.781986
280     2022-05  -2322.689574
281     2022-06  -8485.243671
282     2022-07      0.000000
283     2022-08      0.000000

[284 rows x 2 columns]
```
