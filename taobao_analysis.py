import pandas as pd
import datetime
# 1. 读取数据
file_path = 'UserBehavior.csv'
# 定义列名
columns = ['user_id', 'item_id', 'category_id', 'behavior', 'timestamp']
# 读取csv文件，指定列名，读取10w行
df = pd.read_csv(file_path, header=None, names=columns, nrows=100000)

# 2. 概览数据
# 查看数据前5行
print("=== 数据前5行 ===")
print(df.head())
# 查看数据基本信息
print("\n=== 数据基本信息 ===")
print(df.info())
# 统计每种行为类型的数量
print("\n=== 每种行为类型的数量 ===")
print(df['behavior'].value_counts())

# 3. 时间戳转换
# 将时间戳转化为日期格式
df['date'] = pd.to_datetime(df['timestamp'], unit='s')
# 去除时分秒，保留日期
df['date'] = df['date'].dt.date
# 查看转换后结果
print("\n=== 日期转换后前5行 ===")
print(df[['user_id', 'behavior', 'date']].head())
# 查看数据时间范围
print("\n=== 数据日期范围 ===")
print("最早日期:", df['date'].min())
print("最晚日期:", df['date'].max())

# 4. 分析用户行为
# 根据收藏行为，按商品类型ID分组统计数量，取前10名
fav_items = df[df['behavior'] == 'fav']['category_id'].value_counts().head(10)
print("\n=== 收藏最多的10个商品类目 ===")
print(fav_items)

# 5. 分析收藏多购买少的品类ID
category_stats = df.groupby('category_id')['behavior'].value_counts().unstack(fill_value=0)
# 计算“收藏/购买”比
if 'fav' in category_stats.columns and 'buy' in category_stats.columns:
    category_stats['fav_buy_ratio'] = category_stats['fav'] / (category_stats['buy'] + 1) #加1防止除以0，边界问题
    # 按比率大小，降序排序，取前10名
    high_fav_low_buy = category_stats.nlargest(10, 'fav_buy_ratio')
    print("\n=== 收藏/购买比最高的10个类目 ===")
    print(high_fav_low_buy[['fav', 'buy', 'fav_buy_ratio']])

# 6. 分析“收藏/购买”比高的产品
# 按品类分组，统计每个品类的各种行为数量
category_behavior = df.groupby(['category_id', 'behavior']).size().unstack(fill_value=0)
# 每个品类包括“收藏”，“加购”，“购买”这三列
for col in ['fav', 'cart', 'buy']:
    if col not in category_behavior.columns:
        category_behavior[col] = 0 # 没有则补充0
# 计算兴趣总数
# 兴趣 = 收藏 + 加购
category_behavior['interest'] = category_behavior['fav'] + category_behavior['cart'] # 兴趣 = 收藏 + 加购
# 计算“兴趣/购买”比率
category_behavior['interest_buy_ratio'] = category_behavior['interest'] / (category_behavior['buy'] + 1)#边界问题
#按“兴趣/购买”比率大小降序排序，取前10名
high_interest_low_buy = category_behavior.nlargest(10, 'interest_buy_ratio')
print("\n=== 收藏+加购高但购买低的10个类目 ===")
print(high_interest_low_buy[['fav', 'cart', 'buy', 'interest', 'interest_buy_ratio']])