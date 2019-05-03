import requests
#from bs4 import BeautifulSoup
from lxml import etree
import argparse
import logging
import datetime

#global variables
apikey = ''
offset = '0'
response = None
course_api_exception = []
reading_list_api_exception = []
term_code = None

#create new log file
#2.6.6 needs a 0
log_file = 'course_deletion_' + '{0:%Y%m%dT%H%M%S}'.format(datetime.datetime.now()) + '.log'
logging.basicConfig(filename=log_file,level=logging.DEBUG,format='%(message)s')
logging.getLogger("requests").setLevel(logging.WARNING)

parser = argparse.ArgumentParser(description='Process string for code parser.')
parser.add_argument('termCode', metavar='termCode', type=str, nargs='+', help='an integer for the accumulator')
args = parser.parse_args()
term_code = args.termCode[0]
if len(args.termCode[0]) is not 5:
    raise ValueError("Invalid argument. Must be 5 character string <year><term> (1 for fall, 5 for summer, 8 for spring) (ex. 20168 (Fall 2016)")
    logging.debug("job ran with invalid argument: " + term_code)
logging.info("deleting all courses for term " + term_code)


def retrieve_courses(): 
    """method to call course api and retrieve all courses
    parameters: none
    response: etree object with all courses
    """  

    logging.info("*******retrieving courses*******")
    
    payload = {
        'apikey' : apikey,
        'limit' : '100',
        'offset' : offset,
        'order_by' : 'code,section',
        'direction' : 'ASC'
        #'q' : 'code~2016'
        }

    response = requests.get('https://api-na.hosted.exlibrisgroup.com/almaws/v1/courses/', params=payload)
    logging.info("***" + response.url + "***")
   
    try:
        root = etree.fromstring(response.content)
    except etree.XMLSyntaxError:
        logging.info("SYNTAX ERROR with above")
        course_api_exception.append(response.url)
    return root
    
def get_course_ids(courses):
    """because the q parameter in the request don't fully work for filtering, we must filter for the results we want through here
    parameters: etree object with courses from get course api
    response: list of filtered course ids
    """  

    logging.info("*******courses matching filter*******") 
    
    code = etree.XPath(".//code[contains(text(),'" + str(term_code) + "')]")
    #name = etree.XPath(".//name")
    course_id = etree.XPath(".//id")
    courseids = []
    for element in courses:
        if code(element):
            #logging.info(name(element)[0].text + " | " + code(element)[0].text)
            logging.info(code(element)[0].text)
            courseids.append(course_id(element)[0].text)
        else:
            root.remove(element)
    if not courseids:
        logging.info("No matches")
    return courseids


def check_reading_lists(courseids):
    """method to call reading list api and retrieve the reading list for a single course
    parameters: list of active course ids  
    response: list of reading list ids
    """

    logging.info("*******checking reading lists*******")

    payload = {
        'apikey' : apikey,
        'limit' : '100',
        'offset' : '0'
        }    
        
    courses_to_delete = []
    
    for courseid in courseids:
        url = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/courses/' + courseid + '/reading-lists'
        #logging.info(url)
        r = requests.get(url, params=payload)
        logging.info(r.url)
        
        try:
            root = etree.fromstring(r.content)
            
            readinglistid = etree.XPath('/reading_lists/reading_list/id')
            if not readinglistid(root):
                courses_to_delete.append(courseid)
            else:
                logging.info("Reading list id: " + readinglistid(root)[0].text + " | course id: " + courseid)
        except etree.XMLSyntaxError:
            logging.info("SYNTAX ERROR with above")
            reading_list_api_exception.append(courseid)
            
    return courses_to_delete
        
def delete_courses(courses_to_delete):
    """method to delete courses from alma
    parameters: list of course ids that dont have reading lists associated
    response: none. logs delete request and status code (204 for success)
    """
    logging.info("*******deleting courses*******")
    
    payload = {
        'apikey' : apikey
        }
    
    if courses_to_delete:    
        logging.info("deleting " + str(len(courses_to_delete)) + " courses")
        for courseid in courses_to_delete:
            logging.info("deleting: " + courseid)
            url = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/courses/' + courseid
            response = requests.delete(url, params=payload)
            #logging.info(response.url)
            #logging.info(response.status_code)
    else:
        logging.info("Nothing to delete")
    
    courses_to_delete = []
    
#**********************************
# first retrieve list of courses from get courses api
# then filter the courses, removing all old courses and get their ids
# send course ids to reading list api and see if they have a reading list.
# put all courses without a reading list into a list to delete.
#**********************************

root = retrieve_courses()
response_contains_courses = etree.XPath("/courses/course")

while response_contains_courses(root):
    
        course_ids = get_course_ids(root)
        
        if len(course_ids) > 0:
            courses_to_delete = check_reading_lists(course_ids)
            delete_courses(courses_to_delete)
            
        offset = str(int(offset) + 100)

        #if int(offset) < 100:
        root = retrieve_courses()
        #else:
        #    break

if course_api_exception:
    logging.info("***failed course api***")
    for failed_course in course_api_exception:
        logging.info(failed_course)
if reading_list_api_exception:
    logging.info("***failed reading list***")
    for failed_reading_list in reading_list_api_exception:
        logging.info(failed_reading_list)
    
    
#optional: write response to file instead of delete
#soup = str(BeautifulSoup(etree.tostring(root), 'lxml'))

#response_file = open("courses.xml", "w")
#response_file.write(soup)
#response_file.close()

logging.info("done")
