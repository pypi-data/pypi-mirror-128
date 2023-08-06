from pyspark.sql.types import *


def equivalent_type(f):
    if f == 'datetime64[ns]':
        return TimestampType()
    elif f == 'int64':
        return LongType()
    elif f == 'int32':
        return IntegerType()
    elif f == 'float64':
        return FloatType()
    else:
        return StringType()


def define_structure(string, format_type):
    try:
        typo = equivalent_type(format_type)
    except:
        typo = StringType()
    return StructField(string, typo)


def pandas_to_spark(spark, pandas_df):
    columns = list(pandas_df.columns)
    types = list(pandas_df.dtypes)
    struct_list = []
    for column, typo in zip(columns, types):
        struct_list.append(define_structure(column, typo))
    p_schema = StructType(struct_list)
    return spark.createDataFrame(pandas_df, p_schema)


def show_pd_df(self):
    from IPython.display import HTML
    style = """
    <style scoped>
        .dataframe-div {
          max-height: 300px;
          overflow: auto;
          position: relative;
        }

        .dataframe thead th {
          position: -webkit-sticky; /* for Safari */
          position: sticky;
          top: 0;
          background: black;
          color: white;
        }

        .dataframe thead th:first-child {
          left: 0;
          z-index: 1;
        }

        .dataframe tbody tr th:only-of-type {
                vertical-align: middle;
            }

        .dataframe tbody tr th {
          position: -webkit-sticky; /* for Safari */
          position: sticky;
          left: 0;
          background: black;
          color: white;
          vertical-align: top;
        }
    </style>
    """
    df_html = self.to_html()
    df_html = style + '<div class="dataframe-div">' + df_html + "\n</div>"
    HTML(df_html)


def show_spark_df(self, limit=10):
    import os
    import jinja2
    import humanize
    from IPython.display import display, HTML

    def collect_to_dict(df_collect):
        dict_result = [v.asDict() for v in df_collect]
        return dict_result

    _columns = [c for c in self.columns]

    data_select = self.select(_columns).limit(limit)
    data = collect_to_dict(data_select.toLocalIterator())

    path = os.path.dirname(os.path.abspath("__file__"))
    template_loader = jinja2.FileSystemLoader(searchpath='templates')
    template_env = jinja2.Environment(loader=template_loader, autoescape=True)
    template = template_env.get_template("table.html")

    dtypes = [(i[0], i[1],) for i, j in zip(data_select.dtypes, data_select.schema)]

    total_rows = self.count()
    if total_rows < limit:
        limit = total_rows

    total_rows = humanize.intword(total_rows)
    total_cols = len(_columns)
    total_partitions = data_select.rdd.getNumPartitions()

    output = template.render(cols=dtypes, data=data, limit=limit,
                             total_rows=total_rows, total_cols=total_cols,
                             partitions=total_partitions)
    return display(HTML(output))
