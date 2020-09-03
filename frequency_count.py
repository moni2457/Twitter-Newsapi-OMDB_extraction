from pyspark import SparkContext
sc = SparkContext("local", "frequency_count")

# read the input file
input_file = sc.textFile("/home/ubuntu/server/spark-2.4.5-bin-hadoop2.7/Data_Assignment_3/data_file.txt")
# for single words
list_single = {'education':0,'canada':0,'university':0,'dalhousie':0,'expensive':0,'faculty':0,'graduate':0}
# for double words
list_double = {'good school':0,'good schools':0,'bad school':0,'bad schools':0,'poor school':0,'poor schools':0,'computer science':0}

def list_Single(input_file):
    # Reference taken from https://spark.apache.org/examples.html
    single_word = input_file.flatMap(lambda line: line.split(" "))
    sl = single_word.map(lambda word: (word.lower(), 1))
    s_final = sl.reduceByKey(lambda a, b: a + b).collect()
    for element in s_final:
        if element[0] in list_single:
            list_single[element[0]] = element[1]


# method invoked to get two words input
def get_two_words(words):
    two_word = []
    for i in range (0, len(words)-1):
        two_word.append(((words[i],words[i+1]),1))
    return two_word

def list_Double(input_file):
    # Reference taken from https://spark.apache.org/examples.html
    double_word = input_file.map(lambda line: line.split(" "))
    dbl = double_word.flatMap(lambda words: get_two_words(words))
    d_final = dbl.reduceByKey(lambda a, b: a + b).collect()
    for element in d_final:
        if str(element[0][0].lower() +' '+element[0][1].lower()) in list_double:
            list_double[element[0][0] +' '+element[0][1]] = element[1]
    list_single.update(list_double)
    # # Reference taken from https://pythonspot.com/save-a-dictionary-to-a-file/
    f = open("/home/ubuntu/server/spark-2.4.5-bin-hadoop2.7/Data_Assignment_3/output_spark_test.txt", "a+")
    f.write(str(list_single))
    f.close()
    print ("output file created successfully !")

# method invoked for single words and double words
list_Single(input_file)
list_Double(input_file)