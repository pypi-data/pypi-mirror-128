
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

## Side note
 # Due to the use of a newer Java version, which is not supported for Pyspark and the will to continue using JDK16 for other projects, the following command was necessary
 # export JAVA_HOME="/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home"
 # SOURCE: https://stackoverflow.com/questions/53375699/unable-to-execute-pyspark-after-installation, https://mkyong.com/java/how-to-set-java_home-environment-variable-on-mac-os-x/

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

## Project

# importModules
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


# defineVariables (Settings)

appName= "bigDataSMLStudentPerformance"
dataPath = "../data/StudentsPerformance.csv"
saveWithHeader = True
outputPath = "../output/studenPerformanceResults.csv"
  
def main():

    # startSparkSession
    spark = SparkSession \
        .builder \
        .master("local") \
        .appName(appName) \
        .getOrCreate()

    # loadDataFromCsv
    df = spark.read.option("header",True) \
        .csv(dataPath)

    # caluculateAverageScoreOfMath,ReadingAndWriting
    df=  df \
        .withColumn("avg_score", (col("math score")+col("reading score")+col("writing score"))/3)

    # createDataFrameForAllMales
    male = df \
        .filter(df.gender == "male") \
        .groupby('ethnicity') \
        .agg({'avg_score': 'mean'}) \
        .withColumnRenamed("ethnicity", "key1") \
        .withColumnRenamed("avg(avg_score)", "Durchschnittsnoten - Männlich")
        

    # createDataFrameForAllFemales
    female = df \
        .filter(df.gender == "female") \
        .groupby('ethnicity') \
        .agg({'avg_score': 'mean'}) \
        .withColumnRenamed("ethnicity", "key2") \
        .withColumnRenamed("avg(avg_score)", "Durchschnittsnoten - Weiblich")

    # modifyDataFrameForAllStudents
    df = df \
        .groupby('ethnicity') \
        .agg({'avg_score': 'mean'}) \
        .withColumnRenamed("ethnicity", "Ethnische Gruppe") \
        .withColumnRenamed("avg(avg_score)", "Durchschnittsnoten")
        
    # showDataFrames
    #df.show()
    #male.show()
    #female.show()
    

    # mergeTables

    df = df \
    .join(female, col('Ethnische Gruppe') == col('key2')) \
    .drop('key2') \
    .join(male, col('Ethnische Gruppe') == col('key1')) \
    .drop('key1') \
    .sort(['Durchschnittsnoten','Durchschnittsnoten - Weiblich', 'Durchschnittsnoten - Männlich'],
               ascending = False)

    # showFinalDataFrame
    df.show()

    # saveDataFrameIntoCsv
    df.write.option("header",saveWithHeader) \
        .csv(outputPath)

    # endSparkSession
    spark.stop()



if __name__ == "__main__":
    main()