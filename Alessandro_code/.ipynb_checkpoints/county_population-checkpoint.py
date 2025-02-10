import pandas as pd
import numpy as np

def interpolate_population_data(df):
    # from 1900 to 2020
    years = list(range(1900, 2021))
    
    new_df = pd.DataFrame()
    new_df['cty_fips'] = df['cty_fips']
    new_df['cty'] = df['cty']
    
    # For each county, interpolate population for all years
    for year in years:
        if year % 10 == 0:
            col_name = f'pop_{year}'
            new_df[f'pop_{year}'] = df[col_name]
        else:
            lower_decade = (year // 10) * 10
            upper_decade = lower_decade + 10
            
            # Get populations for surrounding decades
            pop_lower = df[f'pop_{lower_decade}']
            pop_upper = df[f'pop_{upper_decade}']
            
            # Linear interpolation
            weight_upper = (year - lower_decade) / 10
            weight_lower = 1 - weight_upper
            
            new_df[f'pop_{year}'] = (pop_lower * weight_lower + 
                                   pop_upper * weight_upper).round().astype(int)
    
    year_cols = [f'pop_{year}' for year in years]
    new_df = new_df[['cty_fips', 'cty'] + year_cols]
    
    return new_df

df = pd.read_csv('/Users/acastillo/Library/CloudStorage/OneDrive-Personal/Spring 2025/Climate Prediction/Project_1/Hurricane_ML_proj_t5-1/Alessandro_code/data/historical_county_populations_v2.csv')
interpolated_df = interpolate_population_data(df)
print(interpolated_df)