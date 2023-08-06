from akerbp.models.rule_based_models import BS_helpers

def flag_bad_den_shallow(df_well):
    #Look for parial DEN measurement for the same BS in the shallow end of the well
    df_well = BS_helpers.find_BS_jumps(df_well)
    #get the index of the first DEN value
    first_DEN_idx     = df_well[df_well['DEN'].notna()].index.min()
    first_BS_region   = df_well.loc[first_DEN_idx, 'BS_region']
    first_region_idx  = df_well[df_well['BS_region']==first_BS_region].index.min()
    bad_region_length = len(df_well[df_well['BS_region']==first_BS_region]['DEN'].dropna())
    if (first_region_idx < first_DEN_idx) and (bad_region_length<1000):
        dencorr_casing = df_well[df_well['BS_region']==first_BS_region].index
    else:
        dencorr_casing = []
    return dencorr_casing

def flag_bad_den_at_jump(df_well):
    #Look around the regions where BS value changes, if there are missing DEN measurements, 
    # mark X measurements before and after that as potentioally bad
    df_well = BS_helpers.find_BS_jumps(df_well)
    bad_den_idx = []
    for region in df_well['BS_region'].unique():
        min_region_idx = df_well[df_well['BS_region']==region].index.min()
        min_den_idx    = df_well[df_well['BS_region']==region]['DEN'].dropna().index.min()
        if min_den_idx > min_region_idx:
            bad_den_idx.extend(df_well[
                df_well['BS_region']==region]['DEN'].dropna().head(20).index.tolist()
            )
        max_region_idx = df_well[df_well['BS_region']==region].index.max()
        max_den_idx = df_well[df_well['BS_region']==region]['DEN'].dropna().index.max()
        if max_den_idx < max_region_idx:
            bad_den_idx.extend(df_well[
                df_well['BS_region']==region]['DEN'].dropna().tail(20).index.tolist()
            )
    return bad_den_idx

def flag_casing(df_well, y_pred=None):
    """
    Returns anomalous DEN at the top of the well

    Args:
        df_well (pd.DataFrame): [description]

    Returns:
        [type]: [description]
    """
    print('Method: casing...')
    bad_den_casing = []
    bad_den_casing.extend(flag_bad_den_shallow(df_well))
    bad_den_casing.extend(flag_bad_den_at_jump(df_well))
    if y_pred is None:
        y_pred = df_well.copy()
    y_pred.loc[:, ['flag_casing_gen', 'flag_casing_den']] = 0, 0
    y_pred.loc[bad_den_casing, ['flag_casing_gen', 'flag_casing_den']] = 1
    return y_pred