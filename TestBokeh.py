import time
from random import shuffle
from bokeh.plotting import figure, output_server, cursession, show

# prepare output to server
output_server("animated_line")

p = figure(plot_width=400, plot_height=400)
p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], name='ex_line')
show(p)

# create some simple animation..
# first get our figure example data source
renderer = p.select(dict(name="ex_line"))
ds = renderer[0].data_source

while True:
    # Update y data of the source object
    shuffle(ds.data["y"])

    # store the updated source on the server
    cursession().store_objects(ds)
    time.sleep(0.5)


# Create the main plot
def create_figure(current_feature_year, bins):
	p = Histogram(df, current_feature_year, title=current_feature_year,
	 	bins=bins, legend='top_right', width=600, height=400)

	# Set the x axis label
	p.xaxis.axis_label = current_feature_year

	# Set the y axis label
	p.yaxis.axis_label = 'Count'
	return p

# Index page
@app.route('/')
def index():
	# Determine the selected feature
	current_feature_year = request.args.get("feature_year")


	# Create the plot
	plot = create_figure(current_feature_year, 10)

	# Embed plot into HTML via Flask Render
	script, div = components(plot)
	return render_template("temp.html", script=script, div=div,
		feature_years=feature_years,  current_feature_year=current_feature_year)

# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)
