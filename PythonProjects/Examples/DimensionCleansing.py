print('Initializing')

from fuzzywuzzy import fuzz
from pandas import read_csv
from pydomo import Domo

# My Domo Client ID and Secret (https://developer.domo.com/manage-clients)
creddf = read_csv('./examples/Credentials.csv')

CLIENT_ID = creddf.iat[0,0]
CLIENT_SECRET = creddf.iat[0,1]

# The Domo API host domain. This can be changed as needed - for use with a proxy or test environment
API_HOST = 'api.domo.com'

domo = Domo(CLIENT_ID,CLIENT_SECRET,API_HOST) # get secure Domo Access 

# Download the right data set from Domo. If it is the first pass then use the seed dsid
# If alread processed then use the created dsid
dsl = domo.ds_list() # Get list of all datasets in instance
matchdsrow = next(iter(dsl[dsl['name'] == 'Python_Oppty'].index), 'no match') # Find if the dataset exists and where
if matchdsrow == 'no match' :
    dsid = 'f11ad79a-e450-4be2-a9e5-0c13161844de' # the seed dataset id
    mydf = domo.ds_get(dsid) # get the oppty dataset from Domo
    mydf['LeadSourceCleaned'] = False # add LeadSourceCleaned column when seeding
else : 
    matchcol = dsl.columns.get_loc('id') # get the index for the id column
    dsid = dsl.iloc[matchdsrow,matchcol] # set the dsid for the matched dataset
    mydf = domo.ds_get(dsid) # get a previously cleaned dataset from Domo

#Flags and Counters
bug = False
madechanges = 0

#*****************************************************************************************************

# Fuzzy Match Arrary
fuzar = {'Partner', 'Referral', 'Direct', 'Inc', 'Event', 'Marketing','Strategic Account Marketing',
        'Sales','Social','Renewal'}

# Contains Match Array
containar = {'cur':['Strategic','Jigsaw','Social','Event','Sales','Content','Self' ],
        	 'mapto':['Sales','Marketing','Marketing','Event','Sales','Marketing','Sales' ] }

#Mapping Array
mapar = {'cur':['Efeal','Patneing','Direct','Email','Chat', 'Event' , 'Inc'], 
         'mapto':['Referral','Partner','Sales','Marketing','Marketing','Marketing','Sales' ] }

#*****************************************************************************************************


# High Level Cleansing
mydf['LeadSource'] = mydf['LeadSource'].str.title() # Change all Leadsource values to Title Case
mydf['LeadSource'].fillna('Unknown', inplace = True ) # Change all null Leadsource Values to Unknown

lsi = mydf.columns.get_loc('LeadSource') # Find column index of the LeadSource Column
lsc = mydf.columns.get_loc('LeadSourceCleaned') # Find column index of the LeadSourceCleaned Column

# Loop through each Oppty row and cleanse
print('Looping through Oppty Rows')
for i in range(len(mydf['LeadSource'])) : 
    # Process only rows that have not been cleaned
    cleansed = mydf['LeadSourceCleaned'].iloc[i]
    if cleansed == False : 
        ls = mydf['LeadSource'].iloc[i]
        
        # fuzzy======================= Loop through the fuzar array
        for newls in fuzar : 
            score = fuzz.ratio( newls, ls)
            # If the fuzzy match score is in bounds then change the leadsource
            if (score >= 60 and score < 100) :  
                mydf.iat[i,lsi] = newls
                mydf.iat[i,lsc] = True  # Set LeadSourceCleansed to True
                madechanges += 1
                if bug : 
                    print(i, 'FUZZY REPLACED', ls, 'WITH', newls, score, mydf.iloc[i,0])
                ls = newls
            
        # contains ===================   Loop through the containar array 
        for j in range(len(containar['cur'])) : 
            compsrc = containar['cur'][j]
            newls = containar['mapto'][j]
            # if the search is found in the leadsource change it
            if compsrc.lower() in ls.lower() and ls != newls : 
                mydf.iat[i,lsi] = newls
                mydf.iat[i,lsc] = True  # Set LeadSourceCleansed to True
                madechanges += 1
                if bug :
                    print(i,'CONTAINS FOUND', compsrc, 'REPLACED', ls, 'WITH', newls, mydf.iloc[i,0])
                ls = newls

        # Map ======================== loop through the mapar array
        for j in range(len( mapar['cur'])) :  
            compsrc = mapar['cur'][j]
            newls = mapar['mapto'][j]
            # if there is an exact match change the Leadsource to the Mapped Value
            if ls == compsrc :  
                mydf.iat[i,lsi] = newls
                mydf.iat[i,lsc] = True  # Set LeadSourceCleansed to True
                madechanges += 1
                if bug : 
                    print(i, 'MAPPED from', ls, 'TO', newls , mydf.iloc[i,0])
                ls = newls       

if matchdsrow == 'no match' :  #if first run create new dataset
    domo.ds_create(mydf,'Python_Oppty','Lead Source Cleansed')
    print('First run created new cleansed dataset Python_Oppty with ' + str(madechanges) + ' changes. View the dataset in the Domo DataSets page')
else:   # if not first run then update the dataset
    if madechanges > 0 :
        domo.ds_update(dsid,mydf)
        print(madechanges,'Changes Made')
    else:
        print('No Changes Found')




    

