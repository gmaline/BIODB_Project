import SOFT
import sqldb

if __name__ == '__main__':
    samples = ["^SAMPLE = GSM4733279", "^SAMPLE = GSM4733280", "^SAMPLE = GSM4733281", "^SAMPLE = GSM4733282"]
    dict1 = SOFT.id2gene("GSE156544_family.soft")
    SOFT.expression_data(dict1, "GSE156544_family.soft", samples)
    sqldb.format_insert_gene("data_dump.csv")

