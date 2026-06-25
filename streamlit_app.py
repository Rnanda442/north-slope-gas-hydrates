from dashboard import app as dashboard_app
from dashboard import mapbox_map_clean


def render_regional_map() -> None:
    mapbox_map_clean.render_regional_atlas_clean(dashboard_app)


dashboard_app.render_regional_atlas = render_regional_map
main = dashboard_app.main


if __name__ == "__main__":
    main()
