import streamlit as st
import pandas as pd
import altair as alt

st.title("Weekly Stock Market Analytics Dashboard")

# Load weekly aggregation files
weekly_volume = pd.read_parquet("agg1.parquet")
weekly_avg_return = pd.read_parquet("agg2.parquet")
weekly_validated = pd.read_parquet("agg3.parquet")

# Weekly Volume per Sector
st.subheader("Weekly Total Volume per Sector")
line_volume = alt.Chart(weekly_volume).mark_line().encode(
    x='trade_date:T',
    y='volume:Q',
    color='sector:N',
    tooltip=['trade_date:T', 'sector:N', 'volume:Q']
).interactive()

st.altair_chart(line_volume, use_container_width=True)

# Weekly Average % Return per Sector

st.subheader("Weekly Average Percentage Return per Sector")
line_return = alt.Chart(weekly_avg_return).mark_line().encode(
    x='trade_date:T',
    y='daily_return:Q',
    color='sector:N',
    tooltip=['trade_date:T', 'sector:N', 'daily_return:Q']
).interactive()

st.altair_chart(line_return, use_container_width=True)

# Weekly Count of Validated Trades per Sector

st.subheader("Weekly Count of Validated Trades per Sector")
line_validated = alt.Chart(weekly_validated).mark_line().encode(
    x='trade_date:T',
    y='validated_count:Q',
    color='sector:N',
    tooltip=['trade_date:T', 'sector:N', 'validated_count:Q']
).interactive()

st.altair_chart(line_validated, use_container_width=True)

#Volatility
st.subheader("Weekly Sector Volatility (Std Dev of Weekly % Return)")

weekly_volatility = (
    weekly_avg_return
    .groupby('sector', dropna=False)['daily_return']
    .std()
    .reset_index()
    .rename(columns={'daily_return': 'volatility'})
)

bar_volatility = alt.Chart(weekly_volatility).mark_bar().encode(
    x='sector:N',
    y='volatility:Q',
    color='sector:N',
    tooltip=['sector:N', 'volatility:Q']
).interactive()

st.altair_chart(bar_volatility, use_container_width=True)


#Percent Share of Market
st.subheader("Weekly Sector Share of Total Market Volume (%)")

weekly_volume_pct = (
    weekly_volume
    .copy()
    .assign(total_volume=lambda x: x.groupby('trade_date')['volume'].transform('sum'))
)
weekly_volume_pct['volume_pct'] = weekly_volume_pct['volume'] / weekly_volume_pct['total_volume']

area_volume_share = alt.Chart(weekly_volume_pct).mark_area(opacity=0.6).encode(
    x='trade_date:T',
    y=alt.Y('volume_pct:Q', axis=alt.Axis(format='%')),
    color='sector:N',
    tooltip=['trade_date:T', 'sector:N', 'volume_pct:Q']
).interactive()

st.altair_chart(area_volume_share, use_container_width=True)
