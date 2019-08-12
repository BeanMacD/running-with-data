from bokeh.charts import Donut, show, output_file
from bokeh.charts.utils import df_from_json
from bokeh.sampledata.olympics2014 import data

import pandas as pd

# utilize utility to make it easy to get json/dict data converted to a dataframe
df = df_from_json(data)

# filter by countries with at least one medal and sort by total medals
df = df[df['total'] > 8]
df = df.sort("total", ascending=False)
df = pd.melt(df, id_vars=['abbr'],
             value_vars=['bronze', 'silver', 'gold'],
             value_name='medal_count', var_name='medal')

# original example
d = Donut(df, label=['abbr', 'medal'], values='medal_count',
          text_font_size='8pt', hover_text='medal_count')

output_file("donut.html", title="donut.py example")

show(d)


<nav class="w3-sidebar w3-bar-block w3-animate-left w3-grey" style="display:none", id="my_sidebar">
<button class="w3-bar-item w3-button w3-xlarge" onclick="w3_close()">Close &times;</button>
<a href="#" class="w3-bar-item w3-button w3-padding-large w3-grey">
 <i class="fa fa-home w3-xxlarge">

 </i>
 <p>Home</p>
</a>
<a href="/Runners.html" class="w3-bar-item w3-button w3-padding-large w3-grey w3-hover-dark-grey">
 <i class="fa fa-users w3-xxlarge">

</i>
 <p>Runners</p>
</a>
<a href="#Race" class="w3-bar-item w3-button w3-padding-large w3-grey w3-hover-dark-grey">
 <i class="fa fa-map w3-xxlarge">

 </i>
 <p>Race</p>
</a>
<a href="#Stats" class="w3-bar-item w3-button w3-padding-large w3-grey w3-hover-dark-grey">
 <i class="fa fa-line-chart w3-xxlarge">

</i>
 <p>Statistics</p>
</a>
<a href="#about" class="w3-bar-item w3-button w3-padding-large w3-grey w3-hover-dark-grey">
 <i class="fa fa-question-circle w3-xxlarge">

</i>
 <p>About</p>
</a>
</nav>
