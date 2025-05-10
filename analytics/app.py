# app.py

import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px

# 1. Load your data
df = pd.read_excel("data.xlsx")  # put your Excel file here

# 2. Compute a pivot table
#    Here: count of rows per first categorical column,
#    sum of values in the first numeric column.
cat_col = df.select_dtypes(include="object").columns[0]
num_col = df.select_dtypes(include="number").columns[0]

pivot = pd.pivot_table(
    df,
    index=cat_col,
    values=num_col,
    aggfunc=["count", "sum"]
)
pivot.columns = ["Count", "Sum"]  # flatten multi-index

# 3. Initialize Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Quick Excel Analytics Dashboard"),

    # Show raw data
    html.H2("Raw Data Preview"),
    dash_table.DataTable(
        data=df.head(10).to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
    ),

    html.H2("Pivot Table"),
    dash_table.DataTable(
        data=pivot.reset_index().to_dict("records"),
        columns=[{"name": i, "id": i} for i in pivot.reset_index().columns],
        style_table={"overflowX": "auto"},
    ),

    # Charts row
    html.Div([
        html.Div([
            html.H3("Bar Chart (Count)"),
            dcc.Graph(
                figure=px.bar(
                    pivot.reset_index(),
                    x=cat_col,
                    y="Count",
                    title=f"Count per {cat_col}"
                )
            )
        ], style={"width": "48%", "display": "inline-block"}),

        html.Div([
            html.H3("Pie Chart (Sum)"),
            dcc.Graph(
                figure=px.pie(
                    pivot.reset_index(),
                    names=cat_col,
                    values="Sum",
                    title=f"Sum of {num_col} per {cat_col}"
                )
            )
        ], style={"width": "48%", "display": "inline-block", "float": "right"}),
    ]),

    # Extra: line chart of Sum over categories
    html.H3("Line Chart (Sum)"),
    dcc.Graph(
        figure=px.line(
            pivot.reset_index(),
            x=cat_col,
            y="Sum",
            markers=True,
            title=f"Sum of {num_col} by {cat_col}"
        )
    ),
])

if __name__ == "__main__":
    app.run_server(debug=True)
