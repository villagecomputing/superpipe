import pandas as pd
from typing import TypedDict, Type, Dict, get_type_hints
from pydantic import create_model


def validate_dict(dict: Dict, type: Type[TypedDict]) -> Dict:
    field_definitions = get_type_hints(type)
    pydantic_model = create_model(
        type.__name__, **{k: (v, ...) for k, v in field_definitions.items()})
    pydantic_model.model_validate(dict)


def gradient_color(val, min_val, median_val, max_val, reverse=False):
    if pd.isna(val):
        return 'background-color: white; color: black'  # Handle NaN values

    if min_val != median_val and median_val != max_val:
        if val < median_val:
            closeness = (val - min_val) / (median_val - min_val)
            red = 255 if not reverse else int(closeness * 255)
            green = int(closeness * 255) if not reverse else 255
            color = f'rgb({red},{green},0)'
        else:
            closeness = (val - median_val) / (max_val - median_val)
            green = 255 if not reverse else int((1 - closeness) * 255)
            red = int((1 - closeness) * 255) if not reverse else 255
            color = f'rgb({red},{green},0)'
    else:
        color = 'rgb(255,255,0)' if not reverse else 'rgb(0,255,255)'

    return f'background-color: {color}; color: black;'


def df_apply_gradients(df, higher_columns, lower_columns):
    styles = {col: {'min_val': df[col].min(), 'median_val': df[col].median(), 'max_val': df[col].max(
    ), 'reverse': col in lower_columns} for col in higher_columns + lower_columns}

    def apply_style(val, col):
        info = styles[col]
        return gradient_color(val, info['min_val'], info['median_val'], info['max_val'], reverse=info['reverse'])

    styler = df.style
    for col in styles:
        styler = styler.applymap(
            lambda val, col=col: apply_style(val, col), subset=[col])
    return styler
