import uvicorn
from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from rest import appMeal, appComment, appUser, appOrder


# 由于jsdelivr老崩溃，换CDN解决docs崩溃
def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css")


# Actual monkey patch
applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI(
    title='OrderRecommendationSystemBackend',
    version='0.0.1',
    docs_url='/docs',
    redoc_url='/redoc'
)

app.include_router(appMeal, prefix='/Meal', tags=['MealAPI'])
app.include_router(appComment, prefix='/Comment', tags=['CommentAPI'])
app.include_router(appUser, prefix='/User', tags=['UserAPI'])
app.include_router(appOrder, prefix='/Order', tags=['OrderAPI'])

if __name__ == '__main__':
    uvicorn.run(app="app:app", reload=True)
