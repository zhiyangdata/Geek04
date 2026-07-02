import akshare as ak
from datetime import datetime, timedelta

# 燕京啤酒股票代码
stock_code = "000729"

# 计算近一年的日期范围
end_date = datetime.now().strftime("%Y%m%d")
start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")

# 获取日K线数据
stock_zh_a_hist_df = ak.stock_zh_a_hist(
    symbol=stock_code,
    period="daily",
    start_date=start_date,
    end_date=end_date,
    adjust="qfq"  # 前复权
)

print(f"获取燕京啤酒(000729)近一年日K数据...")
print(f"日期范围: {start_date} 至 {end_date}")
print(f"数据条数: {len(stock_zh_a_hist_df)}")
print("\n数据预览:")
print(stock_zh_a_hist_df.head())

# 保存到CSV文件
csv_filename = f"yanjing_beer_daily_k_{start_date}_{end_date}.csv"
stock_zh_a_hist_df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
print(f"\n数据已保存至: {csv_filename}")