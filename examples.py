import stock_quality_score as qs
from get_all_tickers import get_tickers as gt
import warnings
warnings.filterwarnings("ignore")

# some example tickers
my_tickers = ['AAPL','MCD','SAP']
result = qs.quality_scores_30y(tickers = my_tickers)

# all unique tickers
all_tickers = gt.get_tickers()
all_tickers = list(set(all_tickers))
result = qs.quality_scores_30y(tickers = all_tickers) # takes long time

# calculate sum of decade scores and sort
result['score_sum'] = result.fillna(0).score_1990s + result.fillna(0).score_2000s + result.fillna(0).score_2010s
result = result.sort_values(by='score_sum', ascending=False)