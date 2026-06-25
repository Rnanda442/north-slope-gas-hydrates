from dashboard import app as dashboard_app
from dashboard import static_png_review


def render_regional_map() -> None:
    static_png_review.render_regional_atlas_with_static_png_review(dashboard_app)


dashboard_app.render_regional_atlas = render_regional_map
main = dashboard_app.main


if __name__ == "__main__":
    main()
