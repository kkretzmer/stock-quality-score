import pandas as pd
from pandas_datareader import data
import math
from datetime import date

def calculate_scores(data):
    if len(data) == 0:
        return math.nan, math.nan
    else:
        #relative stock performance
        data_pct = (data - data.iloc[0])/data.iloc[0]*100
        
        #yearly stock performance
        data_year = data.groupby([data.index.year]).apply(lambda x: (x.iloc[-1]-x.iloc[0])/x.iloc[0]*100)
        year_median = data_year.median()
        cagr = (((data_pct.iloc[-1] / 100 + 1) ** (1/data_year.index.size) - 1) * 100)
        
        return cagr, year_median


def quality_scores_30y(tickers, start_date = '1990-01-01', end_date = date.today().strftime('%Y-%m-%d')):
    stock_result = pd.DataFrame()

    for ticker in tickers:
        try:
            stock_data = data.DataReader([ticker], 'yahoo', start_date, end_date)
        except:
            continue
        stock_data = stock_data[~stock_data.index.duplicated(keep='first')]
        stock_data = stock_data.loc[:,'Close']
        
        stock_data_1990s = stock_data[(stock_data.index.year >= 1990) & (stock_data.index.year < 2000)] if 1990 in stock_data.index.year else pd.DataFrame()
        stock_data_2000s = stock_data[(stock_data.index.year >= 2000) & (stock_data.index.year < 2010)] if 2000 in stock_data.index.year else pd.DataFrame()
        stock_data_2010s = stock_data[(stock_data.index.year >= 2010) & (stock_data.index.year < 2020)] if 2010 in stock_data.index.year else pd.DataFrame()
        
        stock_data_l3ys = stock_data[(stock_data.index >= date(date.today().year-3, date.today().month, date.today().day).strftime('%Y-%m-%d'))] if date.today().year-3 in stock_data.index.year else pd.DataFrame()
        stock_data_l5ys = stock_data[(stock_data.index >= date(date.today().year-5, date.today().month, date.today().day).strftime('%Y-%m-%d'))] if date.today().year-5 in stock_data.index.year else pd.DataFrame()
        stock_data_l10ys = stock_data[(stock_data.index >= date(date.today().year-10, date.today().month, date.today().day).strftime('%Y-%m-%d'))] if date.today().year-10 in stock_data.index.year else pd.DataFrame()
        stock_data_l20ys = stock_data[(stock_data.index >= date(date.today().year-20, date.today().month, date.today().day).strftime('%Y-%m-%d'))] if date.today().year-20 in stock_data.index.year else pd.DataFrame()
        
        cagr_total, median_total = calculate_scores(stock_data)
        cagr_1990s, median_1990s = calculate_scores(stock_data_1990s)
        cagr_2000s, median_2000s = calculate_scores(stock_data_2000s)
        cagr_2010s, median_2010s = calculate_scores(stock_data_2010s)
        cagr_l3ys, median_l3ys = calculate_scores(stock_data_l3ys)
        cagr_l5ys, median_l5ys = calculate_scores(stock_data_l5ys)
        cagr_l10ys, median_l10ys = calculate_scores(stock_data_l10ys)
        cagr_l20ys, median_l20ys = calculate_scores(stock_data_l20ys)
        
        tmp_result = pd.DataFrame({'score_1990s': cagr_1990s+median_1990s,
                                   'score_2000s': cagr_2000s+median_2000s,
                                   'score_2010s': cagr_2010s+median_2010s,
                                   'score_l20ys': cagr_l20ys+median_l20ys,
                                   'score_l10ys': cagr_l10ys+median_l10ys,
                                   'score_l5ys': cagr_l5ys+median_l5ys,
                                   'score_l3ys': cagr_l3ys+median_l3ys,
                                   'score_total': cagr_total+median_total,
                                   'cagr_total': cagr_total,
                                   'median_total': median_total,
                                   'years_total': stock_data.index.year.nunique()
                                  })
        
        stock_result = pd.concat([stock_result, tmp_result])
    
    stock_result = stock_result.round(1)
    return stock_result