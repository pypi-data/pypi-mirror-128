import hashlib
from datetime import timedelta
from typing import List, Union

import numpy as np
from pandas import DataFrame, concat, to_datetime
from sqlalchemy import Column, and_, func, literal, text
from stakenix import MySQL, PostgreDB
from stakenix.utils.common import merger


def get_traffic_source(df: DataFrame, user_id_column: str = "player_id") -> DataFrame:
    ph = hashlib.md5(b"project").hexdigest()
    projects = [
        "mk5",
        "mk1",
        "mk2",
        "mk3",
        "vipclub",
        "vipclub2",
        "vipclub",
        "lara",
        "vipt",
        "pobeda",
    ]
    regexp = "p[a-z0-9]+p[a-z0-9]+p[a-z0-9]{4}"
    players = concat(
        [
            MySQL(project)
            .query(
                columns=[
                    Column("player_id"),
                    func.regexp_substr(Column("partner_code"), regexp).label(
                        "ref_code"
                    ),
                    Column("partner_subid"),
                ],
                table="players",
                where=Column("player_id").in_(df[user_id_column].unique()),
            )
            .assign(project=project)
            for project in projects
        ]
    )
    unique_projects = players.project.unique()
    campaings = concat(
        [
            MySQL(project).query(
                table="campaigns",
                columns=[
                    Column("id"),
                    Column("name").label("promo_name"),
                    Column("cost_type_label"),
                ],
            )
            for project in projects
        ]
    )

    lp_users = concat(
        [
            MySQL(project)
            .query(table="lp_users", columns=[text("*"), literal(project).label(ph)])
            .rename({"id": "user_id", "login": "Account"}, axis=1)
            for project in projects
        ]
    )
    partners = PostgreDB("customdata").query(
        table="partner_accounts", columns=[text("*")]
    )
    ref_codes = concat(
        [
            MySQL(project).query(
                columns=[
                    func.regexp_substr(Column("ref_code"), regexp).label("ref_code"),
                    Column("campaign_id"),
                    Column("user_id"),
                ],
                table="ref_codes",
            )
            for project in projects
        ]
    )

    merged = merger(
        (df,),
        (players, {"left_on": user_id_column, "right_on": "player_id"}),
        (ref_codes.drop_duplicates(), {"on": "ref_code", "how": "left"}),
        (
            campaings.drop_duplicates(),
            {"left_on": "campaign_id", "right_on": "id", "how": "left"},
        ),
        (lp_users.drop_duplicates(), {"on": "user_id", "how": "left"}),
        (partners.drop_duplicates(), {"on": "Account", "how": "left"}),
    )
    duplicates = merged[merged[user_id_column].duplicated(keep=False)].loc[
        (~merged["ref_code"].isna())
    ]
    to_filter = duplicates.loc[~duplicates[ph].isin(unique_projects)]
    to_filter = to_filter.loc[
        ~(~(to_filter["ref_code"].isna()) & to_filter["Account"].isna())
    ]
    return _set_provider(merged[~merged.index.isin(to_filter.index)]).drop(
        columns=[ph, user_id_column] if user_id_column != "player_id" else [ph]
    )


def _set_provider(df):
    df, col = df.copy(), "source"
    df[col] = df["Provider"].fillna("undefined")
    prv, acc, ref = (df[i] for i in (col, "Account", "ref_code"))
    df[col] = np.where(ref.isnull(), "Direct", prv)
    df[col] = np.where(
        (prv == "undefined") & (acc.isnull() == False), "Partnerka", df[col]
    )
    df[col] = np.where(
        (df[col] == "undefined") & (acc.isnull() == True), "UndefRef", df[col]
    )
    df[col] = np.where(df[col].isin(["Experiments", "Inhouse"]), "Inhouse", df[col])
    df["Provider"] = df["Provider"].fillna(df[col])
    return df


def query_rates(
    dates: List, currencies: Union[List[str], str], delta: timedelta = timedelta(days=1)
):
    dates = [date - delta for date in dates]
    if isinstance(currencies, str):
        currencies = [currencies]
    rates = (
        MySQL(schema="currency_rates")
        .query(
            table="rates",
            columns=[
                Column("date").label("rate_date"),
                Column("symbol").label("currency"),
                Column("rate"),
            ],
            where=and_(
                Column("date").in_(dates),
                Column("symbol").in_(currencies),
            ),
        )
        .replace(to_replace={date: date + delta for date in dates})
    )
    rates["rate_date"] = to_datetime(rates["rate_date"])
    return rates


def _to_usd(
    df: DataFrame,
    values_fields: Union[str, List[str]],
    dates_field: str = "date",
    currencies_field: str = "currency",
) -> DataFrame:
    if df.empty:
        return df
    else:
        try:
            unique_dates = df[~df[dates_field].isna()][dates_field].dt.date.unique()
            df["transaction_date"] = to_datetime(df[dates_field].dt.date)
        except AttributeError:
            dates = df[~df[dates_field].isna()]
            dates[dates_field] = to_datetime(dates[dates_field])
            unique_dates = dates[dates_field].dt.date.unique()
            df["transaction_date"] = to_datetime(to_datetime(df[dates_field]).dt.date)

        currencies = df[currencies_field].unique()
        rates = query_rates(dates=unique_dates, currencies=currencies)
        rated = df.merge(
            rates,
            how="left",
            left_on=["transaction_date", "currency"],
            right_on=["rate_date", "currency"],
        )
        if isinstance(values_fields, list):
            rated[
                [
                    "{column_name}_usd".format(column_name=column)
                    for column in values_fields
                ]
            ] = rated.loc[:, values_fields].div(rated["rate"], axis=0)
            rated = rated.drop(columns=["transaction_date", "rate_date", "rate"])
            return rated
        else:
            rated = rated.assign(
                **{f"{values_fields}_usd": lambda x: x[values_fields] / x["rate"]}
            )
            return rated.drop(columns=["transaction_date", "rate_date", "rate"])


def _to_target_currency(
    df: DataFrame,
    target_currency: str,
    values_fields: Union[str, List[str]],
    dates_field: str = "date",
    currencies_field: str = "currency",
):
    df_in_usd = _to_usd(df, values_fields, dates_field, currencies_field)
    try:
        dates = df_in_usd[dates_field].dt.date.unique()
        df_in_usd["transaction_date"] = to_datetime(df_in_usd[dates_field].dt.date)
    except AttributeError:
        dates = df_in_usd[dates_field].unique()
        df_in_usd["transaction_date"] = to_datetime(
            to_datetime(df_in_usd[dates_field]).dt.date
        )
    rates_in_target_currency = query_rates(dates, target_currency).drop(
        columns=["currency"]
    )
    merged_target_currency_rates = df_in_usd.merge(
        rates_in_target_currency, how="left", left_on="transaction_date", right_on="rate_date"
    )
    if isinstance(values_fields, list):
        merged_target_currency_rates[
            [
                "{column_name}_{target_currency}".format(
                    column_name=column, target_currency=target_currency.lower()
                )
                for column in values_fields
            ]
        ] = merged_target_currency_rates.loc[
            :, [f"{field}_usd" for field in values_fields]
        ].mul(
            merged_target_currency_rates["rate"], axis=0
        )
        merged_target_currency_rates = merged_target_currency_rates.drop(
            columns=["transaction_date", "rate_date", "rate"]
        )
        return merged_target_currency_rates
    else:
        merged_target_currency_rates = merged_target_currency_rates.assign(
            **{
                f"{values_fields}_{target_currency.lower()}": lambda x: x[
                    f"{values_fields}_usd"
                ]
                * x["rate"]
            }
        )
        return merged_target_currency_rates.drop(
            columns=["transaction_date", "rate_date", "rate"]
        )


def get_rates(
    df: DataFrame,
    values_fields: Union[str, List[str]],
    dates_field: str = "date",
    currencies_field: str = "currency",
    target_currency: str = "USD",
) -> DataFrame:
    """Method to convert money sums to usd (or other currency). Currency rate getted on date that was 1 day before transaction

    Args:
        df (DataFrame): Datafra,e with transactions
        values_fields (Union[str, List[str]]): fields that must be converted to usd or other currency
        dates_field (str, optional): column name of df that relates to date of transaction. Defaults to "date".
        currencies_field (str, optional): column name of df that relates to currencies of transactions. Defaults to "currency".
        target_currency (str, optional): currency code in ISO 4217 format. Defaults to "USD".

    Raises:
        KeyError: if values_fields arg is None

    Returns:
        DataFrame: input dataframe with additional column of calculated values in usd or other currency
    """

    if target_currency == "USD":
        result = _to_usd(df, values_fields, dates_field, currencies_field)
        return result
    else:
        result = _to_target_currency(
            df,
            target_currency=target_currency,
            values_fields=values_fields,
            dates_field=dates_field,
            currencies_field=currencies_field,
        )
        return result
