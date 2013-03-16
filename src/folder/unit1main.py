import random,string

list_of_entries = {} #import globaltable

features = ('large_screen_size' , 'medium_screen_size', 'small_screen_size', 'camera','flash_support','media_queries' , 'geolocation','app_cache','local_storage')
screen_size=('large_screen_size','medium_screen_size','small_screen_size')

def gen_table(rec):
    '''the gen_table fun is used to generate a test database'''
    list_of_enteries=[]
    wfile = open("database.txt","w")
    for i in range(rec) :
        d={}            #list of dictionaries representing database
        url = 'www.' + ''.join(random.sample(string.letters,random.randint(10,15)))+random.choice(('.com','.org','.edu','.net'))
        d['url']= url
        d['large_screen_size'] = True #it is assumed that every url supports large_screen_size(ie PC)
        for j in range(1,9) :
            d[features[j]] = random.choice((True,False))
        d['media_queries'] = d[features[1]] or d[features[2]] #media query is true if any other screen size apart from large is also supported
        list_of_enteries.append(d)
        for each in d.keys() : #or d same #writing the test database to a file
            wfile.write(each+':'+str(d[each])+' ')
        wfile.write('\n')
    return list_of_enteries

def readdb():
    '''reads database.txt to form the database required for the queries'''
    myfile=open('database.txt')
    data=[]
    for line in myfile :
        x=line.strip()
        keyvaldata=(x.split(' '))
        e={}
        for item in keyvaldata :
            #print keyvaldata,'keyvaldata'
            key,value = item.split(':')
            value = value.strip()
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            #d={key.strip() : value }
            e[key.strip()] = value #.update(d)

        data.append(e)
    return data


#if shortform is used then it is a selection get those in find that are true - default or as specified, url must be specified in this case else error
#such a query can must have specific url as constraint, other constraints that can be used are the shortforms in find
#if shortform is not used everything in find is fetched
def resolve_query(find,constraint) :
    '''Resolves the query fetches data that satisfies the constraints'''
    try :
        shortform = {'screen_size':screen_size,'features':features} #dict of aliases
        shortused = []
        for selectitem in find :
            if selectitem in shortform :
                shortused.append(selectitem) #shortform[ ]
                if constraint.has_key(selectitem) == False:
                    constraint[selectitem] = True
                find.remove(selectitem)

        if len(shortused)!=0 : #To handle cases where shortform is used
            if constraint.has_key('url') == False or len(constraint)>(1+len(shortused)):
                return 'error in query'
            row=None
            for each in list_of_entries: #finding the url
                if each['url']==constraint['url']:
                    row = each
                    break
            if row is None:
                return 'no such url'

            result={} #[]    #dict containing results of the query
            for i in shortused:
                for j in shortform[i] :
                    #print j,row[j],constraint[i],row[j]==constraint[i]
                    if row[j] == constraint[i] :
                        result[j] = constraint[i]
            for select in find :
                result[select] = row[select]

            return result #[]

        else:
            rows=[] #list containing results of the query
            cons = constraint.keys()
            for elem in list_of_entries:
                add = True
                for con in cons :
                    if elem[con] != constraint[con]:
                        add = False
                        break
                if add : #adding field in to result if value is what is mensioned in the query
                    row={}
                    for select in find :
                        row[select] = elem[select]
                    rows.append(row)
            return rows
    except KeyError as k:
        return 'check your query no such field in table'+str(k)


def query(stmt):
    '''the query function is used to split up the query into requirements and constraints and pass the the constraints as key value pairs'''
    try :
        line = stmt.split(':') #separating requirements and constraints
        find = line[0].split(',')
        for i in range(0,len(find)):
            find[i] = find[i].strip()
        constraint ={}
        if len(line) > 1 :
            cons = line[1].split(',')
            for con in cons :
                key,val = con.split('-')
                key = key.strip()
                val = val.strip()
                if val.lower() == 'true' : #making true/false case insensitive
                    val = True
                elif val.lower() == 'false':
                    val = False
                constraint[key] = val
        #print find
        #print constraint
    except ValueError:
        return 'error in query'
    return resolve_query(find,constraint)

if __name__=='__main__':
    use = raw_input('use the existing database(y/n) ?')
    if use.lower()=='y' :
        list_of_entries = readdb()
    else :
        entered = False
        while not entered :
            no_entries=raw_input('specify the number of entries in the database(1-100)')

            if no_entries.isdigit() == False or int(no_entries)<1 or int(no_entries)>100 :
                print 'invalid entry'
            else :
                entered = True

        list_of_entries = gen_table(int(no_entries))

    #Displays the generated database
    for each_row in list_of_entries :
        print each_row,'\n\n'

    print '''Sample query \n 1)To list the url and geolocation facility of a website which support media_queries but not camera
            \n url,geolocation:media_queries-true,camera-false \n'''
    print ' 2)To find the features of a url \n www.abc.com:features \n where features is a tuple \n'#features:url-www.abc.com,features-true
    continu = 'y'
    print 'query format \n <requirement1,requirement2,..>:<constraint1,constraint2,...>\n'
    while continu == 'y' :
        input = raw_input(' Enter the query : \n')
        result = query(input)
        #print find,'\n'
        print 'result for the query is : \n',result
        continu = raw_input(' do you want to continue (y/n) :')

else :
        use = raw_input('use the existing database(y/n) ?')
        if use.lower()=='y' :
            list_of_entries = readdb()
        else :
            entered = False
            while not entered :
                no_entries=raw_input('specify the number of entries in the database(1-100)')
                if no_entries.isdigit() == False or int(no_entries)<1 or int(no_entries)>100 :
                    print 'invalid entry'
                else :
                    entered = True
            list_of_entries = gen_table(int(no_entries))
