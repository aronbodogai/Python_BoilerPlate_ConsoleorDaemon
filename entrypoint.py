import argparse
import logging

from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import trange
from tqdm.contrib.logging import logging_redirect_tqdm
from tqdm import tqdm

import pandas as pd
from pandas import json_normalize


from environs import Env

from myutils import *

# Define logging levels
LOG_LEVELS = {
    0: logging.ERROR,
    1: logging.WARNING,
    2: logging.INFO,
    3: logging.DEBUG
}
def configure_logging(verbosity_level,silent):
    logging.basicConfig(level=LOG_LEVELS.get(verbosity_level),filename='enrich.log', encoding='utf-8',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVELS.get(verbosity_level))

    # Create a file handler
    file_handler = logging.FileHandler('enrich.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    

    # Create a stream handler (for console output)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    if not silent:
        logger.addHandler(stream_handler)

def setup_logging():
    global parser
    parser = argparse.ArgumentParser(description="This is a tamplate app")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="Increase verbosity level (-v, -vv, -vvv)")
    parser.add_argument("-s","--silent", action="store_true", help="Don't log to the console, dont show progressbar" )
    
    args = parser.parse_args()
    global silent
    silent = args.silent
    configure_logging(args.verbosity,silent)

def save_dataframe_to_file(df, filename):
    file_extension = filename.split('.')[-1].lower()
    logging.info(f"filextension selected:{file_extension}" )
    # Define a dictionary mapping extensions to Pandas functions
    save_functions = {
        'csv': lambda:json_normalize(df.to_dict(orient='records')).to_csv(filename, index=False,sep='|'),
        'xlsx': lambda: json_normalize(df.to_dict(orient='records')).to_excel(filename, index=False),# df.to_excel(filename, index=False),#json_normalize(df.to_dict(orient='records')).to_excel(filename, index=False),
        'json': df.to_json(filename),
        'feather': df.to_feather,
        'ft': df.to_feather,  # Alias for feather
        'parquet': df.to_parquet,
        'h5': lambda: df.to_hdf(filename, key='data', mode='w'),
        'hdf5': lambda: df.to_hdf(filename, key='data', mode='w')
    }
    
    save_function = save_functions.get(file_extension)
    if save_function:
        save_function()
        logging.info(f"output file saved:{filename}" )
    else:
        logging.critical(f"Unsupported file extension: {file_extension}")

def SingleThreadedOperation(func,iterable):
    resultArray=[]
    with logging_redirect_tqdm():
        for i in  trange(len(iterable), disable=silent ):
             result= func(i)
             logging.info("TestLogWhile {} ".format (result))  
             resultArray.append( result)
               
    logging.info("Sequential Iteration Successful")
    return resultArray

def MultiThreadedOperation(func,iterable,max_workers): 
    resultArray=[]
    with tqdm(total=len(iterable)) as pbar :
        with ThreadPoolExecutor(max_workers=max_workers) as e:
            futures = [
                e.submit(func, i) for i in iterable
            ]
            for future in as_completed(futures):
                result = future.result()
                pbar.update(1)

                logging.info(f"TestLogWhile {result}")  
                resultArray.append(result)
                
                  
    logging.info("Concurrent Iteration Successful")
    return resultArray



if __name__ == '__main__':
    setup_logging()
    
    parser.add_argument("-o", action="store", help="Output format like asd.xlsx or asd.json" )
    args = parser.parse_args()

    env = Env()
    # Read .env into os.environ
    env.read_env()
    print (env.str("NOTSOSECRETKEY"), env.int("PORT"))  

    logging.info("Application start with args {}".format(args))

    myIterable = range(1,10)
    resultArray=SingleThreadedOperation(arbitraryTestFunc,myIterable)

    myIterable = range(1,100)
    resultArray=MultiThreadedOperation(arbitraryTestFunc,myIterable,6)
    

    df = pd.DataFrame(resultArray)
    print("result:",df)
    if args.o:
        save_dataframe_to_file(df,args.o)
    

    logging.info("Application end")
    