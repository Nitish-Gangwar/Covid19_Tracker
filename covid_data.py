"""
COVID-19 Tracker.
Developed by: TwistingTornadoes
"""
import pymysql
from tabulate import tabulate
import requests
from bs4 import BeautifulSoup
#######################################################################################################
"""
Headers for
1. state_database collection,
2. advisory_data_collection
3. research_data_collection
 are defined here.
"""

header=["Name","Cases","Increased_cases","Cured","Cured_and_Sent","Active","Deaths","Deaths_Today"]
research_paper_header=["Title","link"]
advisories_header=["Date","Heading","Link"]


#######################################################################################################

def create_table(table_name,c):
   """
   This function creates state-wise tables
   """
   try:
        c.execute("CREATE TABLE "+str(table_name)+" (Name VARCHAR(255) PRIMARY KEY,Cases INTEGER,Increased_cases INTEGER,Cured INTEGER,Cured_and_Sent INTEGER,Active INTEGER,Deaths INTEGER,Deaths_Today INTEGER)")
   except:
        pass


#######################################################################################################

def insert_data(table_name,arr,c,conn1):
   """
   This function inserts records in state-wise tables
   """
   for i in arr:
        Name=i[0]
        Cases=i[1]
        Increased_cases=i[2]
        Cured=i[3]
        Cured_and_Sent=i[4]
        Active=i[5]
        Deaths=i[6]
        Deaths_Today=i[7]
        try:
            #will execute this part when first time insert needs to be done
            arguments=(Name,Cases,Increased_cases,Cured,Cured_and_Sent,Active,Deaths,Deaths_Today)
            query="INSERT INTO "+str(table_name)+"(Name,Cases,Increased_cases,Cured,Cured_and_Sent,Active,Deaths,Deaths_Today) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            c.execute(query,arguments)
        except:
            #This will execute when table is their and we have to update the entries
            arguments=(Cases,Increased_cases,Cured,Cured_and_Sent,Active,Deaths,Deaths_Today,Name)
            query="UPDATE "+str(table_name)+" SET Cases = %s , Increased_cases = %s , Cured= %s , Cured_and_Sent = %s , Active = %s , Deaths = %s , Deaths_Today = %s WHERE Name = %s"
            c.execute(query,arguments)
        conn1.commit()


#######################################################################################################

def print_data(table_name,c,conn1):
   """
   This function prints the state-wise data inserted in the table
   """
   query=" SELECT * FROM "+str(table_name)+" "
   c.execute(query)
   rows = c.fetchall()
   print(tabulate(rows, header, tablefmt="fancy_grid"))


#######################################################################################################

def state_database_collection(c,conn1):
    """
    This function crawls state-wise and district-wise data from
    the URL "https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/"
    and calls functions to execute DML queries
    """
    url="https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/"
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'html.parser')
    # State data gets populated here
    states=[]
    state_name=""
    for i in soup.find_all("div","skgm-states"):
        state=[]

        for j in i.find_all("span","show-district"):
            #get the state name
            state.append(j.text)
            state_name=j.text
            state_name=state_name.replace(' ','_')
            create_table(state_name,c)
        for k in i.find_all("div","skgm-td"):
            for k1 in k.findAll("div","td-sc"):
                #   cases
                state.append(k1.text)
            for k2 in k.findAll("div","td-sdc"):
                # increase in cases
                if(k2.text==''):
                    state.append('0')
                else:
                    state.append(k2.text)
            for k1 in k.findAll("div","td-sr"):
                #   cured cases
                state.append(k1.text)
            for k2 in k.findAll("div","td-sdr"):
                #   increase in cured cases
                if(k2.text==''):
                    state.append('0')
                else:
                    state.append(k2.text)
            for k1 in k.findAll("div","td-sa"):
                state.append(k1.text)
            for k2 in k.findAll("div","td-sd"):
                state.append(k2.text)
            for k2 in k.findAll("div","td-sdd"):
                if(k2.text==''):
                    state.append('0')
                else:
                    state.append(k2.text)
        states.append(state)

        # District data gets populated here

        districts=[]
        for res in i.find_all('div'):
            count=0

            for k in res.find_all("div","skgm-tr"):
                count=0
                district=[]
                for l in k.find_all("div","skgm-td"):
                    if(count==0):
                        district.append(l.text)
                    elif(count==1):
                        for l in k.find_all("div","td-dc"):
                            district.append(l.text)
                        for l in k.find_all("div","td-ddc"):
                            if(l.text==''):
                                district.append('0')
                            else:
                                district.append(l.text)
                    elif(count==2):
                        for l in k.find_all("div","td-dr"):
                            district.append(l.text)
                        for l in k.find_all("div","td-ddr"):
                            if(l.text==''):
                                district.append('0')
                            else:
                                district.append(l.text)
                    elif(count==3):
                        for l in k.find_all("div","td-da"):
                            district.append(l.text)
                    elif(count==4):
                        for l in k.find_all("div","td-dd"):
                            district.append(l.text)
                        for l in k.find_all("div","td-ddd"):
                            if(l.text==''):
                                district.append('0')
                            else:
                                district.append(l.text)
                    count+=1
                districts.append(district)
        insert_data(state_name,districts, c, conn1) #Inserting district-wise data for all states
        print_data(state_name, c, conn1)

    create_table("States",c) #Creating the state table for India
    table_name="States"
    insert_data(table_name,states,c,conn1)


#######################################################################################################

def create_advisories_table(table_name,c):
   """
   This function creates the advisories table
   """
   try:
        c.execute("CREATE TABLE "+str(table_name)+"(Date VARCHAR(255) ,Heading VARCHAR(255),Link VARCHAR(255))")
   except:
        print(table_name + " already inside the database")


#######################################################################################################

def insert_advisories_data(table_name,arr, c, conn1):
   """
   This function inserts advisory data into its respective table
   """
   for i in arr:
        Date= i[0]
        Heading= i[1]
        Link=  i[2]
        try:
            #will execute this part when first time insert needs to be done
            arguments=(Date, Heading, Link)

            query="INSERT INTO "+str(table_name)+"(Date, Heading, Link) VALUES (%s,%s,%s)"
            c.execute(query,arguments)
        except:
            #This will execute when table is their and we have to update the entries
            arguments=(Date, Heading, Link)
            query="UPDATE "+str(table_name)+" SET Date = %s , Heading = %s , Link= %s"
            c.execute(query,arguments)
        conn1.commit()


#######################################################################################################

def print_advisories_data(table_name,c,conn1):
   """
   This function prints the advisory data inserted in the advisories table
   """
   query=" SELECT * FROM "+str(table_name)+" "
   c.execute(query)
   rows = c.fetchall()
   print(tabulate(rows,advisories_header, tablefmt="fancy_grid"))


#######################################################################################################

def advisory_data_collection(c,conn1):
    """
    This function crawls the government advisories on COVID-19 from the URL https://www.mohfw.gov.in/
    and inserts it into one of 9 tables listed below:
           1. Awareness advisories
           2. Behavioural advisories
           3. Citizens advisories
           4. Employee advisories
           5. Hospital advisories
           6. Inspirational advisories
           7. Travel advisories
           8. Training advisories
           9. States advisories
    """
    page_url="https://www.mohfw.gov.in/"

    r=requests.get(page_url)
    soup=BeautifulSoup(r.content,'html.parser')

    tableName = ["Travel_advisories", "Behavioural_advisories",
                "Citizens_advisories" ,"Hospitals_advisories" ,"Training_advisories", "States_advisories", "Employees_advisories", "Awareness_advisories",
                "Inspirational_advisories"]


    for name in tableName:
        create_advisories_table(name,c)

    subcontainer = soup.findAll("div", {"class": "panes"})
    i = 0

    for contain in subcontainer:
      a = contain.findAll("li")
      # date = []
      # head = []
      # link = []
      arr_name=[]
      for list in a:
          temp=[]
          if((list.find("a") and list.find("span"))):
              temp.append(list.find("span").text)

              # date.append(list.find("span").text)
              b = list.find("a")
              # head.append(b.text.strip())
              temp.append(b.text.strip())
              # link.append(b["href"])
              temp.append(b["href"])
              arr_name.append(temp)
      insert_advisories_data(tableName[i],arr_name, c, conn1)
      print_advisories_data(tableName[i],c,conn1)
      i = i+1


#######################################################################################################

def create_research_papers_table(table_name,c):
   """
   This function creates the research papers table
   """
   try:
        c.execute("CREATE TABLE "+str(table_name)+" (Title VARCHAR(255) PRIMARY KEY,link VARCHAR(255))")
   except:
        pass


#######################################################################################################

def insert_research_papers_in_table(table_name,arr,c,conn1):
    """
    This function inserts records into the research papers table
    """
    for i in arr:
        Title=i[0]
        link=i[1]

        try:
            arguments=(Title,link)
            #will execute this part when first time insert needs to be done
            query="INSERT INTO "+str(table_name)+"(Title,link) VALUES (%s,%s)"
            c.execute(query,arguments)
        except:
            arguments=(link,Title)
            query="UPDATE "+str(table_name)+" SET link = %s WHERE Title = %s"
            c.execute(query,arguments)
            #This will execute when table is their and we have to update the entries
            pass
        conn1.commit()


#######################################################################################################

def print_research_papers_data(table_name,c,conn1):
        """
        This function prints the contents of the research papers table
        """
        query=" SELECT * FROM "+str(table_name)+" "
        c.execute(query)

        rows = c.fetchall()
        print(tabulate(rows,research_paper_header, tablefmt="fancy_grid"))


#######################################################################################################

def research_paper_collection(c,conn1):
   """
   This function fetches the links of papers from the first 5 pages in google scholar with keywords "covid 19"
   and adds them to the research paper table
   """
   papers=[]
   for i in range(0,5):
      url="https://scholar.google.com/scholar?start="+str(i*10)+"&q=covid+19&hl=en&as_sdt=0,5"
      r=requests.get(url)
      soup=BeautifulSoup(r.content,'html.parser')

      for containers in soup.findAll("h3", {"class": "gs_rt"}):
        temp=[]
        for i in containers.findAll("a",href=True):
           temp.append(i.text)
           temp.append(i["href"])
        papers.append(temp)
   table_name="rpapers"
   create_research_papers_table(table_name,c)
   insert_research_papers_in_table(table_name,papers,c,conn1)
   print_research_papers_data(table_name,c,conn1)


#######################################################################################################

def main():
        """
        Main function. The flow of control is as follows:
                1. Create 'covid_19_database'
                2. Crawl state-wise data
                3. Crawl advisories
                4. Crawl research papers
        """

        conn1 = pymysql.connect(host="localhost",user="root",password="")
        c = conn1.cursor()
        database_name="covid_19_database"

        try:
            c.execute("CREATE DATABASE "+ str(database_name))
            conn1 = pymysql.connect(host="localhost",user="root",password="",database=database_name)
            c = conn1.cursor()
        except:
            conn1 = pymysql.connect(host="localhost",user="root",password="",database=database_name)
            c = conn1.cursor()
            pass
        state_database_collection(c,conn1)

        advisory_data_collection(c,conn1)

        research_paper_collection(c,conn1)

        conn1.close()

#######################################################################################################
if __name__ == "__main__":
    main()
