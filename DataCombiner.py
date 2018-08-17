import pythonprelude.FPToolBox as fp
import os
import errno
import pythonprelude.EasyWriter as ew
import pythonprelude.TableReader as tr

# a set save current headers
# key: header list, value fname with surfix

wFile = ew.wFile
dataFormat = tr.dataFormat

# function that dealing with all files in a folder
def rwFiles(filter_func, rfolder='../', wfolder='./combined', 
            wName='combined', counter=0, osfix='.dat'):
    headers = {}
    files = os.listdir(rfolder)
    for fname in files:
        if filter_func(fname):
            counter, headers = rwFile(rfolder, fname, wfolder, 
                                    wName, counter, osfix, headers)


# function that dealing with single file
def rwFile(rfolder, rfname, wfolder, wfname, cnt, osfix, headers):
    # get info lists
    flst = dataFormat(rfolder + '/' + rfname)
    outStr = ''

    if flst != []:
        head = flst[0]
        info = flst[1:]
        headtp = tuple(head)
        # check if head is already there
        if headtp in headers.keys():
            fsave = headers[headtp]
            headStr = ''
        else:
            fsave = wfname + str(cnt) + osfix
            cnt = cnt + 1
            headers[headtp] = fsave
            headStr = 'fname\t' + rowStr(head)
        # create outname 
        wffname = wfolder + '/' + fsave
        # create out string
        if info == []:
            outStr = rfname + '\tNo contents!\n'
        else:
            outStr = ''.join(fp.lmap(lambda x: rfname + '\t' + rowStr(x), info))
        outStr = headStr + outStr

        # write file
        wFile(wffname, outStr)
    else:
        effname = wfolder + '/' + 'error.dat'
        errStr = rfname + '\t' + 'empty file'
        wFile(effname, errStr)

    return (cnt, headers)
           

# form a row
def rowStr(slst):
    # get the concatnation function
    sConcat = fp.concat('\t')
    return fp.foldr(sConcat, slst, '')[:-1] + '\n'


# basic filter function use prefix, surfix, and contains
def prefix_filter(strs):
    if strs == '':
        return trueFunc
    def isprefix(x):
        if x[:len(strs)] == strs:
            return True
        else:
            return False
    return isprefix


def surfix_filter(strs):
    if strs == '':
        return trueFunc
    def issurfix(x):
        if x[-len(strs):] == strs:
            return True
        else:
            return False
    return issurfix


def contain_filter(strs):
    if strs == '':
        return trueFunc
    def iscontain(x):
        return strs in x
    return iscontain


def trueFunc(x):
    return True


if __name__ == '__main__':
    while True:
        print('\n' + ('-'*50))
        print('Enter file filter: prefix;contains;surfix:')
        x = input()
        val = x.split(';')
        if len(val) != 3:
            print('\nInput incorrect, please specify file filter requirements, examples:')
            print('test;2018;dat   -- means start with "test", end with "dat, contain "2018"')
            print('test;;          -- means start with "test", no other requirements.')
            print('\npress any key to enter again.')
            print('press q to exit.')
            y = input()
            if y == 'q':
                exit()
        else:
            # print(val[0])
            # print(val[1])
            # print(val[2])
            pfunc = prefix_filter(val[0])
            cfunc = contain_filter(val[1])
            sfunc = surfix_filter(val[2])
            filterFunc = lambda x: pfunc(x) and cfunc(x) and sfunc(x)
            rwFiles(filterFunc)
            print('data extraction done.')
            exit()

##    rfolder = './'
##    rfname = 'EXP_201808020047_confignew0_local_config0.dat'
##    wfolder = './combinedtest'
##    wfname = 'combine'
##    cnt = 1
##    osfix = '.dat'
##    headers = {}
##    cnt, headers = rwFile(rfolder, rfname, wfolder, wfname, cnt, osfix, headers)
##    print(cnt)
##    print(headers)
        


