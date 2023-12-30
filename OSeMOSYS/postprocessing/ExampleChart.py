import pandas as pd
import plotly.express as px

def plot_activity(datafile):
    data = pd.read_csv(datafile)
    color_map = {
        'CTMG': 'gray',
        'CTOP': 'gray',
        'CTEG': 'gray',
        'CTAG': 'gray',
        'CTCM': 'gray',
        'CTDO': 'gray',
        'CTLR': 'gray',
        'CTAM': 'gray',
        'CTNUE': 'gray',
        'PV': 'yellow',
        'EOLICA': 'blue',
    }

    data['TIMESLICE'] = data['TIMESLICE'].astype(str)
    # Create a stacked bar chart using Plotly
    fig = px.bar(data, x='TIMESLICE', y='value', color='TECHNOLOGY', animation_frame='YEAR',
                 labels={'value': 'Values'}, height=600,
                 category_orders={'TIMESLICE': data['TIMESLICE'], 'YEAR': data['YEAR']},
                 color_discrete_map=color_map)

    fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)])])])

    # Show the interactive plot
    fig.show()


if __name__ == '__main__':
    datafile = '../../results/v_RateOfTotalActivity.csv'
    plot_activity(datafile)