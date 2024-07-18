import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

def plot_activity(datafile):
    data = pd.read_csv(datafile)
    color_dict = {
    'PWRCRUD001': 'gray',
    'PWRCRUD002': 'dimgray',
    'PWRCRUD003': 'darkgray',
    'PWRCRUD004': 'silver',
    'PWRCRUD005': 'lightgray',
    'PWRCRUD006': 'gainsboro',
    'PWRCRUD007': 'whitesmoke',
    'PWRCRUD008': 'black',
    'PWRHFO01': '#8B0000',
    'PWRNG01': 'orange',
    'PWRNG02': 'darkorange',
    'PWRGHFO2': 'gray',
    'PWRBIO': '#9ACD32',
    'PWRWND001': 'deepskyblue',#4169E1
    'PWRWND002': 'deepskyblue',
    'PWRPV01': '#FFD700',
    'PWRPV02': '#CCAC00',
    'PWRCSP': 'gray',
    'PWRFO': '#FF6961',
    'PWRDSL': 'brown',
    'PWRHYD01': '#0d5c91',
    'PWRHYD02': '#1f77b4'
}


    # data['TIMESLICE'] = data['TIMESLICE'].astype(str)
    # Create a stacked bar chart using Plotly
    data['value']= data['value']*277.78
    data= data[data['TECHNOLOGY'].str.contains('PWR')].sort_values(by='TECHNOLOGY')
    data = data[~data['TECHNOLOGY'].str.contains('PWRDIST|PWRTRANS')]
    data = data[round(data['value'],4) != 0]

    fig = px.bar(data, x="YEAR", y = "value", color="TECHNOLOGY",
                color_discrete_map = color_dict,
                opacity = 0.7,
                )

    fig.update_layout(hovermode='x unified', 
                    autosize=False,
                    width= 1000,
                    height= 600, 
                    yaxis_title="Energy Production in GWh",
                    plot_bgcolor='white',
                    #   paper_bgcolor='lightgrey',
                    xaxis=dict(
            tickfont=dict(size=14),  # Tamaño de la fuente de las etiquetas del eje x
            titlefont=dict(size=16)
                    ),
                    yaxis=dict(
            showgrid=False,
            tickfont=dict(size=14),      
            gridwidth=0.5,        #
            gridcolor='lightgrey',
            tickformat='.0f' 
            ),
    legend=dict(font=dict(size=16)),
    title={'text': 'Energy production base scenario by technology', 'x': 0.5},
    font=dict( size=16,color='black')
    )

    # Show the interactive plot
    fig.show()
    fig1 = px.pie(data[data['YEAR']==2019], names='TECHNOLOGY', values='value', hole=0.5, title='Gráfico de Dona 1',color = 'TECHNOLOGY',color_discrete_map = color_dict,
    opacity=0.7, category_orders={'TECHNOLOGY': data['TECHNOLOGY'].tolist()})
    fig2 = px.pie(data[data['YEAR']==2030], names='TECHNOLOGY', values='value', hole=0.5, title='Gráfico de Dona 1',color = 'TECHNOLOGY',color_discrete_map = color_dict,
    opacity=0.7, category_orders={'TECHNOLOGY': data['TECHNOLOGY'].tolist()} )
    fig3 = px.pie(data[data['YEAR']==2050], names='TECHNOLOGY', values='value', hole=0.5, title='Gráfico de Dona 2',color = 'TECHNOLOGY',color_discrete_map = color_dict,
    opacity=0.7, category_orders={'TECHNOLOGY': data['TECHNOLOGY'].tolist()})
    

    fig = make_subplots(
        rows=1, cols=3, 
        specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]],
        subplot_titles=('2019','2030', '2050')
    )


    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)

    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)
    for trace in fig3.data:
        fig.add_trace(trace, row=1, col=3)
    

    fig.update_layout(height=700, width=1200,title={'text': 'Energy Production by technology REN37 scenario(%)', 'x': 0.5} , font=dict( size=16,color='black'))

    fig.show()

if __name__ == '__main__':
    datafile = '../../results/v_ProductionByTechnologyAnnual.csv'
    plot_activity(datafile)