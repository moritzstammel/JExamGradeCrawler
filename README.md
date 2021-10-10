# JExamGradeCrawler
Simple Python WebCrawler for JExam using Selenium

For Easy Use:
  Just fill in the first three Constants the appropriate values for your JExamAccount / Operating System -> 

  PASSWORD = "Your Password"  
  USERNAME = "Your Username"  

  CHROMEDRIVER_PATH = "Path to chromedriver"  
  
  After that you can run grade_crawler.py.  

------------------------------------------------------------------------------------------------------------

 - get_grades(username, password, chromedriver_path=""):

   -collects your grade from JExam
   
   -Takes JExam Username and Password and additionally the path to your chromedriver
   
   -Returns an Array of 
   
      [1] Exams ->   
          {  
            "name": string,   
            "type": "exam",
            "grade": float,  
            "points": float,  
            "passed": true | false  
          }  
      [2] Completed Modules ->  
         {  
            "name": string,   
            "type": "completed module",
            "grade": float,   
            "passed": true | false,  
            "exams" : [Exams]  
          }  
       [3] Pending Modules ->  
        {    
            "name": string,     
            "type": "pending module",  
            "grade": None,     
            "passed": None,   
            "exams" : [Exams]  
          }  
