import xml.etree.ElementTree as ET


'''
Takes a list, returns a string with individual elements of that list seperated by commas

If list is empty, returns an empty list
'''


def toString(list):


    if None in list:
        return []
    else:
        return ', '.join(list)
    


'''
Given root from parsed XML file

Searches for tag 'level', which returns 3 strings

Returns 3 strings representing the three product levels
'''
def extract_levels(root):
    productLevels = []
    for level in root.iter(tag='Level'):
        productLevels.append(level.text)
    return productLevels[0],productLevels[1],productLevels[2]



'''
Given root from parsed XML file

Searches for the description tag

Returns a string representing the product description
'''
def extract_description(root):
    descriptions=[]
    for description in root.iter(tag='Description'):
        descriptions.append(description.text)
    return toString(descriptions)



'''
Given root from parsed XML file

Extracts various strings that are found using the longtextitems tag

returns each of these items as strings
'''
def extract_longtextitems(root):
    ingredients=[]
    features=[]
    recycling_other=[]
    
    for statements in root.iter(tag='LongTextItems'):
        statementAttr = statements.attrib

        if statementAttr['Name'] == 'Ingredients':
            for statement in statements:
                ingredients.append(statement.text)

        elif statementAttr['Name'] =='Features':
            for statement in statements:
                features.append(statement.text)

        elif statementAttr['Name'] =='Recycling Other Text':
            for statement in statements:
                recycling_other.append(statement.text)
    
    return toString(ingredients), toString(features), toString(recycling_other)



'''
Given root from parsed XML file

Searches for the statements tag, then filters further by the Name of the elements found

returns the string found which represents the storage and usage statements
'''
def extract_statements(root):
    storage=[]

    for statements in root.iter(tag='Statements'):
        statementAttr = statements.attrib

        if statementAttr['Name'] == 'Storage and Usage Statements':
            for statement in statements:
                storage.append(statement.text)

    return toString(storage)



'''
Given root from parsed XML file

Searches the nameTextItems tags, and filters by the name 'Identification'

Returns a string of the elements found, which represents the preserve information
'''
def extract_nameTextItems(root):
    preserves=[]

    for statements in root.iter(tag='NameTextItems'):
        statementAttr = statements.attrib
        if statementAttr['Name'] == 'Identification':
            for statement in statements:
                for preserve in statement:
                    preserves.append(preserve.text)
    
    return toString(preserves[2:])



'''
Given root from parsed XML file

Searches for the memo tag, then further filters by the name 'Product Marketing'

Returns a string which represents the marketing information of the products
'''
def extract_marketing(root):
    marketing=[]
    for statements in root.iter(tag='Memo'):

        statementAttr = statements.attrib
        
        if statementAttr['Name'] == 'Product Marketing':
            marketing.append(statements.text)

    return toString(marketing)


'''
Given root from parsed XML file

Extracts information from the  namelookup tag

Searches the namelookup tag elements for the following data:
-Allergy advice
-Recycling Information
-Standardised Brand

Returns 3 strings, each representing one of the above
'''

def extract_NameLookups(root):
    allergyAdvice=[]
    recycling=[]
    brands=[]

    for statements in root.iter(tag='NameLookups'):
        statementAttr = statements.attrib

        if statementAttr['Name'] == 'Allergy Advice':
            for statement in statements:
                for allergy in statement:
                    allergyAdvice.append(allergy.text)

        elif statementAttr['Name'] == 'Recycling Info':
            for statement in statements:
                for recyclingstatement in statement:
                    recycling.append(recyclingstatement.text)

        elif statementAttr['Name'] == 'Standardised Brand':
            for statement in statements:
                brands.append(statement[1].text)
    
   

    #handle None Type Errors before returning
    allergyAdviceString = toString(allergyAdvice)
    recyclingString = toString(recycling)
    brandsString = toString(brands)
    return allergyAdviceString, recyclingString, brandsString



'''
Given root from parsed XML file

Searches for the code tag, which contains the gtin number

returns the gtin number as a string
'''
def extract_GTIN(root):
    gtin=''
    for statements in root.iter(tag='Code'):
        statementAttr = statements.attrib
        if statementAttr['Scheme'] == 'GTIN':
            gtin = statements.text
    return gtin



'''
Given root from parsed XML file

Searches for the product tag. the 'VersionDateTime' attribute of this attribute contains the date/time the product was added

The time is filtered out

Returns a string containing the date the product was added
'''
def extract_date(root):
    for statements in root.iter(tag='Product'):
        return statements.attrib['VersionDateTime'][:10]
    

'''
Given the filename, and the path to the folder

Parses the XML file, creates tree and stores the root to that tree

Checks to see if the file is a 'Delete' file or not.

If it is, returns a list containing the xml name, the gtin, the date & isDelete = 1

If it is not, it extract various strings from the xml file using the extract functions, and retuns a list containing them all
'''
def extract_from_xml(xmlpath,name):

    tree = ET.parse(xmlpath)
    root = tree.getroot()
    productList=[]

    for product in root.iter(tag='Product'):
        productAttr = product.attrib
        if productAttr['UpdateType'] != 'Delete':
            isDelete=0

            gtin = extract_GTIN(root)


            pl1,pl2,pl3 = extract_levels(root)


            date = extract_date(root)


            description = extract_description(root)
        

            allergyAdvice, recycling, brands = extract_NameLookups(root)

        
            marketing = extract_marketing(root)


            ingredients, features, recycling_other = extract_longtextitems(root)
            

            storage = extract_statements(root)


            preserves = extract_nameTextItems(root)

            productList=[
                name,
                gtin,
                isDelete,
                date,
                pl1,pl2,pl3,
                description,
                allergyAdvice,
                recycling,
                recycling_other,
                brands,
                marketing,
                ingredients,
                features,
                storage,
                preserves]
        else:
            gtin=extract_GTIN(root)
            date = extract_date(root)
            isDelete=1
            productList=[
                name,
                gtin,
                isDelete,
                date,
                '','','','','','',
                '','','','', '','','']
            

    return productList


