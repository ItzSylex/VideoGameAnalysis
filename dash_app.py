from platform import platform, release
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input


app = Dash(__name__)

figures = []

# Importing data 

df = pd.read_csv("vgsales.csv")

# Checking null values. Since the data is quite big compared to the amount of nulls, I decided to
# drop these.
 
df.isnull().sum()
df = df.dropna()

# Top 5 Publishers with most releases

publisher_releases_df = df.Publisher.value_counts().head(5).rename_axis("Publisher").reset_index(name = "TotalReleases")

# Creating bar chart 

releases_per_publisher = px.bar(
    data_frame = publisher_releases_df, 
    x = "Publisher",
    y = "TotalReleases",
    barmode = "group",
    title = "Total Releases Per Publisher",
    color_discrete_sequence = px.colors.sequential.Aggrnyl
)

figures.append(releases_per_publisher)

# Top 5 Publishers with most sales

publisher_sales_df = df.groupby("Publisher").sum().reset_index().sort_values(by="Global_Sales", ascending = False).head(5)

#Rename Columns to display properly in plot

publisher_sales_df = publisher_sales_df.rename(
    columns = {

        "NA_Sales": "North America",
        "JP_Sales": "Japan",
        "EU_Sales": "Europe",
        "Other_Sales": "Other"

    }
)

# Creating stacked bar chart that displays total sales per region. Shows top 5 publisher with most sales

sales_per_publisher = px.bar(

    data_frame = publisher_sales_df,
    x = "Publisher",
    y = ["North America", "Europe", "Japan", "Other"],
    barmode = "relative",
    title = "Top 5 Publishers with most sales",

    labels = {
        "variable" : "Regions",

        "NA_Sales": "North America",
        "JP_Sales": "Japan",
        "EU_Sales": "Europe",
        "Other_Sales": "Other",

        "value": "Sales in Millions"
    },
    color_discrete_sequence = px.colors.sequential.Aggrnyl
)

figures.append(sales_per_publisher)

# Game genre most released

genre_releases_df = df.Genre.value_counts().rename_axis("Genre").reset_index(name = "Releases")

# Pie chart for most released genre

most_released_genre = px.pie(

    data_frame = genre_releases_df,
    values = "Releases",
    names = "Genre",
    title = "Most released genre",
    hole = .3,
    color_discrete_sequence = px.colors.sequential.Aggrnyl

)

figures.append(most_released_genre)

# How are sales looking over the years categorized by region.

sales_over_year_by_region = df[['Year','NA_Sales','EU_Sales','JP_Sales','Other_Sales']].groupby(['Year'], as_index = False).sum()


sales_year_region = px.line(

    data_frame = sales_over_year_by_region,
    x = "Year",
    y = ['NA_Sales','EU_Sales','JP_Sales','Other_Sales'],
    color_discrete_sequence = px.colors.sequential.Aggrnyl
)

figures.append(sales_year_region)


# What region has made more sales

# What year had more releases

# Releases over the years by publisher

releases_over_the_years = df.groupby(["Year", "Publisher"])["Name"].count().reset_index(name = "Count")
releases_over_the_years = releases_over_the_years[releases_over_the_years.Publisher.isin(df.Publisher.value_counts().head(5).index.values.tolist())]

releases_over_the_years_by_publisher = px.line(

        data_frame = releases_over_the_years,
        x = "Year",
        y = "Count",
        color = "Publisher",
        color_discrete_sequence = px.colors.sequential.Aggrnyl
    )

releases_over_the_years_by_publisher.update_layout(legend=dict(
    yanchor = "bottom", 
    y = 0.99,
    xanchor = "left",
    x = 0.01,
    orientation = "h"
))

figures.append(releases_over_the_years_by_publisher)

app.layout = html.Div([

    html.Div([
        html.Div([dcc.Graph(figure = releases_per_publisher)], className="div1"),

        html.Div([dcc.Graph(figure = sales_per_publisher)], className="div2"),

        html.Div([dcc.Graph(figure = most_released_genre)], className="div3"),

        html.Div([dcc.Graph(figure = releases_over_the_years_by_publisher)], className="div4"),

        html.Div([dcc.Graph(figure = sales_year_region)], className="div5"),

        html.Div([dcc.Graph(figure = releases_per_publisher)], className="div6"),

    ], className = "parent")

], className = "main_container")



# Styling plots.

for figure in figures:
    figure.update_layout(

        paper_bgcolor = "#16161a",
        plot_bgcolor = "#16161a",
        font_color = "#a7a9be"

    )
    figure.update_xaxes(showgrid = False, zeroline = False)
    figure.update_yaxes(showgrid = False, zeroline = False)


if __name__ == '__main__':
    app.run_server(debug=True)