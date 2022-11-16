# EEL4835_Final_Project
The final project for programming desgin (EEL4835) is to create an executable python file that will list the synonyms of an input word by accessing the database at thesaurus.com

**Requirements:**
 
 1.) The synonym database is at https://www.thesaurus.com/. In particular, the website  https://www.thesaurus.com/browse/[word] gives  you the webpage content  that shows all synonyms of [word]. 
  
  2.) In  order  to  reduce  network  traffic  and  improve  efficiency,  once  your  code  obtains  all  synonyms of a given word, it should store them at local storage for the next use. In other words,  your  code,  upon  start,  should  first  check  whether  its  local  storage  has  stored  all  synonyms of the given word. If yes, just return the locally stored information; otherwise, get the synonyms from thesaurus then store them. Carefully think about what kind of data you should store and how to store such data. 
  
  3.) The website thesaurus can periodically update its database. Thus, the storage of synonyms for  a  given  word  should  be  associated  with  an  expiring  time  (you  can  set  this  time  to  a  value  that  you  feel  reasonable),  your  code  should  check  whether  the  storage  time  has  expired. If yes, your code should re-obtain the information from thesaurus, and then update the local storage (with the new expiring time).  
  
  4.) Create a batch-run Linux script, which saves all obtained the synonyms of all words given by an input file to an output file. Please create your own input file with at least 30 words. Your script should first read the words from the input file, then repeatedly run synonym (or  synonym.py)  for  each  word  and  obtain  the  corresponding  result.  All  the  results  are  finally saved by the script to the output file.  
