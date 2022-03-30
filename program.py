import pandas as pd
import requests 


# Find the prime factors of population



# class needs a url to be provided
class statePopulation:
    
    def __init__(self, url):
        
        self.df = requests.get(url).json()
        
        if not self.df["data"]:
            print("URL broken.")
        
    
    # Determine prime factors of a number
    def primeFactors(n):
    
        c = 2
        factors = []

        while(n > 1):

            if(n % c == 0):
                factors.append(str(c))
                n = n / c
            else:
                c = c + 1

        return  ";".join(factors)
    
    
    # creating a dataframe using json
    def createDataframe(self):
        
        
        # ensuring data exists
        if self.df["data"]:
            
            self.df = pd.DataFrame(self.df["data"])

            # dropped duplicate col's -- redundant data
            del self.df['Slug State']
            del self.df['ID Year']
            
            print("Created Dataframe")
            
    
    # Using the dataframe to create a report
    def createReport(self):

            # grouping the data by states, since we are trying to reflect on population by each state
            new_data = self.df.groupby(by=["State"])


            data = []
            for key, item in new_data:
                data.append([key] + list(map(str, list(item["Population"])[::-1])) + [str(-1)])

            years = list(map(str, sorted(item["Year"].unique())))
            col = ["s_name"] + years + [years[len(years)-1] + " Factors"] # prepare columns names for df

            df2 = pd.DataFrame(data, columns = col)

            for i, row in df2.iterrows():

                prev = 0

                for j in range(1, len(row)-1):

                    val = row[j]

                    # Since we skip the first year the while calculating
                    if j > 1:

                        diff =  ((int(row[j]) - int(prev)) / int(prev)) * 100
                        df2.at[i, row.index[j]] = str(row[j]) + " (" + str(round(diff, 2)) + "%)"

                    if j+1 == len(row)-1:
                        factor = primeFactors(int(val))
                        df2.at[i, row.index[j+1]] = factor

                    prev = val
                
                del self.df
                
                self.df = df2
                
            print("Created Report.")
    
    # output the data in CSV format
    def output(self):
        self.df.to_csv("report.csv", index=False)
        print("Successfully created report.csv")
                    
        
if __name__ == "__main__":
   
    # get the data and create dataframe using pandas lib
    
    result = statePopulation("https://datausa.io/api/data?drilldowns=State&measures=Population")
    
    result.createDataframe()
    result.createReport()
    result.output()