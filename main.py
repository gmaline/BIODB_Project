import SOFT
import sqldb

if __name__ == '__main__':
    # Parsing the first project.
    samples1 = ["^SAMPLE = GSM4733279", "^SAMPLE = GSM4733280", "^SAMPLE = GSM4733281", "^SAMPLE = GSM4733282"]
    # dict1 = SOFT.id2gene("GSE156544_family.soft")
    # SOFT.expression_data(dict1, "GSE156544_family.soft", samples1, "GSE156544")
    # SOFT.project_info("GSE156544_family.soft")

    # Parsing the second project.
    samples2 = ["!Series_sample_id = GSM4861695", "!Series_sample_id = GSM4861696"]
    dict2 = SOFT.id2gene("GSE160163_family.soft")
    print(dict2)
    #SOFT.expression_data(dict2, "GSE156544_family.soft", samples2, "GSE160163")
    #SOFT.project_info("GSE160163_family.soft")


    #Creating the sql data dump files.
    # sqldb.format_insert_gene("data_dump.csv")
    #sqldb.format_insert_project("project_info_data_dump.csv")

