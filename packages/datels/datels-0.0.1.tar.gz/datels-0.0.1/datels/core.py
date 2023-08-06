import fire
import pandas as pd

def datels(start, end, freq='D', closed='left', format='%Y%m%d'):
    for date in pd.date_range(start=start, end=end, freq=freq, closed=closed):
        print(date.strftime(format))
    return

def main():
    fire.Fire(datels)

if __name__ == "__main__":
    main()