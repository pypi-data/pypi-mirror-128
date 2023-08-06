import pandas as pd


def subtotal(data, columns, total_label='', size=None,
             width_col='width', start_col='start', sort_index=True):
    result = []
    for i in range(len(columns) + 1):
        blanked = data.assign(**{col: total_label for col in columns[i:]})
        total = blanked.groupby(columns).sum()
        if size is not None:
            if width_col is not None:
                total[width_col] = total[size].cumsum() / total[size].sum()
                if start_col is not None:
                    total[start_col] = total[width_col].shift(1).fillna(0)
        result.append(total)
    result = pd.concat(result)
    if sort_index:
        result.sort_index(inplace=True)
    return result
