from dashboard import app as dashboard_app
from dashboard import map_code_integration as map_integration


def render_regional_map() -> None:
    map_integration.render_regional_atlas_v3(dashboard_app)


dashboard_app.render_regional_atlas = render_regional_map
main = dashboard_app.main


if __name__ == "__main__":
    main()
