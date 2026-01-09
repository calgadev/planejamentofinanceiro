import os
import dash
import dash_bootstrap_components as dbc

# Ensure Dash serves static assets from the top-level `assets/` directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
ASSETS_FOLDER = os.path.join(PROJECT_ROOT, "assets")

estilos = [
	"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
	"https://fonts.googleapis.com/icon?family=Material+Icons",
	dbc.themes.COSMO,
]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = dash.Dash(
	__name__,
	external_stylesheets=estilos + [dbc_css],
	suppress_callback_exceptions=True,
	assets_folder=ASSETS_FOLDER,
)
app.scripts.config.serve_locally = True
server = app.server

app.title = "Planejamento Financeiro"

