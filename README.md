# alma-delete-course-api

Python script to delete courses in Alma that dont have reading lists.


## delete_courses.py
the main file. run this as such: "delete_courses.py", or with a course term argument such as "delete_courses.py 20171" and it will delete courses that don't have reading lists. Pulls all courses (or courses based on the course term argument), searches each course individually to see if it has a reading list, and deletes the ones that don't have a reading list.

### required packages
1. requests (necessary to make the API calls)
2. lxml (necessary for parsing the returned xml objects)

### notes
replace the api key with the key you created in the developer network. recommended testing with a sandbox key first, then production.

the course term (ex. 20171) is optional when running, and is specific to UM and should be modified for other institutions.

query search (q) did not work at the time I created this, but it might work in the future.

The code takes quite a bit of time to run, perhaps a few hours if you have a few thousand courses.

logging file is optional. beautifulsoup is also optional for printing to a file.


## searchable_id_count.py
test file to get counts.
