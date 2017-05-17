#DO NOT MODIFY THIS FILE
import LobbyDBClient
import pandas
from hdrh import histogram
from datetime import datetime
import random
import numpy
from multiprocessing import Process, Queue
import sys, traceback
import zlib
import cPickle as pickle
import argparse
import logging
from HWUtils import RecordNotFound

#logging
logger= logging.getLogger('lobbyhw')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)

# FYI These are the debug levels
#logger.debug('debug message')
#logger.info('info message')
#logger.warn('warn message')
#logger.error('error message')
#logger.critical('critical message')


#phases
LOADC = 'LOAD_CLIENT'
LOADL = 'LOAD_LOBBYIST'
LOADE = 'LOAD_EMP'

#DFS
EMP = 'emp'
LOB_EMP_CLIENT = 'lobbyist_emp_client'
CLIENT = 'client'
LOB_EXPEND = 'lob_expend'
LOB_COMPENSATION = 'lob_comp'
LOB_ACTIVITY = 'lob_activity'
LOB_GIFT = 'lob_gift' # TODO add
LOB_CONTRIBUTIONS = 'lob_contributions' # TODO add

#OPS
INSERT_EXPEND='INSERT_EXPEND'
READ_EXPEND_BY_ID='READ_EXPEND_BY_ID'
READ_EXPEND_BY_LOBBYIST_ID='READ_EXPEND_BY_LOBBYIST_ID'
INSERT_COMP='INSERT_COMP'
READ_COMP_BY_ID='READ_COMP_BY_ID'
READ_COMP_BY_CLIENT_ID='READ_COMP_BY_CLIENT_ID'
READ_COMP_BY_GREATER_THAN_COMPENSATION='READ_COMP_BY_GREATER_THAN_COMPENSATION'
INSERT_ACTIVITY='INSERT_ACTIVITY'
READ_ACTIVITY_BY_ID='READ_ACTIVITY_BY_ID'
COUNT_ACTIVITY_BY_CLIENT_ID='COUNT_ACTIVITY_BY_CLIENT_ID'





#Main
def runLobbyDB(args):
    logger.info("Staring LobbyDB")
    if (args.debug):
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug Mode")
    dfs = loadDFs()
    procs = []
    dbClients = []
    loadHists = {}
    opHists = {}
    dbClient = LobbyDBClient.client(args.override)
    if args.skipload:
        logger.warn("==>Skipping load phase")
    else:
        try:
            dbClient.openConnection()
            loadHists = loadInitialData(dfs, dbClient)
        except:
            logger.error( "Error: %s" % sys.exc_info()[0])

            traceback.print_exc()
        finally:
            dbClient.closeConnection()

    if args.skipops:
        logger.warn("==>Skipping operations phase")
    else:
        try:
            opList = genOpList(dfs)
            if args.limit_ops:
                opList= opList[:args.limit_ops]
            splitOpList = chunkList(opList, args.procs)

            q = Queue()
            logger.debug("Starting %s processes to read and write lobby activity" %args.procs)
            for i, ops in enumerate(splitOpList):

                _dbC = LobbyDBClient.client(args.override)
                _dbC.openConnection()
                p = Process(target=runOperations, args=(dfs,_dbC,ops,q,i))
                p.start()
                procs.append(p)
                dbClients.append(_dbC)
            logger.debug("Waiting on %s processes to finish "%len(procs))
            for p in procs:
                p.join()
            logger.debug("Getting results")
            # get ops
            opHists = {}
            while not q.empty():
                _opHists = q.get()
                for key in _opHists.keys():
                    h = getHist()
                    if key in opHists:
                        #merge
                        opHists[key].add(h.decode(_opHists[key]))
                        pass
                    else:
                        opHists[key] = h.decode(_opHists[key])


            printStats(opHists,loadHists)
        except:
            logger.error("Error:%s" % sys.exc_info()[0])
            traceback.print_exc()
        finally:
            for _dbC in dbClients:
                _dbC.closeConnection()

        if args.skipanalyze:
            logger.warn("==> Skipping analyze phase")
        else:
            try:
                dbClient.openConnection()
                analyzeHists = analyzeData(dfs, dbClient)
                logger.info("Load Analyze Times")
                for key in analyzeHists.keys():
                    logger.info(getStatString(key, analyzeHists[key]))

            except:
                logger.error("Error: %s"% sys.exc_info()[0])
                traceback.print_exc()
            finally:
                dbClient.closeConnection()

def getStatString(key, hist):
    if hist.get_total_count() == 0:
        d = {50:0,95:0,99:0,100:0}
    else:
        d = hist.get_percentile_to_value_dict([50,95,99,100])

    return "%40s -  Latency Perecentiles(ms) - 50th:%4.2f, 95th:%4.2f, 99th:%4.2f, 100th:%4.2f - Count:%s" % (key, d[50],d[95],d[99],d[100], hist.get_total_count() )

def printStats(opHists,loadHists):
    logger.info("Load Operation Times")
    for key in loadHists.keys():
        logger.info(getStatString(key, loadHists[key]))
    logger.info("Operation Times")
    for key in opHists.keys():
        logger.info(getStatString(key, opHists[key]))

#from http://stackoverflow.com/questions/2130016/splitting-a-list-of-arbitrary-size-into-only-roughly-n-equal-parts
def chunkList(seq, num):
  out = []
  try:
    avg = len(seq) / float(num)
    last = 0.0
    while last < len(seq):
      out.append(seq[int(last):int(last + avg)])
      last += avg
  except:
    pass
  return out

def loadDFs():
    dfs = {}
    try:
      with open('data/dfs.pi','r') as f:
          zstr = f.read()
          str = zlib.decompress(zstr)
          dfs = pickle.loads(str)
    except:
      dfs = pandas.read_pickle('data/pandas.pi')
    return dfs

def getHist():
    return histogram.HdrHistogram(1,1000*60*60,2)

def genOpList(dfs):
    ops = []
    lobbyist_ids = dfs[LOB_EMP_CLIENT].LOBBYIST_ID.values
    client_ids = dfs[CLIENT].CLIENT_ID.values
    #keys for expend
    exp_write_ids = dfs[LOB_EXPEND].index.values
    exp_read_ids = numpy.random.choice(exp_write_ids, len(exp_write_ids)/3)
    exp_by_lobbyist = numpy.random.choice(lobbyist_ids, 400)
    #keys for comp
    lob_comp_ids = dfs[LOB_COMPENSATION].index.values
    comp_read_ids = numpy.random.choice(lob_comp_ids, len(lob_comp_ids)/5)
    comp_by_client = numpy.random.choice(client_ids, 500)
    comp_amounts = numpy.random.choice(dfs[LOB_COMPENSATION].COMPENSATION_AMOUNT.values,100)
    #keys for activity
    lob_act_ids = dfs[LOB_ACTIVITY].index.values
    act_read_ids = numpy.random.choice(lob_act_ids, len(lob_act_ids)/2)
    act_client_ids = numpy.random.choice(dfs[LOB_ACTIVITY].CLIENT_ID, 1000)

    ops.extend((INSERT_EXPEND,LOB_EXPEND, x) for x in exp_write_ids )
    ops.extend((READ_EXPEND_BY_ID,LOB_EXPEND, x) for x in exp_read_ids )
    ops.extend((READ_EXPEND_BY_LOBBYIST_ID,LOB_EXPEND, x) for x in exp_by_lobbyist)
    ops.extend((INSERT_COMP,LOB_COMPENSATION, x) for x in lob_comp_ids )
    ops.extend((READ_COMP_BY_ID,LOB_COMPENSATION, x) for x in comp_read_ids )
    ops.extend((READ_COMP_BY_CLIENT_ID,LOB_COMPENSATION, x) for x in comp_by_client )
    ops.extend((READ_COMP_BY_GREATER_THAN_COMPENSATION,LOB_COMPENSATION, x) for x in comp_amounts )
    ops.extend((INSERT_ACTIVITY,LOB_ACTIVITY, x) for x in lob_act_ids )
    ops.extend((READ_ACTIVITY_BY_ID,LOB_ACTIVITY, x) for x in act_read_ids )
    ops.extend((COUNT_ACTIVITY_BY_CLIENT_ID,LOB_ACTIVITY, x) for x in act_client_ids )

    random.shuffle(ops)
    return ops


def loadInitialData(dfs, dbClient):
    logger.info("Loading Initial Data")
    start = datetime.now()
    hists = {}
    #load clients
    loadc= getHist()
    for i, c in  dfs[CLIENT].iterrows():
        s = datetime.now()
        dbClient.loadClient(c['CLIENT_ID'], c['NAME'], c['ADDRESS_1'], c['ADDRESS_2'], c['CITY'], c['STATE'], c['ZIP'])
        e = datetime.now()
        time = e - s
        loadc.record_value(time.total_seconds() * 1000)
    hists[LOADC] = loadc


    #load employees
    loade = getHist()
    for i, r in  dfs[EMP].iterrows():
        s = datetime.now()
        dbClient.loadEmployer(r['EMPLOYER_ID'], r['NAME'], r['ADDRESS_1'], r['ADDRESS_2'], r['CITY'], r['STATE'], r['ZIP'])
        e = datetime.now()
        time = e - s
        loade.record_value(time.total_seconds() * 1000)
    hists[LOADE] = loade

    #load lobbyist and connections
    loadl = getHist()
    for i, r in  dfs[LOB_EMP_CLIENT].iterrows():
        s = datetime.now()
        dbClient.loadLobbyistAndCreateEmployerClientConnection(r['LOBBYIST_ID'], r['EMPLOYER_ID'], r['CLIENT_ID'], r['LOBBYIST_SALUTATION'],r['LOBBYIST_FIRST_NAME'],r['LOBBYIST_LAST_NAME'])
        e = datetime.now()
        time = e - s
        loadl.record_value(time.total_seconds() * 1000)
    hists[LOADL] = loadl
    end = datetime.now()
    time = end - start
    logger.info("Time to load base tables :%s (sec) " % time.total_seconds())
    return hists

def runOperations(dfs, dbClient, ops, q, i):
    logger.info("Running Operations")

    hists = {}
    for o in ops:
        op = o[0]
        if op not in hists:
            hists[op] = getHist()
        try:
            s = datetime.now()
            if op == INSERT_EXPEND:
                r = dfs[o[1]].ix[o[2]]
                dbClient.insertExpenditure(r['EXPENDITURE_ID'], r['LOBBYIST_ID'], r['ACTION'], r['AMOUNT'], r['EXPENDITURE_DATE'], r['PURPOSE'], r['RECIPIENT'], r['CLIENT_ID'])
            elif op == READ_EXPEND_BY_ID:
                dbClient.readExpenditureById(o[2])
            elif op == READ_EXPEND_BY_LOBBYIST_ID:
                dbClient.readExpendituresByLobbyistId(o[2])
            elif op == INSERT_COMP:
                r = dfs[o[1]].ix[o[2]]
                dbClient.insertCompensation(r['COMPENSATION_ID'], r['LOBBYIST_ID'], r['COMPENSATION_AMOUNT'], r['CLIENT_ID'])
            elif op == READ_COMP_BY_ID:
                dbClient.readCompensationById(o[2])
            elif op == READ_COMP_BY_CLIENT_ID:
                dbClient.readCompensationsByClientId(o[2])
            elif op == READ_COMP_BY_GREATER_THAN_COMPENSATION:
                dbClient.readCompensationsInBetween(o[2],float(o[2])+1000)
            elif op == INSERT_ACTIVITY:
                r = dfs[o[1]].ix[o[2]]
                dbClient.insertActivity(r['LOBBYING_ACTIVITY_ID'], r['ACTION_SOUGHT'], r['DEPARTMENT'], r['CLIENT_ID'], r['LOBBYIST_ID'])
            elif op == READ_ACTIVITY_BY_ID:
                dbClient.readActivityById(o[2])
            elif op == COUNT_ACTIVITY_BY_CLIENT_ID:
                dbClient.countActivityByClientId(o[2])
            else:
                logger.error("Unknown operation: %s" %o)
                continue
            e = datetime.now()
            time = e - s
            hists[op].record_value(time.total_seconds() * 1000)
        except RecordNotFound as e:
            logger.debug("RecordNotFound %s" % e)
        except NotImplementedError as e:
            logger.error("NotImplementedError %s" % e)
        except:
            e = sys.exc_info()[0]
            logger.error( e)

    enc_hists = {}
    for h in hists.keys():
        enc_hists[h] = hists[h].encode()
    q.put(enc_hists)

def analyzeData(dfs, dbClient):
    logger.info("Analyzing Data")
    ahists = {'MOST_PRODUCTIVE_LOBBYIST': getHist(), 'LEAST_EFFICIENT_CLIENT':getHist()}

    s = datetime.now()
    dbClient.findMostProductiveLobbyist()
    e = datetime.now()
    time = e - s
    ahists['MOST_PRODUCTIVE_LOBBYIST'].record_value(time.total_seconds() * 1000)
    s = datetime.now()
    dbClient.findLeastEfficientClient()
    e = datetime.now()
    time = e - s
    ahists['LEAST_EFFICIENT_CLIENT'].record_value(time.total_seconds() * 1000)
    return ahists


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Do a simple lobbyist benchmark application. Phases in order are Load, Ops, Analyze')
    parser.add_argument('--processes', dest='procs', type=int, default=4, help='The number of parallel processes to do read and write operations')
    parser.add_argument('--limit_ops', help='Limit the number of operations (use only for testing)', type=int, dest='limit_ops', default=None)
    parser.add_argument('--skipload', action='store_true', help='Skip the loading phase')
    parser.add_argument('--skipops', action='store_true', help='Skip the operation phase')
    parser.add_argument('--skipanalyze', action='store_true', help='Skip the analyze phase')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--override', action='store_true', help='Override Client db connection parameters (for grading only)')
    args = parser.parse_args()
    runLobbyDB(args)
