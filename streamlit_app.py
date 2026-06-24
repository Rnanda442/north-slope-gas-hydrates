from dashboard import app as dashboard_app
from dashboard.map_v2 import render_regional_atlas_v2


dashboard_app.render_regional_atlas = lambda: render_regional_atlas_v2(dashboard_app)
main = dashboard_app.main


if __name__ == "__main__":
    main()
