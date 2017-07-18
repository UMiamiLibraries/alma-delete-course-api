import requests
from bs4 import BeautifulSoup
from lxml import etree

#global variables
apikey = '' #use blackboard api key from ex libris developer site
offset = '0'
response = None
full_reading_list = []
course_ids = []
readinglistids = []
courses_to_delete = []

#*************************
#method to call course api and retrieve all courses
#parameters: none
#response: xml response of courses
#****************************
def retrieve_courses():    

    print("*******retrieving courses*******")
    #create search parameters
    payload = {
        'apikey' : apikey,
        'limit' : '100',
        'offset' : offset,
        'order_by' : 'code,section',
        'direction' : 'ASC'
        #'q' : 'code~2016'
        }

    #create request url
    response = requests.get('https://api-na.hosted.exlibrisgroup.com/almaws/v1/courses/', params=payload)
    print("***" + response.url + "***")
   
    root = etree.fromstring(response.content)
    return root
    
#****************************
#filter initial results to remove inactive courses
#parameters: initial response object from get course api    
#response: list of active courses in xml format
#****************************    
def get_course_ids(courses):
    #is_inactive = etree.XPath(".//status[text()='ACTIVE']")
    code = etree.XPath(".//code[contains(text(),'2016')]")
    course_id = etree.XPath(".//id")
    courseids = []
    for element in courses:
        if code(element):
            print(code(element)[0].text)
            courseids.append(course_id(element)[0].text)
        else:
            root.remove(element)
    return courseids


#****************************
#method to call reading list api and retrieve the reading list for a single course
#parameters: list of active course ids  
#response: list of reading list ids
#****************************
def check_reading_lists(courseids):

    print("*******checking reading lists*******")
    #create search parameters
    payload = {
        'apikey' : apikey,
        'limit' : '100',
        'offset' : '0',
        }    
    
    #create request url
    for courseid in courseids:
        url = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/courses/' + courseid + '/reading-lists'
        r = requests.get(url, params=payload)
        print(r.url)                
        
        #for parsing with etree
        root = etree.fromstring(r.content)
        readinglistid = etree.XPath('/reading_lists/reading_list/id')
        if not readinglistid(root):
            courses_to_delete.append(courseid)
        else:
            print("Reading list id: " + readinglistid(root)[0].text + " | course id: " + courseid)
                
    #return readinglistids
    
def delete_courses(courseids):
    print("*******deleting courses*******")
    #TODO: call delete course
    for courseid in courseids:
        print("deleting course" + courseid)
    
    
    
#************************
# first retrieve list of courses from get courses api
# then filter the courses, removing all old courses and get their ids
# send course ids to reading list api and see if they have a reading list.
# put all courses without a reading list into a list to delete.
# TODO: delete those courses
#**********************
root = retrieve_courses()
response_contains_courses = etree.XPath("/courses/course")

while response_contains_courses(root):

    #root = etree.fromstring(response.content)
    
    course_ids = get_course_ids(root)
    
    check_reading_lists(course_ids)
    
    offset = str(int(offset) + 100)
    root = retrieve_courses()
    
delete_courses(courses_to_delete)

#create soup for pretty print xml
soup = str(BeautifulSoup(etree.tostring(root), 'lxml'))

#write response to file
response_file = open("courses.xml", "w")
response_file.write(soup)
response_file.close()
print("done")